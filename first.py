print("🧬 SMART HEALTH HELPER 🧬")

name = input("Enter your name: ")
age = int(input("Enter your age: "))
water = int(input("How many glasses of water today? "))
sleep = float(input("How many hours did you sleep? "))
protien= int(input("how many grams of protien you have consumed today?"))

score = 0

if water >= 8:
    score += 1
if sleep >= 7:
    score += 1
if age < 30:
    score += 1
if protien >=100:
    score +=1

print("\n--- HEALTH REPORT ---")
print("Name:", name)

print ("your score is ",score)
if score == 4:
    print("Excellent health habits! 🔥")
elif score == 3:
    print("Good, but can improve 🙂")
elif score ==2:
    print ("your body needs some rest and a healthy meal which is rich in protien")
else:
    print("You need to take better care of your health ⚠️")

