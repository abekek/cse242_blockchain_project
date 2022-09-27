import random
import string

# number of total blocks
num_blocks = 30

for num_block in range(num_blocks):
    data = []
    num_addresses = random.randint(50, 100)
    for row_num in range(num_addresses):
        # get string of length 40 generated randomly with from the hexadecimal alphabet
        row = ''.join(random.choices(string.hexdigits, k=40)).lower()
        balance = random.randint(0, 1000000)
        data.append((row, balance))

    # put the data into a txt file
    with open(f'code/datagen_{num_block}.txt', 'w+') as f:
        for row, balance in data:
            f.write(f'{row} {balance}\n')