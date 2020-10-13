import numpy as np

# numpy.random.randint
a = np.random.randint(2, size=10)
b = np.random.randint(1, size=10)
c = np.random.randint(-2, 2, size=10)
print(a, b, c)

# numpy.random.rand
# numpy.random.randn

a1 = np.random.rand(3, 2)
b1 = np.random.randn(3, 2)
print(a1, b1)

# numpy.random.random_integers [弃用]
a2 = np.random.random_integers(1, 2, size=10)
print(a2)

# numpy.random.choice
a3 = np.random.choice(5, 3)
print(a3)

# numpy.random.seed
np.random.seed(0)
a4 = np.random.randn(5)
np.random.seed(0)
a5 = np.random.randn(5)

print(a4)
print(a5)
