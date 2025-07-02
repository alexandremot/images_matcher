from classes.sort import Sort
from pathlib import Path

def main():

    sort = Sort()

    figma_dir = Path("./figma")
    screenshots_dir = Path("./screenshots")
    
    pares = sort.encontrar_pares(figma_dir, screenshots_dir)
    print("\nPares encontrados:")
    for figma, screenshot in pares:
        print(f"{figma} -> {screenshot}")



if __name__ == "__main__":
    main()
