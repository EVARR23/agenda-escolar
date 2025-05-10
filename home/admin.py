import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Cuidador, Responsavel, Crianca, Registro_Diario

# admin.py (acrescente no topo)
def exportar_modelo_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    nome_arquivo = f"{meta.verbose_name_plural}.csv"
    campos = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
    writer = csv.writer(response)

    # Cabeçalhos
    writer.writerow(campos)

    # Linhas
    for obj in queryset:
        row = [getattr(obj, campo) for campo in campos]
        writer.writerow(row)

    return response

exportar_modelo_csv.short_description = "Exportar como CSV"


@admin.register(Cuidador)
class CuidadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'profissao')  
    search_fields = ('nome',)
    list_filter = ('telefone',)
    actions = [exportar_modelo_csv] 


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'profissao', 'local_trabalho')  
    search_fields = ('nome',)
    list_filter = ('telefone',)
    actions = [exportar_modelo_csv] 


@admin.register(Crianca)
class CriancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_de_nascimento', 'rua', 'numero',
                    'cidade', 'cep', 'mora_com_quem', 'tem_irmaos', 'problema_saude_qual', 
                    'medicamento_continuo', 'mendicamento_qual', 'tem_alergias', 
                    'alergias_qual', 'responsavel')  
    search_fields = ('nome',)
    list_filter = ('data_de_nascimento',)
    actions = [exportar_modelo_csv]


@admin.register(Registro_Diario)
class Registro_DiarioAdmin(admin.ModelAdmin):
    list_display = ('crianca', 'cuidador', 'data',
                    'cafe_da_manha', 'almoco', 'colacao', 'jantar',
                    'evacuacao_liquida', 'evacuacao_pastosa', 'banho',
                    'sono', 'observacoes', 'assinatura')  
    search_fields = ('crianca',)
    list_filter = ('cuidador',)
    actions = [exportar_modelo_csv]

