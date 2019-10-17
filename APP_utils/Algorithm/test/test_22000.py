# def RBF_result(x, c, s):
#     return np.exp(-(x - c) ** 2 / (2 * s ** 2))
#
# d=[1,2,3,4,5,6,7,8,8]
# start = time.perf_counter()
# rbfnet_y = RBFNet()
# wb_y = rbfnet_y.fit(d, y_real)
#
# plt.plot(X, list_F, color='#0000ff', marker='+', linestyle='-', label='predict')
# plt.tight_layout()
# plt.show()
# elapsed = (time.perf_counter() - start)
# print("Time used:", elapsed)

a = ['c,d,as,f,ds', 'f,d,b,vf,d']
b = [ele.split(',') for ele in a]
c = a[:]
c.reverse()
for i in range(len(a)):
    a[i].split(",")
print(c)
print(a)
print(b)
d = ','.join(a).split(',')
print(d)
print(float(1.3908832e-002))


