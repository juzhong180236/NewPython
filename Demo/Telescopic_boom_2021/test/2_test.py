FREECAD_PATH = r'D:\Alai\code_Alai\DT_Project\Telescopic_Boom_Project\ZLG_CLOUD_DATA_C#_FILE_SAVEDATA\ZLG_CLOUD_DATA\bin\Debug\2021年7月12日01.txt'
infile = open(FREECAD_PATH, 'rt')
list_ = []
i = 0
for line in infile:
    list_everyline = line.split()
    i += 1
    if list_everyline[2] == "98ff4427":
        list_.append(i)
print(list_)
print(list_[-1])
print(i)
for _i, num in enumerate(list_):
    if _i < len(list_) - 1:
        if list_[_i + 1] - num > 8:
            print(list_[_i + 1], " ", num)
            print("dsadfads")
            continue
