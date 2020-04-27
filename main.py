import sys
import pygame
from pygame.locals import *

fps = 30  # частота кадров в секунду
win_width = 900  # ширина окна в пикселях
win_height = 600  # высота окна в пикселях
half_win_width = int(win_width / 2)  # определение центра
half_win_height = int(win_height / 2)  # определение центра

tile_width = 50  # ширина каждой плитки
tile_height = 40  # длина каждой плитки
cam_move_speed = 5  # количество пикселей на кадр
outside_decoration = 20  # процент плиток, которые будут задекорированы

bg = pygame.image.load("1.jpg")  # изображение, которое будет использовать в качестве фона

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global fps_clock, display, images_dict, level_map, decor_map, basic_font, gamer_map, currentImage
    pygame.init()  # инициализация всех импортированных модулей Pygame
    fps_clock = pygame.time.Clock()  # создание объекта, чтобы отслеживать время (частоту кадров)
    display = pygame.display.set_mode((win_width, win_height))  # создаем окна с размерами 900 * 600
    pygame.display.set_caption('UFO')  # задаем имя окну
    basic_font = pygame.font.Font('freesansbold.ttf', 18)  # основной шрифт
    # создаем словарь из изображений. Не делаем каждое изображение в отдельной переменной, т.к. тогда пришлось бы
    # создавать под каждое изображение свою глобальную переменную
    images_dict = {
        'title': pygame.image.load('star_title.png'),
        'text_title': pygame.image.load('text_title.png')
    }

    pygame.mixer.init()  # инициализация модуля микшера
    pygame.mixer.music.load('NLO.mp3')  # загрузка музыки
    pygame.mixer.music.set_volume(0.02)  # устанавливаем громкость
    pygame.mixer.music.play(-1)  # звук повторяется бесконечно

    startScreen()  # будет отображаться стартовая страничка, пока не будет начата игра


def startScreen():
    # Отображается начальный экран, пока не будет нажата клавиша

    titleRect = images_dict['title'].get_rect()  # помещаем заголовок - изображение
    titleRect.top = 10  # сколько пикселей отступить от верхнего края
    titleRect.centerx = half_win_width  # выравнивание по центру

    textRect = images_dict['text_title'].get_rect()  # помещаем текст - изображение
    textRect.top = 240  # сколько пикселей отступить от верхнего края
    textRect.centerx = half_win_width  # выравнивание по центру

    display.blit(bg, (0, 0))  # фоном сделали картинку
    display.blit(images_dict['title'], titleRect)  # добавили картинку на фон
    display.blit(images_dict['text_title'], textRect)  # добавили текст на фон

    # основной цикл для главной страницы
    # по нему программа понимает, надо завершить работу или вернуться из функции startScreen
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # если нажали крестик - выход
                terminate()
            elif event.type == KEYDOWN:  # если клавиша нажата и это esc - выход
                if event.key == K_ESCAPE:
                    terminate()
                return
        # пока игрок не делает ничего, вызываем функции, чтобы главная страница отображалась на экране
        pygame.display.update()
        fps_clock.tick()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
