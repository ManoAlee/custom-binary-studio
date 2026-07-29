"""
Reverse Engineer Engine — Ferramenta de Engenharia Reversa e Descompilação Binária

Este módulo realiza engenharia reversa em sequências binárias desconhecidas ou ofuscadas:
1. Análise de Entropia de Shannon (Mede a aleatoriedade/compactação da informação).
2. Detecção Heurística de Tipo (Texto UTF-8, Pesos de IA em Float32, Bitmap 8x8 ou Fita de DNA).
3. Descompilação Automática por Análise de Frequência de Símbolos Desconhecidos.
"""

import sys
import io
import math
import struct

# Forçar stdout UTF-8 no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


class BinaryReverser:
    @staticmethod
    def calculate_shannon_entropy(bit_string: str) -> float:
        """
        Calcula a Entropia de Shannon (H) da sequência binária:
        H = - ∑ p_i * log2(p_i)
        Varia de 0.0 (totalmente previsível/repetitivo) até 1.0 (máximo caos/criptografado).
        """
        cleaned = [b for b in bit_string if b in ('0', '1')]
        if not cleaned:
            return 0.0

        n = len(cleaned)
        count_0 = cleaned.count('0')
        count_1 = cleaned.count('1')

        p0 = count_0 / n
        p1 = count_1 / n

        entropy = 0.0
        if p0 > 0:
            entropy -= p0 * math.log2(p0)
        if p1 > 0:
            entropy -= p1 * math.log2(p1)

        return entropy

    @classmethod
    def reverse_engineer_blob(cls, raw_bits: str) -> dict:
        """
        Analisa um blob binário e executa a engenharia reversa para identificar o payload.
        """
        bits = raw_bits.replace(" ", "").replace("\n", "").replace("\r", "")
        n_bits = len(bits)
        entropy = cls.calculate_shannon_entropy(bits)

        report = {
            "total_bits": n_bits,
            "total_bytes": n_bits // 8,
            "shannon_entropy": round(entropy, 4),
            "detected_type": "Desconhecido",
            "decompiled_content": None
        }

        # Case 1: Tentar descompilar como Texto ASCII / UTF-8
        if n_bits % 8 == 0 and n_bits >= 8:
            try:
                chars = []
                is_printable_text = True
                for i in range(0, n_bits, 8):
                    byte_str = bits[i:i+8]
                    code = int(byte_str, 2)
                    if 32 <= code <= 126 or code in (9, 10, 13):
                        chars.append(chr(code))
                    else:
                        is_printable_text = False
                        break

                if is_printable_text and len(chars) > 0:
                    report["detected_type"] = "Texto Imprimível (ASCII / UTF-8)"
                    report["decompiled_content"] = "".join(chars)
                    return report
            except Exception:
                pass

        # Case 2: Tentar descompilar como Pesos de IA (Float32 IEEE 754 - múltiplos de 32 bits)
        if n_bits % 32 == 0 and n_bits >= 32:
            try:
                floats = []
                all_valid_floats = True
                for i in range(0, n_bits, 32):
                    chunk = bits[i:i+32]
                    byte_vals = [int(chunk[j:j+8], 2) for j in range(0, 32, 8)]
                    flt = struct.unpack('>f', bytes(byte_vals))[0]
                    if math.isnan(flt) or math.isinf(flt) or abs(flt) > 1e6:
                        all_valid_floats = False
                        break
                    floats.append(round(flt, 6))

                if all_valid_floats:
                    report["detected_type"] = "Pesos/Vetores de IA (Float32 IEEE 754)"
                    report["decompiled_content"] = floats
                    return report
            except Exception:
                pass

        # Case 3: Tentar descompilar como Imagem Bitmap 8x8 (64 bits)
        if n_bits == 64:
            ascii_grid = []
            for row in range(8):
                line = bits[row*8:(row+1)*8]
                ascii_row = "".join("██" if b == '1' else "  " for b in line)
                ascii_grid.append(ascii_row)
            report["detected_type"] = "Matriz de Imagem Bitmap 8x8 (64 Bits)"
            report["decompiled_content"] = "\n" + "\n".join(ascii_grid)
            return report

        return report

    @classmethod
    def decompile_custom_symbols_by_frequency(cls, custom_stream: str) -> tuple[str, str, str]:
        """
        Engenharia Reversa por Análise de Frequência:
        Descobre quais símbolos correspondem a 0 e 1 em uma stream de símbolos totalmente desconhecida.
        """
        # Extrai caracteres/símbolos únicos
        unique_syms = list(set(custom_stream.replace(" ", "")))
        if len(unique_syms) < 2:
            return custom_stream, "?", "?"

        sym_a, sym_b = unique_syms[0], unique_syms[1]
        freq_a = custom_stream.count(sym_a)
        freq_b = custom_stream.count(sym_b)

        # Na maioria das codificações convencionais de texto/instrução, o bit 0 costuma ser mais frequente
        if freq_a >= freq_b:
            sym_zero, sym_one = sym_a, sym_b
        else:
            sym_zero, sym_one = sym_b, sym_a

        # Subsituição
        decompiled_bin = custom_stream.replace(sym_one, "1").replace(sym_zero, "0").replace(" ", "")
        return decompiled_bin, sym_zero, sym_one


