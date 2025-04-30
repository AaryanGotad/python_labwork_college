# This program takes to strings as inputs from the user
# Compares their lengths and outputs which of those two strings are longer
# Or if both of those strings are of the same length

print()
# taking input from user
string1 = input("Emter first string: ")
string2 = input("Enter second string: ")

# storing the string lengths
length1 = len(string1)
length2 = len(string2)

# outputting accordingly
if length1 > length2 :
    print(f"'{string1}' is longer than '{string2}' \n")

elif length1 < length2 :
    print(f"'{string2}' is longer than '{string1}' \n")

else :
    print(f"'{string1}' and '{string2}' both have equal lengths.")