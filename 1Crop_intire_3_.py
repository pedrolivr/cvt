import os
import fitz  # PyMuPDF
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm

def pdf_to_full_png(pdf_path, output_dir, zoom_factor, pbar):
    # Abrir o documento PDF
    pdf_document = fitz.open(pdf_path)
    
    # Iterar sobre cada página
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        
        # Configurar o zoom para aumentar a resolução
        mat = fitz.Matrix(zoom_factor, zoom_factor)
        pix = page.get_pixmap(matrix=mat)
        
        # Converter para imagem PIL
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Criar um nome de arquivo para a imagem de saída
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = os.path.join(output_dir, f"{pdf_name}_page_{page_num + 1}.png")
        
        # Salvar a imagem completa como PNG
        image.save(output_path, "PNG")
        
        # Atualizar a barra de progresso
        pbar.update(1)

    #print(f"Todas as páginas do arquivo {pdf_name} foram processadas e salvas.")

def process_all_pdfs_in_directory(input_dir, output_dir, zoom_factor=5.0):
    # Verificar se o diretório de saída existe, se não, criar
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Listar todos os arquivos no diretório de entrada
    pdf_files = [filename for filename in os.listdir(input_dir) if filename.lower().endswith('.pdf')]
    
    # Contar o número total de páginas em todos os PDFs
    total_pages = 0
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        pdf_document = fitz.open(pdf_path)
        total_pages += len(pdf_document)
    
    # Criar uma barra de progresso para o total de páginas
    with tqdm(total=total_pages, desc="Processando PDFs", unit="página") as pbar:
        for filename in pdf_files:
            pdf_path = os.path.join(input_dir, filename)
            pdf_to_full_png(pdf_path, output_dir, zoom_factor, pbar)
    
    print("Processamento concluído para todos os arquivos PDF.")

def selecionar_pasta():
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal

    input_dir = filedialog.askdirectory(title="Selecione a pasta de entrada")
    if not input_dir:  # Usuário clicou em "Cancelar"
        print("Operação cancelada.")
        return

    # Pedir ao usuário para fornecer o nome da pasta de saída
    output_folder_name = input("Digite o nome da pasta de saída: ")
    
    # Diretório de saída com o nome fornecido pelo usuário
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, output_folder_name)
    
    # Verificar se o diretório de entrada existe
    process_all_pdfs_in_directory(input_dir, output_dir)

# Chamar a função para selecionar a pasta
selecionar_pasta()
