from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Cliente, Endereco
from .forms import ClienteForm, EnderecoForm


class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(total_enderecos=Count('enderecos'))
        
        # Busca
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(cpf__icontains=search) |
                Q(telefone__icontains=search) |
                Q(email__icontains=search)
            )
        
        # Ordenação
        ordering = self.request.GET.get('ordering', '-criado_em')
        queryset = queryset.order_by(ordering)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['ordering'] = self.request.GET.get('ordering', '-criado_em')
        context['total_clientes'] = Cliente.objects.filter(ativo=True).count()
        return context


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enderecos'] = self.object.enderecos.all().order_by('-principal', 'tipo')
        return context


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        messages.success(self.request, 'Cliente cadastrado com sucesso!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('clientes:cliente-detail', kwargs={'pk': self.object.pk})


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('clientes:cliente-detail', kwargs={'pk': self.object.pk})


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes:cliente-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Cliente excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# Views de Endereço
class EnderecoCreateView(CreateView):
    model = Endereco
    form_class = EnderecoForm
    template_name = 'clientes/endereco_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.cliente = get_object_or_404(Cliente, pk=kwargs['cliente_pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente'] = self.cliente
        return context
    
    def form_valid(self, form):
        form.instance.cliente = self.cliente
        
        # Se marcado como principal, desmarcar outros
        if form.cleaned_data.get('principal'):
            Endereco.objects.filter(cliente=self.cliente, principal=True).update(principal=False)
        
        messages.success(self.request, 'Endereço adicionado com sucesso!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('clientes:cliente-detail', kwargs={'pk': self.cliente.pk})


class EnderecoUpdateView(UpdateView):
    model = Endereco
    form_class = EnderecoForm
    template_name = 'clientes/endereco_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente'] = self.object.cliente
        return context
    
    def form_valid(self, form):
        # Se marcado como principal, desmarcar outros
        if form.cleaned_data.get('principal'):
            Endereco.objects.filter(
                cliente=self.object.cliente, 
                principal=True
            ).exclude(pk=self.object.pk).update(principal=False)
        
        messages.success(self.request, 'Endereço atualizado com sucesso!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('clientes:cliente-detail', kwargs={'pk': self.object.cliente.pk})


class EnderecoDeleteView(DeleteView):
    model = Endereco
    template_name = 'clientes/endereco_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('clientes:cliente-detail', kwargs={'pk': self.object.cliente.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Endereço excluído com sucesso!')
        return super().delete(request, *args, **kwargs)