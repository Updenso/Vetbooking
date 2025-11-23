import unittest
import sys
import os

# Adicionar o diretório do app ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

class TestesFuncionais(unittest.TestCase):
    """Testes funcionais simples para fluxos da aplicação"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_01_fluxo_acesso_login(self):
        """Teste 1: Fluxo completo de acesso à página de login"""
        # Acessar página inicial
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Acessar página de login
        response = self.client.get('/pages/login.html')
        self.assertEqual(response.status_code, 200)
        print("\n  ✓ Fluxo: Inicial → Login funcionando")
    
    def test_02_fluxo_navegacao_cadastro(self):
        """Teste 2: Fluxo de navegação para cadastro"""
        # Página de escolha de cadastro
        response = self.client.get('/pages/cadastro.html')
        self.assertEqual(response.status_code, 200)
        
        # Página de cadastro de tutor
        response = self.client.get('/pages/cadastro-tutor-new.html')
        self.assertEqual(response.status_code, 200)
        
        # Página de cadastro de clínica
        response = self.client.get('/pages/cadastro-clinica.html')
        self.assertEqual(response.status_code, 200)
        
        print("\n  ✓ Fluxo: Navegação por páginas de cadastro funcionando")
    
    def test_03_protecao_rotas_autenticadas(self):
        """Teste 3: Proteção de rotas que exigem autenticação"""
        rotas_protegidas = [
            ('/dashboard', 'Dashboard'),
            ('/gerenciar-pets', 'Gerenciar Pets'),
            ('/editar-perfil.html', 'Editar Perfil')
        ]
        
        for rota, nome in rotas_protegidas:
            response = self.client.get(rota, follow_redirects=False)
            # Deve redirecionar ou bloquear
            self.assertIn(response.status_code, [302, 403], 
                         f"{nome} não está protegida")
        
        print("\n  ✓ Todas as rotas protegidas estão bloqueando acesso")
    
    def test_04_fluxo_sessao_usuario(self):
        """Teste 4: Fluxo de sessão de usuário"""
        with self.client as client:
            # Verificar que não está logado
            response = client.get('/check_login')
            data = response.get_json()
            self.assertFalse(data['logged_in'])
            
            # Simular login (criar sessão)
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['user_name'] = 'Teste Usuário'
                sess['user_type'] = 'tutor'
            
            # Verificar que está logado
            response = client.get('/check_login')
            data = response.get_json()
            self.assertTrue(data['logged_in'])
            self.assertEqual(data['user_name'], 'Teste Usuário')
            
            # Fazer logout
            response = client.get('/logout', follow_redirects=False)
            self.assertEqual(response.status_code, 302)
            
            # Verificar que não está mais logado
            response = client.get('/check_login')
            data = response.get_json()
            self.assertFalse(data['logged_in'])
            
        print("\n  ✓ Fluxo: Login → Verificação → Logout funcionando")
    
    def test_05_tentativa_acao_sem_autenticacao(self):
        """Teste 5: Tentativa de ações sem autenticação"""
        # Tentar adicionar pet sem login
        response = self.client.post('/adicionar-pet', data={
            'nome_pet': 'Rex',
            'especie': 'Cachorro'
        })
        self.assertEqual(response.status_code, 403)
        
        # Tentar atualizar pet sem login
        response = self.client.post('/atualizar-pet', data={
            'pet_id': 1,
            'nome_pet': 'Rex Atualizado'
        })
        self.assertEqual(response.status_code, 403)
        
        # Tentar salvar agendamento sem login
        response = self.client.post('/salvar-agendamento', data={
            'pet_id': 1,
            'clinica_id': 1
        })
        self.assertEqual(response.status_code, 403)
        
        print("\n  ✓ Ações protegidas bloqueando acesso não autenticado")

if __name__ == '__main__':
    unittest.main(verbosity=2)