"""
Хрестики-нулики 3х3
  1 2 3
a _ _ _
b _ _ _
c _ _ _
"""
import sys

vert_coord = ('a', 'b', 'c')
underline = '_'
AI_TURN = True
USER_TURN = False


def give_choice():# Функція,яка надає вибір за кого хоче грати гравець.
    user_char = input('Введіть,за кого ви граєте (X або O): ').strip(' ').lower()
    while user_char not in ('x', 'o'):
        print('Помилка,перевірте чи правильно ви ввели дані та спробуйте ще раз!')
        user_char = input('Введіть,за кого ви граєте (X або O): ').strip(' ').lower()
    return user_char


def show_field(field):#Функція,яка виводе поле з координатами
    print(' ', '1', '2', '3')
    for y, v in enumerate(vert_coord):
        print(v, ' '.join(field[y]))


def is_draw(field):#Функція,яка робе перевірку на нічию або відсутність ходів
    count = 0
    for y in range(3):  # так як кожен раз ми будемо заміняти '_' на 'x' або 'о',то ми проходимо по всіх рядках і перевіряємо на наявність '_',якщо ж його немає в жодному рядку,отримуємо нічию
        count += 1 if underline in field[y] else 0
    return count == 0


def player_coord(game_field):
    converted_x, converted_y = 0, 0  #Перетворені х та у
    while True:
        coord = input('Введіть координати: '.lower().strip(' '))# Просимо ввести координати
        y, x = tuple(coord) # Розділяємо введені дані

        if int(x) not in (1, 2, 3,) or y not in vert_coord:  # Перевіряємо правильність введених даних
            print('Помилка,перевірте чи правильно ви ввели дані та спробуйте ще раз!')
            continue

        converted_x, converted_y = int(x) - 1, vert_coord.index(y)
        if game_field[converted_y][converted_x] == underline:
            break
        else:
            print('Дана позиція не порожня')

    return converted_x, converted_y


def get_opponent_choice(choice):
    return '0' if choice == 'x' else 'x'


def check_win(choice, field):
    opponent_choice = get_opponent_choice(choice)
    #Рядки
    for y in range(3): #Перевірка рядків
        if opponent_choice not in field[y] and underline not in field[y]:
            return True

    #Стовпці
    for x in range(3):#Перевірка стовпців
        col = [field[0][x], field[1][x], field[2][x]]
        if opponent_choice not in col and underline not in col:
            return True

    #Діагоналі
    diagonal = [field[0][0], field[1][1], field[2][2]]
    if opponent_choice not in diagonal and underline not in diagonal:# Перевірка чи стоять в нас по діагоналі символи 'choice'
        return True
    diagonal = [field[0][2], field[1][1], field[2][0]]
    if opponent_choice not in diagonal and underline not in diagonal:# Перевірка чи стоять в нас по другій діагоналі символи 'choice'
        return True

    return False


def minimax(board, depth, is_ai_turn):
    if check_win(computer_choice, board):
        return scores[computer_choice]
    if check_win(player_choice, board):
        return scores[player_choice]
    if is_draw(board):
        return scores['draw']

    if is_ai_turn:
        #Після ходу суперника вибираємо той,який нам вигодніше
        best_score = - sys.maxsize
        for y in range(3):
            for x in range(3):
                if board[y][x] == underline:
                    board[y][x] = computer_choice
                    score = minimax(board, depth + 1, USER_TURN)
                    board[y][x] = underline
                    best_score = max(best_score, score)
    else:
        # Суперник вибирає хід,який нам не вигідний
        best_score = sys.maxsize
        for y in range(3):
            for x in range(3):
                if board[y][x] == underline:
                    board[y][x] = player_choice
                    score = minimax(board, depth + 1, AI_TURN)
                    board[y][x] = underline
                    best_score = min(best_score, score)
    return best_score


def get_computer_position(field): # Реалізуємо хід думок компютера за допомогою алгоритму Мінімакс
    move = None
    best_score = -sys.maxsize #Надаємо максимального значення,нам потрібен тільки найкращий хід
    board = [field[y].copy() for y in range(3)] #Робимо копію,щоб не відбувались зміни на головному полі
    for y in range(3):
        for x in range(3):
            if board[y][x] == underline:
                board[y][x] = computer_choice
                score = minimax(board, 0, USER_TURN)
                board[y][x] = underline
                if score > best_score:
                    best_score = score
                    move = (x, y)

    return move


game_field = [
    [underline for x in range(3)] for y in range(3)
]# 1) Створюємо ігрове поле

player_choice = give_choice() # 2) Даємо для гравця Х або О,в залежності від вибору
computer_choice = get_opponent_choice(player_choice)  # 3) Даємо для компютера Х або О в залежності від вибору гравця

scores = {
    player_choice: -100,
    computer_choice: 100,
    'draw': 0
}

while True:
    show_field(game_field) # 4)Виводимо поле з координатами
    if is_draw(game_field): # 5)Перевіряємо поле на нічию
        print('Нічия!')
        break

    x, y = player_coord(game_field)
    game_field[y][x] = player_choice # 6)Ставимо вибрану фігуру на ігрове поле за вибраними координатами
    if check_win(player_choice, game_field):
        print('Гравець виграв!')
        break

    move = get_computer_position(game_field)
    if move is not None:
        x, y = move
        game_field[y][x] = computer_choice
        if check_win(computer_choice, game_field):
            print("Комп'ютер виграв!")
            break