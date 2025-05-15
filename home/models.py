from django.db import models

class Cuidador(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    profissao = models.CharField(max_length=200 , verbose_name="Profissão")

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

    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"



    def __str__(self):
        return self.nome



class Crianca(models.Model):
    SIM_OU_NAO = [
        ('sim', 'Sim'),
        ('não', 'Não'),
    ]

    AVOS_OU_PAIS_OU_TIOS = [
        ("avós", "avós"),
        ("Pais","Pais"),
        ("Outros", "Outros"),
    ]

    SALA1_OU_SALA2 = [
        ("sala 1", "sala 1"),
        ("sala 2", "sala 2"),
    ]
    
    nome = models.CharField(max_length=100)
    data_de_nascimento = models.DateField()
    qual_sala = models.CharField(max_length=100, choices=SALA1_OU_SALA2, verbose_name="Qual e a sala?")
    rua = models.CharField(max_length=200)
    numero = models.IntegerField(verbose_name="Número")
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=200)
    mora_com_quem = models.CharField(max_length=200,  choices=AVOS_OU_PAIS_OU_TIOS, verbose_name="Mora com quem?")
    tem_irmaos = models.CharField(max_length=3, choices=SIM_OU_NAO, verbose_name="Tem irmãos?")
    problema_saude_qual = models.CharField(max_length=200, choices=SIM_OU_NAO, verbose_name="problema saúde qual")
    medicamento_continuo = models.CharField(max_length=200,  choices=SIM_OU_NAO, verbose_name = "Medicamento continuo?")
    mendicamento_qual = models.CharField(max_length=200,verbose_name="Medicamento qual?")
    tem_alergias = models.CharField(max_length=200,  choices=SIM_OU_NAO,verbose_name="Tém alergias?")
    alergias_qual = models.CharField(max_length=200, verbose_name="Alergias qual?")
    responsavel = models.ForeignKey('Responsavel', on_delete=models.CASCADE, related_name='criancas', verbose_name="responsável")


    class Meta:
        verbose_name = "Criança"
        verbose_name_plural = "Crianças"

    def __str__(self):
        return self.nome



class Registro_Diario(models.Model):
    NADA_OU_POUCO_OU_TUDO = [
        ('nada', 'nada'),
        ('pouco', 'pouco'),
        ('tudo', 'tudo')
    ]

    ANO_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ]
   
    SIM_OU_NAO = [
        ('sim', 'Sim'),
        ('não', 'Não'),
    ]

    TRANQUILO_OU_AGITADO_NAODORMIU = [
        ("tranquilo", "tranquilo"),
        ("agitado", "agitado"),
        ("não dormiu", "não dormiu"),
    ]

    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE, related_name='registros', verbose_name="Criança")
    cuidador = models.ForeignKey(Cuidador, on_delete=models.SET_NULL, null=True, related_name='registros')
    data = models.DateField()
    cafe_da_manha = models.CharField(max_length=100, verbose_name="Café da manhã", choices=NADA_OU_POUCO_OU_TUDO)
    almoco = models.CharField(max_length=100, null=True, blank=True, verbose_name="Almoço", choices=NADA_OU_POUCO_OU_TUDO)
    colacao = models.CharField(max_length=100, verbose_name = "Colação", choices=NADA_OU_POUCO_OU_TUDO)
    jantar = models.CharField(max_length=100, choices=NADA_OU_POUCO_OU_TUDO)
    evacuacao_liquida = models.CharField(max_length=100, choices=ANO_CHOICES, verbose_name="Evacuação liquida")
    evacuacao_pastosa = models.CharField(max_length=100, choices=ANO_CHOICES, verbose_name="Evacuação pastosa")
    banho = models.CharField(max_length=100, choices=SIM_OU_NAO)
    sono = models.CharField(max_length=100, choices=TRANQUILO_OU_AGITADO_NAODORMIU)
    observacoes = models.TextField(max_length=100,verbose_name = "observações")
   

    class Meta:
        verbose_name = "Registro Diário"
        verbose_name_plural = "Registro Diário"

    def __str__(self):
        return f"Registro de {self.crianca.nome} em {self.data}"

