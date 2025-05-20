from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse
from django.contrib import admin
from django.conf import settings
from django.contrib.admin import SimpleListFilter
from datetime import datetime
import os
import locale
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
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

# --- Função para rodapé com data e nome do usuário ---
def rodape(canvas, doc):
    canvas.saveState()
    largura, altura = A4

    data_str = datetime.now().strftime("%d de %B de %Y")
    canvas.setFont('Helvetica-Oblique', 8)
    canvas.drawString(2 * cm, 1.5 * cm, f"Data de emissão: {data_str}")

    nome_usuario = getattr(doc, 'nome_usuario', '')
    if nome_usuario:
        canvas.drawRightString(largura - 2 * cm, 1.5 * cm, f"Emitido por: {nome_usuario}")

    canvas.restoreState()

# --- Função para exportar PDF ---
def exportar_modelo_pdf(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    campos = [field.name for field in meta.fields if field.name != 'id']

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{meta.verbose_name_plural}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4,
                            leftMargin=3*cm, rightMargin=3*cm,
                            topMargin=3*cm, bottomMargin=3*cm)

    elementos = []

    # --- Cabeçalho com logo e título centralizado ---
    caminho_logo = os.path.join(settings.BASE_DIR, 'home', 'static', 'logo.png')
    styles = getSampleStyleSheet()

    if os.path.exists(caminho_logo):
        img = Image(caminho_logo, width=3.5*cm, height=2*cm)
    else:
        img = Spacer(3.5*cm, 2*cm)  # Espaço reservado

    titulo = Paragraph(
        f'<b><font size=14 color=blue>{meta.verbose_name_plural.title()}</font></b>',
        ParagraphStyle(name='TituloCentral', alignment=TA_CENTER, fontSize=14)
    )

    cabecalho = Table(
        [[img, titulo]],
        colWidths=[4*cm, 12*cm]
    )
    cabecalho.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    elementos.append(cabecalho)
    elementos.append(Spacer(1, 12))

    # --- Quantidade de registros ---
    total_registros = queryset.count()
    estilo_qtd = ParagraphStyle(name='Centro', alignment=TA_CENTER, fontSize=10)
    qtd_paragraph = Paragraph(f"<b>Quantidade de registros: {total_registros}</b>", estilo_qtd)
    elementos.append(qtd_paragraph)
    elementos.append(Spacer(1, 12))

    # --- Tabela de dados ---
    dados = [[campo.title() for campo in campos]]
    for obj in queryset:
        linha = [str(getattr(obj, campo)) for campo in campos]
        dados.append(linha)

    tabela = Table(dados, repeatRows=1)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elementos.append(tabela)

    # --- Nome do usuário autenticado ---
    usuario = request.user
    nome_usuario = usuario.get_full_name() or usuario.username if usuario.is_authenticated else ""
    doc.nome_usuario = nome_usuario

    doc.build(elementos, onFirstPage=rodape, onLaterPages=rodape)

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
    list_display = ('nome', 'telefone', 'profissao', 'local_trabalho', 'auth_user')
    search_fields = ('nome',)
    list_filter = ('telefone',)
    actions = [exportar_modelo_pdf]

@admin.register(Crianca)
class CriancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sal', 'data_de_nascimento', 'rua', 'num',
                    'cidade', 'cep', 'mora_com_quem', 'tem_irmaos', 'prob_saude',
                    'medic_continuo', 'medic_qual', 'tem_alergias',
                    'aler_qual', 'responsavel')
    search_fields = ('nome',)
    list_filter = ('data_de_nascimento',)
    actions = [exportar_modelo_pdf]

@admin.register(Registro_Diario)
class Registro_DiarioAdmin(admin.ModelAdmin):
    list_display = ('crianca', 'cuidador', 'data',
                    'cafe', 'alm', 'col', 'jnt',
                    'ev_L', 'ev_P', 'bnh',
                    'sono', 'obs',)
    search_fields = ('crianca__nome',)
    list_filter = ('crianca', MesFiltro)
    actions = [exportar_modelo_pdf]
