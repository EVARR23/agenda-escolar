from django.contrib import admin
from .models import Cuidador, Responsavel, Crianca,Registro_Diario

admin.site.register(Cuidador)
admin.site.register(Responsavel)
admin.site.register(Crianca)
admin.site.register(Registro_Diario)

