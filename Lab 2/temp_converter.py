# takes input for temperature in Celsius and converts it to Fahrenheit using the formula F=9/5C+32.
# It then prints the result.
while(True):

    # taking user input in celcius and converting it to fahrenheit
    celsius = float(input("Celsius: "))
    fahrenheit = (9/5) * celsius + 32

    # printing the result in fahrenheit and prompting the user to calculate again or exit
    print(f"Fahrenheit: {fahrenheit:.2f}")
    print()
    prompt = input("type 'q' to calculate again or 'e' to exit: ")
    
    if prompt == 'q':
        print()
        continue
    
    elif prompt == 'e':
        print()
        print("Thank you for using the program!")
        print("Exiting...")
        print()
        break
    
    else:
        print("Invalid input. Please try again.")
        print()