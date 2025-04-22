# takes input for thecoefficients aa, bb, and cc of a quadratic equation
# ax2+bx+c=0ax2+bx+c=0 and computes its roots using the quadratic formula.
# and outputs the roots to the user
import cmath

try:

    while(True):

        # taking coefficient values from user
        a = float(input("Coefficient a: "))
        b = float(input("Coefficient b: "))
        c = float(input("Coefficient c: "))

        # calculating the roots based on the value of delta or the discriminant
        delta = b**2 - 4*a*c
        print()
        print("Roots:")
        if delta > 0 :
            x1 = ((-b) + delta) / (2*a)
            x2 = ((-b) - delta) / (2*a)

            print("Two real roots are:")
            print(f" 1) {x1:.2f}")
            print(f" 2) {x2:.2f}")

        elif delta == 0 :
            x = ((-b) / (2 * a))

            print(f"One positive root: {x:.2f}")

        else:
            x1 = (-b) + cmath.sqrt(delta) / (2 * a)
            x2 = (-b) - cmath.sqrt(delta) / (2 * a)
            
            print(f"Two complex roots:")
            print(f" 1) {x1}")
            print(f" 2) {x2}")

        print()

        # asking the user to restart the program for new calculation or to exit it
        prompt = input("Enter 'q' to calculate roots for some other equation, or enter 'e' to exit the program: ")

        if prompt == 'q' :
            continue

        elif prompt == 'e' :
            print("Thank you for using my program!")
            print("Exiting...")
            print()
            break
        else:
            print("Invalid! Pls try again after next iteration.")
            print()
            continue

# handling exceptions
except Exception as e:
    print(f"An error occurred while running the program: {e}.")