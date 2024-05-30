import matplotlib.pyplot as plt

# Veriler
abc = {
    600: 94.48066,
    1200: 96.90525000000002,
    1800: 97.57737666666667,
    2400: 98.23415000000001,
    3000: 98.39595666666669,
    3600: 98.95819666666668
}


x = list(abc.keys())
y = list(abc.values())

plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', linestyle='-', color='g', label='PDR')
plt.xlabel('Period Sayısı')
plt.ylabel('Packet Delivery Rate')
plt.title('Packet Delivery Rate (PDR) Metrigi')
for i, value in enumerate(y):
        plt.text(x[i], y[i], f'{value:.1f}', ha='center', va='bottom',fontsize=8)
plt.xticks(x) 
plt.grid(True)
plt.legend()
plt.show()
