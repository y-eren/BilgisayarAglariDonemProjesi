import matplotlib.pyplot as plt

abc = {
    600: 98.53333333333333,
    1200: 54.63333333333333,
    1800: 38.9,
    2400:30.0,
    3000: 20.7,
    3600:13.233333333333333
     
    
}


x = list(abc.keys())
y = list(abc.values())

plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', linestyle='-', color='g', label='PDR')
plt.xlabel('Period Sayısı')
plt.ylabel('Ortalama Gecikme Süresi (milisaniye)')
plt.title('Ortalama Gecikme Süresi')
for i, value in enumerate(y):
        plt.text(x[i], y[i], f'{value:.1f}', ha='center', va='bottom',fontsize=8)
plt.xticks(x) 
plt.grid(True)
plt.legend()
plt.show()
