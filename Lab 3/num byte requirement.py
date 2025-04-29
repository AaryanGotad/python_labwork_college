# This program takes an integer input from the user and returns the no. of bytes requred to represent tha no. in binary
# Ex. input: 2
#     output: "'2' requires '1' byte(s) to be represented in binary." 
#           [since, 2 = 10 in binary, which equals to 2 bits which equals to 1 byte
#                   (rounded off as 1 byte is made of 8 bits, and 1 byte is the least possible representation in memory?storage of data)]

import math

try:

    print()
    decimal_number = int(input("Enter an integer number (No fractions or decimals, just whole numbers!): "))
    binary_number = bin(decimal_number)[2:]
    bytes_required = math.ceil(len(binary_number) / 8.0)
    print((f"'{decimal_number}' requires '{bytes_required}' to be represented in binary."))
    print()

except Exception as e:
    print(f"An unknown error '{e}' occurred while running the program. Exiting...")