import sys
import pygame
import os
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
    global fps_clock, display, images_dict, level_map, decor_map, basic_font, gamer_map, current_image
    pygame.init()  # инициализация всех импортированных модулей Pygame
    fps_clock = pygame.time.Clock()  # создание объекта, чтобы отслеживать время (частоту кадров)
    display = pygame.display.set_mode((win_width, win_height))  # создаем окна с размерами 900 * 600
    pygame.display.set_caption('UFO')  # задаем имя окну
    basic_font = pygame.font.Font('freesansbold.ttf', 18)  # основной шрифт
    # создаем словарь из изображений. Не делаем каждое изображение в отдельной переменной, т.к. тогда пришлось бы
    # создавать под каждое изображение свою глобальную переменную
    images_dict = {
        'title': pygame.image.load('star_title.png'),
        'text_title': pygame.image.load('text_title.png'),
        'corner': pygame.image.load('Wall_Block_Tall.png'),
        'wall': pygame.image.load('Wood_Block_Tall.png'),
        'inside floor': pygame.image.load('Plain_Block.png'),
        'outside floor': pygame.image.load('Grass_Block.png'),
        'rock': pygame.image.load('Rock.png'),
        'short tree': pygame.image.load('Tree_Short.png'),
        'tall tree': pygame.image.load('Tree_Tall.png'),
        'ugly tree': pygame.image.load('Tree_Ugly.png'),
        'princess': pygame.image.load('princess.png'),
        'boy': pygame.image.load('boy.png'),
        'catgirl': pygame.image.load('catgirl.png'),
        'horngirl': pygame.image.load('horngirl.png'),
        'pinkgirl': pygame.image.load('pinkgirl.png')
    }

    # связка символа на карте уровня и изображением, соответстсвующим символу
    level_map = {
        'x': images_dict['corner'],
        '#': images_dict['wall'],
        'o': images_dict['inside floor'],
        ' ': images_dict['outside floor']
    }

    # связка предмета, изображенного поверх травы, и его номера
    decor_map = {'1': images_dict['rock'],
                 '2': images_dict['short tree'],
                 '3': images_dict['tall tree'],
                 '4': images_dict['ugly tree']
                 }

    current_image = 0  # начальный костюм героя

    # список костюмов героя
    game_map = [
        images_dict['princess'],
        images_dict['boy'],
        images_dict['catgirl'],
        images_dict['horngirl'],
        images_dict['pinkgirl']]

    start_screen()  # будет отображаться стартовая страничка, пока не будет начата игра

    levels = read_levels_file('maps.txt')  # считывает уровень из текстового файла
    current_level_index = 0  # игрок начинает с 1го уровня, в списке это индекс 0

    # главный цикл игры
    while True:
        result = run_level(levels, current_level_index)  # отдаем все уровни и номер уровня, который нам нужен
        if result in ('solved', 'next'):  # переход на следующий уровень
            current_level_index += 1
            if current_level_index >= len(levels):  # если уровни закончился, начинаем с начала
                current_level_index = 0
        elif result == 'back':  # вернуться на уровень назад
            current_level_index -= 1
            if current_level_index < 0:  # если это самый первый уровень, остаемся на нем
                current_level_index = 0
        elif result == 'reset':  # если был сброс уровня - ничего не делаем
            pass


def start_screen():
    # Отображается начальный экран, пока не будет нажата клавиша

    music()  # фоновая музыка
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


def music():
    # фоновая музыка

    pygame.mixer.init()  # инициализация модуля микшера
    pygame.mixer.music.load('NLO.mp3')  # загрузка музыки
    pygame.mixer.music.set_volume(0.03)  # устанавливаем громкость
    pygame.mixer.music.play(-1)  # звук повторяется бесконечно


