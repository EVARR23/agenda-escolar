from django.contrib import admin
from django.urls import path
from home.views import line_chart, line_chart_json
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .admin import admin_statistics_view 

urlpatterns = [
      path(   # new
        "admin/statistics/",
        admin.site.admin_view(admin_statistics_view),
        name="admin-statistics"
    ),
    path('agenda/', admin.site.urls),
    path('chart/', line_chart, name='line_chart'),
    path('chartJSON/', line_chart_json, name='line_chart_json'),
    path('painel/', include('painel.urls')),
  

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
