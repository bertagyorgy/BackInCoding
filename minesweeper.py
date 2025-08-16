import random
import os


# 8 irány az aknaszomszédok számolásához
directions8 = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def create_board(width, height, num_mines):
    board = [["☐" for _ in range(width)] for _ in range(height)]
    mines_set = set()
    while len(mines_set) < num_mines:
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        mines_set.add((y, x))
    return board, mines_set

def count_adjacent_mines(y, x, mines_set, width, height):
    count = 0
    for dy, dx in directions8:
        ny, nx = y+dy, x+dx
        if 0 <= ny < height and 0 <= nx < width and (ny,nx) in mines_set:
            count += 1
    return count

def flood_fill(board, mines_set, y, x, width, height, revealed):
    """Rekurzívan fedi fel a 0 mezőket és a körülöttük lévő számokat."""
    if revealed[y][x] or board[y][x] == "⚑":
        return
    revealed[y][x] = True

    if (y, x) in mines_set:
        return

    count = count_adjacent_mines(y, x, mines_set, width, height)
    if count == 0:
        board[y][x] = " "
        for dy, dx in directions8:
            ny, nx = y+dy, x+dx
            if 0 <= ny < height and 0 <= nx < width:
                flood_fill(board, mines_set, ny, nx, width, height, revealed)
    else:
        board[y][x] = str(count)

def print_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in board:
        print(" ".join(row))
    print()

def check_victory(board, mines_set):
    """Győzelem, ha minden akna helyén zászló van."""
    for y, x in mines_set:
        if board[y][x] != "⚑":
            return False
    return True

def jatek(width=8, height=8, mines=10):
    board, mines_set = create_board(width, height, mines)
    flags_left = mines
    revealed = [[False]*width for _ in range(height)]

    while True:
        print_board(board)
        print(f"🚩 Hátralévő zászlók: {flags_left}")

        parts = input("Add meg a koordinátát (pl: '3 2', '3 2 f', '3 2 u'): ").split()
        if len(parts) < 2:
            print("Legalább két számot adj meg!")
            continue

        try:
            y, x = map(int, parts[:2])
            y -= 1
            x -= 1
        except ValueError:
            print("Hibás bevitel!")
            continue

        if not (0 <= y < height and 0 <= x < width):
            print("Hibás koordináta!")
            continue

        # Zászló lehelyezése
        if len(parts) == 3 and parts[2].lower() == "f":
            if board[y][x] == "☐" and flags_left > 0:
                board[y][x] = "⚑"
                flags_left -= 1
            elif flags_left == 0:
                print("Nincs több zászlód!")
            else:
                print("Ide nem tehetsz zászlót!")
            if check_victory(board, mines_set):
                print_board(board)
                print("🎉 Gratulálok, győztél!")
                break
            continue

        # Zászló visszavonása
        if len(parts) == 3 and parts[2].lower() == "u":
            if board[y][x] == "⚑":
                board[y][x] = "☐"
                flags_left += 1
            else:
                print("Itt nincs zászló!")
            continue

        # Ha aknára lép
        if (y,x) in mines_set:
            board[y][x] = "X"
            for my, mx in mines_set:
                if board[my][mx] != "X":
                    board[my][mx] = "*"
            print_board(board)
            print("💥 Aknára léptél! Vége a játéknak!")
            break

        # Felfedés
        flood_fill(board, mines_set, y, x, width, height, revealed)

# Indítás
jatek(5, 5, 2) #x-méret, y-méret, aknák száma
