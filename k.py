import re
mtext = "12沒 吱吱55"
if re.match(".*吱吱.*", mtext) != None:
    print("ok")
else:
    print("kk")
