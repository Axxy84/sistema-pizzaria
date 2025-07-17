# 🔧 Resolver Erro Alpine.js - adicionarPizzaDireto

## ❌ Erro Encontrado
```
Alpine Expression Error: adicionarPizzaDireto is not defined
```

## ✅ Solução Implementada

### 1. **Função Adicionada ao JavaScript**
A função `adicionarPizzaDireto` foi adicionada ao arquivo `/static/js/pedidos-simples.js` na linha 346.

### 2. **Contexto Alpine Corrigido**
O template foi atualizado para usar `$root.adicionarPizzaDireto()` que acessa a função no contexto raiz do Alpine.js.

### 3. **Versão do Cache Atualizada**
A versão do arquivo JS foi atualizada para `v=5.1` para forçar o recarregamento.

## 🚀 Como Resolver o Problema de Cache

### **Opção 1: Hard Refresh (Recomendado)**
- **Windows/Linux**: `Ctrl + Shift + R` ou `Ctrl + F5`
- **Mac**: `Cmd + Shift + R`

### **Opção 2: Limpar Cache do Navegador**
1. Abra o DevTools (F12)
2. Clique com botão direito no botão de recarregar
3. Selecione "Esvaziar cache e recarregar permanentemente"

### **Opção 3: Modo Incógnito**
Abra a página em uma nova janela anônima/incógnita para testar sem cache.

### **Opção 4: DevTools - Desabilitar Cache**
1. Abra o DevTools (F12)
2. Vá para a aba Network
3. Marque "Disable cache"
4. Recarregue a página

## 🧪 Como Verificar se Funcionou

1. Abra o console do navegador (F12)
2. Você deve ver: `Função adicionarPizzaDireto existe? function`
3. Clique em um botão de tamanho de pizza
4. Deve aparecer no console: `🍕 Adicionando pizza direto: [nome] [tamanho]`
5. A pizza deve ser adicionada ao carrinho instantaneamente

## 📝 Alterações Técnicas Realizadas

### **Arquivo: `/templates/pedidos/components/pizza_lista.html`**
```html
<!-- Antes -->
<button @click="abrirModalPedidoCompleto(produto, tamanho)">

<!-- Depois -->
<button @click="$root.adicionarPizzaDireto(produto, tamanho)">
```

### **Arquivo: `/static/js/pedidos-simples.js`**
```javascript
// Nova função adicionada (linha 346)
adicionarPizzaDireto(produto, tamanho) {
    // Adiciona pizza diretamente ao carrinho
    // Sem abrir modal
}
```

## 🎯 Resultado Esperado

Após limpar o cache e recarregar:
1. Clicar no tamanho da pizza adiciona instantaneamente ao carrinho
2. Aparece notificação de sucesso
3. Scroll automático para o carrinho
4. Sem erros no console

**Se o erro persistir após limpar o cache, reinicie o servidor Django:**
```bash
# Pare o servidor (Ctrl+C)
# Inicie novamente
python manage.py runserver
```