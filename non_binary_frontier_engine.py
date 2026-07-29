"""
Non-Binary Frontier Engine — Computação Além da Caixinha Tradicional

Este módulo explora 3 fronteiras da física e biologia computacional:
1. Bio-Computação com DNA (Mapeamento de 2 bits por nucleotídeo A, T, C, G).
2. Computação Quântica (Qubit com superposição de estados e Porta Hadamard).
3. Memória Física de Mudança de Fase (PCM - Transições amorfa/cristalina).
"""

import sys
import io
import math
import random

# Forçar stdout UTF-8 no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# ==============================================================================
# 1. BIO-COMPUTAÇÃO GENÉTICA (SINTETIZADOR DE DNA BINÁRIO)
# ==============================================================================

class DNABioBinaryEngine:
    """
    O DNA usa 4 nucleotídeos (A, T, C, G). 
    Como 4 = 2^2, cada nucleotídeo armazena exatamente 2 BITS de informação:
      00 -> A (Adenina)   [2 ligações H]
      01 -> T (Timina)    [2 ligações H]
      10 -> C (Citosina)  [3 ligações H]
      11 -> G (Guanina)   [3 ligações H]
    """

    NUCLEOTIDE_MAP = {
        '00': 'A',
        '01': 'T',
        '10': 'C',
        '11': 'G'
    }

    REVERSE_NUCLEOTIDE_MAP = {v: k for k, v in NUCLEOTIDE_MAP.items()}

    @classmethod
    def encode_bytes_to_dna(cls, data_bytes: bytes) -> tuple[str, int]:
        """Converte bytes brutos em uma fita sintética de DNA."""
        bit_stream = ''.join(f"{b:08b}" for b in data_bytes)
        
        dna_strand = []
        total_hydrogen_bonds = 0

        for i in range(0, len(bit_stream), 2):
            pair = bit_stream[i:i+2]
            nuc = cls.NUCLEOTIDE_MAP[pair]
            dna_strand.append(nuc)

            # Contagem de ligações de hidrogênio (A-T = 2, C-G = 3)
            total_hydrogen_bonds += 2 if nuc in ('A', 'T') else 3

        return ''.join(dna_strand), total_hydrogen_bonds

    @classmethod
    def decode_dna_to_bytes(cls, dna_strand: str) -> bytes:
        """Sintetiza de volta os bytes originais a partir da fita de DNA."""
        bit_stream = ''.join(cls.REVERSE_NUCLEOTIDE_MAP[nuc] for nuc in dna_strand)
        
        byte_list = []
        for i in range(0, len(bit_stream), 8):
            byte_val = int(bit_stream[i:i+8], 2)
            byte_list.append(byte_val)

        return bytes(byte_list)


# ==============================================================================
# 2. COMPUTADOR QUÂNTICO (SIMULADOR DE QUBIT E SUPERPOSIÇÃO DE HADAMARD)
# ==============================================================================

class Qubit:
    """
    Um Qubit representa o estado quântico: |Ψ⟩ = α|0⟩ + β|1⟩
    onde |α|^2 + |β|^2 = 1 (Normalização de probabilidade).
    """

    def __init__(self, alpha: float = 1.0, beta: float = 0.0):
        # Normalizar para garantir |α|^2 + |β|^2 = 1
        norm = math.sqrt(alpha**2 + beta**2)
        self.alpha = alpha / norm
        self.beta = beta / norm

    def apply_hadamard(self):
        """
        Aplica a Porta Quântica Hadamard (H):
        Coloca o Qubit em SUPERPOSIÇÃO PERFEITA (50% de ser 0, 50% de ser 1).
        Matriz H = 1/√2 * [[1, 1], [1, -1]]
        """
        inv_sqrt2 = 1.0 / math.sqrt(2)
        new_alpha = inv_sqrt2 * (self.alpha + self.beta)
        new_beta = inv_sqrt2 * (self.alpha - self.beta)

        self.alpha = new_alpha
        self.beta = new_beta

    def get_probabilities(self) -> tuple[float, float]:
        """Retorna as probabilidades de medição de |0⟩ e |1⟩."""
        prob_0 = self.alpha**2
        prob_1 = self.beta**2
        return prob_0, prob_1

    def measure(self) -> int:
        """
        Mede o Qubit: Colapso da Função de Onda!
        O estado quântico em superposição escolhe ser 0 ou 1 com base em suas probabilidades.
        """
        prob_0 = self.alpha**2
        rolled = random.random()

        if rolled < prob_0:
            self.alpha = 1.0
            self.beta = 0.0
            return 0
        else:
            self.alpha = 0.0
            self.beta = 1.0
            return 1


# ==============================================================================
# 3. MEMÓRIA FÍSICA DE MUDANÇA DE FASE (PCM - PHASE CHANGE MEMORY)
# ==============================================================================

