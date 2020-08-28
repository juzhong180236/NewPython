import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('statistic_char.csv',index_col=0)

fig, ax = plt.subplots()
#ax = plt.gca()
plt.plot(list(data.index),data)
plt.yticks(range(0,35000000,2000000))

fig.set_figwidth(15)
fig.tight_layout()
ax.set_xlim(-1,)
#ax.yaxis.set_ticks_position('left')
#ax.spines['left'].set_position(('data', 0))
plt.show()