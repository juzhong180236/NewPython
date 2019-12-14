def colorStep(array_ele, list_min_ele, pressureStep, i):
    if i == 0:
        return array_ele < list_min_ele + pressureStep * (i + 1)
    else:
        return list_min_ele + pressureStep * i <= array_ele < list_min_ele + pressureStep * (i + 1)


def define_Color(array_ele, list_min_ele, pressureStep):
    if colorStep(array_ele, list_min_ele, pressureStep, 0):
        colors = '0,0,1'
    elif colorStep(array_ele, list_min_ele, pressureStep, 1):
        colors = '0,' + str(42 / 255) + ',1'
    elif colorStep(array_ele, list_min_ele, pressureStep, 2):
        colors = '0,' + str(85 / 255) + ',1'
    elif colorStep(array_ele, list_min_ele, pressureStep, 3):
        colors = '0,' + str(127 / 255) + ',1'
    elif colorStep(array_ele, list_min_ele, pressureStep, 4):
        colors = '0,' + str(170 / 255) + ',1'
    elif colorStep(array_ele, list_min_ele, pressureStep, 5):
        colors = '0,1,1'
    elif colorStep(array_ele, list_min_ele, pressureStep, 6):
        colors = '0,1,' + str(170 / 255)
    elif colorStep(array_ele, list_min_ele, pressureStep, 7):
        colors = '0,1,' + str(127 / 255)
    elif colorStep(array_ele, list_min_ele, pressureStep, 8):
        colors = '0,1,' + str(85 / 255)
    elif colorStep(array_ele, list_min_ele, pressureStep, 9):
        colors = '0,1,' + str(42 / 255)
    elif colorStep(array_ele, list_min_ele, pressureStep, 10):
        colors = '0,1,0'
    elif colorStep(array_ele, list_min_ele, pressureStep, 11):
        colors = str(42 / 255) + ',1,0'
    elif colorStep(array_ele, list_min_ele, pressureStep, 12):
        colors = str(85 / 255) + ',1,0'
    elif colorStep(array_ele, list_min_ele, pressureStep, 13):
        colors = str(127 / 255) + ',1,0'
    elif colorStep(array_ele, list_min_ele, pressureStep, 14):
        colors = str(170 / 255) + ',1,0'
    elif colorStep(array_ele, list_min_ele, pressureStep, 15):
        colors = '1,1,0'
    elif colorStep(array_ele, list_min_ele, pressureStep, 16):
        colors = '1,' + str(170 / 255) + ',0'
    elif colorStep(array_ele, list_min_ele, pressureStep, 17):
        colors = '1,' + str(127 / 255) + ',0'
    elif colorStep(array_ele, list_min_ele, pressureStep, 18):
        colors = '1,' + str(85 / 255) + ',0'
    elif colorStep(array_ele, list_min_ele, pressureStep, 19):
        colors = '1,' + str(42 / 255) + ',0'
    elif colorStep(array_ele, list_min_ele, pressureStep, 20):
        colors = '1,0,0'
    else:
        colors = '1,0,0'
    return colors
