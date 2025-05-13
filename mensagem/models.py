from django.db import models
from django.contrib.auth.models import User
# from .models import Crianca  # Descomente isso se tiver o modelo Crianca

class Mensagem(models.Model):
    COMUNICACAO_OU_EVENTO_OU_OBSERVACAO_OU_PEDAGOGICOS = [
        ("comunicação", "Comunicação"),
        ("evento","Evento"),
        ("observação","Observação"),
        ("pedagogicos","Pedagogicos"),
    ]

    tipo = models.CharField(max_length=255, choices=COMUNICACAO_OU_EVENTO_OU_OBSERVACAO_OU_PEDAGOGICOS,  verbose_name="Tipo")
    descricao = models.TextField(max_length=100,verbose_name = "Descrições")
    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"

    def __str__(self):
        return self.tipo
