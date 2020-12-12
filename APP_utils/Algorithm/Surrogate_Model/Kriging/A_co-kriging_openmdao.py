from openmdao.surrogate_models.multifi_cokriging import MultiFiCoKriging
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
# Prediction on x=0.05
# print(np.abs(float(model.predict([0.05])[0]) - ((0.05 * 6 - 2) ** 2) * np.sin((0.05 * 6 - 2) * 2)) < 0.05)
print(model.y_std)
XE_PRED = np.linspace(0, 1).reshape(-1, 1)
y_pre_E = model.predict(XE_PRED)
# print(y_pre_E)
y_real = ((XE_PRED * 6 - 2) ** 2) * np.sin((XE_PRED * 6 - 2) * 2)
plt.plot(XE_PRED, y_real, color='#ff0000',
         label='co-Kriging low-high fidelity data interpolation curve',
         linestyle='--')
plt.plot(XE_PRED, y_pre_E[0], color='#000000',
         label='co-Kriging low-high fidelity data interpolation curve',
         linestyle='--')
plt.show()
