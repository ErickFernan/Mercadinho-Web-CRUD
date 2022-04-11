from django.shortcuts import render, redirect
from django.db import connection
from .models import Produto, Fabricante, Tipoproduto, Listaproduto, Cliente, Compra
from .forms import ContatoForm, AddModelForm, ExcluirForm, EditarForm, ResumoForm
from django.contrib import messages


def trata_dados(dados, nome, teste):
    titulos = dados[0].keys()
    valores = []

    for p in range(0, len(dados)):
        valores.append(dados[p].values())

    context = {
        'nome': nome,
        'valores': valores,
        'titulos': titulos,
        'dados': dados,
        'teste': teste
    }

    return context


def dadostabelas():
    opcoes = {
        'Fabricante': Fabricante,
        'Produto': Produto,
        'Listaproduto': Listaproduto,
        'Cliente': Cliente,
        'Compra': Compra,
        'Tipoproduto': Tipoproduto
    }
    return opcoes


def tabelas():
    tables = connection.introspection.table_names()
    filt_table = [s for s in tables if "core_" in s]
    filt_table[:] = [s.replace('core_', '').capitalize() for s in filt_table]
    return filt_table


def index(request):
    tab = tabelas()
    context = {
        'tabelas': tab
    }
    return render(request, 'index.html', context)


def mostratabela(request, tabela):
    opcoes = dadostabelas()
    dados = opcoes[tabela].objects.all().values()
    teste = opcoes[tabela].objects.all()
    context = trata_dados(dados, tabela, teste)
    return render(request, 'mostratabela.html', context)


def contato(request):
    form = ContatoForm(request.POST or None)
    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()

            messages.success(request, 'Enviado com sucesso')
            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar')

    context = {
        'form': form
    }
    return render(request, 'contato.html', context)


def adicionar(request):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            form = AddModelForm(request.POST, request.FILES)
            if form.is_valid():

                form.save()

                messages.success(request, 'Produto salvo com sucesso.')
                form = AddModelForm()
            else:
                messages.error(request, 'Erro ao salvar produto')
        else:
            form = AddModelForm()
        context = {
            'form': form
        }
        return render(request, 'adicionar.html', context)

    else:
        return redirect('index')


def excluir(request):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            form = ExcluirForm(request.POST, request.FILES)
            if form.is_valid():

                pk = form.cleaned_data['pk']
                modelo = form.cleaned_data['modelo']

                # Executar comando parar excluir:
                opcoes = dadostabelas()[modelo]
                deletar = opcoes.objects.get(pk=pk)
                deletar.delete()

                messages.success(request, 'Produto salvo com sucesso.')
                form = ExcluirForm()
            else:
                messages.error(request, 'Erro ao salvar produto')
        else:
            form = ExcluirForm()
        context = {
            'form': form
        }
        return render(request, 'excluir.html', context)

    else:
        return redirect('index')


def editar(request):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            form = EditarForm(request.POST, request.FILES)
            if form.is_valid():

                pk = form.cleaned_data['pk']
                modelo = form.cleaned_data['modelo']
                campo = form.cleaned_data['campo']
                novo_valor = form.cleaned_data['valor']

                # Executar comando para editar:
                opcoes = dadostabelas()
                dados = opcoes[modelo].objects.all()
                valor = dados.get(pk=pk)
                setattr(valor, campo, novo_valor)
                valor.save()

                messages.success(request, 'Produto salvo com sucesso.')
                form = EditarForm()
            else:
                messages.error(request, 'Erro ao salvar produto')
        else:
            form = EditarForm()
        context = {
            'form': form
        }
        return render(request, 'editar.html', context)

    else:
        return redirect('index')


def resumo(request):

    if str(request.method) == 'POST':
        form = ResumoForm(request.POST, request.FILES)

        if form.is_valid():
            cliente = form.cleaned_data['nome']
            data = form.cleaned_data['data']
            # Executar comando parar excluir:-----------------------------------------------------------------------
            # dados = dadostabelas()

            info_cliente = Cliente.objects.filter(nome=cliente).first()
            # # Aqui consigo todos os dados do cliente
            # print(info_cliente)

            info_compras = Compra.objects.filter(data=data, cliente_id=info_cliente.id).first()
            # # Aqui todos os dados de compras do cliente escolhido
            # print(info_compras.cliente_id)

            info_listaproduto = Listaproduto.objects.filter(compra_id=info_compras.id)
            # # dados da lista de produto
            # for v in info_listaproduto:
            #     print(v.produto.nome, v.produto.preco, v.produto.tipo, v.produto.fabricante, v.quantidade,
            #           v.compra.data,
            #           v.compra.cliente.cpf)  # posso usar isso no html, ta mostrando o nome de cada produto

            # ------------------------------------------------------------------------------------------------------
            messages.success(request, 'Feito.')
            context = {
                'info_cliente': info_cliente,
                'info_compras': info_compras,
                'info_listaproduto': info_listaproduto
            }

            return render(request, 'resumo_apresentacao.html', context)
        else:
            messages.error(request, 'Erro.')
    else:
        form = ResumoForm()
        context = {
                'form': form
        }
        return render(request, 'resumo.html', context)