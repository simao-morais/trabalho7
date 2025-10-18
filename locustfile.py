from locust import HttpUser, task, between
import random
import json

class PetClinicUser(HttpUser):
    """
    Simula um usuário acessando o Spring PetClinic.
    """
    
    # Tempo de espera entre requisições (1 a 3 segundos)
    wait_time = between(1, 3)
    
    # Lista de IDs de owners existentes (será preenchida no início)
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
                print(f"✓ {len(self.owner_ids)} owners carregados para teste")
        except Exception as e:
            print(f"⚠ Erro ao carregar owners: {e}")
            # IDs padrão caso falhe
            self.owner_ids = list(range(1, 11))
    
    @task(40)  # 40% das requisições
    def get_owners_list(self):
        """
        GET /api/customer/owners - Lista todos os donos
        """
        with self.client.get(
            "/api/customer/owners",
            catch_response=True,
            name="GET /owners (lista)"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status {response.status_code}")
    
    @task(30)  # 30% das requisições
    def get_owner_by_id(self):
        """
        GET /api/customer/owners/{id} - Busca um dono específico
        """
        if not self.owner_ids:
            return
        
        owner_id = random.choice(self.owner_ids)
        
        with self.client.get(
            f"/api/customer/owners/{owner_id}",
            catch_response=True,
            name="GET /owners/{id}"
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.failure("Owner não encontrado")
            else:
                response.failure(f"Status {response.status_code}")
    
    @task(20)  # 20% das requisições
    def get_vets(self):
        """
        GET /api/vet/vets - Lista todos os veterinários
        """
        with self.client.get(
            "/api/vet/vets",
            catch_response=True,
            name="GET /vets"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status {response.status_code}")
    
    @task(10)  # 10% das requisições
    def create_owner(self):
        """
        POST /api/customer/owners - Cria um novo dono
        """
        # Gera dados aleatórios para o novo owner
        random_id = random.randint(10000, 99999)
        
        new_owner = {
            "firstName": f"Teste{random_id}",
            "lastName": f"Silva{random_id}",
            "address": f"Rua Teste, {random_id}",
            "city": "Picos",
            "telephone": f"89999{random_id % 10000:04d}"
        }
        
        with self.client.post(
            "/api/customer/owners",
            json=new_owner,
            catch_response=True,
            name="POST /owners (criar)"
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
                # Adiciona o novo ID à lista se retornou
                try:
                    created = response.json()
                    if 'id' in created:
                        self.owner_ids.append(created['id'])
                except:
                    pass
            else:
                response.failure(f"Status {response.status_code}")