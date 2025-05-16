from django.db import models

class Mensagem(models.Model):
    TIPOS_MENSAGEM = [
        ("comunicacao", "Comunicação"),
        ("evento", "Evento"),
        ("observacao", "Observação"),
        ("pedagogicos", "Pedagógicos"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS_MENSAGEM, verbose_name="Tipo")
    descricao = models.TextField(verbose_name="Descrição")
    imagem = models.ImageField(upload_to="images/user")
    crianca = models.ForeignKey('home.Crianca', on_delete=models.CASCADE, related_name='mensagem', verbose_name="criança")

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"

    def __str__(self):
        return self.tipo

