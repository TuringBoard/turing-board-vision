import sys

h = float(sys.argv[1])
s = float(sys.argv[2])
v = float(sys.argv[3])

newH = int(h*2)
newS = int((s/255)*100)
newV = int((v/255)*100)
print(newH, newS, newV)
print("Low:", newH-10, newS-40, newV-40)
print("High:", newH+10, newS+40, newV+40)