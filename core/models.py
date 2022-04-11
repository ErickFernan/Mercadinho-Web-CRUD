from django.db import models
from stdimage.models import StdImageField
from django.db.models import signals
from django.template.defaultfilters import slugify


class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Tipoproduto(models.Model):
    tipo = models.CharField('Tipo', max_length=100)

    class Meta:
        verbose_name = 'TipoProduto'
        verbose_name_plural = 'TiposProduto'

    def __str__(self):
        return self.tipo


class Fabricante(models.Model):
    nome = models.CharField('Nome', max_length=100)

    class Meta:
        verbose_name = 'Fabricante'
        verbose_name_plural = 'Fabricantes'

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField('Nome', max_length=100)
    endereco = models.CharField('Endereço', max_length=200)
    telefone = models.CharField('Telefone', max_length=20)
    cep = models.CharField('CEP', max_length=10)
    cidade = models.CharField('Cidade', max_length=50)
    cpf = models.IntegerField('CPF')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome


class Compra(models.Model):
    data = models.DateField('Data')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        data = f'{self.data}'
        return data


class Produto(Base):
    nome = models.CharField('Nome', max_length=100)
    estoque = models.IntegerField('Estoque')
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipoproduto, on_delete=models.CASCADE)
    imagem = StdImageField('Imagem', upload_to='produtos', variations={'thumb': (124, 124)})
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome


def produto_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nome)


signals.pre_save.connect(produto_pre_save, sender=Produto)


class Listaproduto (models.Model):
    quantidade = models.IntegerField('Quantidade')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'ListaProduto'
        verbose_name_plural = 'ListaProdutos'

    def __str__(self):
        quantidade = f'{self.quantidade}'
        return quantidade
