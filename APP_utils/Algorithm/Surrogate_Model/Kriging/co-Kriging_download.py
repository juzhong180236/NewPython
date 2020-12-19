import numpy as np
import matplotlib.pyplot as plt
from smt.applications import MFK

A_value = 0.8
B_value = 20
C_value = -5


# Define the
def LF_function(x, A=A_value, B=B_value, C=C_value):
    return A * HF_function(x) + B * (x - 0.5) + C


def HF_function(x):
    return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


# Problem set up
ndim = 1
Xt_e = np.linspace(0, 1, 4).reshape(-1, ndim)
Xt_c = np.linspace(0, 1, 11).reshape(-1, ndim)

nt_exp = Xt_e.shape[0]
nt_cheap = Xt_c.shape[0]

# Evaluate the HF and LF functions
yt_e = HF_function(Xt_e)
yt_c = LF_function(Xt_c)

sm = MFK(theta0=np.array(Xt_e.shape[1] * [1.0]), print_global=False)

print(Xt_e.shape[1] * [1.0])

# low-fidelity dataset names being integers from 0 to level-1
sm.set_training_values(Xt_c, yt_c, name=0)
print(Xt_c)
# high-fidelity dataset without name
sm.set_training_values(Xt_e, yt_e)
print(Xt_e)

# train the model
sm.train()

x = np.linspace(0, 1, 101, endpoint=True).reshape(-1, 1)

# query the outputs
y = sm.predict_values(x)
MSE = sm.predict_variances(x)
der = sm.predict_derivatives(x, kx=0)

plt.figure()

plt.plot(x, HF_function(x), label="reference")
plt.plot(x, y, linestyle="-.", label="mean_gp")
plt.scatter(Xt_e, yt_e, marker="o", color="k", label="HF doe")
plt.scatter(Xt_c, yt_c, marker="*", color="g", label="LF doe")

plt.legend(loc=0)
plt.ylim(-10, 17)
plt.xlim(-0.1, 1.1)
plt.xlabel(r"$x$")
plt.ylabel(r"$y$")

plt.show()
