from django import forms
from django.core.mail.message import EmailMessage
from .models import Produto, Fabricante, Tipoproduto, Listaproduto, Cliente, Compra


class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-mail')
    assunto = forms.CharField(label='Assunto')
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea())

    def send_mail(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        conteudo = f'Nome: {nome}\nE-mail: {email}\nAssunto: {assunto}\nMenssagem: {mensagem}'

        mail = EmailMessage(
            subject='Email enviado pelo sistema django2',
            body=conteudo,
            from_email='contato@seudominio.com.br',
            to=['contato@seudominio.com', ],  # posso add varios email na lista para receber
            headers={'Reply-To': email},
        )

        mail.send()


class AddModelForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'estoque', 'imagem', 'fabricante', 'tipo']


class ExcluirForm(forms.Form):
    pk = forms.IntegerField(label='ID')
    modelo = forms.CharField(label='Nome da tabela')


class EditarForm(ExcluirForm):
    campo = forms.CharField(label='Campo')
    valor = forms.CharField(label='Novo valor')


class ResumoForm(forms.Form):
    nome = forms.CharField(label='Nome')
    data = forms.DateField(label='Data')