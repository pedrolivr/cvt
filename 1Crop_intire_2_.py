import os
import fitz  # PyMuPDF
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def pdf_to_full_png(pdf_path, output_dir, zoom_factor=5.0):
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
        print(f"Página {page_num + 1} do arquivo {pdf_name} salva como {output_path}")

    print(f"Todas as páginas do arquivo {pdf_name} foram processadas e salvas.")

def process_all_pdfs_in_directory(input_dir, output_dir, zoom_factor=2.0):
    # Verificar se o diretório de saída existe, se não, criar
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Listar todos os arquivos no diretório de entrada
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            print(f"Processando arquivo: {pdf_path}")
            pdf_to_full_png(pdf_path, output_dir, zoom_factor)
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
