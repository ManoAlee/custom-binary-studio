"""
Custom Binary Engine — Motor Algorítmico Cru de Lógica Binária

Este módulo implementa a lógica computacional binária a partir de princípios fundamentais:
1. Portas Lógicas construídas a partir de uma única primitiva (NAND Universal).
2. Circuito Somador Ripple-Carry (Half-Adder e Full-Adder) bit a bit.
3. Classe de Sistema Binário Personalizado para codificação, decodificação e aritmética.
"""

import sys
import io

# Configurar stdout para UTF-8 no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ==============================================================================
# 1. ÁLGEBRA BOOLEANA: CONSTRUÇÃO DE PORTAS A PARTIR DA PRIMITIVA UNIVERSAL (NAND)
# ==============================================================================

def gate_nand(a: int, b: int) -> int:
    """Primitiva Fundamental: Porta NAND (0 se ambos forem 1, senão 1)."""
    return 0 if (a == 1 and b == 1) else 1

def gate_not(a: int) -> int:
    """Porta NOT construída a partir de NAND(a, a)."""
    return gate_nand(a, a)

def gate_and(a: int, b: int) -> int:
    """Porta AND construída a partir de NOT(NAND(a, b))."""
    return gate_not(gate_nand(a, b))

def gate_or(a: int, b: int) -> int:
    """Porta OR construída pela lei de De Morgan: NAND(NOT(a), NOT(b))."""
    return gate_nand(gate_not(a), gate_not(b))

def gate_xor(a: int, b: int) -> int:
    """Porta XOR construída com combinações de AND, OR e NAND."""
    nand_ab = gate_nand(a, b)
    or_ab = gate_or(a, b)
    return gate_and(nand_ab, or_ab)


# ==============================================================================
# 2. CIRCUITO ARITMÉTICO: HALF-ADDER E FULL-ADDER (SOMADOR RIPPLE-CARRY)
# ==============================================================================

def half_adder(a: int, b: int) -> tuple[int, int]:
    """
    Meio-Somador (Half Adder):
    Soma = XOR(a, b)
    Vai-Um (Carry) = AND(a, b)
    """
    soma = gate_xor(a, b)
    carry = gate_and(a, b)
    return soma, carry

def full_adder(a: int, b: int, carry_in: int) -> tuple[int, int]:
    """
    Somador Completo (Full Adder):
    Soma dois bits mais um bit de vai-um (carry_in).
    """
    sum1, carry1 = half_adder(a, b)
    final_sum, carry2 = half_adder(sum1, carry_in)
    final_carry = gate_or(carry1, carry2)
    return final_sum, final_carry

def ripple_carry_adder(bits_a: list[int], bits_b: list[int]) -> tuple[list[int], int]:
    """
    Algoritmo Somador Ripple-Carry:
    Soma duas sequências de bits de tamanho arbitrário (da direita para a esquerda).
    """
    max_len = max(len(bits_a), len(bits_b))
    # Pad com 0s à esquerda
    a = [0] * (max_len - len(bits_a)) + bits_a
    b = [0] * (max_len - len(bits_b)) + bits_b

    result_bits = []
    carry = 0

    for i in range(max_len - 1, -1, -1):
        bit_sum, carry = full_adder(a[i], b[i], carry)
        result_bits.insert(0, bit_sum)

    return result_bits, carry


# ==============================================================================
# 3. CLASSE DE SISTEMA BINÁRIO PERSONALIZADO (CUSTOM BINARY SYSTEM)
# ==============================================================================

