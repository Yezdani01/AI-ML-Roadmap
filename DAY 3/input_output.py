# Outputting a welcome message
print("--- Welcome to the Profile Generator ---")

# Gathering user input
name = input("Enter your name: ")
age_input = input("Enter your age: ")

# Type casting: Converting the age string into an integer
age = int(age_input)

# Calculating a future value
age_in_five_years = age + 5

# Outputting results using an f-string (formatted string)
print(f"Hello, {name}!")
print(f"You are currently {age} years old.")
print(f"In 5 years, you will be {age_in_five_years}.")
