# This program calculates the energy equivalent of a given mass using Einstein's equation E=mc^2.
while(True):
    # It prompts the user to enter a mass in kilograms and then calculates the energy in Joules.
    
    mass = float(input("Enter the mass in kg: "))
    c = 3 * (10 ** 8)  # speed of light in m/s
    energy = mass * (c ** 2)
    print(f"Energy: {energy:.2f} Joules")
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