from django.db import models

class Mensagem(models.Model):
    TIPOS_MENSAGEM = [
        ("comunicacao", "Comunicação"),
        ("evento", "Evento"),
        ("observacao", "Observação"),
        ("pedagogicos", "Pedagógicos"),
    ]

    SALA1_OU_SALA2 = [
        ("sala 1", "sala 1"),
        ("sala 2", "sala 2"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS_MENSAGEM, verbose_name="Tipo")
    descricao = models.TextField(verbose_name="Descrição")
    imagem = models.ImageField(upload_to="images/user")

    salas = models.ManyToManyField('home.Sala', blank=True)  # Relacionamento M:N
    criancas = models.ManyToManyField('home.Crianca', blank=True)  # Relacionamento M:N

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"

    def __str__(self):
        return self.tipo

