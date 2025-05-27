import random
from random import randint
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from painel.models import Cuidador, Responsavel, Crianca, Registro_Diario

class Command(BaseCommand):
    help = "Popula o banco com dados de exemplo"

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int, default=10, help='Quantidade de registros a criar')

    def handle(self, *args, **options):
        amount = options['amount']

        nomes = ["Ana", "Bruno", "Carla", "Daniel", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Júlia"]
        profissoes = ["Cuidador", "Professor", "Médico", "Enfermeiro", "Motorista"]
        locais_trabalho = ["Hospital", "Escola", "Clínica", "Empresa X", "Instituto Y"]

        # Garante que existe um usuário para associar (usar o primeiro ou criar um default)
        user, created = User.objects.get_or_create(username='default_user')
        
        self.stdout.write("Populando cuidadores...")
        cuidadores = []
        for i in range(amount):
            c = Cuidador.objects.create(
                nome=f"Cuid {nomes[i % len(nomes)]}",
                telefone=f"99999-99{str(i).zfill(2)}",
                profissao=random.choice(profissoes)
            )
            cuidadores.append(c)

        self.stdout.write("Populando responsáveis...")
        responsaveis = []
        for i in range(amount):
            r = Responsavel.objects.create(
                nome=f"Resp {nomes[i % len(nomes)]}",
                telefone=f"98888-88{str(i).zfill(2)}",
                profissao=random.choice(profissoes),
                local_trabalho=random.choice(locais_trabalho),
                auth_user=user
            )
            responsaveis.append(r)

        self.stdout.write("Populando crianças...")
        SELECIONE_SALA = ['sala 1', 'sala 2']
        SELECIONE_AVOS_PAIS_OUTROS = ["avós", "Pais", "Outros"]
        SELECIONE_SIM_NAO = ['sim', 'não']

        for i in range(amount):
            Crianca.objects.create(
                nome=f"Criança {nomes[i % len(nomes)]}",
                data_de_nascimento=date.today() - timedelta(days=365*randint(2, 6)),
                sal=random.choice(SELECIONE_SALA),
                ru=f"RU{1000 + i}",
                num=randint(1, 100),
                cid=f"Cidade{i}",
                cep=f"00000-0{i:03d}",
                mor_q=random.choice(SELECIONE_AVOS_PAIS_OUTROS),
                irm=random.choice(SELECIONE_SIM_NAO),
                pr_sau=random.choice(SELECIONE_SIM_NAO),
                med=random.choice(SELECIONE_SIM_NAO),
                med_q="Medicamento X",
                aler=random.choice(SELECIONE_SIM_NAO),
                aler_q="Alergia Y",
                resp=responsaveis[i]
            )

        self.stdout.write("Populando registros diários...")
        SELECIONE_NADA_POUCO_TUDO = ['nada', 'pouco', 'tudo']
        SELECIONE_ANO = ['1', '2', '3']
        SELECIONE_TRANQUILO_AGITADO_NAODORMIU = ["tranquilo", "agitado", "não dormiu"]
        SELECIONE_SIM_NAO = ['sim', 'não']

        criancas = list(Crianca.objects.all())
        for i in range(amount):
            Registro_Diario.objects.create(
                crianca=criancas[i % len(criancas)],
                cuidador=cuidadores[i % len(cuidadores)],
                data=date.today() - timedelta(days=randint(0, 10)),
                cafe=random.choice(SELECIONE_NADA_POUCO_TUDO),
                alm=random.choice(SELECIONE_NADA_POUCO_TUDO),
                col=random.choice(SELECIONE_NADA_POUCO_TUDO),
                jnt=random.choice(SELECIONE_NADA_POUCO_TUDO),
                ev_L=random.choice(SELECIONE_ANO),
                ev_P=random.choice(SELECIONE_ANO),
                bnh=random.choice(SELECIONE_SIM_NAO),
                sono=random.choice(SELECIONE_TRANQUILO_AGITADO_NAODORMIU),
                obs="Sem observações"
            )

        self.stdout.write(self.style.SUCCESS(f"População concluída com {amount} registros!"))
