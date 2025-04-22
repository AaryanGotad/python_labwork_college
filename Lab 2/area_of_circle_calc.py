# takes input for the radius of a circle and computes its area using the formula
# A=π*r**r, where π is a constant (use an approximation like 3.14159).
# It then prints the result.
# The program continues to prompt the user for input until they choose to exit.
import math

while(True):
    radius = float(input("Radius: "))
    area = math.pi * (radius ** 2)
    print(f"Area: {area:.2f} square units")
    print()

    prompt = input("type 'q' for calculating area of a different circle, or 'e' to exit the program: ")
    print()
    
    if prompt == 'q' :
        continue
    
    elif prompt == 'e' :
        print("Thank you for using my program!")
        print("Exiting...")
        print()
        break
    
    else :
        print("Invaalid! please type between q (calculating again) and e (exiting the program)")
