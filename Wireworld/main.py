import numpy as np
import pyxel as px

# Estados do WireWorld
EMPTY = 0
CONDUCTOR = 1
HEAD = 3
TAIL = 2

# Definir um tamanho de matriz maior
width, height = 60, 60  
atual = np.zeros((width, height), dtype=int)
next = np.zeros_like(atual)


scale = 5  

# Função para carregar o padrão a partir de um arquivo de texto
def initialize_pattern_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if y < height and x < width:
                if char == '0':
                    atual[x, y] = EMPTY
                elif char == '1':
                    atual[x, y] = CONDUCTOR
                elif char == '2':
                    atual[x, y] = TAIL
                elif char == '3':
                    atual[x, y] = HEAD

class Button:
    def __init__(self, x, y, action, text):
        self.x, self.y, self.action, self.text = x, y, action, text

    def _hitPointBox(self):
        return self.x <= px.mouse_x < self.x + 45 and self.y <= px.mouse_y < self.y + 25

    def _update(self):
        if px.btnp(px.MOUSE_BUTTON_LEFT) and self._hitPointBox():
            self.action()

    def _draw(self):
        px.rect(self.x, self.y, 45, 25, 12)  # Botão preenchido
        px.rectb(self.x, self.y, 45, 25, 6)  # Bordas do botão
        px.text(self.x + 8, self.y + 10, self.text, 0)  # Texto centralizado


class WireWorldSimulator:
    def __init__(self):
        self.paused = False
        self.allSpeed = [0.5, 1, 2, 5, 10]
        self.speedIndex = 1
        self.frame_count = 0
        self.frames_per_update = int(30 / self.allSpeed[self.speedIndex])  # Controlar a velocidade
        self.pause_unpauseButton = Button(310, 10, self._pause_unpauseButton, 'PAUSE')
        self.stepButton = Button(310, 40, self._stepButton, 'STEP')
        self.resetButton = Button(310, 70, self._resetButton, 'RESET')
        self.saveButton = Button(310, 100, self._saveButton, 'SAVE')
        self.speedButton = Button(310, 130, self._speedButton, f'SPEED:{self.allSpeed[self.speedIndex]}')

        px.init(width * scale + 100, height * scale, title='WireWorld Simulator', fps=144, quit_key=ord('q'))
        px.run(self.update, self.draw)

    def update(self):
        self.pause_unpauseButton._update()
        self.stepButton._update()
        self.resetButton._update()
        self.saveButton._update()
        self.speedButton._update()

        if not self.paused:
            self.frame_count += 1
            if self.frame_count >= self.frames_per_update:
                self.frame_count = 0
                self.update_pattern()

    def draw(self):
        px.cls(0)
        self.draw_pattern()
        self.pause_unpauseButton._draw()
        self.stepButton._draw()
        self.resetButton._draw()
        self.saveButton._draw()
        self.speedButton._draw()

    def draw_pattern(self):
        for x in range(width):
            for y in range(height):
                if atual[x, y] == EMPTY:
                    px.rect(x * scale, y * scale, scale, scale, 0)
                elif atual[x, y] == CONDUCTOR:
                    px.rect(x * scale, y * scale, scale, scale, 10)
                elif atual[x, y] == HEAD:
                    px.rect(x * scale, y * scale, scale, scale, 1)
                elif atual[x, y] == TAIL:
                    px.rect(x * scale, y * scale, scale, scale, 8)

    def update_pattern(self):
        global atual, next
        px.mouse(True)
        next = np.zeros_like(atual)

        for x in range(width):
            for y in range(height):
                if atual[x, y] == HEAD:
                    next[x, y] = TAIL
                elif atual[x, y] == TAIL:
                    next[x, y] = CONDUCTOR
                elif atual[x, y] == CONDUCTOR:
                    count_heads = self.count_heads(x, y)
                    if count_heads == 1 or count_heads == 2:
                        next[x, y] = HEAD
                    else:
                        next[x, y] = CONDUCTOR
                else:
                    next[x, y] = EMPTY

        atual, next = next, atual

    def count_heads(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if atual[nx, ny] == HEAD:
                        count += 1
        return count

    def _pause_unpauseButton(self):
        self.paused = not self.paused
        self.pause_unpauseButton.text = 'PAUSE' if self.paused else 'UNPAUSE'

    def _stepButton(self):
        if self.paused:
            self.update_pattern()

    def _resetButton(self):
        initialize_pattern_from_file('inicial.txt') 
        self.paused = False

    def _saveButton(self):
        np.savetxt('saída.txt', atual, fmt='%d')

    def _speedButton(self):
        self.speedIndex = (self.speedIndex + 1) % len(self.allSpeed)
        self.frames_per_update = int(30 / self.allSpeed[self.speedIndex])

# Inicializar o padrão a partir do arquivo
#Antes de rodar o código não esqueça de atualizar o caminho do arquivo de texto
initialize_pattern_from_file('c:\\Users\\reich\\OneDrive\\Área de Trabalho\\trab_comp_cient\\inicial.txt')

# Iniciar o simulador
WireWorldSimulator()
