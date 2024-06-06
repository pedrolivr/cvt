import cv2
import pytesseract
import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd

# Configurar o caminho do executável do Tesseract, se necessário
pytesseract.pytesseract.tesseract_cmd = r'C:/Users/pe.oliveira/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'

# Função para ler texto de uma região específica da imagem
def read_text_from_region(image_path, region):
    """
    Lê texto de uma região específica de uma imagem.

    Args:
    image_path (str): Caminho para a imagem.
    region (tuple): Região da imagem no formato (x, y, largura, altura).

    Returns:
    str: Texto lido da região.
    """
    # Carregar a imagem
    image = cv2.imread(image_path)
    
    # Extrair a região de interesse (ROI)
    x, y, w, h = region
    roi = image[y:y+h, x:x+w]
    
    # Converter a ROI para escala de cinza
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Aplicar OCR na ROI usando o idioma português
    text = pytesseract.image_to_string(gray, lang='por')
    
    return text

# Função para selecionar o diretório
def select_directory():
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    folder_selected = filedialog.askdirectory()
    return folder_selected

# Selecionar o diretório contendo as imagens
directory = select_directory()

# Definir as regiões de interesse (ROIs)
regions = [
     # Exemplo de coordenadas (x, y, largura, altura)
    (3820, 2960, 900, 150),
    (3720, 3100, 300, 70),
    (4200, 3100, 350, 70),
    (3720, 3200, 900, 70),
    (3720, 3250, 300, 70),
    (4200, 3250, 300, 70),
    (4, 3260, 150, 50),
    (4330,2570,400,70)

]

# Lista para armazenar os dados para o Excel
excel_data = []

# Processar todas as imagens no diretório selecionado
for filename in os.listdir(directory):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(directory, filename)
        output_file = os.path.join(directory, f'resultados_{os.path.splitext(filename)[0]}.txt')
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(f'Resultados para {filename}:\n')
            # Armazenar apenas os primeiros 35 caracteres do nome do arquivo
            image_data = {"Imagem": filename[:35]}
            for i, region in enumerate(regions):
                text = read_text_from_region(image_path, region)
                file.write(f'Texto da região {i + 1}:\n')
                file.write(text)
                file.write('\n' + '-' * 30 + '\n')
                image_data[f'Região {i + 1}'] = text
            file.write('\n' + '=' * 30 + '\n')
            excel_data.append(image_data)

# Criar um DataFrame do pandas e salvar como arquivo Excel
df = pd.DataFrame(excel_data)
excel_output_file = os.path.join(directory, 'resultados.xlsx')
df.to_excel(excel_output_file, index=False)

print(f"Processamento concluído. Resultados exportados para arquivos de texto separados e para {excel_output_file}")
