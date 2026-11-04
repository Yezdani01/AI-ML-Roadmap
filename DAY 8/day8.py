# # Python Errors and Files
# # Exception handling, file reading/writing, pathlib, CSV and JSON files.


# # def voter():
# #     a = input("Enter the age of the user")
# #     return int(a)

# # try:
# #     age = voter()
# #     if age >= 18:
# #         print("Can Vote")
# #     else:
# #         print("Can't Vote")
# # except ValueError:
# #     print("Please Enter the correct numerical values")


# try:
#     # Code that might cause an error
#     number = int(input("Enter a number: "))
#     result = 10 / number
# except ZeroDivisionError:
#     # Runs ONLY if a ZeroDivisionError occurs
#     print("Error: You cannot divide by zero!")
# except ValueError:
#     # Runs ONLY if a ValueError occurs (e.g., typing 'abc')
#     print("Error: That wasn't a valid integer!")
# except Exception as e:
#     # Catch-all for any other unexpected exceptions
#     print(f"An unexpected error occurred: {e}")
# else:
#     # Runs ONLY if the try block succeeded without errors
#     print(f"Success! The result is {result}")
# finally:
#     # ALWAYS runs, no matter what (used for cleanup tasks)
#     print("Execution complete.")


# with open("DAY 8/notes.txt","w",encoding="utf-8") as file:
#     file.write("Hello This is a new file")
#     file.write("This is the second line in the file")

try:
    with open("DAY 8/notes.txt","r",encoding="utf-8") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("Does not exist")

    