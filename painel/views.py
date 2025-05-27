from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render
from painel.models import Registro_Diario
from painel.models import Purchase, Item
from utils.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict



    
@staff_member_required
def get_filter_options(request):
    grouped_purchases = Purchase.objects.annotate(year=ExtractYear("time")).values("year").order_by("-year").distinct()
    options = [purchase["year"] for purchase in grouped_purchases]

    return JsonResponse({
        "options": [
    2023,
    2022,
    2021,
    2020,
    2019,
    2018
  ]
    })



@staff_member_required
def statistics_view(request):
    return render(request, "statistics.html", {})


@staff_member_required
def anos_disponiveis(request):
    anos = Registro_Diario.objects.annotate(ano=ExtractYear("data")).values_list("ano", flat=True).distinct()
    return JsonResponse({"options": sorted(anos, reverse=True)})


@staff_member_required
def refeicoes_chart(request, year):
    registros = Registro_Diario.objects.filter(data__year=year).annotate(month=ExtractMonth("data"))

    grouped = registros.values("month").annotate(
        total_cafe=Count("id", filter=Q(cafe="tudo")),
        total_almoco=Count("id", filter=Q(alm="tudo")),
        total_colacao=Count("id", filter=Q(col="tudo")),
        total_janta=Count("id", filter=Q(jnt="tudo")),
    ).order_by("month")

    labels = [months[group["month"] - 1] for group in grouped]
    cafe_data = [group["total_cafe"] for group in grouped]
    almoco_data = [group["total_almoco"] for group in grouped]
    colacao_data = [group["total_colacao"] for group in grouped]
    janta_data = [group["total_janta"] for group in grouped]

    return JsonResponse({
        "title": f"Refeições completas em {year}",
        "data": {
            "labels": labels,
            "datasets": [
                {"label": "Café", "backgroundColor": colorPrimary, "data": cafe_data},
                {"label": "Almoço", "backgroundColor": colorSuccess, "data": almoco_data},
                {"label": "Colação", "backgroundColor": colorDanger, "data": colacao_data},
                {"label": "Janta", "backgroundColor": "#facc15", "data": janta_data},
            ]
        }
    })


@staff_member_required
def sono_chart(request, year):
    registros = Registro_Diario.objects.filter(data__year=year)

    data_counts = [
        registros.filter(sono="tranquilo").count(),
        registros.filter(sono="agitado").count(),
        registros.filter(sono="não dormiu").count(),
    ]

    return JsonResponse({
        "title": f"Qualidade do Sono em {year}",
        "data": {
            "labels": ["Tranquilo", "Agitado", "Não dormiu"],
            "datasets": [{
                "label": "Quantidade",
                "backgroundColor": [colorSuccess, colorDanger, colorPrimary],
                "data": data_counts,
            }]
        }
    })


@staff_member_required
def registros_por_crianca_chart(request):
    registros = Registro_Diario.objects.values("crianca__nome").annotate(total=Count("id")).order_by("-total")

    labels = [r["crianca__nome"] for r in registros]
    data = [r["total"] for r in registros]

    return JsonResponse({
        "title": "Registros por Criança",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Total de Registros",
                "backgroundColor": generate_color_palette(len(labels)),
                "data": data,
            }]
        }
    })


@staff_member_required
def banho_chart(request):
    data = Registro_Diario.objects.values('bnh').annotate(total=Count('id'))

    labels = [item['bnh'].capitalize() for item in data]
    counts = [item['total'] for item in data]

    return JsonResponse({
        "title": "Crianças que tomaram banho",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Quantidade",
                "backgroundColor": generate_color_palette(len(labels)),
                "data": counts,
            }]
        }
    })


@staff_member_required
def evacuacao_liquida_chart(request):
    data = Registro_Diario.objects.values('ev_L').annotate(total=Count('id'))

    labels = [item['ev_L'] for item in data]
    counts = [item['total'] for item in data]

    return JsonResponse({
        "title": "Evacuação Líquida",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Quantidade",
                "backgroundColor": generate_color_palette(len(labels)),
                "data": counts,
            }]
        }
    })


@staff_member_required
def evacuacao_pastosa_chart(request):
    data = Registro_Diario.objects.values('ev_P').annotate(total=Count('id'))

    labels = [item['ev_P'] for item in data]
    counts = [item['total'] for item in data]

    return JsonResponse({
        "title": "Evacuação Pastosa",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Quantidade",
                "backgroundColor": generate_color_palette(len(labels)),
                "data": counts,
            }]
        }
    })


@staff_member_required
def medicamentos_chart(request):
    data = Registro_Diario.objects.values('med').annotate(total=Count('id'))

    labels = [item['med'].capitalize() for item in data]
    counts = [item['total'] for item in data]

    return JsonResponse({
        "title": "Medicamento Contínuo",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Quantidade",
                "backgroundColor": generate_color_palette(len(labels)),
                "data": counts,
            }]
        }
    })


@staff_member_required
def problemas_saude_chart(request):
    data = Registro_Diario.objects.values('pr_sau').annotate(total=Count('id'))

    labels = [item['pr_sau'].capitalize() for item in data]
    counts = [item['total'] for item in data]

    return JsonResponse({
        "title": "Problemas de Saúde",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Quantidade",
                "backgroundColor": generate_color_palette(len(labels)),
                "data": counts,
            }]
        }
    })


@staff_member_required
def alergias_chart(request):
    data = Registro_Diario.objects.values('aler').annotate(total=Count('id'))

    labels = [item['aler'].capitalize() for item in data]
    counts = [item['total'] for item in data]

    return JsonResponse({
        "title": "Crianças com Alergias",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Quantidade",
                "backgroundColor": generate_color_palette(len(labels)),
                "data": counts,
            }]
        }
    })
    
