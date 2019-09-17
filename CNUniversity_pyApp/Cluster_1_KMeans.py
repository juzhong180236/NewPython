import numpy as np
from sklearn.cluster import KMeans


def loadData(filePath):
    fr = open(filePath, 'r+')
    lines = fr.readlines()
    retData = []
    retCityName = []
    for line in lines:
        items = line.strip().split(",")
        retCityName.append(items[0])
        retData.append([float(items[i]) for i in range(1, len(items))])
    return retData, retCityName


print(__name__)
if __name__ == '__main__':  # “Make a script both importable and executable” 意思就是说让你写的脚本模块既可以导入到别的模块中用，另外该模块自己也可执行。
    data, cityName = loadData('city.txt')
    km = KMeans(n_clusters=7)
    label = km.fit_predict(data)
    expenses = np.sum(km.cluster_centers_, axis=1)
    # print(expenses)
    CityCluster = [[], [], [], [], [], [], []]
    for i in range(len(cityName)):
        CityCluster[label[i]].append(cityName[i])
    for i in range(len(CityCluster)):
        print("Expenses:%.2f" % expenses[i])
        print(CityCluster[i])
