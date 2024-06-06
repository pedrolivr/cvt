import os
from PIL import Image
import pytesseract
import tkinter as tk
from tkinter import filedialog

# Configurar o caminho para o executável Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Users/pe.oliveira/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'

# Configurar a variável de ambiente TESSDATA_PREFIX
tesseract_dir = r'C:/Users/pe.oliveira/AppData/Local/Programs/Tesseract-OCR/tessdata'
os.environ['TESSDATA_PREFIX'] = tesseract_dir

# Função para processar uma única imagem
def processar_imagem(imagem_caminho):
    try:
        # Abrir a imagem usando PIL
        imagem = Image.open(imagem_caminho)
        # Extrair texto da imagem usando Tesseract
        texto = pytesseract.image_to_string(imagem, lang='por')  # 'lang' define o idioma
        return texto
    except Exception as e:
        print(f"Erro ao processar a imagem {imagem_caminho}: {e}")
        return ""

# Função principal para processar todas as imagens na pasta
def processar_pasta_imagens(pasta):
    # Iterar sobre todos os arquivos na pasta
    for nome_arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, nome_arquivo)
        # Verificar se é um arquivo (e não uma subpasta)
        if os.path.isfile(caminho_arquivo):
            # Processar a imagem e obter o texto
            texto = processar_imagem(caminho_arquivo)
            # Definir o nome do arquivo de saída
            nome_saida = os.path.splitext(nome_arquivo)[0] + '.txt'
            caminho_saida = os.path.join(pasta, nome_saida)
            # Escrever o texto em um arquivo de texto
            with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
                arquivo_saida.write(texto)
            print(f"Texto extraído e salvo em {caminho_saida}")

def selecionar_pasta():
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal

    pasta = filedialog.askdirectory(title="Selecione a pasta que contém as imagens")
    if not pasta:  # Usuário clicou em "Cancelar"
        print("Operação cancelada.")
        return

    processar_pasta_imagens(pasta)

# Chamar a função para selecionar a pasta
selecionar_pasta()
