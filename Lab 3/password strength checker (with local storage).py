# This is a password strength checker which evaluates a given password into these three criterias
# based on the following conditions :
# * Weak - Less than 6 characters long
# * Medium - Is at least 6 characters long but does not contain at least one uppercase letter,
#           one lowercase letter, one digit and a special character
# * Strong - has at least on of each uppercase, lowercase, digit, and special characters,
#           and is at least 6 characters long
# With an added functionality of storing all the tested passwords in a text file locally

import string

# using a try except block to ensure this program is safe from all possible errors
try:

    # stores all the tested passwords in a text file in the same directory
    def store_password(password, filename = "password history.txt") :

        with open(filename, "a") as file :
            file.write(password + "\n")

    def password_category_assign(upper, lower, digit, special) :

        """ 
        checks the strength of the password based on its contents

        Args:
            upper: total count of uppercase letters
            lower: total count of lowercase letters
            digit: total count of digits
            special: total count of special characters

        Returns:
            "Medium" : if a password lacks atleast one of thses categories of characters
            "Strong" : if a password contains at least one character of each category
        
        """

        # stores the minimum value among the categories of characters
        minimum_category_val = min(upper, lower, digit, special)

        if minimum_category_val == 0 :
            return 'Medium'
        
        else :
            return "Strong"

    # a list to keep track of all the passwords tested
    passwords = []

    def main () :

        # contained inside a true while loop to run as long as the user wants
        while(True):

            password = input("Please enter your password: ")

            passwrd_len = len(password)

            # checking if the password is less than 6 characters long
            if passwrd_len < 6 :
                print()
                store_password(password)
                print("Weak password! Your password is too short. Try again with a password greater than 6 characters long.")
                print()
                continue

            # storing count of characters of each category present inside the password using a for loop
            up = 0
            low = 0
            digit = 0
            special = 0

            for char in password :
                if char.isupper() :
                    up += 1

                elif char.islower() :
                    low += 1

                elif char.isdigit() :
                    digit += 1

                elif char in string.punctuation and not char.isspace() :
                    special += 1

                else :
                    store_password(password)
                    print("Invalid characters found! Please try again with a different password.")
                    print()
                    continue

            # making sure the password was read properly by comparing the sum of category counts with its length
            if passwrd_len != (up + low + digit + special) :
                store_password(password)
                raise SystemExit("String could not be entirely read. Exiting the program...")

            # adding the password in the list
            passwords.append(password)

            # obtaining the assigned category of the password from the category assigning function
            category = password_category_assign(up, low, digit, special)

            # outputting accordingly
            if category == 'Medium' :

                store_password(password)

                print("Medium. Try making a password with a combination of speacial characters, uppercase letters, lowercase letters and numbers,\nmaking sure the length is atleast of 6 characters")
                
                prompt = input("Enter 'q' to retry and 'e' to exit the program: ")
                if prompt == 'q' :
                    print()
                    continue

                elif prompt == 'e' :
                    print()
                    print("Thank you for using my program!")
                    print("Exiting...")
                    break

                else :
                    print()
                    print("Invalid! Try entering between 'q' and 'e' when asked again in the next iteration")
                    continue
            
            elif category == "Strong" :
                print()
                store_password(password)
                print("Strong password! Great job!")
                print("Thank you for using my program!")
                print("Exiting...")
                print()
                break
            
            else :
                print()
                store_password(password)
                raise SystemExit("An unknown error occurred while checking the strength of the string. Exiting the program...")

    main()
    
except Exception as e:
    print(f"An unknown error '{e}' occurred while running the program. Exiting...")