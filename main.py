import copy
import random
import sys
import pygame
import os
from pygame.locals import *

FPS = 30  # частота кадров в секунду
WIN_WIGHT = 900  # ширина окна в пикселях
WIN_HEIGHT = 600  # высота окна в пикселях
HALF_WIN_WIDHT = int(WIN_WIGHT / 2)  # определение центра
HALF_WIN_HEIGHT = int(WIN_HEIGHT / 2)  # определение центра
TILE_WIDTH = 50  # ширина каждой плитки
TILE_HEIGHT = 85  # длина каждой плитки
TILE_FLOR_HEIGHT = 40  # длина части плитки, которая будет видна
CAM_MOVE_SPEED = 5  # количество пикселей на кадр
OUTSIDE_DECORATION = 20  # процент плиток, которые будут задекорированы
BG = pygame.image.load("1.jpg")  # изображение, которое будет использовать в качестве фона
TEXT_COLOR = (255, 255, 255)  # цвет текста
FONT = 15  # размер шрифта
UP = 'up'  # движение вверх
DOWN = 'down'  # движение вниз
LEFT = 'left'  # движение влево
RIGHT = 'right'  # движение вправо
current_image = 0  # начальный костюм героя
# создаем словарь из изображений
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
    'costume5': pygame.image.load('costume5.png'),
    'uncovered goal': pygame.image.load('RedSelector.png'),
    'covered goal': pygame.image.load('Selector.png'),
    'star': pygame.image.load('star.png'),
    'solved': pygame.image.load('star_solved.png')
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
# список костюмов героя
game_costume = [
    images_dict['costume1'],
    images_dict['costume2'],
    images_dict['costume3'],
    images_dict['costume4'],
    images_dict['costume5']
]

pygame.init()  # инициализация всех импортированных модулей Pygame
fps_clock = pygame.time.Clock()  # создание объекта, чтобы отслеживать частоту кадров
display = pygame.display.set_mode((WIN_WIGHT, WIN_HEIGHT))  # создаем окно с размерами 900 * 600
pygame.display.set_caption('STRANGER')  # задаем имя окну
basic_font = pygame.font.Font('freesansbold.ttf', FONT)  # основной шрифт


def main():
    # главная функция

    pygame.mixer.init()  # инициализация модуля микшера
    pygame.mixer.music.load('NLO.mp3')  # загрузка музыки
    pygame.mixer.music.set_volume(0.1)  # устанавливаем громкость
    pygame.mixer.music.play(-1)  # звук повторяется бесконечно

    start_screen()  # будет отображаться стартовая страничка, пока не будет начата игра

    levels = read_levels_file('maps.txt')  # считывает уровень из текстового файла
    current_level_index = 0  # игрок начинает с 1го уровня, в списке это индекс 0

    # главный цикл игры
    while True:
        result = run_level(levels, current_level_index)  # отдаем все уровни и номер уровня, который нам нужен
        if result in ('пройден', 'следующий'):  # переход на следующий уровень
            current_level_index += 1
            if current_level_index >= len(levels) and result == 'пройден':  # если уровни все пройдены, попадаем на
                # главную
                current_level_index = 0
                start_screen()
            elif current_level_index >= len(levels) and result == 'следующий':  # если больше уровней нет, переходи
                # на первый
                current_level_index = 0
        elif result == 'назад':  # вернуться на уровень назад
            current_level_index -= 1
            if current_level_index < 0:  # если это самый первый уровень, остаемся на нем
                current_level_index = 0
        elif result == 'заново':  # если был сброс уровня - ничего не делаем (можно опустить эту ветку, но для логики
            # программы - написала)
            pass


