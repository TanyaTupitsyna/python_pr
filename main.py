import copy
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
tile_height = 85  # длина каждой плитки
tile_flor_height = 40
cam_move_speed = 5  # количество пикселей на кадр
outside_decoration = 20  # процент плиток, которые будут задекорированы
bg = pygame.image.load("1.jpg")  # изображение, которое будет использовать в качестве фона
text_color = (255, 255, 255)
up = 'up'
down = 'down'
left = 'left'
right = 'right'


def main():
    # главная функция

    music()  # фоновая музыка
    global fps_clock, display, images_dict, level_map, decor_map, basic_font, game_costume, current_image
    pygame.init()  # инициализация всех импортированных модулей Pygame
    fps_clock = pygame.time.Clock()  # создание объекта, чтобы отслеживать время (частоту кадров)
    display = pygame.display.set_mode((win_width, win_height))  # создаем окна с размерами 900 * 600
    pygame.display.set_caption('UFO')  # задаем имя окну
    basic_font = pygame.font.Font('freesansbold.ttf', 15)  # основной шрифт
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
        'costume1': pygame.image.load('costume1.png'),
        'costume2': pygame.image.load('costume2.png'),
        'costume3': pygame.image.load('costume3.png'),
        'costume4': pygame.image.load('costume4.png'),
        'costume5': pygame.image.load('costume5.png')
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
    game_costume = [
        images_dict['costume1'],
        images_dict['costume2'],
        images_dict['costume3'],
        images_dict['costume4'],
        images_dict['costume5']
    ]

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

    titleRect = images_dict['title'].get_rect()  # помещаем заголовок - изображение
    titleRect.top = 10  # сколько пикселей отступить от верхнего края
    titleRect.centerx = half_win_width  # выравнивание по центру

    textRect = images_dict['text_title'].get_rect()  # помещаем текст - изображение
    textRect.top = 240  # сколько пикселей отступить от верхнего края
    textRect.centerx = half_win_width  # выравнивание по центру

    instruction_text = 'Push the stars over the marks.'  # текст инструкции
    inst_surf = basic_font.render(instruction_text, 1, text_color)
    inst_rect = inst_surf.get_rect()
    inst_rect.top = 395
    inst_rect.centerx = half_win_width

    display.blit(bg, (0, 0))  # фоном сделали картинку
    display.blit(images_dict['title'], titleRect)  # добавили картинку на фон
    display.blit(images_dict['text_title'], textRect)  # добавили текст на фон
    display.blit(inst_surf, inst_rect)  # добавили описание

    # основной цикл для главной страницы
    # по нему программа понимает, надо завершить работу или вернуться из функции startScreen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # если нажали крестик - выход
                terminate()
            elif event.type == pygame.KEYDOWN:  # если клавиша нажата и это esc - выход
                if event.key == pygame.K_ESCAPE:
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
    # работа уровня (обработка действий в игре)

    global current_image  # начальный костюм героя
    level_obj = levels[level_num]  # объект уровня текущего уровня (тот, который мы хотим видеть)
    map_obj = decorate_map(level_obj['map_obj'], level_obj['start_state']['player'])  # объект карты
    game_state_obj = copy.deepcopy(level_obj['start_state'])  # копия уровня для отслеживания. Запомнили исходный
    # уровень, если игрок захочет играть заново - уровень восстановится
    map_needs_redraw = True  # установили True для вызова draw_map
    level_surf = basic_font.render('Уровень %s / %s' % (level_num + 1, len(levels)), 1, text_color)  # текст об урове
    level_rect = level_surf.get_rect()  # создание rect
    level_rect.bottomleft = (20, win_width - 35)  # координата правого нижнего угла
    map_width = len(map_obj) * tile_width  # ширина уровня (умнодаем на ширину плитки)
    map_height = (len(map_obj[0]) - 1) * tile_flor_height + tile_height  # высота уровня (добавляем плитку в конце,
    # т.к. она не будет перекрыта (нижний ряд))
    level_is_complete = False  # устанвливаем, что уровень не пройден

    while True:
        # сброс переменных
        player_move_to = None  # переместить игрока на карте
        key_pressed = False  # клавиша нажата
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # если нажали крестик - выход
                terminate()
            elif event.type == pygame.KEYDOWN:  # если клавиша нажата
                key_pressed = True
                if event.key == pygame.K_LEFT:
                    player_move_to = left
                elif event.key == pygame.K_RIGHT:
                    player_move_to = right
                elif event.key == pygame.K_UP:
                    player_move_to = up
                elif event.key == pygame.K_DOWN:
                    player_move_to = down
                elif event.key == pygame.K_n:
                    return 'next'
                elif event.key == pygame.K_b:
                    return 'back'
                elif event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_BACKSPACE:
                    return 'reset'
                elif event.key == pygame.K_p:
                    current_image += 1
                    if current_image >= len(game_costume):
                        current_image = 0
                    map_needs_redraw = True

        # если игрок совершил перемещение и уровень не окончен
        if player_move_to is not None and not level_is_complete:
            moved = make_move(map_obj, game_state_obj, player_move_to)  # вызов функции обработки координат Х,У
            # если вернулась истина - игрок действительно переместился. Если ложь - игрок пытался пройти через
            # препятсвие или толкнуть звезду, у которой впереди было препятствие (игрок не может двигаться и на карте
            # ничего не меняется)
            if moved:
                game_state_obj['step_counter'] += 1  # счетчик шагов
                map_needs_redraw = True
            # если уровень пройден, показываем "Пройден" и обнуляем параметры
            if level_finished(level_obj, game_state_obj):
                level_is_complete = True
                key_pressed = False

        display.blit(bg, (0, 0))  # добавили фон

        #рисуем объект
        display.blit(level_surf, level_rect)
        step_surf = basic_font.render('Шаги: %s' % (game_state_obj['step_counter']), 1, text_color)
        step_rect = step_surf.get_rect()
        step_rect.bottomleft = (20, win_height - 10)
        display.blit(step_surf, step_rect)

        # если игрок переместился, то карту нужно перерисовать
        if map_needs_redraw:
            mapSurf = draw_map(map_obj, game_state_obj, level_obj['goals'])
            map_needs_redraw = False

        # если уровень пройден, пишем надпись поверх уровня, что он пройден
        if level_is_complete:
            solved_rect = images_dict['solved'].get_rect()
            solved_rect.center = (half_win_width, half_win_height)
            display.blit(images_dict['solved'], solved_rect)
            # если пользователь нажимает клавишу в этот момент, то переходит на новый уровень
            if key_pressed:
                return 'solved'
        # отображаем страничку на экране
        pygame.display.update()
        fps_clock.tick()


def decorate_map(map_obj, start_x_y):
    pass


def draw_map(map_obj, game_state_obj, goals):
    pass


def make_move(map_obj, game_state_obj, player_move_to):
    pass


def level_finished(level_obj, game_state_obj):
    # Уровень будет пройден, если на всех целях есть звезды. некоторые уровни имееют больше звезд, чем целей. Поэтому
    # проверяем, чтобы все цели были покрыты звездами, а не все ли звезды на цели
    for goal in level_obj['goals']:
        if goal not in game_state_obj['stars']:
            return False
    return True


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
