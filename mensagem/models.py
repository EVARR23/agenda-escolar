from django.db import models

class Mensagem(models.Model):
    SELECIONE = [
        ('selecione', 'Selecione'),
    ]

    SELECIONE_TIPOS_MENSAGEM = SELECIONE + [
        ("comunicacao", "Comunicação"),
        ("evento", "Evento"),
        ("observacao", "Observação"),
        ("pedagogicos", "Pedagógicos"),
    ]

    tipo = models.CharField(
        max_length=20,
        choices=SELECIONE_TIPOS_MENSAGEM,
        verbose_name="Tipo",
        default="selecione",  # valor padrão
        blank=False           # impede deixar vazio no admin
    )
    descricao = models.TextField(verbose_name="Descrição")
    imagem = models.ImageField(upload_to="images/user")
    crianca = models.ForeignKey(
        'home.Crianca',
        on_delete=models.CASCADE,
        related_name='mensagem',
        verbose_name="Criança",
        default="",  # valor padrão
        blank=False       
    )

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.crianca}"
