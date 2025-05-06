# Take user input
original_string = input("Enter a string to reverse: ")

# Reverse the string using a loop
reversed_string = ""
for char in original_string:
    reversed_string = char + reversed_string  # Prepend each character

# Output the result
print("Reversed string:", reversed_string)