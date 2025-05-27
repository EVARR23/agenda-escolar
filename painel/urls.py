from django.urls import path
from . import views

urlpatterns = [
    path("charts/refeicoes/<int:year>/", views.refeicoes_chart, name="chart-refeicoes"),
    path("charts/sono/<int:year>/", views.sono_chart, name="chart-sono"),
    path("charts/registros-por-crianca/", views.registros_por_crianca_chart, name="chart-registros-por-crianca"),
    path("charts/banho/", views.banho_chart, name="chart-banho"),
    path("charts/evacuacao-liquida/", views.evacuacao_liquida_chart, name="chart-evacuacao-liquida"),
    path("charts/evacuacao-pastosa/", views.evacuacao_pastosa_chart, name="chart-evacuacao-pastosa"),
    path("charts/medicamentos/", views.medicamentos_chart, name="chart-medicamentos"),
    path("charts/problemas-saude/", views.problemas_saude_chart, name="chart-problemas-saude"),
    path("charts/alergias/", views.alergias_chart, name="chart-alergias"),
    path("charts/anos-disponiveis/", views.anos_disponiveis, name="chart-anos-disponiveis"),
    path("statistics/", views.statistics_view, name="statistics-view"),
    path("chart/filter-options/", views.get_filter_options, name="chart-filter-options"),
    
]
