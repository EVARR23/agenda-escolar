from django.contrib import admin
from .models import Cuidador, Responsavel, Crianca, Registro_Diario


@admin.register(Cuidador)
class CuidadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'profissao')  
    search_fields = ('nome',)
    list_filter = ('telefone',)


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'profissao', 'local_trabalho')  
    search_fields = ('nome',)
    list_filter = ('telefone',)


@admin.register(Crianca)
class CriancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_de_nascimento', 'rua', 'numero',
                    'cidade', 'cep', 'mora_com_quem', 'tem_irmaos', 'problema_saude_qual', 
                    'medicamento_continuo', 'mendicamento_qual', 'tem_alergias', 
                    'alergias_qual', 'responsavel')  
    search_fields = ('nome',)
    list_filter = ('data_de_nascimento',)


@admin.register(Registro_Diario)
class Registro_DiarioAdmin(admin.ModelAdmin):
    list_display = ('crianca', 'cuidador', 'data',
                    'cafe_da_manha', 'almoco', 'colacao', 'jantar',
                    'evacuacao_liquida', 'evacuacao_pastosa', 'banho',
                    'sono', 'observacoes', 'assinatura')  
    search_fields = ('crianca',)
    list_filter = ('cuidador',)
