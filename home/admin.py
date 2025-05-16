from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from django.http import HttpResponse
from django.contrib import admin
from django.conf import settings
from django.contrib.admin import SimpleListFilter
from datetime import datetime
import os
import locale

from .models import Cuidador, Responsavel, Crianca, Registro_Diario

# --- Define locale para datas em português ---
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Linux/Mac
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')  # Windows

# --- Filtro por mês no admin ---
class MesFiltro(SimpleListFilter):
    title = 'Mês'
    parameter_name = 'mes'

    def lookups(self, request, model_admin):
        meses = Registro_Diario.objects.dates('data', 'month')
        return [(d.strftime("%Y-%m"), d.strftime("%B/%Y").capitalize()) for d in meses]

    def queryset(self, request, queryset):
        if self.value():
            ano, mes = self.value().split("-")
            return queryset.filter(data__year=ano, data__month=mes)


# --- Função para exportar PDF ---
def exportar_modelo_pdf(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    campos = [field.name for field in meta.fields]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{meta.verbose_name_plural}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    p.setTitle(meta.verbose_name_plural.title())
    width, height = A4

    y = height - 2 * cm
    x = 2 * cm

    # --- LOGO no canto superior esquerdo ---
    caminho_logo = os.path.join(settings.BASE_DIR, 'home', 'static', 'logo.png')  # ajuste conforme o caminho real
    if os.path.exists(caminho_logo):
        p.drawImage(caminho_logo, x, y - 0.5 * cm, width=3.5 * cm, height=2 * cm, preserveAspectRatio=True, mask='auto')

    # --- TÍTULO centralizado em azul ---
    titulo = f"{meta.verbose_name_plural.title()}"
    p.setFont("Helvetica-Bold", 14)
    largura_titulo = p.stringWidth(titulo, "Helvetica-Bold", 14)
    p.setFillColor(colors.blue)
    p.drawString((width - largura_titulo) / 2, y, titulo)
    p.setFillColor(colors.black)
    y -= 3 * cm  # espaço após logo + título

    p.setFont("Helvetica", 10)

    for obj in queryset:
        if y < 3 * cm:
            p.showPage()
            y = height - 2 * cm
            p.setFont("Helvetica", 10)

        for campo in campos:
            valor = str(getattr(obj, campo))
            p.setFont("Helvetica-Bold", 10)
            p.drawString(x, y, f"{campo.title()}:")
            p.setFont("Helvetica", 10)
            p.drawString(x + 4.5 * cm, y, valor)
            y -= 0.5 * cm

        y -= 0.2 * cm
        p.line(x, y, width - x, y)
        y -= 0.5 * cm

    p.showPage()
    p.save()
    return response

exportar_modelo_pdf.short_description = "Exportar como PDF"


# --- Admins ---
@admin.register(Cuidador)
class CuidadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'profissao')
    search_fields = ('nome',)
    list_filter = ('telefone',)
    actions = [exportar_modelo_pdf]


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'profissao', 'local_trabalho')
    search_fields = ('nome',)
    list_filter = ('telefone',)
    actions = [exportar_modelo_pdf]


@admin.register(Crianca)
class CriancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'qual_sala', 'data_de_nascimento', 'rua', 'numero',
                    'cidade', 'cep', 'mora_com_quem', 'tem_irmaos', 'problema_saude_qual',
                    'medicamento_continuo', 'mendicamento_qual', 'tem_alergias',
                    'alergias_qual', 'responsavel')
    search_fields = ('nome',)
    list_filter = ('data_de_nascimento',)
    actions = [exportar_modelo_pdf]


@admin.register(Registro_Diario)
class Registro_DiarioAdmin(admin.ModelAdmin):
    list_display = ('crianca', 'cuidador', 'data',
                    'cafe_da_manha', 'almoco', 'colacao', 'jantar',
                    'evacuacao_liquida', 'evacuacao_pastosa', 'banho',
                    'sono', 'observacoes',)
    search_fields = ('crianca__nome',)
    list_filter = ('crianca', MesFiltro)
    actions = [exportar_modelo_pdf]
