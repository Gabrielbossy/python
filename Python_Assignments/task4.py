teacher = input("Enter teacher's name: ")
subject = input("Enter subject's name: ")
students = int(input("Enter number of students: "))
scores = []

total = 0
passed = 0
failed = 0

for a in range(students):
    score = int(input(f"Enter score of student {a + 1}: "))
    scores.append(score)
    total += score 
    
    if score >= 50:
        passed += 1
    else:
        failed += 1
        
average = total / students

highest  = max(scores) 
lowest = min(scores)

if average >= 70:
    performance = "Excellent"
elif average >= 50:
    performance = "Good"
else:
    performance = "Needs improvement"
    
print("\n========== STUDENT REPORT ==========")
print("Teacher:", teacher)
print("Subject:", subject)

print("\nAll Scores:")
for score in scores:
    print(score)

print("\nPassing Scores:")
for score in scores:
    if score >= 50:
        print(score)

print("\nFailing Scores:")
for score in scores:
    if score < 50:
        print(score)

print("\nNumber Passed:", passed)
print("Number Failed:", failed)
print("Highest Score:", highest)
print("Lowest Score:", lowest)
print("Average Score:", average)

print("\nOverall Performance:", performance)
print("====================================")           