def start_screen():
    # Отображается начальный экран, пока не будет нажата клавиша

    inst()
    # основной цикл для главной страницы
    # по нему программа понимает, надо завершить работу или вернуться из функции start_screen
    while True:
        click = False  # флаг, что левая кнопка мыши нажата
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # если нажата мышка и кнопка
                click = True  # инвертируем флаг
                mx, my = pygame.mouse.get_pos()  # переменные для хранения позиции мыши
                if image[1].collidepoint(mx, my) and click:  # если нажали на кнопку
                    display.blit(pygame.image.load("manual.jpg"), (0, 0))  # рисую инструкцию
                    image1 = button('main.png', (125, 20), display)  # кнопка назад
                if image1[1].collidepoint(mx, my) and click:  # если нажали назад - перерисовываю начальный экран
                    inst()
            elif event.type == pygame.QUIT:  # если нажали крестик - выход
                terminate()
            elif event.type == pygame.KEYDOWN:  # если клавиша нажата
                if event.key == pygame.K_ESCAPE:  # выход
                    terminate()
                if event.key == pygame.K_SPACE:  # закрыли окно
                    return
        # пока игрок не делает ничего, вызываем функции, чтобы главная страница отображалась на экране
        pygame.display.update()  # отображение всего на экране
        fps_clock.tick()  # миллисекунды работы программы


