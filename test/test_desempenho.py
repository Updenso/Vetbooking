import unittest
import time
import sys
import os

# Adicionar o diretório do app ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

class TestesDesempenho(unittest.TestCase):
    """Testes de desempenho simples da aplicação"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_01_desempenho_pagina_inicial(self):
        """Teste 1: Desempenho da página inicial em múltiplas requisições"""
        num_requisicoes = 20
        tempos = []
        
        print(f"\n  Executando {num_requisicoes} requisições...")
        
        for i in range(num_requisicoes):
            inicio = time.time()
            response = self.client.get('/')
            fim = time.time()
            
            tempo = fim - inicio
            tempos.append(tempo)
            self.assertEqual(response.status_code, 200)
        
        tempo_medio = sum(tempos) / len(tempos)
        tempo_minimo = min(tempos)
        tempo_maximo = max(tempos)
        
        print(f"  Tempo médio: {tempo_medio:.4f}s")
        print(f"  Tempo mínimo: {tempo_minimo:.4f}s")
        print(f"  Tempo máximo: {tempo_maximo:.4f}s")
        
        # Página inicial deve responder em média em menos de 1 segundo
        self.assertLess(tempo_medio, 1.0, "Página inicial muito lenta")
    
    def test_02_desempenho_check_login(self):
        """Teste 2: Desempenho do endpoint check_login"""
        num_requisicoes = 50
        tempos = []
        
        print(f"\n  Testando {num_requisicoes} verificações de login...")
        
        for i in range(num_requisicoes):
            inicio = time.time()
            response = self.client.get('/check_login')
            fim = time.time()
            
            tempo = fim - inicio
            tempos.append(tempo)
            self.assertEqual(response.status_code, 200)
        
        tempo_medio = sum(tempos) / len(tempos)
        tempo_total = sum(tempos)
        
        print(f"  Tempo médio: {tempo_medio:.4f}s")
        print(f"  Tempo total: {tempo_total:.4f}s")
        print(f"  Requisições/segundo: {num_requisicoes/tempo_total:.2f}")
        
        # API simples deve ser muito rápida (< 0.5s em média)
        self.assertLess(tempo_medio, 0.5, "Check login muito lento")
    
    def test_03_desempenho_multiplas_paginas(self):
        """Teste 3: Desempenho ao carregar várias páginas em sequência"""
        paginas = [
            ('/', 'Página Inicial'),
            ('/pages/login.html', 'Login'),
            ('/pages/cadastro.html', 'Cadastro'),
            ('/pages/cadastro-tutor-new.html', 'Cadastro Tutor'),
            ('/check_login', 'Check Login')
        ]
        
        print(f"\n  Testando carregamento de {len(paginas)} páginas...")
        
        resultados = []
        inicio_total = time.time()
        
        for url, nome in paginas:
            inicio = time.time()
            response = self.client.get(url)
            fim = time.time()
            
            tempo = fim - inicio
            resultados.append({
                'nome': nome,
                'tempo': tempo,
                'status': response.status_code
            })
            
            print(f"  - {nome}: {tempo:.4f}s (Status: {response.status_code})")
        
        fim_total = time.time()
        tempo_total = fim_total - inicio_total
        tempo_medio = tempo_total / len(paginas)
        
        print(f"  Tempo total: {tempo_total:.4f}s")
        print(f"  Tempo médio: {tempo_medio:.4f}s")
        
        # Todas as páginas juntas devem carregar em menos de 10 segundos
        self.assertLess(tempo_total, 10.0, "Carregamento de páginas muito lento")
    
    def test_04_desempenho_requisicoes_sequenciais(self):
        """Teste 4: Desempenho em requisições sequenciais intensivas"""
        num_requisicoes = 30
        
        print(f"\n  Executando {num_requisicoes} requisições sequenciais...")
        
        inicio = time.time()
        sucessos = 0
        
        for i in range(num_requisicoes):
            response = self.client.get('/')
            if response.status_code == 200:
                sucessos += 1
        
        fim = time.time()
        tempo_total = fim - inicio
        tempo_medio = tempo_total / num_requisicoes
        taxa_sucesso = (sucessos / num_requisicoes) * 100
        
        print(f"  Requisições bem-sucedidas: {sucessos}/{num_requisicoes} ({taxa_sucesso:.1f}%)")
        print(f"  Tempo total: {tempo_total:.4f}s")
        print(f"  Tempo médio por requisição: {tempo_medio:.4f}s")
        print(f"  Throughput: {num_requisicoes/tempo_total:.2f} req/s")
        
        # Todas devem ser bem-sucedidas
        self.assertEqual(sucessos, num_requisicoes)
        # Deve processar em menos de 30 segundos
        self.assertLess(tempo_total, 30.0, "Processamento muito lento")
    
    def test_05_desempenho_com_sessao(self):
        """Teste 5: Comparação de desempenho com e sem sessão"""
        num_requisicoes = 20
        
        print(f"\n  Comparando desempenho com e sem sessão...")
        
        # Teste SEM sessão
        tempos_sem_sessao = []
        for i in range(num_requisicoes):
            inicio = time.time()
            response = self.client.get('/check_login')
            fim = time.time()
            tempos_sem_sessao.append(fim - inicio)
            self.assertEqual(response.status_code, 200)
        
        tempo_medio_sem = sum(tempos_sem_sessao) / len(tempos_sem_sessao)
        
        # Teste COM sessão
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['user_name'] = 'Teste Desempenho'
                sess['user_type'] = 'tutor'
            
            tempos_com_sessao = []
            for i in range(num_requisicoes):
                inicio = time.time()
                response = client.get('/check_login')
                fim = time.time()
                tempos_com_sessao.append(fim - inicio)
                self.assertEqual(response.status_code, 200)
        
        tempo_medio_com = sum(tempos_com_sessao) / len(tempos_com_sessao)
        diferenca = abs(tempo_medio_com - tempo_medio_sem)
        percentual = (diferenca / tempo_medio_sem) * 100 if tempo_medio_sem > 0 else 0
        
        print(f"  Sem sessão - Tempo médio: {tempo_medio_sem:.4f}s")
        print(f"  Com sessão - Tempo médio: {tempo_medio_com:.4f}s")
        print(f"  Diferença: {diferenca:.4f}s ({percentual:.1f}%)")
        
        # Ambos devem ser rápidos
        self.assertLess(tempo_medio_sem, 1.0, "Sem sessão está lento")
        self.assertLess(tempo_medio_com, 1.0, "Com sessão está lento")

if __name__ == '__main__':
    unittest.main(verbosity=2)