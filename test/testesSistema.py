import unittest
import sys
import os

# Adicionar o diretório do app ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

class TestesSistema(unittest.TestCase):
    """Testes de sistema para integração completa da aplicação"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_01_integracao_sistema_navegacao(self):
        """Teste 1: Integração completa do sistema de navegação"""
        print("\n  Testando fluxo completo de navegação...")
        
        # 1. Acessar página inicial
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        print("  ✓ Página inicial carregada")
        
        # 2. Navegar para login
        response = self.client.get('/pages/login.html')
        self.assertEqual(response.status_code, 200)
        print("  ✓ Página de login carregada")
        
        # 3. Navegar para cadastro
        response = self.client.get('/pages/cadastro.html')
        self.assertEqual(response.status_code, 200)
        print("  ✓ Página de cadastro carregada")
        
        # 4. Navegar para cadastro de tutor
        response = self.client.get('/pages/cadastro-tutor-new.html')
        self.assertEqual(response.status_code, 200)
        print("  ✓ Página de cadastro de tutor carregada")
        
        # 5. Voltar para cadastro de clínica
        response = self.client.get('/pages/cadastro-clinica.html')
        self.assertEqual(response.status_code, 200)
        print("  ✓ Página de cadastro de clínica carregada")
        
        print("  ✅ Sistema de navegação totalmente integrado")
    
    """  def test_02_integracao_sistema_autenticacao(self):
        #Teste 2: Integração do sistema de autenticação e sessão
        print("\n  Testando integração de autenticação...")
        
        with self.client as client:
            # 1. Verificar estado inicial (não logado)
            response = client.get('/check_login')
            data = response.get_json()
            self.assertFalse(data['logged_in'])
            print("  ✓ Estado inicial: não autenticado")
            
            # 2. Simular login criando sessão
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['user_name'] = 'João Silva'
                sess['user_type'] = 'tutor'
            print("  ✓ Sessão criada (simulando login)")
            
            # 3. Verificar estado logado
            response = client.get('/check_login')
            data = response.get_json()
            self.assertTrue(data['logged_in'])
            self.assertEqual(data['user_name'], 'João Silva')
            self.assertEqual(data['user_type'], 'tutor')
            print("  ✓ Estado confirmado: autenticado como tutor")
            
            # 4. Tentar acessar rota protegida (deve funcionar)
            response = client.get('/dashboard', follow_redirects=False)
            # Pode retornar 200 ou 500 (erro de banco), mas não 302 (redirect)
            self.assertNotEqual(response.status_code, 302)
            print("  ✓ Acesso a rota protegida permitido")
            
            # 5. Fazer logout
            response = client.get('/logout', follow_redirects=False)
            self.assertEqual(response.status_code, 302)
            print("  ✓ Logout executado")
            
            # 6. Verificar estado após logout
            response = client.get('/check_login')
            data = response.get_json()
            self.assertFalse(data['logged_in'])
            print("  ✓ Estado confirmado: não autenticado")
            
        print("  ✅ Sistema de autenticação totalmente integrado")
    """
    
    """ 
        def test_03_integracao_controle_acesso(self):
        #Teste 3: Integração do sistema de controle de acesso
        print("\n  Testando integração de controle de acesso...")
        
        rotas_publicas = [
            ('/', 'Página Inicial'),
            ('/pages/login.html', 'Login'),
            ('/pages/cadastro.html', 'Cadastro'),
            ('/check_login', 'Check Login')
        ]
        
        rotas_protegidas = [
            ('/dashboard', 'Dashboard'),
            ('/gerenciar-pets', 'Gerenciar Pets'),
            ('/editar-perfil.html', 'Editar Perfil')
        ]
        
        # 1. Testar rotas públicas (devem ser acessíveis)
        print("  Testando rotas públicas:")
        for rota, nome in rotas_publicas:
            response = self.client.get(rota)
            self.assertIn(response.status_code, [200, 302])
            print(f"    ✓ {nome} - Acessível")
        
        # 2. Testar rotas protegidas SEM autenticação (devem bloquear)
        print("  Testando rotas protegidas (sem login):")
        for rota, nome in rotas_protegidas:
            response = self.client.get(rota, follow_redirects=False)
            self.assertIn(response.status_code, [302, 403])
            print(f"    ✓ {nome} - Bloqueada")
        
        # 3. Testar rotas protegidas COM autenticação
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['user_type'] = 'tutor'
            
            print("  Testando rotas protegidas (com login):")
            for rota, nome in rotas_protegidas:
                response = client.get(rota, follow_redirects=False)
                # Com login, não deve redirecionar (302)
                # Pode dar 200 (sucesso) ou 500 (erro de banco)
                self.assertNotEqual(response.status_code, 302)
                print(f"    ✓ {nome} - Permitida")
        
        print("  ✅ Sistema de controle de acesso totalmente integrado") 
    """

    """ def test_04_integracao_operacoes_protegidas(self):
        #Teste 4: Integração de operações que exigem autenticação
        print("\n  Testando integração de operações protegidas...")
        
        operacoes = [
            ('/adicionar-pet', {'nome_pet': 'Rex', 'especie': 'Cachorro'}, 'Adicionar Pet'),
            ('/atualizar-pet', {'pet_id': 1, 'nome_pet': 'Rex'}, 'Atualizar Pet'),
            ('/salvar-agendamento', {'pet_id': 1, 'clinica_id': 1}, 'Salvar Agendamento')
        ]
        
        # 1. Tentar operações SEM autenticação
        print("  Testando operações sem autenticação:")
        for rota, dados, nome in operacoes:
            response = self.client.post(rota, data=dados)
            self.assertEqual(response.status_code, 403)
            print(f"    ✓ {nome} - Bloqueada (403)")
        
        # 2. Tentar operações COM autenticação
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['user_type'] = 'tutor'
            
            print("  Testando operações com autenticação:")
            for rota, dados, nome in operacoes:
                response = client.post(rota, data=dados)
                # Com autenticação, não deve retornar 403
                self.assertNotEqual(response.status_code, 403)
                print(f"    ✓ {nome} - Permitida (não bloqueada)")
        
        print("  ✅ Sistema de operações protegidas integrado") """
    
    def test_05_integracao_fluxo_completo_usuario(self):
        """Teste 5: Integração de fluxo completo do usuário"""
        print("\n  Testando fluxo completo de uso do sistema...")
        
        with self.client as client:
            # 1. Usuário acessa página inicial
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            print("  ✓ Passo 1: Acessou página inicial")
            
            # 2. Usuário navega para login
            response = client.get('/pages/login.html')
            self.assertEqual(response.status_code, 200)
            print("  ✓ Passo 2: Navegou para login")
            
            # 3. Usuário decide se cadastrar
            response = client.get('/pages/cadastro.html')
            self.assertEqual(response.status_code, 200)
            print("  ✓ Passo 3: Acessou página de cadastro")
            
            # 4. Usuário escolhe cadastro de tutor
            response = client.get('/pages/cadastro-tutor-new.html')
            self.assertEqual(response.status_code, 200)
            print("  ✓ Passo 4: Escolheu cadastro de tutor")
            
            # 5. Simular que usuário completou cadastro e fez login
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['user_name'] = 'Maria Santos'
                sess['user_type'] = 'tutor'
            print("  ✓ Passo 5: Cadastrou e fez login")
            
            # 6. Verificar que está autenticado
            response = client.get('/check_login')
            data = response.get_json()
            self.assertTrue(data['logged_in'])
            print("  ✓ Passo 6: Confirmou autenticação")
            
            # 7. Tentar acessar dashboard
            response = client.get('/dashboard', follow_redirects=False)
            self.assertNotEqual(response.status_code, 302)
            print("  ✓ Passo 7: Acessou dashboard")
            
            # 8. Tentar gerenciar pets
            response = client.get('/gerenciar-pets', follow_redirects=False)
            self.assertNotEqual(response.status_code, 302)
            print("  ✓ Passo 8: Acessou gerenciamento de pets")
            
            # 9. Fazer logout
            response = client.get('/logout', follow_redirects=False)
            self.assertEqual(response.status_code, 302)
            print("  ✓ Passo 9: Fez logout")
            
            # 10. Verificar que não está mais autenticado
            response = client.get('/check_login')
            data = response.get_json()
            self.assertFalse(data['logged_in'])
            print("  ✓ Passo 10: Confirmou logout")
        
        print("  ✅ Fluxo completo do usuário totalmente integrado")

if __name__ == '__main__':
    unittest.main(verbosity=2)