class CustomBinarySystem:
    def __init__(self, sym_zero: str = "0", sym_one: str = "1", bit_width: int = 8):
        self.sym_zero = sym_zero
        self.sym_one = sym_one
        self.bit_width = bit_width

    def int_to_bits(self, number: int) -> list[int]:
        """Converte um número inteiro em lista de bits purosa (ex: 42 -> [0,0,1,0,1,0,1,0])."""
        if number == 0:
            return [0] * self.bit_width
        
        bits = []
        val = number
        while val > 0:
            bits.insert(0, val % 2)
            val = val // 2

        # Pad até o bit_width desejado
        if len(bits) < self.bit_width:
            bits = [0] * (self.bit_width - len(bits)) + bits
        return bits

    def bits_to_int(self, bits: list[int]) -> int:
        """Converte uma lista de bits purosa em inteiro decimal usando algoritmo posicional (Base 2)."""
        val = 0
        power = 1
        for bit in reversed(bits):
            if bit == 1:
                val += power
            power *= 2
        return val

    def bits_to_custom_symbols(self, bits: list[int], separator: str = " ") -> str:
        """Mapeia os bits numéricos 0 e 1 para os símbolos customizados."""
        return separator.join([self.sym_one if b == 1 else self.sym_zero for b in bits])

    def custom_symbols_to_bits(self, custom_str: str) -> list[int]:
        """Converte uma string de símbolos customizados de volta em bits puramente numéricos."""
        bits = []
        i = 0
        n = len(custom_str)
        len_zero = len(self.sym_zero)
        len_one = len(self.sym_one)

        while i < n:
            if custom_str[i:i+len_one] == self.sym_one:
                bits.append(1)
                i += len_one
            elif custom_str[i:i+len_zero] == self.sym_zero:
                bits.append(0)
                i += len_zero
            else:
                i += 1  # Ignora separadores ou espaços
        return bits

    def add_custom(self, custom_a: str, custom_b: str) -> tuple[str, str]:
        """Soma duas strings de binário customizado usando o algoritmo de somador puramente lógico."""
        bits_a = self.custom_symbols_to_bits(custom_a)
        bits_b = self.custom_symbols_to_bits(custom_b)

        result_bits, overflow_carry = ripple_carry_adder(bits_a, bits_b)
        
        result_custom = self.bits_to_custom_symbols(result_bits)
        carry_custom = self.sym_one if overflow_carry == 1 else self.sym_zero
        
        return result_custom, carry_custom


# ==============================================================================
# 4. EXECUÇÃO DE DEMONSTRAÇÃO E TESTES ALGORÍTMICOS CRUS
# ==============================================================================

# ==============================================================================
# 5. DECODIFICAÇÃO E EXECUÇÃO DE PESOS DE IA EM BINÁRIO
# ==============================================================================

import struct

def float_to_ieee754_bits(val: float) -> str:
    """Converte um número float (32 bits FP32) na sequência binária bruta do padrão IEEE 754."""
    packed = struct.pack('>f', val)
    return ''.join(f"{b:08b}" for b in packed)

def ieee754_bits_to_float(bit_str: str) -> float:
    """Converte uma string binária de 32 bits de volta para um float."""
    byte_vals = [int(bit_str[i:i+8], 2) for i in range(0, 32, 8)]
    packed = bytes(byte_vals)
    return struct.unpack('>f', packed)[0]

def decode_and_use_ai():
    print("\n" + "=" * 70)
    print("      DECODIFICADOR E EXECUTOR DE INTELIGÊNCIA ARTIFICIAL EM BINÁRIO")
    print("=" * 70)

    # 1. Decodificação da sigla 'IA'
    texto = "IA"
    system_custom = CustomBinarySystem(sym_zero="🔴", sym_one="🔵")
    
    print("\n[1] DECODIFICAÇÃO DE TEXTO DA SIGLA 'IA':")
    for char in texto:
        bits = system_custom.int_to_bits(ord(char))
        custom_syms = system_custom.bits_to_custom_symbols(bits)
        std_bin = ''.join(str(b) for b in bits)
        print(f"  Caractere '{char}' (ASCII {ord(char):2d}) -> Binário: {std_bin} | Customizado: {custom_syms}")

    # 2. Decodificação de Pesos de Rede Neural (IA)
    pesos_ia = [0.5, -0.75, 1.25, 0.0]
    print("\n[2] DECODIFICAÇÃO DE PESOS DE UMA CAMADA DE IA (FP32 IEEE 754):")
    for idx, peso in enumerate(pesos_ia):
        bits_32 = float_to_ieee754_bits(peso)
        sinal = bits_32[0]
        expoente = bits_32[1:9]
        mantissa = bits_32[9:]
        
        # Converter para símbolos customizados
        custom_bits = ''.join(["🔵" if b == '1' else "🔴" for b in bits_32])

        print(f"  Neurônio {idx+1} | Peso: {peso:5.2f}")
        print(f"    -> Sinal: {sinal} | Expoente: {expoente} | Mantissa: {mantissa[:12]}...")
        print(f"    -> Visual Customizado: {custom_bits[:16]}...")

    # 3. Execução de Cálculo de Neurônio (Soma Ponderada Simulação)
    print("\n[3] EXECUÇÃO DE PROCESSAMENTO BINÁRIO DE UM NEURÔNIO:")
    entrada_a = 5  # Ativação do neurônio anterior (5)
    entrada_b = 3  # Peso da sinapse (3)
    
    bits_ent_a = system_custom.int_to_bits(entrada_a)
    bits_ent_b = system_custom.int_to_bits(entrada_b)
    
    res_bits, carry = ripple_carry_adder(bits_ent_a, bits_ent_b)
    res_val = system_custom.bits_to_int(res_bits)

    print(f"  Ativação A ({entrada_a}) + Sinapse B ({bits_ent_b}) = Saída Neuronal: {res_val}")
    print(f"  Sinal Binário Resultante: {system_custom.bits_to_custom_symbols(res_bits)}")

    print("\n" + "=" * 70)


