import os
import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

# Expressões regulares
padrao1 = r'[A-Z]{3}-\d{3}[A-Z]{2}-\d{3}-\d{3}-[A-Z]{3}-[A-Z]{3}-[A-Z]{2}-[A-Z]\d-\d{3}'
padrao2 = r'\d{3}\+\d{3}'
regex1 = re.compile(padrao1)
regex2 = re.compile(padrao2)

def selecionar_pasta():
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal

    diretorio_entrada = filedialog.askdirectory(title="Selecione o diretório de entrada")
    if not diretorio_entrada:  # Usuário clicou em "Cancelar"
        print("Operação cancelada.")
        return

    diretorio_entrada = Path(diretorio_entrada)
    diretorio_saida = diretorio_entrada / 'output'
    diretorio_saida.mkdir(parents=True, exist_ok=True)  # Criar diretório de saída se não existir

    arquivo_saida_combinado = diretorio_saida / "matches_combinado.txt"
    arquivo_saida_padrao1 = diretorio_saida / "matches_padrao1.txt"

    matches_combinado = []
    matches_padrao1 = []

    for arquivo in diretorio_entrada.glob("*.txt"):
        with open(arquivo, 'r', encoding="utf-8") as f:
            matches1 = []
            matches2 = []
            linha_num = 0
            for linha in f:
                linha_num += 1
                encontrados1 = regex1.findall(linha)
                encontrados2 = regex2.findall(linha)
                for match in encontrados1:
                    matches1.append((linha_num, match))
                for match in encontrados2:
                    matches2.append((linha_num, match))
            
            # Agrupar todas as correspondências da primeira expressão em uma string separada por ';'
            matches1_str = ';'.join([f"{linha_num}:{match}" for linha_num, match in matches1]) if matches1 else ''
            # Agrupar todas as correspondências da segunda expressão em uma string separada por ';'
            matches2_str = ';'.join([f"{linha_num}:{match}" for linha_num, match in matches2]) if matches2 else ''
            
            # Adicionar todas as correspondências da primeira expressão ao arquivo correspondente
            matches_padrao1.extend(matches1)
            
            # Adicionar a linha combinada de matches das duas expressões
            combined_match = f"{matches1_str};{matches2_str}"
            if combined_match.strip(';'):  # Adiciona somente se houver algum match
                matches_combinado.append(combined_match)

    # Escrever os resultados combinados no arquivo de saída combinado
    with open(arquivo_saida_combinado, 'w', encoding="utf-8") as f:
        for match in matches_combinado:
            f.write(match + '\n')

    # Escrever os resultados da primeira expressão no arquivo de saída correspondente
    with open(arquivo_saida_padrao1, 'w', encoding="utf-8") as f:
        for linha_num, match in matches_padrao1:
            f.write(f"{linha_num}:{match}\n")

    print(f"Matches combinados salvos em {arquivo_saida_combinado}")
    print(f"Matches da primeira expressão salvos em {arquivo_saida_padrao1}")

# Chamar a função para selecionar o diretório de entrada
selecionar_pasta()
