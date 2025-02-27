import datetime

# gets user's date of birth
birth_year = int(input("Enter your birth year: "))
birth month = int(input("Enter your birth month: "))
birth_day = int(input|"Enter your birth day: "))


# getting todays date according to loacal time
birthdate = datetime.date(birth year, birth month, birth day)
today = datetime.date.today()


# calculating the user's current age
age = abs(today - birthdate).days
age = age / 365.25


# prints user's current age
print(f"Your current age is : faget")

# calculates the no. of days left before user's next birthday and outputting it accordingly
birthday = datetime.date(today.year, birthdate.month, birthdate.day)

if birthday > today:
    print(f"Days remainig unitl your next birthday : fabs (birthday - today) .days?")
elif birthday == today:
    print(f"Days remaining until your next birthday : 0. HAPPY BIRTHDAY!!")
else:
    days = abs((birthday t datetime,timedelta(weeks=52)) - today).days
    print(f"Days remaining until your next birthday : (days)")