class PhaseChangeCell:
    """
    Simula uma célula física de mudança de fase atômica.
    - Estado Amorfo (Desordenado): Alta Resistência (R ~ 1MΩ) -> Representa Bit 0
    - Estado Cristalino (Ordenado): Baixa Resistência (R ~ 1kΩ) -> Representa Bit 1
    """

    def __init__(self):
        self.temperature_celsius = 25.0
        self.is_crystalline = False  # Amorfo por padrão (Bit 0)
        self.resistance_ohms = 1000000.0

    def apply_thermal_pulse(self, temp_celsius: float, duration_ns: float):
        """
        Aplica pulso térmico com laser/corrente elétrica:
        - Reset (Melt & Quench: > 600°C curto): Transforma em Amorfo (Bit 0)
        - Set (Crystallize: ~ 400°C longo): Transforma em Cristalino (Bit 1)
        """
        self.temperature_celsius = temp_celsius

        if temp_celsius >= 600.0 and duration_ns < 10.0:
            # Resfriamento rápido -> Estrutura atômica desordenada (Amorfa / Bit 0)
            self.is_crystalline = False
            self.resistance_ohms = 1000000.0  # 1 Megaohm
        elif 350.0 <= temp_celsius <= 500.0 and duration_ns >= 50.0:
            # Aquecimento controlado -> Átomos se alinham em rede cristalina (Bit 1)
            self.is_crystalline = True
            self.resistance_ohms = 1000.0     # 1 Kiloohm

    def read_bit(self) -> int:
        """Lê o bit medindo a resistência elétrica da matéria física."""
        return 1 if self.is_crystalline else 0


# ==============================================================================
# DEMONSTRAÇÃO COMPLETA DAS TRÊS FRONTEIRAS
# ==============================================================================

def run_frontier_demo():
    print("=" * 75)
    print("    MOTOR FORA DA CAIXINHA: COMPUTAÇÃO GENÉTICA, QUÂNTICA E FÍSICA")
    print("=" * 75)

    # --------------------------------------------------------------------------
    # FRONTEIRA 1: DNA BIO-COMPUTAÇÃO
    # --------------------------------------------------------------------------
    print("\n🧬 [1] FRONTEIRA BIOLÓGICA: SÍNTESE DE DADOS EM FITA DE DNA")
    mensagem_original = "LIFE"
    data_bytes = mensagem_original.encode('utf-8')
    
    dna_strand, h_bonds = DNABioBinaryEngine.encode_bytes_to_dna(data_bytes)
    reconstructed_bytes = DNABioBinaryEngine.decode_dna_to_bytes(dna_strand)

    print(f"  Mensagem Original:     '{mensagem_original}' ({len(data_bytes) * 8} bits)")
    print(f"  Fita de DNA Sintetizada: {dna_strand}")
    print(f"  Tamanho da Fita:       {len(dna_strand)} Nucleotídeos")
    print(f"  Ligações de Hidrogênio: {h_bonds} Pontes H na molécula")
    print(f"  Decodificação do DNA:   '{reconstructed_bytes.decode('utf-8')}' (100% Fiel)")

    # --------------------------------------------------------------------------
    # FRONTEIRA 2: COMPUTADOR QUÂNTICO (SUPERPOSIÇÃO E COLAPSO)
    # --------------------------------------------------------------------------
    print("\n⚛️ [2] FRONTEIRA QUÂNTICA: SUPERPOSIÇÃO E COLAPSO DE ONDA (QUBIT)")
    qubit = Qubit(alpha=1.0, beta=0.0)  # Estado inicial rígido |0⟩

    p0, p1 = qubit.get_probabilities()
    print(f"  Qubit Inicial (|0⟩ Rígido): P(0) = {p0*100:.1f}%, P(1) = {p1*100:.1f}%")

    # Aplicação da Porta Hadamard (Entra em Superposição Quântica)
    qubit.apply_hadamard()
    p0_sup, p1_sup = qubit.get_probabilities()
    print(f"  Após Porta Hadamard (Superposição): P(0) = {p0_sup*100:.1f}%, P(1) = {p1_sup*100:.1f}%")
    print("  -> O Qubit existe como 0 E 1 simultaneamente!")

    # Execução de 10 Medições Quânticas (Colapso de Onda)
    print("\n  Simulando 10 Medições Independentes no Laboratório:")
    resultados = []
    for i in range(10):
        # Novo qubit em superposição para cada teste
        test_q = Qubit(1.0, 0.0)
        test_q.apply_hadamard()
        medido = test_q.measure()
        resultados.append(medido)
    
    count_0 = resultados.count(0)
    count_1 = resultados.count(1)
    print(f"  Resultados das Medições: {resultados}")
    print(f"  Estatística do Colapso:  Zeros = {count_0} ({count_0*10}%) | Uns = {count_1} ({count_1*10}%)")

    # --------------------------------------------------------------------------
    # FRONTEIRA 3: MEMÓRIA FÍSICA DE MUDANÇA DE FASE (PCM)
    # --------------------------------------------------------------------------
    print("\n🔥 [3] FRONTEIRA FÍSICA: MATÉRIA E TRANSIÇÃO DE FASE ATÔMICA")
    cell = PhaseChangeCell()
    print(f"  Estado Inicial da Célula: Cristalina = {cell.is_crystalline} | Resistência = {cell.resistance_ohms:,.0f} Ω | Bit = {cell.read_bit()}")

    print("\n  Aplicando Pulso Térmico de Escrita (400°C por 80ns)...")
    cell.apply_thermal_pulse(temp_celsius=400.0, duration_ns=80.0)
    print(f"  Estado Pós-Aquecimento:   Cristalina = {cell.is_crystalline} | Resistência = {cell.resistance_ohms:,.0f} Ω | Bit = {cell.read_bit()}")

    print("\n  Aplicando Pulso Térmico de Reset (650°C por 5ns)...")
    cell.apply_thermal_pulse(temp_celsius=650.0, duration_ns=5.0)
    print(f"  Estado Pós-Reset Laser:   Cristalina = {cell.is_crystalline} | Resistência = {cell.resistance_ohms:,.0f} Ω | Bit = {cell.read_bit()}")

    print("\n" + "=" * 75)
    print("    Demonstração das 3 fronteiras concluída com sucesso!")
    print("=" * 75)


if __name__ == "__main__":
    run_frontier_demo()
