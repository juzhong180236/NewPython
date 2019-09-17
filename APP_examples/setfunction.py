import random
import os.path

# p = {"fdasfadsfds"}
#
# try:
#     while True:
#         print(p.pop(), end="")
# except:
# set1 = {"China": 125, "America": 3, "中国": 5}
# list1 = list(set1.items())
# list1.sort(key=lambda x: x[1], reverse=True)
# print(list1)
list1 = [2, 3, 4, 5]
list2 = [4, 5, 6]
list1.append(list2)
print(list1[4][0])
print(os.path.join("D:/", "cds"))
print(os.path.basename("D:/file"))
print(os.path.isfile("D://file"))
print("{:.1}".format(random.random()))
for i in range(5):
    print(i)


