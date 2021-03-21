from cs50 import get_int

height = 0

while height < 1 or height > 8:
    height = get_int("Height: ")

for row in range(height):
    for column in range(height):

        if row + column < height - 1:
            print(" ", end="")
        else:
            print("#", end="")
    print()
