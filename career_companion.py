print("Welcome to AI Career Companion!")

name = input("Enter your name: ")
degree = input("Enter your degree: ")
skills = input("Enter your skills: ")

print("\n----- YOUR CAREER PROFILE -----")
print("Name:", name)
print("Degree:", degree)
print("Skills:", skills)

print("\nYour career journey starts today!")
print("\n----- CAREER SUGGESTIONS -----")

if "python" in skills.lower() and "excel" in skills.lower():
    print("Suggested Path: Data Analyst")
    print("Next learn: SQL, Power BI, and basic statistics")

elif "python" in skills.lower():
    print("Suggested Path: Python Developer")
    print("Next learn: SQL, functions, and projects")

elif "html" in skills.lower() or "css" in skills.lower():
    print("Suggested Path: Web Developer")
    print("Next learn: JavaScript and responsive design")

else:
    print("Suggested Path: Explore beginner-friendly IT careers")
    print("Start with Python, Excel, and basic computer skills")