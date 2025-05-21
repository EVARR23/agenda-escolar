from django.db import models
from django.conf import settings


SELECIONE = [('selecione', 'Selecione')]

SELECIONE_SIM_NAO = SELECIONE + [
    ('sim', 'Sim'),
    ('não', 'Não'),
]

SELECIONE_AVOS_PAIS_OUTROS = SELECIONE + [
    ("avós", "Avós"),
    ("Pais", "Pais"),
    ("Outros", "Outros"),
]

SELECIONE_SALA = SELECIONE + [
    ("sala 1", "Sala 1"),
    ("sala 2", "Sala 2"),
]

SELECIONE_NADA_POUCO_TUDO = SELECIONE + [
    ('nada', 'Nada'),
    ('pouco', 'Pouco'),
    ('tudo', 'Tudo'),
]

SELECIONE_ANO = SELECIONE + [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
]

SELECIONE_TRANQUILO_AGITADO_NAODORMIU = SELECIONE + [
    ("tranquilo", "Tranquilo"),
    ("agitado", "Agitado"),
    ("não dormiu", "Não dormiu"),
]


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

    nome = models.CharField(max_length=100)
    data_de_nascimento = models.DateField()
    sal = models.CharField(
        max_length=100,
        choices=SELECIONE_SALA,
        verbose_name="Qual sala?",
        default="selecione",
        blank=False
    )
    ru = models.CharField(max_length=200)
    num = models.IntegerField(verbose_name="Num")
    cid = models.CharField(max_length=100)
    cep = models.CharField(max_length=200)
    mor_q = models.CharField(
        max_length=200,
        choices=SELECIONE_AVOS_PAIS_OUTROS,
        verbose_name="Mora com quem?",
        default="selecione",
        blank=False
    )
    irm = models.CharField(
        max_length=9,
        choices=SELECIONE_SIM_NAO,
        verbose_name="Tem irmãos?",
        default="selecione",
        blank=False
    )
    pr_sau = models.CharField(
        max_length=200,
        choices=SELECIONE_SIM_NAO,
        verbose_name="Prob. saúde",
        default="selecione",
        blank=False
    )
    med = models.CharField(
        max_length=200,
        choices=SELECIONE_SIM_NAO,
        verbose_name="Medic. contínuo?",
        default="selecione",
        blank=False
    )
    med_q = models.CharField(max_length=50, verbose_name="Medic qual?")
    aler = models.CharField(
        max_length=200,
        choices=SELECIONE_SIM_NAO,
        verbose_name="Tem alergias?",
        default="selecione",
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
        choices=SELECIONE_NADA_POUCO_TUDO,
        default='selecione',
        blank=False
    )
    alm = models.CharField(
        max_length=100,
        verbose_name="Almoço",
        choices=SELECIONE_NADA_POUCO_TUDO,
        default='selecione',
        blank=False
    )
    col = models.CharField(
        max_length=100,
        verbose_name="Colação",
        choices=SELECIONE_NADA_POUCO_TUDO,
        default='selecione',
        blank=False
    )
    jnt = models.CharField(
        max_length=100,
        verbose_name="Janta",
        choices=SELECIONE_NADA_POUCO_TUDO,
        default='selecione',
        blank=False
    )
    ev_L = models.CharField(
    max_length=9,  # mudou de 1 para 9
    choices=SELECIONE_ANO,
    verbose_name="Ev. Líquida",
    default='selecione',
    blank=False
    )
    ev_P = models.CharField(
    max_length=9,  # mudou de 1 para 9
    choices=SELECIONE_ANO,
    verbose_name="Ev. Pastosa",
    default='selecione',
    blank=False
    )
    bnh = models.CharField(
        max_length=100,
        verbose_name="Banho",
        choices=SELECIONE_SIM_NAO,
        default='selecione',
        blank=False
    )
    sono = models.CharField(
        max_length=100,
        choices=SELECIONE_TRANQUILO_AGITADO_NAODORMIU,
        default="selecione",
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
