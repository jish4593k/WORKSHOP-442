import os
import tempfile
import concurrent.futures 
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdfminer.high_level import extract_text
import seaborn as sns
import torch

def split_and_extract(arquivo_entrada):
    with tempfile.TemporaryDirectory() as path:
        leitor = PdfFileReader(arquivo_entrada)
        caminhos_saida = [f"{path}/parte_{i+1}" for i in range(min(4, len(leitor.pages)))]

        for i, caminho_saida in enumerate(caminhos_saida):
            escritor = PdfFileWriter()
            escritor.addPage(leitor.getPage(i))
            with open(f"{caminho_saida}.pdf", 'wb') as f:
                escritor.write(f)

        with concurrent.futures.ThreadPoolExecutor(4) as executor:
            futures = [executor.submit(extract_text, f'{caminho}.pdf') for caminho in caminhos_saida]
            results = concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED).done

        with open(f'anotacoes.txt', 'w') as arquivo_saida:
            for caminho, result in zip(caminhos_saida, results):
                if result:
                    arquivo_saida.write(result.result())

def display_info(arquivo_entrada):
    leitor = PdfFileReader(arquivo_entrada)
    print(f"Number of pages: {len(leitor.pages)}")
    print(f"PDF Metadata: {leitor.getDocumentInfo()}")

def generate_torch_tensor():
    torch_tensor = torch.randn(100)
    print(f"Torch Tensor: {torch_tensor}")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    

    arquivo_entrada = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    
    if arquivo_entrada:
        
        display_info(arquivo_entrada)

      
        split_and_extract(arquivo_entrada)

        
        generate_torch_tensor()

        
        sns.lineplot(x=range(10), y=range(10))
        plt.show()

if __name__ == '__main__':
    main()
