# This program takes the following input from the user,
# Student's Name
# Student's Roll No.
# Marks in Maths
# Marks in Physics
# Marks in Chemistry
# And provides a scorecard with their grades as output
# With an added functionality of all the student records maintained in a json file

import json

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

# data to be written in the file
data = {
    "name": name,
    "roll no.": roll_no,
    "Marks in Maths": maths,
    "Marks in Physics": physics,
    "Marks in Chemistry": chemistry,
    "Grade in Maths": grade(maths),
    "Grade in Physics": grade(physics),
    "Grade in Chemistry": grade(chemistry),
    "Overall Grade": grade(average)
}

filename = 'student records.json'

# loading the existing data (if any) from the json file in a list
try:
    with open(filename) as file:
        existing_data = json.load(file)

except FileNotFoundError :
    existing_data = []

# appending the new data with the existing data list
existing_data.append(data)

# rewriting the data in the json file
with open(filename, "w") as file :
    json.dump(existing_data, file, indent=4)

print("----------------------")
print("Student records updated successfully!")

print("----------------------")
print("Thank You!")
print("----------------------")
