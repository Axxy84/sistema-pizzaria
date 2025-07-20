from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, Endereco
import re


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'email', 'telefone', 'telefone2', 'data_nascimento', 'observacoes']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remove caracteres não numéricos
            cpf = re.sub(r'\D', '', cpf)
            
            # Verifica se tem 11 dígitos
            if len(cpf) != 11:
                raise ValidationError('CPF deve ter 11 dígitos.')
            
            # Verifica se não é uma sequência de números iguais
            if cpf == cpf[0] * 11:
                raise ValidationError('CPF inválido.')
            
            # Validação do CPF
            def calcular_digito(cpf, multiplicadores):
                soma = sum(int(cpf[i]) * multiplicadores[i] for i in range(len(multiplicadores)))
                resto = soma % 11
                return '0' if resto < 2 else str(11 - resto)
            
            # Verifica primeiro dígito
            multiplicadores1 = list(range(10, 1, -1))
            digito1 = calcular_digito(cpf, multiplicadores1)
            if cpf[9] != digito1:
                raise ValidationError('CPF inválido.')
            
            # Verifica segundo dígito
            multiplicadores2 = list(range(11, 1, -1))
            digito2 = calcular_digito(cpf, multiplicadores2)
            if cpf[10] != digito2:
                raise ValidationError('CPF inválido.')
            
            # Verifica duplicação
            if self.instance.pk:
                existe = Cliente.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists()
            else:
                existe = Cliente.objects.filter(cpf=cpf).exists()
            
            if existe:
                raise ValidationError('CPF já cadastrado.')
        
        return cpf
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            # Remove caracteres não numéricos
            telefone = re.sub(r'\D', '', telefone)
            
            # Verifica se tem 10 ou 11 dígitos
            if len(telefone) not in [10, 11]:
                raise ValidationError('Telefone deve ter 10 ou 11 dígitos.')
        
        return telefone
    
    def clean_telefone2(self):
        telefone2 = self.cleaned_data.get('telefone2')
        if telefone2:
            # Remove caracteres não numéricos
            telefone2 = re.sub(r'\D', '', telefone2)
            
            # Verifica se tem 10 ou 11 dígitos
            if len(telefone2) not in [10, 11]:
                raise ValidationError('Telefone deve ter 10 ou 11 dígitos.')
        
        return telefone2


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['tipo', 'cep', 'logradouro', 'numero', 'complemento', 
                  'bairro', 'cidade', 'estado', 'referencia', 'principal']
        
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            # Remove caracteres não numéricos
            cep = re.sub(r'\D', '', cep)
            
            # Verifica se tem 8 dígitos
            if len(cep) != 8:
                raise ValidationError('CEP deve ter 8 dígitos.')
        
        return cep