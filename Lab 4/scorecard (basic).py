# This program takes the following input from the user,
# Student's Name
# Student's Roll No.
# Marks in Maths
# Marks in Physics
# Marks in Chemistry
# And provides a scorecard with their grades as output

# function to return grade based on the provided marks
def grade(marks) :
    if marks >= 90.0 :
        return 'A'
    elif 80.0 <= marks < 90.0 :
        return 'B'
    elif 70.0 <= marks < 80.0 :
        return 'C'
    elif 60.0 <= marks < 70.0 :
        return 'D'
    else :
        return 'F'

# taking students details and marks from user
print("----------------------")
name = input("Enter Student Name: ")
roll_no = input("Enter Roll No. ")
maths = float(input("Enter Marks in Maths: "))
physics = float(input("Enter Marks in Physics: "))
chemistry = float(input("Enter Marks in Chemistry: "))

average = (maths + physics + chemistry) / 3.0 # to find the overall course grade

print("----------------------")
print("Here's The Grade Card:")
print("----------------------")

print(f"Student Name: {name}")
print(f"Student Roll No. {roll_no}")
print(f"Grade in Maths: {grade(maths)}")
print(f"Grade in Physics: {grade(physics)}")
print(f"Grade in Chemistry: {grade(chemistry)}")
print(f"Overall Grade: {grade(average)}")

print("----------------------")
print("Thank You!")
print("----------------------")
