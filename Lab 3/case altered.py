# This program takes user input, alters the cases of each letter and outputs the altered string
# Example,
#   user input: 'This course name is Python Programming!'
#   case altered: 'tHIS COURSE NAME IS pYTHON pROGRAMMING!'

try:

    while(True):

        text = input("user input: ")
        output = ''

        # storing the altered cased characters in an empty string and outputing it
        for char in text :
            if char.islower() :
                output += char.upper()

            elif char.isupper() :
                output += char.lower()

            else :
                output += char

        print(f"Case alered: {output}")
        print()

        # prompting the user to continue or to stop
        prompt = input("Enter 'q' to continue or 'e' to exit: ")
        if prompt == 'q' :
            continue

        elif prompt == 'e' :
            print("Thank you for using my program!")
            print("Exiting...")
            print()
            break

        else :
            print("Invalid! Try entering between 'q' and 'e' when asked again in the next iteration")
            print()
            continue

except Exception as e:
    print("An unknown error '{e}' occured while running the program. Exiting...")