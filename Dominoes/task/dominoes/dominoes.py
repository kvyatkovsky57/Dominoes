# Write your code here
from random import randint


def change_status(status):
    if status == 'player':
        status = 'computer'
    elif status == 'computer':
        status = 'player'

    return status


def check_doubles(player_start_pieces, computer_start_pieces):
    doubles = []
    for piece in player_start_pieces:
        if piece[0] == piece[1]:
            doubles.append(piece)

    for piece in computer_start_pieces:
        if piece[0] == piece[1]:
            doubles.append(piece)

    if len(doubles) > 0:
        return doubles
    else:
        return False


def check_for_fish(domino_snake):

    numbers_pack = dict()

    for piece in domino_snake:
        for dot in piece:
            if dot in list(numbers_pack.keys()):
                numbers_pack[dot] += 1
            else:
                numbers_pack[dot] = 1

    if domino_snake[0][0] == domino_snake[-1][1] and numbers_pack[domino_snake[0][0]] > 7:
        print('fish')
        return True


def end_game(computer_pieces, player_pieces, domino_snake):
    if len(computer_pieces) == 0:
        return 'Status: The game is over. The computer won!'

    elif len(player_pieces) == 0:
         return 'Status: The game is over. You won!'

    elif check_for_fish(domino_snake):
        return "Status: The game is over. It's a draw!"


def get_max_double(doubles):
    doubles_sum = []
    for piece in doubles:
        doubles_sum.append(sum(piece))

    return doubles[doubles_sum.index(max(doubles_sum))]


def get_piece(piece_number, pieces):
    return pieces[abs(int(piece_number)) - 1]


def make_first_move(first_piece, player_start_pieces, computer_start_pieces):
    if first_piece in player_start_pieces:
        status = 'computer'
        player_start_pieces.remove(first_piece)
    elif first_piece in computer_start_pieces:
        status = 'player'
        computer_start_pieces.remove(first_piece)
    return status, player_start_pieces, computer_start_pieces


def make_full_domino_set():
    full_domino_set = []
    a = 0
    while a < 7:
        b = 0
        while b < 7:
            domino_piece = [a, b]
            rev_domino_piece = [b, a]
            if domino_piece and rev_domino_piece not in full_domino_set:
                full_domino_set.append(domino_piece)
            b += 1
        a += 1

    return full_domino_set


def make_snake_tail(domino_snake):
    return domino_snake[0] if len(domino_snake) == 1 else [domino_snake[0][0], domino_snake[len(domino_snake) - 1][1]]


def check_input(piece_number, player_pieces, snake_tail):
    while True:
        try:
            int(piece_number)
        except ValueError:
            piece_number = input('Invalid input. Please try again.\n> ')
        else:
            piece_number = int(piece_number)
            if abs(piece_number) <= len(player_pieces):
                check, piece_number = check_correct_piece(piece_number, player_pieces, snake_tail)
                if check:
                    return int(piece_number)
            else:
                piece_number = input('Invalid input. Please try again.\n> ')


def check_correct_piece(piece_number, player_pieces, snake_tail):
    piece = get_piece(piece_number, player_pieces)

    if piece_number == 0:
        check = True
        return check, piece_number

    elif piece_number < 0:
        if snake_tail[0] in piece:
            check = True
            return check, piece_number

    else:
        if snake_tail[1] in piece:
            check = True
            return check, piece_number

    piece_number = input('Illegal move. Please try again.\n >')
    check = False
    return check, piece_number


def computer_choose_piece(computer_pieces, domino_snake, snake_tail):
    count_dict = {}
    for i in range(0, 7):
        count_dict[i] = 0

    for piece in computer_pieces + domino_snake:
        for x in piece:
            count_dict[x] += 1

    legal_piece_numbers = dict()

    for piece in computer_pieces:
        if snake_tail[0] in piece:
            legal_piece_numbers[(computer_pieces.index(piece) + 1) * -1] = count_dict[piece[0]] + count_dict[piece[1]]

        elif snake_tail[1] in piece:
            legal_piece_numbers[computer_pieces.index(piece) + 1] = count_dict[piece[0]] + count_dict[piece[1]]

    piece_number = 0 if len(legal_piece_numbers) == 0 else max(legal_piece_numbers, key=legal_piece_numbers.get)
    return piece_number


