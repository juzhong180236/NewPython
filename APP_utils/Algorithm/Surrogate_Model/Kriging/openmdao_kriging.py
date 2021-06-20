from openmdao.surrogate_models.kriging import KrigingSurrogate
import numpy as np
import matplotlib.pyplot as plt
import json

# Xe: DOE for expensive code (nested in Xc)
# Xc: DOE for cheap code
# ye: expensive response
# yc: cheap response

# Xc = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]).reshape(-1, 1)
Xc = np.array([0, 0.3, 0.4, 0.5, 0.6, 0.9, 1]).reshape(-1, 1)

yc = 0.5 * ((Xc * 6 - 2) ** 2) * np.sin((Xc * 6 - 2) * 2) + (Xc - 0.5) * 10. - 5
model = KrigingSurrogate()
model.train(Xc, yc)
# print(model.thetas)
# print(model.X_mean)
# print(model.X_std)
# print(model.n_samples)
# print(model.X)
# print(model.alpha)
# print(model.Y_mean)
# print(model.Y_std)
dict_kriging_model = {}
dict_kriging_model["thetas"] = model.thetas.tolist()
dict_kriging_model["X_mean"] = model.X_mean.tolist()
dict_kriging_model["X_std"] = model.X_std.tolist()
dict_kriging_model["n_samples"] = model.n_samples
dict_kriging_model["X"] = model.X.tolist()
dict_kriging_model["alpha"] = model.alpha.tolist()
dict_kriging_model["Y_mean"] = model.Y_mean.tolist()
dict_kriging_model["Y_std"] = model.Y_std.tolist()
print(dict_kriging_model)
json_kriging_model = json.dumps(dict_kriging_model)
with open(r"C:\Users\asus\Desktop\json_test.json", "w") as f:
    json.dump(json_kriging_model, f)
XE_PRED = np.linspace(0, 1).reshape(-1, 1)
test_a = 0.5

y_pre_E = model.predict(XE_PRED)
# print(y_pre_E)
y_real = 0.5 * ((XE_PRED * 6 - 2) ** 2) * np.sin((XE_PRED * 6 - 2) * 2) + (XE_PRED - 0.5) * 10. - 5
plt.plot(XE_PRED, y_real, color='#ff0000',
         label='real data curve',
         linestyle='-')
plt.plot(XE_PRED, y_pre_E, color='#000000',
         label='Kriging interpolation curve',
         linestyle='-')
plt.scatter(Xc, yc)
plt.legend()
plt.show()
