
balance = int(input("balance: "))
roi = int(input("roi: ")) / 100
current = balance
month = 30
target = 10000
i = 1

while True:
    current = current + (current * roi)
    print(f"day {i}: {current}")
    i += 1
    if current >= target:
        break