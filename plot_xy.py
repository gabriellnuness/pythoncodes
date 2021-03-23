import pandas as pd
import matplotlib.pyplot as plt


path = 'D:/Users/Stinky/downloads'

data = pd.read_excel('D:\\Users\\Stinky\\Downloads\\DataFile#49.xlsx')

x = data[data.columns[20]]
y = data[data.columns[22]]



plt.plot(x, y, color=[0.3, 0.3, 0.3])
plt.grid(which='minor', alpha=0.2)
plt.grid(which='major', alpha=0.5)
plt.xlabel('Frequência [MHz]')
plt.ylabel('Impedâancia [$\Omega$]')


plt.show()