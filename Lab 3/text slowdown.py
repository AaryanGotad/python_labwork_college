# Often while listening to a lecture on youtube we slow down/speed up the playback speed.
# This program does something similar but with text.
# The program works as follows:
# user input: 'Hello! I am Tommy!'
# output: 'Hello! ... I ... am ... Tommy!'

try:

    while(True):

        in_text = input("User input: ")
        out_text = in_text.replace(' ', ' ... ')
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