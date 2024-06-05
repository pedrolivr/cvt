import os
import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

# Expressão regular
padrao = r'[A-Z]{3}-\d{3}[A-Z]{2}-\d{3}-\d{3}-[A-Z]{3}-[A-Z]{3}-[A-Z]{2}-[A-Z]\d-\d{3}'
regex = re.compile(padrao)

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

    arquivo_saida = diretorio_saida / "matches.txt"
    matches = []

    for arquivo in diretorio_entrada.glob("*.txt"):
        with open(arquivo, 'r', encoding="utf-8") as f:
            nome_arquivo = arquivo.name[:35]
            for linha in f:
                encontrados = regex.findall(linha)
                for match in encontrados:
                    matches.append(f"{nome_arquivo}: {match}")

    with open(arquivo_saida, 'w', encoding="utf-8") as f:
        for match in matches:
            f.write(match + '\n')

    print(f"Matches salvos em {arquivo_saida}")

# Chamar a função para selecionar o diretório de entrada
selecionar_pasta()
