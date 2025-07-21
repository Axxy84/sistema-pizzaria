# 📋 Novo Sistema de Status Automático

## 🎯 Resumo da Mudança

O sistema de status foi completamente reformulado para ser **calculado automaticamente** baseado em timestamps, eliminando a necessidade de gerenciar transições manuais complexas.

## 🔄 Como Funciona

### Antes (Sistema Antigo)
```python
# Campo status fixo no banco
status = models.CharField(choices=STATUS_CHOICES)

# Mudança manual complexa
pedido.status = 'preparando'
pedido.save()
```

### Agora (Sistema Novo)
```python
# Status calculado automaticamente
@property
def status(self):
    if self.cancelado_em:
        return 'cancelado'
    elif self.entregue_em:
        return 'entregue'
    elif self.saida_confirmada_em:
        return 'saindo'
    elif self.preparacao_iniciada_em:
        return 'preparando'
    else:
        return 'recebido'
```

## 🎮 Ações Disponíveis

### 1. **Iniciar Preparo** 🍳
- **Quando**: Status = 'recebido'
- **Ação**: Define `preparacao_iniciada_em`
- **Resultado**: Status muda para 'preparando'

### 2. **Confirmar Saída** 🚚
- **Quando**: Status = 'preparando' e tipo = 'delivery'
- **Ação**: Define `saida_confirmada_em`
- **Resultado**: Status muda para 'saindo'

### 3. **Confirmar Entrega** ✅
- **Quando**: Status = 'preparando' ou 'saindo'
- **Ação**: Define `entregue_em`
- **Resultado**: Status muda para 'entregue'

### 4. **Cancelar Pedido** ❌
- **Quando**: Status = 'recebido' ou 'preparando'
- **Ação**: Define `cancelado_em` e `motivo_cancelamento`
- **Segurança**: Requer senha configurada
- **Resultado**: Status muda para 'cancelado'

## 🔐 Sistema de Cancelamento com Senha

### Configuração
```python
# settings.py
PEDIDO_CANCELAMENTO_SENHA = '1234'  # Altere em produção!
```

### Interface
- Modal com campo de senha
- Campo opcional para motivo do cancelamento
- Validação no servidor

## 📊 Visualização na Interface

### Botões de Ação
```django
{% include 'pedidos/components/pedido_actions.html' with pedido=pedido %}
```

Mostra automaticamente apenas os botões relevantes para o status atual.

### Timeline Visual
```django
{% include 'pedidos/components/pedido_timeline.html' with pedido=pedido %}
```

Exibe o progresso do pedido com timestamps reais.

## 🚀 Vantagens do Novo Sistema

1. **Simplicidade**: Sem lógica complexa de transições
2. **Rastreabilidade**: Timestamps registram quando cada ação aconteceu
3. **Consistência**: Status sempre reflete a realidade atual
4. **Flexibilidade**: Fácil adicionar novos "status" no futuro
5. **Segurança**: Ações críticas protegidas por senha

## 📝 Exemplo de Uso

```python
# Views simplificadas
@login_required
def pedido_iniciar_preparo(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if pedido.pode_iniciar_preparo:
        pedido.preparacao_iniciada_em = timezone.now()
        pedido.save()
        messages.success(request, "Preparo iniciado!")
    
    return redirect('pedidos:pedido_detail', pk=pk)
```

## 🔍 Campos no Banco de Dados

### Removido
- `status` (CharField)

### Adicionados
- `preparacao_iniciada_em` (DateTimeField)
- `saida_confirmada_em` (DateTimeField)
- `entregue_em` (DateTimeField)
- `cancelado_em` (DateTimeField)
- `motivo_cancelamento` (TextField)

## 📌 Migração Aplicada

```bash
# Migration criada e aplicada com sucesso
apps/pedidos/migrations/0008_remove_pedido_status_pedido_cancelado_em_and_more.py
```

## ✨ Resultado Final

O sistema agora é mais intuitivo, confiável e fácil de manter. Os status são sempre consistentes com as ações realizadas, e toda a progressão do pedido é rastreável através dos timestamps.