import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)

# create some data to use for the plot
dt = 0.001
t = np.arange(0.0, 10.0, dt)
r = np.exp(-t[:1000] / 0.05)  # impulse response
x = np.random.randn(len(t))
s = np.convolve(x, r)[:len(x)] * dt  # colored noise

fig, main_ax = plt.subplots()
main_ax.plot(t, s)
main_ax.set_xlim(0, 1)
main_ax.set_ylim(1.1 * np.min(s), 2 * np.max(s))
main_ax.set_xlabel('time (s)')
main_ax.set_ylabel('current (nA)')
main_ax.set_title('Gaussian colored noise')

# this is an inset axes over the main axes
right_inset_ax = fig.add_axes([.65, .6, .2, .2], facecolor='k')
right_inset_ax.hist(s, 400, density=True)
right_inset_ax.set_title('Probability')
right_inset_ax.set_xticks([])
right_inset_ax.set_yticks([])

# this is another inset axes over the main axes
# left_inset_ax = fig.add_axes([.2, .6, .2, .2], facecolor='k')
left_inset_ax = fig.add_axes([.2, .6, .2, .2])
left_inset_ax.plot(t[:len(r)], r)
left_inset_ax.set_title('Impulse response')
left_inset_ax.set_xlim(0, 0.2)
left_inset_ax.set_xticks([])
left_inset_ax.set_yticks([])

plt.show()

# plt.figure(1)  # the test_first figure
# plt.subplot(211)  # the test_first subplot in the test_first figure
# plt.plot([1, 2, 3])
# plt.subplot(212)  # the test_second subplot in the test_first figure
# plt.plot([4, 5, 6])
#
# plt.figure(2)  # a test_second figure
# plt.plot([4, 5, 6])  # creates a subplot(111) by default
#
# plt.figure(1)  # figure 1 current; subplot(212) still current
# plt.subplot(211)  # make subplot(211) in figure1 current
# plt.title('Easy as 1, 2, 3')  # subplot 211 title
# plt.show()
mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)

# the histogram of the data
n, bins, patches = plt.hist(x, 50, density=1, facecolor='g', alpha=0.75)

plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.title(r'$\sigma_i=15$')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.show()
