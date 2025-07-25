from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q, Count, ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.cache import cache
from django.contrib import messages
from .models import Produto, Categoria, ProdutoPreco, Tamanho
from .forms import ProdutoForm, PizzaForm


class ProductListView(ListView):
    model = Produto
    template_name = 'produtos/product_list.html'
    context_object_name = 'produtos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Produto.objects.select_related('categoria').prefetch_related('precos__tamanho')
        
        # Filtro por status
        status = self.request.GET.get('status', 'ativo')
        if status == 'ativo':
            queryset = queryset.filter(ativo=True)
        elif status == 'inativo':
            queryset = queryset.filter(ativo=False)
        
        # Busca
        search = self.request.GET.get('q', '')
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(descricao__icontains=search) |
                Q(ingredientes__icontains=search)
            )
        
        # Ordenação
        ordering = self.request.GET.get('ordering', 'nome')
        if ordering in ['nome', '-nome', 'criado_em', '-criado_em', 'tipo_produto']:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Contadores otimizados com cache
        cache_key = 'produtos:tipo_counts'
        tipo_counts = cache.get(cache_key)
        
        if tipo_counts is None:
            from django.db.models import Count, Case, When, IntegerField
            
            tipo_counts = Produto.objects.filter(ativo=True).aggregate(
                todos=Count('id'),
                pizza=Count(Case(When(tipo_produto='pizza', then=1), output_field=IntegerField())),
                bebida=Count(Case(When(tipo_produto='bebida', then=1), output_field=IntegerField())),
                borda=Count(Case(When(tipo_produto='borda', then=1), output_field=IntegerField())),
                sobremesa=Count(Case(When(tipo_produto='sobremesa', then=1), output_field=IntegerField())),
                acompanhamento=Count(Case(When(tipo_produto='acompanhamento', then=1), output_field=IntegerField())),
                outro=Count(Case(When(tipo_produto='outro', then=1), output_field=IntegerField())),
            )
            # Cache por 5 minutos
            cache.set(cache_key, tipo_counts, 300)
        
        context['tipo_counts'] = tipo_counts
        
        # Parâmetros da URL para manter filtros
        context['search_query'] = self.request.GET.get('q', '')
        context['current_status'] = self.request.GET.get('status', 'ativo')
        context['current_ordering'] = self.request.GET.get('ordering', 'nome')
        
        return context


