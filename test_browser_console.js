// Teste direto no console do browser
// Cole este código no console do browser (F12 -> Console)

console.log('🚀 Iniciando teste direto no browser...');

// Função para obter CSRF token
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

// Dados de teste
const testData = {
    sabor_1_id: 6,
    sabor_2_id: 5,
    tamanho_id: 1,
    regra_preco: 'mais_caro'
};

const url = '/api/pedidos/meio-a-meio/calcular-preco/';

console.log('📍 Informações do teste:');
console.log('  URL:', url);
console.log('  Full URL:', window.location.origin + url);
console.log('  Data:', testData);
console.log('  CSRF Token:', getCSRFToken());
console.log('  Current page:', window.location.href);

// Teste 1: Fetch
console.log('\n🧪 Teste 1: Fetch API');
fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
    },
    body: JSON.stringify(testData)
})
.then(response => {
    console.log('📋 Fetch Response:');
    console.log('  Status:', response.status);
    console.log('  OK:', response.ok);
    console.log('  URL:', response.url);
    console.log('  Headers:', Object.fromEntries(response.headers.entries()));
    
    return response.text();
})
.then(text => {
    console.log('📄 Response body:', text);
    try {
        const json = JSON.parse(text);
        console.log('✅ JSON parsed:', json);
    } catch (e) {
        console.log('❌ Not valid JSON');
    }
})
.catch(error => {
    console.error('💥 Fetch error:', error);
});

// Teste 2: XMLHttpRequest
console.log('\n🧪 Teste 2: XMLHttpRequest');
const xhr = new XMLHttpRequest();
xhr.open('POST', url, true);
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.setRequestHeader('X-CSRFToken', getCSRFToken());

xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
        console.log('📋 XHR Response:');
        console.log('  Status:', xhr.status);
        console.log('  Response:', xhr.responseText);
        console.log('  All headers:', xhr.getAllResponseHeaders());
    }
};

xhr.onerror = function() {
    console.error('💥 XHR error');
};

xhr.send(JSON.stringify(testData));

// Teste 3: Verificar se endpoint existe (OPTIONS)
console.log('\n🧪 Teste 3: OPTIONS request');
fetch(url, { method: 'OPTIONS' })
.then(response => {
    console.log('📋 OPTIONS Response:');
    console.log('  Status:', response.status);
    console.log('  Allow header:', response.headers.get('Allow'));
})
.catch(error => {
    console.error('💥 OPTIONS error:', error);
});