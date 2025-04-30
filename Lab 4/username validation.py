# This program validates a given username based on the following criterias:
# * Must be atleast 5 chracters long
# * Must not contain any special characters and or any whitespaces

import string

username = input("Enter username: ")
print()

length = len(username)

if length >= 5 :

    for char in username :

        # checking for special character
        if char in string.punctuation and not char.isspace() :
            raise SystemExit("Invalid! Username must not have any special characters and or any whitespaces \n")

        # checking for whitespace
        elif char.isspace() :
            raise SystemExit("Invalid! Username must not have any special characters and or any whitespaces \n")
    
    print("Valid Username! \n")

else :
    print("Invalid! Username must be at least 5 chracters long. \n")