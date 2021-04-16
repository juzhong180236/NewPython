string = r'D:\Alai\ansys_Alai\Telescopic Boom\70_files\dp0\SYS-75\MECH\file'
list_1 = []
for i_str in range(0, len(string), 8):
    print("path_read_" + str(int(i_str / 8)) + "='" + string[i_str:i_str + 8] + "'")
    list_1.append("path_read_" + str(int(i_str / 8)))
print('%' + '%%'.join(list_1) + '%%path_read_8%')
