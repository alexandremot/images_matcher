from PIL import Image, ImageChops
from pathlib import Path
from typing import List, Tuple
from itertools import product
from scipy.optimize import linear_sum_assignment
import numpy as np

class Sort:

    def carregar_imagens(self, diretorio: Path) -> List[Tuple[str, Image.Image]]:
        """
        Carrega todas as imagens de um diretório e retorna uma lista de tuplas
        contendo o caminho e a imagem.
        """
        arquivos = list(diretorio.glob("*.png")) + list(diretorio.glob("*.jpg"))
        return [(str(arquivo), Image.open(arquivo)) for arquivo in arquivos]

    def redimensionar(self, imagem: Image.Image) -> Image.Image:
        """
        Redimensiona a imagem para 16x16 pixels para comparação eficiente.
        """
        return imagem.resize((16, 16))

    def calcular_diferenca(self, img1: Image.Image, img2: Image.Image) -> float:
        """
        Calcula a diferença média entre duas imagens.
        Retorna um valor entre 0 (idênticas) e 1 (completamente diferentes).
        """
        # Garante que as imagens estão no modo RGB
        img1 = img1.convert("RGB")
        img2 = img2.convert("RGB")

        diferenca = ImageChops.difference(img1, img2)
        
        largura, altura = diferenca.size
        soma = 0
        
        for x, y in product(range(largura), range(altura)):
            r, g, b = diferenca.getpixel((x, y))
            soma += (r + g + b) / 3
        
        media = soma / (largura * altura)
        return media / 255  # Normaliza para valor entre 0 e 1


    def encontrar_pares(self, figma_dir: Path, screenshots_dir: Path) -> List[Tuple[str, str]]:
        # Carrega as imagens
        figma_list = self.carregar_imagens(figma_dir)
        screenshots_list = self.carregar_imagens(screenshots_dir)
        
        # Redimensiona todas as imagens
        figma_red = [(nome, self.redimensionar(img)) for nome, img in figma_list]
        screenshots_red = [(nome, self.redimensionar(img)) for nome, img in screenshots_list]
        
        # Matriz de similaridades
        n_figmas = len(figma_red)
        n_screenshots = len(screenshots_red)

        matriz_similaridade = np.zeros((n_figmas, n_screenshots))
        for i, (_, img1) in enumerate(figma_red):
            for j, (_, img2) in enumerate(screenshots_red):
                matriz_similaridade[i][j] = self.calcular_diferenca(img1, img2)

        # Aplica algoritmo húngaro da scipy
        row_ind, col_ind = linear_sum_assignment(matriz_similaridade)

        # Monta os pares finais
        resultado = [(figma_list[i][0], screenshots_list[j][0]) for i, j in zip(row_ind, col_ind)]
        return resultado