def run_algorithmic_demo():
    print("=" * 70)
    print("      CUSTOM BINARY ENGINE — DEMONSTRAÇÃO ALGORÍTMICA CRUA")
    print("=" * 70)

    # 1. Teste de Portas Lógicas Primárias (NAND Universal)
    print("\n[1] TESTE DE PORTAS LÓGICAS (Construídas a partir de NAND):")
    print(f"  gate_nand(1, 1) = {gate_nand(1, 1)}")
    print(f"  gate_not(1)     = {gate_not(1)}")
    print(f"  gate_and(1, 0)  = {gate_and(1, 0)}")
    print(f"  gate_or(1, 0)   = {gate_or(1, 0)}")
    print(f"  gate_xor(1, 1)  = {gate_xor(1, 1)} | gate_xor(1, 0) = {gate_xor(1, 0)}")

    # 2. Teste do Circuito Somador (Full Adder + Ripple-Carry)
    print("\n[2] TESTE DO CIRCUITO SOMADOR (Ripple-Carry Adder):")
    val_a = 42   # Binário: 00101010
    val_b = 27   # Binário: 00011011
    system = CustomBinarySystem(sym_zero="0", sym_one="1", bit_width=8)
    bits_a = system.int_to_bits(val_a)
    bits_b = system.int_to_bits(val_b)

    sum_bits, carry_out = ripple_carry_adder(bits_a, bits_b)
    sum_decimal = system.bits_to_int(sum_bits)

    print(f"  A (Decimal {val_a:3d}) = {bits_a}")
    print(f"  B (Decimal {val_b:3d}) = {bits_b}")
    print(f"  Soma Resultante    = {sum_bits} (Decimal {sum_decimal}) [Vai-Um: {carry_out}]")
    print(f"  Verificação: {val_a} + {val_b} = {val_a + val_b} -> Correcto? {sum_decimal == (val_a + val_b)}")

    # 3. Teste com Símbolos Binários Customizados (Ex: Emojis e Tensão)
    print("\n[3] TESTE COM SISTEMA DE SÍMBOLOS PERSONALIZADO (Ex: 🔴 / 🔵):")
    emoji_system = CustomBinarySystem(sym_zero="🔴", sym_one="🔵", bit_width=8)
    
    bin_emoji_a = emoji_system.bits_to_custom_symbols(bits_a)
    bin_emoji_b = emoji_system.bits_to_custom_symbols(bits_b)
    
    res_emoji, overflow_emoji = emoji_system.add_custom(bin_emoji_a, bin_emoji_b)

    print(f"  A em Símbolos: {bin_emoji_a}")
    print(f"  B em Símbolos: {bin_emoji_b}")
    print(f"  Soma em Símbolos: {res_emoji} (Overflow Carry: {overflow_emoji})")

    # Decodificar e Usar IA
    decode_and_use_ai()


if __name__ == "__main__":
    run_algorithmic_demo()