def read_levels_file(filename):
    # чтение карт уровней из файла

    assert os.path.exists(filename), 'Такого файла не существует: %s' % filename  # фу-ция вернет True, если файл
    # существует
    map_file = open(filename, 'r')  # открываем файл в режиме чтения
    content = map_file.readlines() + ['\n']  # формируем список из строк уровней + перенос строки в конец
    map_file.close()  # закрыли файл

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
            goals = []  # положения (х,у) целей (куда надо передвинуть звезду)
            stars = []  # начальные положения (х,у) звезд
            for x in range(max_width):  # проходим по всем ячейкам карты
                for y in range(len(map_obj[x])):
                    if map_obj[x][y] in ('@', '+'):  # @ - игрок, + - игрок на цели
                        start_x = x
                        start_y = y
                    if map_obj[x][y] in ('.', '+', '*'):  # . - цель, + - игрок на цели, * - звезда на цели
                        goals.append((x, y))
                    if map_obj[x][y] in ('$', '*'):  # $ - звезда, * - зезда на цели
                        stars.append((x, y))

            # убеждаемся, что уровень считан правильно. Если какое-то утверждение будет ложным, получим ошибку
            # 1. В уровне обязательно должен быть игрок
            assert start_x is not None and start_y is not None, 'На уровне %s (строка %s) в файле %s нет символовов ' \
                                                                'начальной точки.' % (level_num + 1, line_num,
                                                                                      filename)
            # 2. В уровне обязательно должна быть хоть одна цель, куда надо передвинуть звезду
            assert len(goals) > 0, 'Уровень %s (строка %s) в файле  %s должен иметь хоть одну цель.' % (
                level_num + 1, line_num, filename)
            # 3. В уровне целей должно быть меньше или равно зездам, больше не может быть
            assert len(stars) >= len(goals), 'Уровень %s (строка %s) в файле  %s нельзя пройти. У него %s целей, ' \
                                             'но всего %s звезд.' % (level_num + 1, line_num, filename, len(goals),
                                                                     len(stars))

            # создаем объект состояния игры
            game_state_obj = {
                'player': (start_x, start_y),  # начальные координаты игрока
                'step_counter': 0,  # количество шагов
                'stars': stars  # координаты звезд
            }

            # создаем объект уровня
            level_obj = {
                'width': max_width,  # ширина
                'height': len(map_obj),  # высота
                'map_obj': map_obj,  # координаты поля
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
    map_obj = decorate_map(level_obj['map_obj'], level_obj['start_state']['player'])  # объект карты (координаты
    # поля, координаты игрока)
    game_state_obj = copy.deepcopy(level_obj['start_state'])  # копия уровня для отслеживания. Запомнили исходный
    # уровень, если игрок захочет играть заново - уровень восстановится
    map_needs_redraw = True  # установили True для вызова draw_map
    level_is_complete = False  # устанвливаем, что уровень не пройден

    # главный цикл
    while True:
        # сброс переменных
        player_move_to = None  # переместить игрока на карте
        key_pressed = False  # клавиша нажата
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # если нажали крестик - выход
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # если нажали мышкой на кнопку
                click = True
                mx, my = pygame.mouse.get_pos()
                if back_i[1].collidepoint(mx, my) and click:
                    return 'назад'
                elif next_i[1].collidepoint(mx, my) and click:
                    return 'следующий'
                elif costum_i[1].collidepoint(mx, my) and click:
                    current_image += 1
                    if current_image >= len(game_costume):
                        current_image = 0
                    map_needs_redraw = True
                elif restart_i[1].collidepoint(mx, my) and click:
                    return 'заново'
                elif esc_i[1].collidepoint(mx, my) and click:
                    terminate()
                elif home_i[1].collidepoint(mx, my) and click:
                    start_screen()
            elif event.type == pygame.KEYDOWN:  # если клавиша нажата
                key_pressed = True
                if event.key == pygame.K_LEFT:
                    player_move_to = LEFT
                elif event.key == pygame.K_RIGHT:
                    player_move_to = RIGHT
                elif event.key == pygame.K_UP:
                    player_move_to = UP
                elif event.key == pygame.K_DOWN:
                    player_move_to = DOWN
                elif event.key == pygame.K_n:
                    return 'следующий'
                elif event.key == pygame.K_b:
                    return 'назад'
                elif event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_BACKSPACE:
                    return 'заново'
                elif event.key == pygame.K_p:
                    current_image += 1
                    if current_image >= len(game_costume):
                        current_image = 0
                    map_needs_redraw = True

        display.blit(BG, (0, 0))  # добавили фон

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

        # если игрок переместился, то карту нужно перерисовать
        if map_needs_redraw:
            map_surf = draw_map(map_obj, game_state_obj, level_obj['goals'])
            map_needs_redraw = False
            mapSurfRect = map_surf.get_rect()
            mapSurfRect.center = (HALF_WIN_WIDHT, HALF_WIN_HEIGHT)
        display.blit(map_surf, mapSurfRect)

        level_surf = basic_font.render('Уровень %s / %s' % (level_num + 1, len(levels)), 1,
                                       TEXT_COLOR)  # инфа  об урове
        level_rect = level_surf.get_rect()  # создание объекта
        level_rect.bottomleft = (20, WIN_HEIGHT - 35)  # координаты расположения надписи
        display.blit(level_surf, level_rect)  # отрисовка на экране

        step_surf = basic_font.render('Шаги: %s' % (game_state_obj['step_counter']), 1, TEXT_COLOR)  # инфа о шагах
        step_rect = step_surf.get_rect()  # создание объекта
        step_rect.bottomleft = (20, WIN_HEIGHT - 10)  # координаты расположения надписи
        display.blit(step_surf, step_rect)  # отрисовка на экране

        back_i = button('back.png', (590, 550), display)  # загрузили кнопку "назад" на фон
        next_i = button('next.png', (650, 550), display)  # загрузили кнопку "вперед" на фон
        costum_i = button('costum.png', (710, 550), display)  # загрузили кнопку "смена костюма" на фон
        restart_i = button('restart.png', (770, 550), display)  # загрузили кнопку "начать заново" на фон
        home_i = button('home.png', (820, 550), display)  # загрузили кнопку "вернуться на главную" на фон
        esc_i = button('esc.png', (880, 550), display)  # загрузили кнопку "выход" на фон

        # если уровень пройден, пишем надпись поверх уровня, что он пройден
        if level_is_complete:
            solved_rect = images_dict['solved'].get_rect()  # добавление изображения
            solved_rect.center = (HALF_WIN_WIDHT, HALF_WIN_HEIGHT)  # координаты центра
            display.blit(images_dict['solved'], solved_rect)  # отрисовка на экране
            # если пользователь нажимает клавишу в этот момент, то переходит на новый уровень
            if key_pressed:
                return 'пройден'
        # отображаем страничку на экране
        pygame.display.update()
        fps_clock.tick()


def decorate_map(map_obj, start_x_y):
    # получаем оформленный объект карты

    start_x, start_y = start_x_y  # запомнили координаты
    map_obj_copy = copy.deepcopy(map_obj)  # делаем копию карты, чтобы не менять оригинал

    # преобразуем символы из карты, которые нам не требуются (игрок, цель, звезды), проходя по всем координатам карты
    for x in range(len(map_obj_copy)):
        for y in range(len(map_obj_copy[0])):
            if map_obj_copy[x][y] in ('$', '.', '@', '+', '*'):
                map_obj_copy[x][y] = ' '
    flood_fill(map_obj_copy, start_x, start_y, ' ', 'o')  # функция преобразует плитки пола с ' ' на 'о'

    # проходимся по всем возможным координатам карты
    for x in range(len(map_obj_copy)):
        for y in range(len(map_obj_copy[0])):
            if map_obj_copy[x][y] == '#':
                # проверяем если ли (х,у) угловая плитка, если да - меняем (х,у) на угловую плитку (проверка идет по
                # две плитки рядом по часовой стрелке)
                if (wall(map_obj_copy, x, y - 1) and wall(map_obj_copy, x + 1, y)) or \
                        (wall(map_obj_copy, x + 1, y) and wall(map_obj_copy, x, y + 1)) or \
                        (wall(map_obj_copy, x, y + 1) and wall(map_obj_copy, x - 1, y)) or \
                        (wall(map_obj_copy, x - 1, y) and wall(map_obj_copy, x, y - 1)):
                    map_obj_copy[x][y] = 'x'
            elif map_obj_copy[x][y] == ' ' and random.randint(0, 99) < OUTSIDE_DECORATION:  # если трава - сажай дерево
                map_obj_copy[x][y] = random.choice(list(decor_map.keys()))
    return map_obj_copy


def flood_fill(map_obj, x, y, old_character, new_character):
    # заливка пола

    if map_obj[x][y] == old_character:  # преобразуем плитку в 'о'
        map_obj[x][y] = new_character

    # если плитки слева, справа, вверху и внизу такие же, как начальная плитка, делаем и с ними заливку пола
    if x < len(map_obj) - 1 and map_obj[x + 1][y] == old_character:
        flood_fill(map_obj, x + 1, y, old_character, new_character)  # справа
    if x > 0 and map_obj[x - 1][y] == old_character:
        flood_fill(map_obj, x - 1, y, old_character, new_character)  # слева
    if y < len(map_obj[x]) - 1 and map_obj[x][y + 1] == old_character:
        flood_fill(map_obj, x, y + 1, old_character, new_character)  # внизу
    if y > 0 and map_obj[x][y - 1] == old_character:
        flood_fill(map_obj, x, y - 1, old_character, new_character)  # вверху


def draw_map(map_obj, game_state_obj, goals):
    # рисует карту уровня (+ игрок, звезды)

    map_surf_width = len(map_obj) * TILE_WIDTH  # ширина поля
    map_surf_height = (len(map_obj[0]) - 1) * TILE_FLOR_HEIGHT + TILE_HEIGHT  # высота поля
    map_surf = pygame.Surface((map_surf_width, map_surf_height))
    map_surf.blit(BG, (0, 0))  # добавляем фон

    # рисуем плитку на карте уровня, проходим по всем возможным координатам (х,у)
    for x in range(len(map_obj)):
        for y in range(len(map_obj[x])):
            space_rect = pygame.Rect((x * TILE_WIDTH, y * TILE_FLOR_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
            if map_obj[x][y] in level_map:  # если (х,у) это символ на карте, запомни его изображение
                base_tile = level_map[map_obj[x][y]]
            elif map_obj[x][y] in decor_map:  # если (х,у) находится в decor_map, то это трава
                base_tile = level_map[' ']
            map_surf.blit(base_tile, space_rect)  # рисуем основание карты (стены и траву)
            if map_obj[x][y] in decor_map:  # рисуем декор поверх основания (камни, кустарники)
                map_surf.blit(decor_map[map_obj[x][y]], space_rect)
            elif (x, y) in game_state_obj['stars']:  # (х,у) это звезда?
                if (x, y) in goals:  # (х,у) это цель для звезды и звезда в ней?
                    map_surf.blit(images_dict['covered goal'], space_rect)  # рисуем цель желтой
                map_surf.blit(images_dict['star'], space_rect)  # рисуем звезду
            elif (x, y) in goals:  # (х,у) это цель?
                map_surf.blit(images_dict['uncovered goal'], space_rect)  # рисуем серую цель
            if (x, y) == game_state_obj['player']:  # (x,y) это герой?
                map_surf.blit(game_costume[current_image], space_rect)  # рисуем героя
    return map_surf


def make_move(map_obj, game_state_obj, player_move_to):
    # является ли перемещение игрока допустимым

    player_x, player_y = game_state_obj['player']  # забрали координаты игрока
    stars = game_state_obj['stars']  # забрали координаты звезд
    # менянем координаты (помним, координаная ось идет из левого верхнего угла)
    if player_move_to == UP:
        x_off_set = 0
        y_off_set = -1
    elif player_move_to == RIGHT:
        x_off_set = 1
        y_off_set = 0
    elif player_move_to == DOWN:
        x_off_set = 0
        y_off_set = 1
    elif player_move_to == LEFT:
        x_off_set = -1
        y_off_set = 0

    if wall(map_obj, player_x + x_off_set, player_y + y_off_set):
        return False  # если встретила стена, верни false
    else:
        if (player_x + x_off_set, player_y + y_off_set) in stars:
            # на пути есть звезда, можно ли ее переместить, смотрим на 2 клетки вперед есть ли препятствие
            if not blocked(map_obj, game_state_obj, player_x + (x_off_set * 2), player_y + (y_off_set * 2)):
                new_stars_xy = stars.index((player_x + x_off_set, player_y + y_off_set))
                stars[new_stars_xy] = (stars[new_stars_xy][0] + x_off_set, stars[new_stars_xy][1] + y_off_set)
            else:
                return False
        game_state_obj['player'] = (player_x + x_off_set, player_y + y_off_set)  # меняем координаты игрока
        return True


def level_finished(level_obj, game_state_obj):
    # Уровень будет пройден, если на всех целях есть звезды. некоторые уровни имееют больше звезд, чем целей. Поэтому
    # проверяем, чтобы все цели были покрыты звездами, а не все ли звезды на цели
    for goal in level_obj['goals']:
        if goal not in game_state_obj['stars']:
            return False
    return True


def wall(map_obj, x, y):
    # возвразщает true, если позиция (х,у) стена, иначе false

    if x < 0 or x >= len(map_obj) or y < 0 or y >= len(map_obj[x]):  # такие координаты лежат за картой уровня
        return False
    elif map_obj[x][y] in ('#', 'x'):  # если (х,у) соотвествуют символу стены
        return True
    return False


def blocked(map_obj, game_state_obj, x, y):
    # возвращает true, если (х,у) заблокирован стеной или звездой

    # (х,у) это стена?
    if wall(map_obj, x, y):
        return True
    # (х,у) лежат за картой уровня?
    elif x < 0 or x >= len(map_obj) or y < 0 or y >= len(map_obj[x]):
        return True
    # (х,у) это звезда?
    elif (x, y) in game_state_obj['stars']:
        return True
    return False


def button(picture, coords, display):
    # создание кнопок

    image = pygame.image.load(picture)  # загрузка изображения, которое будет на кнопке
    image_rect = image.get_rect()  # создаем объект
    image_rect.topright = coords  # загружаем координаты правого верхнего угла кнопки
    display.blit(image, image_rect)  # выводим кнопку на экран
    return image, image_rect


def inst():
    # функция отрисовки главного меню

    global image

    title_rect = images_dict['title'].get_rect()  # помещаем заголовок - изображение
    title_rect.top = 10  # сколько пикселей отступить от верхнего края
    title_rect.centerx = HALF_WIN_WIDHT  # выравнивание по центру (координата х)

    text_rect = images_dict['text_title'].get_rect()  # помещаем текст - изображение
    text_rect.top = 240  # сколько пикселей отступить от верхнего края
    text_rect.centerx = HALF_WIN_WIDHT  # выравнивание по центру (координата х)

    instruction_text = 'Push the stars over the marks.'  # текст инструкции
    inst_surf = basic_font.render(instruction_text, 1, TEXT_COLOR)  # цвет текста (1 - сглаживание)
    inst_rect = inst_surf.get_rect()  # создание объекта
    inst_rect.top = 395  # сколько пикселей отступить от верхнего края
    inst_rect.centerx = HALF_WIN_WIDHT  # выравнивание по центру (координата х)

    display.blit(BG, (0, 0))  # фоном сделали картинку, левый верхний угол картинки - (0,0)
    display.blit(images_dict['title'], title_rect)  # добавили картинку на фон
    display.blit(images_dict['text_title'], text_rect)  # добавили текст на фон
    display.blit(inst_surf, inst_rect)  # добавили описание на фон

    image = button('menu.png', (870, 20), display)  # загрузили кнопку на фон


def terminate():
    # окончание игры

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
