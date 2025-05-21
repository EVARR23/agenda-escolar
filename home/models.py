from django.db import models
from django.conf import settings


class Cuidador(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    profissao = models.CharField(max_length=200, verbose_name="Profissão")

    class Meta:
        verbose_name = "Cuidador"
        verbose_name_plural = "Cuidadores"

    def __str__(self):
        return self.nome


class Responsavel(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    profissao = models.CharField(max_length=200, verbose_name="Profissão")
    local_trabalho = models.CharField(max_length=100, null=True, blank=True)
    auth_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='responsaveis',
        verbose_name="Usuário",
        default="",
        blank=False
    )

    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"

    def __str__(self):
        return self.nome


class Crianca(models.Model):
    SIM_OU_NAO_OU_SELECIONE = [
        ('selecione', 'Selecione'),
        ('sim', 'Sim'),
        ('não', 'Não'),
    ]

    AVOS_OU_PAIS_OU_TIOS = [
        ("avós", "Avós"),
        ("Pais", "Pais"),
        ("Outros", "Outros"),
    ]

    SALA1_OU_SALA2 = [
        ("sala 1", "Sala 1"),
        ("sala 2", "Sala 2"),
    ]

    nome = models.CharField(max_length=100)
    data_de_nascimento = models.DateField()
    sal = models.CharField(
        max_length=100,
        choices=SALA1_OU_SALA2,
        verbose_name="Qual sala?",
        default="sala 1",
        blank=False
    )
    ru = models.CharField(max_length=200)
    num = models.IntegerField(verbose_name="Num")
    cid = models.CharField(max_length=100)
    cep = models.CharField(max_length=200)
    mor_q = models.CharField(
        max_length=200,
        choices=AVOS_OU_PAIS_OU_TIOS,
        verbose_name="Mora com quem?",
        default="Pais",
        blank=False
    )
    irm = models.CharField(
        max_length=9,  # Corrigido para comportar 'selecione'
        choices=SIM_OU_NAO_OU_SELECIONE,
        verbose_name="Tem irmãos?",
        default="não",
        blank=False
    )
    pr_sau = models.CharField(
        max_length=200,
        choices=SIM_OU_NAO_OU_SELECIONE,
        verbose_name="Prob. saúde",
        default="não",
        blank=False
    )
    med = models.CharField(
        max_length=200,
        choices=SIM_OU_NAO_OU_SELECIONE,
        verbose_name="Medic. contínuo?",
        default="não",
        blank=False
    )
    med_q = models.CharField(max_length=50, verbose_name="Medic qual?")
    aler = models.CharField(
        max_length=200,
        choices=SIM_OU_NAO_OU_SELECIONE,
        verbose_name="Tem alergias?",
        default="não",
        blank=False
    )
    aler_q = models.CharField(max_length=200, verbose_name="Alergias qual?")
    resp = models.ForeignKey(
        'Responsavel',
        on_delete=models.CASCADE,
        related_name='criancas',
        verbose_name="Responsável",
        default="",
        blank=False
    )

    class Meta:
        verbose_name = "Criança"
        verbose_name_plural = "Crianças"

    def __str__(self):
        return self.nome


class Registro_Diario(models.Model):
    NADA_OU_POUCO_OU_TUDO = [
        ('nada', 'Nada'),
        ('pouco', 'Pouco'),
        ('tudo', 'Tudo')
    ]

    ANO_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ]

    SIM_OU_NAO_OU_SELECIONE = [
        ('sim', 'Sim'),
        ('não', 'Não'),
    ]

    TRANQUILO_OU_AGITADO_NAODORMIU = [
        ("tranquilo", "Tranquilo"),
        ("agitado", "Agitado"),
        ("não dormiu", "Não dormiu"),
    ]

    crianca = models.ForeignKey(
        Crianca,
        on_delete=models.CASCADE,
        related_name='registros',
        verbose_name="Criança",
        default="",
        blank=False
    )
    cuidador = models.ForeignKey(
        Cuidador,
        on_delete=models.SET_NULL,
        null=True,
        related_name='registros',
        default="",
        blank=False
    )

    data = models.DateField()
    cafe = models.CharField(
        max_length=100,
        verbose_name="Café",
        choices=NADA_OU_POUCO_OU_TUDO,
        default='tudo',
        blank=False
    )
    alm = models.CharField(
        max_length=100,
        verbose_name="Almoço",
        choices=NADA_OU_POUCO_OU_TUDO,
        default='tudo',
        blank=False
    )
    col = models.CharField(
        max_length=100,
        verbose_name="Colação",
        choices=NADA_OU_POUCO_OU_TUDO,
        default='tudo',
        blank=False
    )
    jnt = models.CharField(
        max_length=100,
        verbose_name="Janta",
        choices=NADA_OU_POUCO_OU_TUDO,
        default='tudo',
        blank=False
    )
    ev_L = models.CharField(
        max_length=1,
        choices=ANO_CHOICES,
        verbose_name="Ev. Líquida",
        default='1',
        blank=False
    )
    ev_P = models.CharField(
        max_length=1,
        choices=ANO_CHOICES,
        verbose_name="Ev. Pastosa",
        default='1',
        blank=False
    )
    bnh = models.CharField(
        max_length=100,
        verbose_name="Banho",
        choices=SIM_OU_NAO_OU_SELECIONE,
        default='não',
        blank=False
    )
    sono = models.CharField(
        max_length=100,
        choices=TRANQUILO_OU_AGITADO_NAODORMIU,
        default="tranquilo",
        blank=False
    )
    obs = models.TextField(
        max_length=25,
        verbose_name="Observações",
        blank=False
    )

    class Meta:
        verbose_name = "Registro Diário"
        verbose_name_plural = "Registro Diário"

    def __str__(self):
        return f"Registro de {self.crianca.nome} em {self.data}"
