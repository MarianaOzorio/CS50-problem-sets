from cs50 import get_float

coins = 0
dollars = 0

while dollars <= 0:
    dollars = get_float("Change owed: ")

cents = round(dollars * 100)

while cents >= 25:
    coins += 1
    cents = cents - 25

while cents >= 10:
    coins += 1
    cents = cents - 10

while cents >= 5:
    coins += 1
    cents = cents - 5

while cents >= 1:
    coins += 1
    cents = cents - 1

print(f"{coins}")
