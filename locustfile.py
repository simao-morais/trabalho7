from locust import HttpUser, task, between
import random
import json
import logging
from datetime import datetime
from colorama import Fore, Style, init
import os

# Inicializa o colorama (para colorir o terminal no Windows/Linux)
init(autoreset=True)

# === Configuração de LOGGING ===
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, f"locust_petclinic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()  # mostra também no terminal
    ]
)

logger = logging.getLogger(__name__)


class PetClinicUser(HttpUser):
    """
    Simula um usuário acessando o Spring PetClinic.
    """

    wait_time = between(1, 3)
    owner_ids = []

    def on_start(self):
        """
        Executado quando cada usuário virtual inicia.
        Busca IDs de owners existentes para usar nos testes.
        """
        try:
            response = self.client.get("/api/customer/owners")
            if response.status_code == 200:
                owners = response.json()
                self.owner_ids = [owner['id'] for owner in owners if 'id' in owner]
                msg = f"{len(self.owner_ids)} owners carregados para teste"
                print(Fore.GREEN + "✓ " + msg)
                logger.info(msg)
            else:
                msg = f"Falha ao carregar owners. Status: {response.status_code}"
                print(Fore.RED + "✗ " + msg)
                logger.warning(msg)
        except Exception as e:
            msg = f"Erro ao carregar owners: {e}"
            print(Fore.YELLOW + "⚠ " + msg)
            logger.error(msg)
            self.owner_ids = list(range(1, 11))

    @task(40)
    def get_owners_list(self):
        """GET /api/customer/owners - Lista todos os donos"""
        with self.client.get("/api/customer/owners", catch_response=True, name="GET /owners (lista)") as response:
            if response.status_code == 200:
                response.success()
                logger.info("GET /owners (lista) - sucesso")
            else:
                response.failure(f"Status {response.status_code}")
                logger.warning(f"GET /owners (lista) - falha: {response.status_code}")

    @task(30)
    def get_owner_by_id(self):
        """GET /api/customer/owners/{id} - Busca um dono específico"""
        if not self.owner_ids:
            logger.warning("Lista de owner_ids vazia, pulando tarefa get_owner_by_id.")
            return

        owner_id = random.choice(self.owner_ids)
        with self.client.get(f"/api/customer/owners/{owner_id}",
                             catch_response=True,
                             name="GET /owners/{id}") as response:
            if response.status_code == 200:
                response.success()
                logger.info(f"GET /owners/{owner_id} - sucesso")
            elif response.status_code == 404:
                response.failure("Owner não encontrado")
                logger.warning(f"GET /owners/{owner_id} - não encontrado (404)")
            else:
                response.failure(f"Status {response.status_code}")
                logger.error(f"GET /owners/{owner_id} - erro {response.status_code}")

    @task(20)
    def get_vets(self):
        """GET /api/vet/vets - Lista todos os veterinários"""
        with self.client.get("/api/vet/vets", catch_response=True, name="GET /vets") as response:
            if response.status_code == 200:
                response.success()
                logger.info("GET /vets - sucesso")
            else:
                response.failure(f"Status {response.status_code}")
                logger.warning(f"GET /vets - falha {response.status_code}")

    @task(10)
    def create_owner(self):
        """POST /api/customer/owners - Cria um novo dono"""
        random_id = random.randint(10000, 99999)
        new_owner = {
            "firstName": f"Teste{random_id}",
            "lastName": f"Silva{random_id}",
            "address": f"Rua Teste, {random_id}",
            "city": "Picos",
            "telephone": f"89999{random_id % 10000:04d}"
        }

        with self.client.post("/api/customer/owners",
                              json=new_owner,
                              catch_response=True,
                              name="POST /owners (criar)") as response:
            if response.status_code in [200, 201]:
                response.success()
                logger.info(f"POST /owners - criado com sucesso ({response.status_code})")
                try:
                    created = response.json()
                    if 'id' in created:
                        self.owner_ids.append(created['id'])
                        logger.info(f"Novo owner adicionado à lista: {created['id']}")
                except Exception as e:
                    logger.warning(f"Erro ao interpretar resposta JSON: {e}")
            else:
                response.failure(f"Status {response.status_code}")
                logger.error(f"POST /owners - falha {response.status_code}")
