from django.urls import path
from .views import index, mostratabela, contato, adicionar, excluir, editar, resumo

urlpatterns = [
    path('', index, name='index'),
    path('mostratabela/<str:tabela>', mostratabela, name='mostratabela'),
    path('contato/', contato, name='contato'),
    path('adicionar/', adicionar, name='adicionar'),
    path('excluir/', excluir, name='excluir'),
    path('editar/', editar, name='editar'),
    path('resumo/', resumo, name='resumo'),
]