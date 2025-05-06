from django.db import models

class Cuidador(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    profissao = models.CharField(max_length=200 , verbose_name="Profissão")

    def __str__(self):
        return self.nome


class Responsavel(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    profissao = models.CharField(max_length=200, verbose_name="Profissão")
    local_trabalho = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nome


class Crianca(models.Model):
    nome = models.CharField(max_length=100)
    data_de_nascimento = models.DateField()
    rua = models.CharField(max_length=200)
    numero = models.IntegerField(verbose_name="Número")
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=200)
    mora_com_quem = models.CharField(max_length=200)
    tem_irmaos = models.CharField(max_length=200, verbose_name = "Tem irmãos")
    problema_saude_qual = models.CharField(max_length=200, verbose_name=("problema saúde qual"))
    medicamento_continuo = models.CharField(max_length=200)
    mendicamento_qual = models.CharField(max_length=200)
    tem_alergias = models.CharField(max_length=200)
    alergias_qual = models.CharField(max_length=200)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, related_name='criancas', verbose_name="responsável")

    def __str__(self):
        return self.nome


class Registro_Diario(models.Model):
    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE, related_name='registros', verbose_name="Criança")
    cuidador = models.ForeignKey(Cuidador, on_delete=models.SET_NULL, null=True, related_name='registros')
    data = models.DateField()
    cafe_da_manha = models.CharField(max_length=100, verbose_name="Café da manhã")
    almoco = models.CharField(max_length=100, null=True, blank=True, verbose_name="Almoço")
    colacao = models.CharField(max_length=100, verbose_name = "Colação")
    jantar = models.CharField(max_length=100)
    evacuacao_liquida = models.CharField(max_length=100, verbose_name="Evacuação liquida")
    evacuacao_pastosa = models.CharField(max_length=100,verbose_name="Evacuação pastosa")
    banho = models.CharField(max_length=100)
    sono = models.CharField(max_length=100)
    observacoes = models.CharField(max_length=100,verbose_name = "observações")
    assinatura = models.CharField(max_length=100)

    def __str__(self):
        return f"Registro de {self.crianca.nome} em {self.data}"

