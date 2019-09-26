import math

for i in range(30):
    print(200 * math.sin(math.pi / 180 * (i + 1)))
for i in range(2, 102, 2):
    print("位移" + str(i) + "：" + str(math.asin(i / 200) * 180 / math.pi))
