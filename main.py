from pathlib import Path
from classes.sort import Sort

def main():
    # Cria uma instância da classe Sort
    comparador = Sort()
    
    # Define os diretórios com as imagens
    figma_dir = Path("./figma")
    screenshots_dir = Path("./screenshots")
    
    # Encontra os pares correspondentes
    pares = comparador.encontrar_pares(figma_dir, screenshots_dir)
    
    print(pares)

if __name__ == "__main__":
    main()
