# DayDayUp
def dayUP(df):
    dayup = 1.0
    for i in range(365):
        if i % 7 in [0, 6]:
            dayup *= 1 - 0.01
        else:
            dayup *= 1 + df
    print(dayup)
    return dayup


dayfactor = 0.01
while dayUP(dayfactor) < 37.78:
    dayfactor += 0.001
print('小明工作日的进步百分比应该是:{:,.3f}'.format(dayfactor))
