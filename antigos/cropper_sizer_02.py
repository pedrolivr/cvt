import cv2
import pytesseract
import os
import tkinter as tk
from tkinter import filedialog

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
    (120, 450, 400, 150),   # Exemplo de coordenadas (x, y, largura, altura)
    (150, 600, 350, 70),
    (520, 600, 350, 70),
    (240, 700, 600, 70),
    (620, 750, 350, 70)
]

# Processar todas as imagens no diretório selecionado
for filename in os.listdir(directory):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(directory, filename)
        output_file = os.path.join(directory, f'resultados_{os.path.splitext(filename)[0]}.txt')
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(f'Resultados para {filename}:\n')
            for i, region in enumerate(regions):
                text = read_text_from_region(image_path, region)
                file.write(f'Texto da região {i + 1}:\n')
                file.write(text)
                file.write('\n' + '-' * 30 + '\n')
            file.write('\n' + '=' * 30 + '\n')

print("Processamento concluído. Resultados exportados para arquivos de texto separados.")
