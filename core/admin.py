from django.contrib import admin

from .models import Tipoproduto, Cliente, Fabricante, Compra, Produto, Listaproduto


@admin.register(Tipoproduto)
class TipoProdutoAdmin(admin.ModelAdmin):
    list_display = ('tipo',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'telefone', 'cep', 'cidade', 'cpf',)


@admin.register(Fabricante)
class FabricanteAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('data', 'cliente',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estoque', 'preco', 'fabricante', 'tipo',
                    'imagem', 'slug', 'criado', 'modificado', 'ativo',)


@admin.register(Listaproduto)
class ListaProdutoAdmin(admin.ModelAdmin):
    list_display = ('quantidade', 'produto', 'compra',)