def read_levels_file(filename):
    # чтение карт уровней из файла

    assert os.path.exists(filename), 'Такого файла не существует: %s' % filename  # фу-ция вернет True, если файл
    # существует
    mapFile = open(filename, 'r')  # открываем файл в режиме чтения
    content = mapFile.readlines() + ['\n']  # формируем список из строк уровней + пустая строка в конец
    mapFile.close()  # закрыли файл

    levels = []  # список уровней
    level_num = 0  # количество уровней в файле
    map_text_lines = []  # список строк для одного уровня
    map_obj = []  # объект карты, полученный из map_text_lines

    for line_num in range(len(content)):
        line = content[line_num].rstrip('\n')  # Строку записали в line. Символы новой строки в конце удаляем.
        if ';' in line:
            line = line[:line.find(';')]  # если встретилась ; - считай эту строку комментарием. Берем в line все,
            # что было до ; (в нашем случае это пустота)
        if line != '':
            map_text_lines.append(line)  # добавляем строки уровня, пока строка не пустая
        elif line == '' and len(map_text_lines) > 0:  # если после этого нашли опять пустую строку - уровень закончен
            max_width = -1  # надо найти самую длинную строку, чтобы по ней построить прямоугольник уровня
            for i in range(len(map_text_lines)):
                if len(map_text_lines[i]) > max_width:
                    max_width = len(map_text_lines[i])
            for i in range(len(map_text_lines)):  # дополняем строки нехватающими пробелами, чтобы все были одной длины
                map_text_lines[i] += ' ' * (max_width - len(map_text_lines[i]))
            # преобразование строк в объект карты
            for x in range(len(map_text_lines[0])):  # формируем "столбики" карты
                map_obj.append([])
            for y in range(len(map_text_lines)):  # заносим значения в "столбики"
                for x in range(max_width):
                    map_obj[x].append(map_text_lines[y][x])

            start_x = None  # начальная координата х для игрока
            start_y = None  # начальная координата у для игрока
            goals = []  # положения (х,у) целей
            stars = []  # начальные положения (х,у) звезд
            for x in range(max_width):  # проходим по всем ячейкам карты
                for y in range(len(map_obj[x])):
                    if map_obj[x][y] in ('@', '+'):  # @ - игрок, + - цель и игрок
                        start_x = x
                        start_y = y
                    if map_obj[x][y] in ('.', '+', '*'):  # . - цель, + - цель и игрок, * - цель и звезда
                        goals.append((x, y))
                    if map_obj[x][y] in ('$', '*'):  # $ - звезда, * - цель и звезда
                        stars.append((x, y))

            # убеждаемся, что уровень считан правильно. Если какое-то утверждение будет ложным, получим ошибку
            assert start_x is not None and start_y is not None, 'На уровне %s (строка %s) в файле %s нет символовов ' \
                                                                'начальной точки.' % (level_num + 1, line_num,
                                                                                      filename)
            assert len(goals) > 0, 'Уровень %s (строка %s) в файле  %s должен иметь хоть одну цель.' % (
                level_num + 1, line_num, filename)

            assert len(stars) >= len(goals), 'Уровень %s (строка %s) в файле  %s нельзя пройти. У него %s целей, ' \
                                             'но всего %s звезд.' % (level_num + 1, line_num, filename, len(goals),
                                                                     len(stars))

            # создаем объект состояния игры
            game_state_obj = {
                'player': (start_x, start_y),  # начальные координаты игрока
                'step_сounter': 0,  # количество шагов
                'stars': stars  # координаты звезд
            }

            # создаем объект уровня
            level_obj = {
                'width': max_width,  # ширина
                'height': len(map_obj),  # высота
                'mapObj': map_obj,  # координаты поля
                'goals': goals,  # координаты целей
                'start_state': game_state_obj  # состояние игры
            }

            levels.append(level_obj)  # добавили уровень
            # сброс переменных для нового уровня
            map_text_lines = []
            map_obj = []
            game_state_obj = {}
            level_num += 1
    return levels  # возвращаем множество уровней


def run_level(levels, level_num):
    pass


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