# ==============================================================================
# DEMONSTRAÇÃO COMPLETA DE ENGENHARIA REVERSA
# ==============================================================================

def run_reverse_engineering_demo():
    print("=" * 75)
    print("      LABORATÓRIO DE ENGENHARIA REVERSA E DESCOMPILAÇÃO BINÁRIA")
    print("=" * 75)

    # --------------------------------------------------------------------------
    # AMPOSTRA 1: ENGENHARIA REVERSA EM UM BLOB BINÁRIO DE IMAGEM 8x8
    # --------------------------------------------------------------------------
    print("\n🔍 [AMOSTRA 1] ENGENHARIA REVERSA DE BLOB DE DADOS DESCONHECIDO #1:")
    blob_misterioso_1 = (
        "01100110"
        "11111111"
        "11111111"
        "01111110"
        "00111100"
        "00011000"
        "00000000"
        "00000000"
    )
    print(f"  Stream Bruto Recebido: {blob_misterioso_1[:32]}...")
    res1 = BinaryReverser.reverse_engineer_blob(blob_misterioso_1)
    
    print(f"  -> Tamanho:             {res1['total_bits']} bits ({res1['total_bytes']} bytes)")
    print(f"  -> Entropia de Shannon: {res1['shannon_entropy']}")
    print(f"  -> Tipo Detectado:      {res1['detected_type']}")
    print(f"  -> Imagem Reconstruída: {res1['decompiled_content']}")

    # --------------------------------------------------------------------------
    # AMOSTRA 2: ENGENHARIA REVERSA EM UM BLOB DE PESOS DE IA (FLOAT32)
    # --------------------------------------------------------------------------
    print("\n🔍 [AMOSTRA 2] ENGENHARIA REVERSA DE BLOB DE DADOS DESCONHECIDO #2:")
    # Floats: 0.5 (0x3f000000) e -0.75 (0xbf400000)
    blob_misterioso_2 = "0011111100000000000000000000000010111111010000000000000000000000"
    print(f"  Stream Bruto Recebido: {blob_misterioso_2}")
    res2 = BinaryReverser.reverse_engineer_blob(blob_misterioso_2)

    print(f"  -> Tamanho:             {res2['total_bits']} bits ({res2['total_bytes']} bytes)")
    print(f"  -> Entropia de Shannon: {res2['shannon_entropy']}")
    print(f"  -> Tipo Detectado:      {res2['detected_type']}")
    print(f"  -> Valores Descompilados: {res2['decompiled_content']}")

    # --------------------------------------------------------------------------
    # AMOSTRA 3: DESCOMPILAÇÃO DE SÍMBOLOS CRIPTOGRÁFICOS / CUSTOMIZADOS
    # --------------------------------------------------------------------------
    print("\n🔍 [AMOSTRA 3] ENGENHARIA REVERSA POR ANÁLISE DE FREQUÊNCIA DE SÍMBOLOS:")
    stream_cripto = "🔴🔵🔴🔴🔵🔴🔴🔵 🔴🔵🔴🔴🔴🔴🔴🔵"  # Representação de 'IA'
    print(f"  Sinal Ofuscado Recebido: {stream_cripto}")

    bin_reconstruido, sym_0, sym_1 = BinaryReverser.decompile_custom_symbols_by_frequency(stream_cripto)
    print(f"  -> Mapeamento Identificado: Zero = '{sym_0}' | Um = '{sym_1}'")
    print(f"  -> Binário Reconstruído:    {bin_reconstruido}")
    
    # Passar pelo descompilador de payload
    res3 = BinaryReverser.reverse_engineer_blob(bin_reconstruido)
    print(f"  -> Payload Descompilado:   '{res3['decompiled_content']}'")

    print("\n" + "=" * 75)
    print("    Análise de Engenharia Reversa concluída com sucesso!")
    print("=" * 75)


if __name__ == "__main__":
    run_reverse_engineering_demo()
