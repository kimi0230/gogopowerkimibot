import re
mtext = "ivy"
num = re.sub(r'\D', "", mtext)
if num == "":
    print("kkkk")
print(num)
