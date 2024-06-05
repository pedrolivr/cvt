import cv2
import pytesseract

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

# Caminho para a imagem
image_path = 'C:/Users/pe.oliveira/OneDrive - EGIS Group/Bureau/testepy/output/ECA-153GO-288-319-DPL-ANT-NS-C3-001-R00a_page_1.png'

# Definir as regiões de interesse (ROIs)
regions = [
    (120, 450, 400, 150),   # Exemplo de coordenadas (x, y, largura, altura)
    (150, 600, 350, 70),
    (520, 600, 350, 70),
    (240, 700, 600, 70),
    (620, 750, 350, 70)
                                 # Adicione outras regiões conforme necessário
]

# Caminho para o arquivo de saída
output_file = 'C:/Users/pe.oliveira/OneDrive - EGIS Group/Bureau/testepy/output/resultados.txt'

# Ler texto de cada região e exportar para um arquivo de texto
with open(output_file, 'w', encoding='utf-8') as file:
    for i, region in enumerate(regions):
        text = read_text_from_region(image_path, region)
        file.write(f'Texto da região {i + 1}:\n')
        file.write(text)
        file.write('\n' + '-' * 30 + '\n')

print(f'Resultados exportados para {output_file}')
