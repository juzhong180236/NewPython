from openmdao.surrogate_models.multifi_cokriging import MultiFiCoKriging
from openmdao.surrogate_models.kriging import KrigingSurrogate
import numpy as np
import matplotlib.pyplot as plt

# Xe: DOE for expensive code (nested in Xc)
# Xc: DOE for cheap code
# ye: expensive response
# yc: cheap response
Xe = np.array([[0], [0.4], [0.6], [1]])
Xc = np.vstack((np.array([[0.1], [0.2], [0.3], [0.5], [0.7], [0.8], [0.9]]), Xe))
ye = ((Xe * 6 - 2) ** 2) * np.sin((Xe * 6 - 2) * 2)
yc = 0.5 * ((Xc * 6 - 2) ** 2) * np.sin((Xc * 6 - 2) * 2) + (Xc - 0.5) * 10. - 5
model = MultiFiCoKriging(theta0=1, thetaL=1e-5, thetaU=50.)
model.fit([Xc, Xe], [yc, ye])

model_low = KrigingSurrogate()
model_low.train(Xc, yc)

model_high = KrigingSurrogate()
model_high.train(Xe, ye)

# Prediction on x=0.05
# print(np.abs(float(model.predict([0.05])[0]) - ((0.05 * 6 - 2) ** 2) * np.sin((0.05 * 6 - 2) * 2)) < 0.05)
XE_PRED = np.linspace(0, 1).reshape(-1, 1)
y_pre_multi = model.predict(XE_PRED)
y_pre_low = model_low.predict(XE_PRED)
y_pre_high = model_high.predict(XE_PRED)

# print(y_pre_E)
y_real = ((XE_PRED * 6 - 2) ** 2) * np.sin((XE_PRED * 6 - 2) * 2)
y_real_low = 0.5 * ((XE_PRED * 6 - 2) ** 2) * np.sin((XE_PRED * 6 - 2) * 2) + (XE_PRED - 0.5) * 10. - 5

# 真实数据
plt.plot(XE_PRED, y_real, color='#ff7f0e',
         label='real data',
         linestyle='-.', lw=3)
# 变保真预测
plt.plot(XE_PRED, y_pre_multi[0], color='#0000ff',
         label='multi-fidelity predicted data',
         linestyle='-')
# 高保真预测
plt.plot(XE_PRED, y_pre_high, color='#000000',
         label='high fidelity predicted data',
         linestyle='--')
# 低保真预测
plt.plot(XE_PRED, y_pre_low, color='#1f77b4',
         label='low fidelity predicted data',
         linestyle='-.')
# 高保真观测点
plt.scatter(Xe, ye, color='#0000ff',
            label='high fidelity data points', marker='^')
# 低保真观测点
plt.scatter(Xc, yc, color='#00ff00',
            label='low fidelity data points', marker='s')
plt.legend()
plt.show()
