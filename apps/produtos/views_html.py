from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Produto, Categoria, ProdutoPreco, Tamanho
from .forms import ProdutoForm, PizzaForm


class ProductListView(LoginRequiredMixin, ListView):
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
        
        # Contadores por tipo
        context['tipo_counts'] = {
            'todos': Produto.objects.filter(ativo=True).count(),
            'pizza': Produto.objects.filter(tipo_produto='pizza', ativo=True).count(),
            'bebida': Produto.objects.filter(tipo_produto='bebida', ativo=True).count(),
            'borda': Produto.objects.filter(tipo_produto='borda', ativo=True).count(),
            'sobremesa': Produto.objects.filter(tipo_produto='sobremesa', ativo=True).count(),
            'acompanhamento': Produto.objects.filter(tipo_produto='acompanhamento', ativo=True).count(),
            'outro': Produto.objects.filter(tipo_produto='outro', ativo=True).count(),
        }
        
        # Parâmetros da URL para manter filtros
        context['search_query'] = self.request.GET.get('q', '')
        context['current_status'] = self.request.GET.get('status', 'ativo')
        context['current_ordering'] = self.request.GET.get('ordering', 'nome')
        
        return context


class ProductFilterView(LoginRequiredMixin, TemplateView):
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
        
        # Contadores
        context['tipo_counts'] = {
            'todos': Produto.objects.filter(ativo=True).count(),
            'pizza': Produto.objects.filter(tipo_produto='pizza', ativo=True).count(),
            'bebida': Produto.objects.filter(tipo_produto='bebida', ativo=True).count(),
            'borda': Produto.objects.filter(tipo_produto='borda', ativo=True).count(),
            'sobremesa': Produto.objects.filter(tipo_produto='sobremesa', ativo=True).count(),
            'acompanhamento': Produto.objects.filter(tipo_produto='acompanhamento', ativo=True).count(),
            'outro': Produto.objects.filter(tipo_produto='outro', ativo=True).count(),
        }
        
        # Parâmetros da URL
        context['search_query'] = search
        context['current_status'] = status
        context['current_ordering'] = ordering
        
        return context


class ProductSearchView(LoginRequiredMixin, TemplateView):
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'produtos/product_form.html'
    success_url = reverse_lazy('product_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Adicionar mensagem de sucesso se o sistema de mensagens estiver configurado
        return response


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'produtos/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'produtos/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')


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


class PizzaTableView(LoginRequiredMixin, ListView):
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
            
            # Organizar preços por tamanho
            pizza.precos_dict = {}
            for preco in pizza.precos.all():
                pizza.precos_dict[preco.tamanho.id] = preco.preco_final
            
            pizzas_por_categoria[categoria].append(pizza)
        
        context['pizzas_por_categoria'] = pizzas_por_categoria
        context['search_query'] = self.request.GET.get('q', '')
        
        return context


class PizzaCreateView(LoginRequiredMixin, CreateView):
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


class PizzaUpdateView(LoginRequiredMixin, UpdateView):
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