class ProductFilterView(TemplateView):
    template_name = 'produtos/product_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo = kwargs.get('tipo', 'todos')
        
        # Queryset base
        queryset = Produto.objects.select_related('categoria').prefetch_related('precos__tamanho')
        
        # Filtro por tipo
        if tipo != 'todos':
            queryset = queryset.filter(tipo_produto=tipo)
        
        # Filtro por status
        status = self.request.GET.get('status', 'ativo')
        if status == 'ativo':
            queryset = queryset.filter(ativo=True)
        elif status == 'inativo':
            queryset = queryset.filter(ativo=False)
        
        # Busca
        search = self.request.GET.get('q', '')
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(descricao__icontains=search) |
                Q(ingredientes__icontains=search)
            )
        
        # Ordenação
        ordering = self.request.GET.get('ordering', 'nome')
        if ordering in ['nome', '-nome', 'criado_em', '-criado_em']:
            queryset = queryset.order_by(ordering)
        
        # Paginação
        paginator = Paginator(queryset, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Context
        context['produtos'] = page_obj
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['current_tipo'] = tipo
        
        # Contadores otimizados com cache
        cache_key = 'produtos:tipo_counts'
        tipo_counts = cache.get(cache_key)
        
        if tipo_counts is None:
            from django.db.models import Count, Case, When, IntegerField
            
            tipo_counts = Produto.objects.filter(ativo=True).aggregate(
                todos=Count('id'),
                pizza=Count(Case(When(tipo_produto='pizza', then=1), output_field=IntegerField())),
                bebida=Count(Case(When(tipo_produto='bebida', then=1), output_field=IntegerField())),
                borda=Count(Case(When(tipo_produto='borda', then=1), output_field=IntegerField())),
                sobremesa=Count(Case(When(tipo_produto='sobremesa', then=1), output_field=IntegerField())),
                acompanhamento=Count(Case(When(tipo_produto='acompanhamento', then=1), output_field=IntegerField())),
                outro=Count(Case(When(tipo_produto='outro', then=1), output_field=IntegerField())),
            )
            # Cache por 5 minutos
            cache.set(cache_key, tipo_counts, 300)
        
        context['tipo_counts'] = tipo_counts
        
        # Parâmetros da URL
        context['search_query'] = search
        context['current_status'] = status
        context['current_ordering'] = ordering
        
        return context


class ProductSearchView(TemplateView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        tipo = request.GET.get('tipo', '')
        
        produtos = Produto.objects.filter(ativo=True)
        
        if query:
            produtos = produtos.filter(
                Q(nome__icontains=query) |
                Q(descricao__icontains=query) |
                Q(ingredientes__icontains=query)
            )
        
        if tipo:
            produtos = produtos.filter(tipo_produto=tipo)
        
        produtos = produtos.select_related('categoria')[:20]
        
        # Resposta JSON para AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = []
            for produto in produtos:
                data.append({
                    'id': produto.id,
                    'nome': produto.nome,
                    'tipo': produto.get_tipo_produto_display(),
                    'tipo_value': produto.tipo_produto,
                    'preco': produto.preco_display,
                    'categoria': produto.categoria.nome,
                    'ingredientes': produto.ingredientes or '',
                    'ativo': produto.ativo,
                    'badge_class': produto.get_tipo_display_badge(),
                })
            return JsonResponse({'produtos': data})
        
        # Resposta HTML normal
        return super().get(request, *args, **kwargs)


class ProductCreateView(CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'produtos/product_form.html'
    success_url = reverse_lazy('product_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Adicionar mensagem de sucesso se o sistema de mensagens estiver configurado
        return response


class ProductUpdateView(UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'produtos/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(DeleteView):
    model = Produto
    template_name = 'produtos/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    
    def post(self, request, *args, **kwargs):
        """Override para implementar soft delete ao invés de exclusão física"""
        self.object = self.get_object()
        
        try:
            # Tentar excluir fisicamente primeiro
            self.object.delete()
            messages.success(request, f'Produto "{self.object.nome}" excluído com sucesso!')
            return redirect(self.success_url)
        except ProtectedError:
            # Se falhar por estar em uso, fazer soft delete (desativar)
            self.object.ativo = False
            self.object.save()
            messages.warning(
                request, 
                f'O produto "{self.object.nome}" não pode ser excluído pois está sendo usado em pedidos. '
                f'O produto foi desativado e não aparecerá mais nas listagens.'
            )
            return redirect(self.success_url)


def product_toggle_status(request, pk):
    """Toggle produto ativo/inativo via AJAX"""
    if request.method == 'POST' and request.user.is_authenticated:
        produto = get_object_or_404(Produto, pk=pk)
        produto.ativo = not produto.ativo
        produto.save()
        
        return JsonResponse({
            'success': True,
            'ativo': produto.ativo,
            'message': f'Produto {"ativado" if produto.ativo else "desativado"} com sucesso!'
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)


class PizzaTableView(ListView):
    """View para listagem de pizzas estilo cardápio"""
    model = Produto
    template_name = 'produtos/pizza_table.html'
    context_object_name = 'pizzas'
    paginate_by = 20
    
    def get_queryset(self):
        return Produto.objects.filter(
            tipo_produto='pizza'
        ).select_related('categoria').prefetch_related('precos__tamanho').order_by('categoria', 'nome')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obter todos os tamanhos ordenados
        context['tamanhos'] = Tamanho.objects.filter(ativo=True).order_by('ordem')
        
        # Agrupar pizzas por categoria
        pizzas_por_categoria = {}
        for pizza in context['pizzas']:
            categoria = pizza.categoria.nome
            if categoria not in pizzas_por_categoria:
                pizzas_por_categoria[categoria] = []
            pizzas_por_categoria[categoria].append(pizza)
        
        context['pizzas_por_categoria'] = pizzas_por_categoria
        context['search_query'] = self.request.GET.get('q', '')
        
        return context


class PizzaCreateView(CreateView):
    """View para criar pizza com formulário específico"""
    model = Produto
    form_class = PizzaForm
    template_name = 'produtos/pizza_form.html'
    success_url = reverse_lazy('pizza_table')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tamanhos'] = Tamanho.objects.filter(ativo=True).order_by('ordem')
        return context
    
    def form_valid(self, form):
        form.instance.tipo_produto = 'pizza'
        response = super().form_valid(form)
        
        # Salvar preços por tamanho
        tamanhos = Tamanho.objects.filter(ativo=True)
        for tamanho in tamanhos:
            preco_field = f'preco_{tamanho.nome.lower()}'
            if preco_field in form.cleaned_data:
                preco_value = form.cleaned_data[preco_field]
                if preco_value:
                    ProdutoPreco.objects.create(
                        produto=self.object,
                        tamanho=tamanho,
                        preco=preco_value
                    )
        
        return response


class PizzaUpdateView(UpdateView):
    """View para editar pizza com formulário específico"""
    model = Produto
    form_class = PizzaForm
    template_name = 'produtos/pizza_form.html'
    success_url = reverse_lazy('pizza_table')
    
    def get_queryset(self):
        return super().get_queryset().filter(tipo_produto='pizza')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tamanhos'] = Tamanho.objects.filter(ativo=True).order_by('ordem')
        
        # Preencher preços existentes
        precos_dict = {}
        for preco in self.object.precos.all():
            precos_dict[preco.tamanho.nome.lower()] = preco.preco
        context['precos_existentes'] = precos_dict
        
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        
        # Adicionar preços existentes ao initial data
        for preco in self.object.precos.all():
            field_name = f'preco_{preco.tamanho.nome.lower()}'
            initial[field_name] = preco.preco
        
        return initial
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Atualizar preços por tamanho
        self.object.precos.all().delete()  # Limpar preços antigos
        
        tamanhos = Tamanho.objects.filter(ativo=True)
        for tamanho in tamanhos:
            preco_field = f'preco_{tamanho.nome.lower()}'
            if preco_field in form.cleaned_data:
                preco_value = form.cleaned_data[preco_field]
                if preco_value:
                    ProdutoPreco.objects.create(
                        produto=self.object,
                        tamanho=tamanho,
                        preco=preco_value
                    )
        
        return response


class ProductCreateWizardView(TemplateView):
    """View para o formulário wizard de criação de produtos"""
    template_name = "produtos/product_form_wizard.html"
    
    def post(self, request, *args, **kwargs):
        """Processa o formulário wizard"""
        try:
            tipo_produto = request.POST.get("tipo_produto")
            nome = request.POST.get("nome")
            categoria_id = request.POST.get("categoria")
            ativo = request.POST.get("ativo", "true") == "true"
            
            # Validações básicas
            if not nome or not categoria_id:
                return JsonResponse({
                    "success": False,
                    "error": "Nome e categoria são obrigatórios"
                })
            
            # Buscar categoria
            try:
                categoria = Categoria.objects.get(id=categoria_id)
            except Categoria.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "error": "Categoria inválida"
                })
            
            # Criar produto
            produto = Produto.objects.create(
                nome=nome,
                categoria=categoria,
                tipo_produto=tipo_produto,
                ativo=ativo,
                descricao=request.POST.get("descricao", ""),
                ingredientes=request.POST.get("ingredientes", ""),
                preco_unitario=request.POST.get("preco_unitario") or None
            )
            
            # Se for pizza, criar preços por tamanho
            if tipo_produto == "pizza":
                tamanhos = Tamanho.objects.filter(ativo=True).order_by("ordem")
                for tamanho in tamanhos:
                    preco_field = f"preco_{tamanho.nome.lower()}"
                    preco_value = request.POST.get(preco_field)
                    if preco_value:
                        ProdutoPreco.objects.create(
                            produto=produto,
                            tamanho=tamanho,
                            preco=preco_value
                        )
            
            # Redirecionar baseado no tipo
            if tipo_produto == "pizza":
                redirect_url = reverse_lazy("pizza_list")
            else:
                redirect_url = reverse_lazy("product_list")
            
            return JsonResponse({
                "success": True,
                "redirect_url": str(redirect_url),
                "message": f"{produto.nome} cadastrado com sucesso!"
            })
            
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })
