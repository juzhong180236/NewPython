# a = {1, 2, 3, 4, 5, 6}
# b = {4, 5, 6, 7, 8, 9}
# print((a | b) - (a & b))

print("欢迎来到快递系统！")
# input默认接收的是字符串形式
while True:
    weight = int(input("请输入重量（千克）："))
    num_address = input("请输入地址编号（01.其他 02.东三省 03.新疆 04.国外）：")

    p = 0
    if weight >= 3:
        if num_address == '01':
            p = 8 + 5 * (weight - 3)
        elif num_address == '02':
            p = 10 + 10 * (weight - 3)
        elif num_address == '03':
            p = 20 + 20 * (weight - 3)
        elif num_address == '04':
            p = 'error'
        else:
            print("输入错误")
    elif 0 < weight < 3:
        if num_address == '01':
            p = 8
        elif num_address == '02':
            p = 10
        elif num_address == '03':
            p = 20
        elif num_address == '04':
            p = 100
        else:
            print("输入错误")
    else:
        print("输入错误")

    print('您好，包裹价格为,', p, '元')
