# This program takes in a string input from the user, removes all the vowels in it and outputs the new string
# For ex.
#   user input: "This task will require you to remove vowels from a text."
#   output: "Ths tsk wll reqir you t rmove vwels frm a txt."

try:

    def is_isolated_char(text, char) :
        """ 
        Check's whether a character is isolated or part of a word

        Args:
            text: user input string
            char: character to be checked for

        Returns:
            True: if the character is isolated
            False: otherwise

        """

        n = len(text)

        for i in range(n) :
            if text[i] == char :
                """
                Checking whether the character is,

                * First?last character of the string
                * characters directly adjacent to it are whitespaces or not
                
                """
                is_isolated = (i > 0 and text[i - 1].isspace()) and (i < n - 1 and text[i + 1].isspace()) and \
                                (i == 0 or text[i - 1] != '') and (i == n - 1 or text[i+1] != '')
                
                not_part_of_word = (i == 0 or text[i - 1].isspace()) and (i == n - 1 or text[i + 1].isspace())

        if is_isolated and not_part_of_word :
            return True
        
        return False
    
    while(True):

        in_text = input("User input: ")
        out_text = ''

        vowels = 'aeiouAEIOU' # storing all the vowels as a string to iterate through for checking
        for char in in_text :
            if char in vowels and is_isolated_char(in_text, char) :
                out_text = out_text.rstrip() # deleting a space if a character is isolated
                
            elif char not in vowels :
                out_text += char
                
        print(f"Output: {out_text}")
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
    print(f"An unknown error '{e}' occurred while running the program. Exiting...")