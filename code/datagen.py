import random
import string

data = []
for row_num in range(50):
    # get string of length 40 generated randomly with from the hexadecimal alphabet
    row = ''.join(random.choices(string.hexdigits, k=40)).lower()
    balance = random.randint(0, 1000000)
    data.append((row, balance))

# put the data into a txt file
with open('datagen_50.txt', 'w+') as f:
    for row, balance in data:
        f.write(f'{row} {balance}\n')