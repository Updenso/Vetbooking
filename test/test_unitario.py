import unittest
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import os

# Adicionar o diretório do app ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, allowed_file

class TestesUnitarios(unittest.TestCase):
    """Testes unitários simples para funções individuais"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_01_allowed_file_png(self):
        """Teste 1: Arquivo PNG deve ser aceito"""
        resultado = allowed_file('foto.png')
        self.assertTrue(resultado)
    
    def test_02_allowed_file_pdf(self):
        """Teste 2: Arquivo PDF não deve ser aceito"""
        resultado = allowed_file('documento.pdf')
        self.assertFalse(resultado)
    
    def test_03_hash_senha(self):
        """Teste 3: Hash de senha deve funcionar"""
        senha = "minha_senha_123"
        senha_hash = generate_password_hash(senha)
        
        # Senha e hash devem ser diferentes
        self.assertNotEqual(senha, senha_hash)
        
        # Hash deve validar senha correta
        self.assertTrue(check_password_hash(senha_hash, senha))
    
    def test_04_pagina_inicial(self):
        """Teste 4: Página inicial deve carregar"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_05_check_login_sem_usuario(self):
        """Teste 5: Check login sem usuário logado"""
        response = self.client.get('/check_login')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['logged_in'])

if __name__ == '__main__':
    unittest.main(verbosity=2)