def make_turn(status, domino_snake, player_pieces, computer_pieces, stock):
    snake_tail = make_snake_tail(domino_snake)
    if status == 'player':
        print("Status: It's your turn to make a move. Enter your command.")
        piece_number = check_input(input("> "), player_pieces, snake_tail)
        domino_snake, player_pieces, stock = make_move(domino_snake, piece_number, player_pieces, stock)

    elif status == 'computer':
        print("Status: Computer is about to make a move. Press Enter to continue...")
        input()
        piece_number = computer_choose_piece(computer_pieces, domino_snake, snake_tail)
        domino_snake, computer_pieces, stock = make_move(domino_snake, piece_number, computer_pieces, stock)

    status = change_status(status)

    return status, domino_snake, player_pieces, computer_pieces, stock


def make_move(domino_snake, piece_number, pieces, stock):

    piece = get_piece(piece_number, pieces)

    if piece_number == 0:
        if len(stock) > 0:
            random_piece_number = randint(0, len(stock) - 1)
            random_piece = stock[random_piece_number]
            pieces.append(random_piece)
            stock.remove(random_piece)
            return domino_snake, pieces, stock

    if piece_number > 0:
        pieces.remove(piece)
        if piece[0] == domino_snake[len(domino_snake) - 1][1]:
            domino_snake.append(piece)
        else:
            piece = [piece[1], piece[0]]
            domino_snake.append(piece)

    else:
        pieces.remove(piece)
        if piece[1] == domino_snake[0][0]:
            domino_snake.insert(0, piece)
        else:
            piece = [piece[1], piece[0]]
            domino_snake.insert(0, piece)

    return domino_snake, pieces, stock


def make_piece(domino_set):
    return domino_set[randint(0, len(domino_set) - 1)]


def make_start_pieces(domino_set):
    start_pieces = []
    for i in range(1, 8):
        piece = make_piece(domino_set)
        start_pieces.append(piece)
        domino_set.pop(domino_set.index(piece))
        i += 1

    return start_pieces, domino_set


def main_screen(computer_pieces, domino_snake, player_pieces, stock):
    print(
        f'======================================================================\n'
        f'Stock size: {len(stock)}\n'
        f'Computer pieces: {len(computer_pieces)}\n')

    if len(domino_snake) > 6:
        print(*[*domino_snake[:3], '...', *domino_snake[-3:]], sep='')
    else:
        [print(piece, end='') for piece in domino_snake]
    print(f'\n\nYour pieces:')
    for piece in player_pieces:
        print(f'{player_pieces.index(piece) + 1}:{piece}')
    print()


def main_function():

    full_domino_set = make_full_domino_set()

    first_hand = make_start_pieces(full_domino_set)
    player_pieces, stock = first_hand

    second_hand = make_start_pieces(stock)
    computer_pieces, stock = second_hand

    if not check_doubles(player_pieces, computer_pieces):
        main_function()
    else:
        piece = get_max_double(check_doubles(player_pieces, computer_pieces))
        status, player_pieces, computer_pieces = make_first_move(piece, player_pieces, computer_pieces)
        domino_snake = [piece]

        while True:
            main_screen(computer_pieces, domino_snake, player_pieces, stock)
            if end_game(computer_pieces, player_pieces, domino_snake):
                print(end_game(computer_pieces, player_pieces, domino_snake))
                break

            else:
                status, domino_snake, player_pieces, computer_pieces, stock = make_turn(
                    status, domino_snake, player_pieces, computer_pieces, stock)


main_function()
