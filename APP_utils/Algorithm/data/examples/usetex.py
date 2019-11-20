from matplotlib import rc
import numpy as np
import matplotlib.pyplot as plt

# np.random.seed(19680801)
#
# # create some data to use for the plot
# dt = 0.001
# t = np.arange(0.0, 10.0, dt)
# r = np.exp(-t[:1000] / 0.05)  # impulse response
# x = np.random.randn(len(t))
# s = np.convolve(x, r)[:len(x)] * dt  # colored noise

fig, main_ax = plt.subplots()
# main_ax.plot(t, s)

main_ax.text(5, 25, r'$\alpha_i > \beta_i$')
main_ax.text(10, 25, r'$\sum_{i=0}^\infty x_i$')
main_ax.text(15, 25, r'$\frac{3}{4} \binom{3}{4} \genfrac{}{}{0}{}{3}{4}$')
main_ax.text(20, 25, r'$\frac{5 - \frac{1}{x}}{4}$')
main_ax.text(25, 25, r'$(\frac{5 - \frac{1}{x}}{4})$')
main_ax.text(30, 25, r'$\sqrt{2}$')
main_ax.text(35, 25, r'$\sqrt[3]{x}$')
main_ax.text(5, 30, r'$s(t) = \mathcal{A}\/\sin(2 \omega t)$')
main_ax.text(5, 35, r'$s(t) = \mathcal{A}\mathrm{sin}(2 \omega t)$')

# main_ax.text(5, 40, ur'$\u23ce$')
plt.axis([0, 50, 0, 50])

# rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
## for Palatino and other serif fonts use:
# rc('font',**{'family':'serif','serif':['Palatino']})
# rc('text', usetex=True)
# plt.show()


t = np.arange(0.0, 30, 0.1)
s = 25 * np.cos(0.1 * np.pi * t) + 25
main_ax.plot(t, s, lw=2)

main_ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 )

# plt.ylim(-2, 2)
plt.show()
