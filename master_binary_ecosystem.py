"""
Master Binary Ecosystem — Orquestrador Mestre Unificado

Este módulo integra e executa todo o ecossistema construído:
1. Aplicação Web Interativa (Custom Binary Studio no localhost:8080).
2. Motor Algorítmico de Portas Lógicas e Somador Ripple-Carry.
3. Fronteiras Não-Binárias (Bio-computação DNA, Qubit Quântico e Transição de Fase).
4. Motor de Engenharia Reversa, Entropia e Descompilação.
"""

import sys
import io
import time
import urllib.request

# Forçar stdout UTF-8 no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Importar os módulos do ecossistema
import custom_binary_engine
import non_binary_frontier_engine
import reverse_engineer_engine


def check_web_app_status(url: str = "http://localhost:8080") -> bool:
    """Verifica se o servidor web local da aplicação está rodando."""
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except Exception:
        return False


def run_master_ecosystem():
    print("=" * 80)
    print("      ECOSSISTEMA MESTRE DE SISTEMAS BINÁRIOS E ALGORÍTMICOS UNIFICADOS")
    print("=" * 80)

    # Status da Aplicação Web
    web_status = check_web_app_status()
    status_str = "🟢 ATIVO (http://localhost:8080)" if web_status else "🔴 OFFLINE"
    print(f"\n[0] PAINEL DE STATUS DA APLICAÇÃO WEB:")
    print(f"  Servidor Local: {status_str}")
    print(f"  Diretório do Projeto: C:\\Users\\alessandro.meneses.Automotion\\.gemini\\antigravity-ide\\scratch\\custom-binary-studio\\")

    # Módulo 1: Motor Algorítmico Cru
    print("\n" + "─" * 80)
    print("MÓDULO 1: MOTOR ALGORÍTMICO DE CIRCUITOS E ARITMÉTICA")
    print("─" * 80)
    custom_binary_engine.run_algorithmic_demo()

    # Módulo 2: Computação Além do Binário Tradicional (DNA, Quântico e Matéria)
    print("\n" + "─" * 80)
    print("MÓDULO 2: FRONTEIRAS NÃO-BINÁRIAS (DNA, QUBITS QUÂNTICOS & MUDANÇA DE FASE)")
    print("─" * 80)
    non_binary_frontier_engine.run_frontier_demo()

    # Módulo 3: Engenharia Reversa e Descompilação
    print("\n" + "─" * 80)
    print("MÓDULO 3: ENGENHARIA REVERSA, ENTROPIA E DESCOMPILAÇÃO DE BLOBS")
    print("─" * 80)
    reverse_engineer_engine.run_reverse_engineering_demo()

    print("\n" + "=" * 80)
    print("    ECOSSISTEMA INTEGRADO RECRIADO E EXECUTADO COM 100% DE SUCESSO!")
    print("=" * 80)


if __name__ == "__main__":
    run_master_ecosystem()
