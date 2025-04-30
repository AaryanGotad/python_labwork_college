# This program takes Temperature and its unit as input from the user
# And then outputs the converted temperature with its unit

# taking temperature and unit from user
temp = float(input("Temperature to be converted: "))
unit = input("Its current unit (Celsius / fahrenheit / Kelvin) : ")

# taking the first character only to find unit
unit = unit[0].lower()

# calculating the new temparature based on the unit provided by the user
if unit == 'c' :
    new_temp = (temp * (9/5)) + 32
    print(f"{new_temp} degree Fahrenheit")

elif unit == 'f' :
    new_temp = (temp - 32) * (5/9)
    print(f"{new_temp} degree Celsius")

# giving choice of unit conversion to the user incase of temparature in Kelvin
elif unit == 'k' :
    prompt = input("Which you want to convert to? Celsius or Fahrenheit? : ")

    prompt = prompt[0].lower()

    if prompt == 'c' :
        new_temp = temp - 273.15
        print(f"{new_temp:.2f} degree Celsius")
    
    elif prompt == 'f' :
        new_temp = (temp - 273.15) * (9/5) + 32
        print(f"{new_temp:.2f} degree Fahrenheit")