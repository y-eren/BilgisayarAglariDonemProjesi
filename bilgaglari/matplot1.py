import os
import re
import matplotlib.pyplot as plt
import numpy as np

def extract_gecikme_from_file(file):
    gecikme_value = None
    for line in file:
        gecikme_match = re.search(r'Gecikme:\s*\**(\d+\.?\d*)\** saniye', line)
        if gecikme_match:
            gecikme_value = float(gecikme_match.group(1))
            break  # Sadece ilk gecikme değerini al ve döngüyü sonlandır
    return gecikme_value

def get_gecikme_values(directory):
    all_gecikme_values = []

    for i in range(1, 31):
        subdir = os.path.join(directory, f'run{i}')
        log_file_path = os.path.join(subdir, 'log.txt')
        
        if os.path.isfile(log_file_path):
            print(f"Processing {log_file_path}")  # Dosyanın işleme alındığını gösterir
            with open(log_file_path, 'r') as file:
                gecikme = extract_gecikme_from_file(file)
                if gecikme is not None:
                    all_gecikme_values.append(gecikme)
                else:
                    print(f"No valid gecikme found in {log_file_path}")
        else:
            print(f"File not found: {log_file_path}")

    return all_gecikme_values

def plot_gecikme_values(gecikme_values):
    plt.figure(figsize=(12, 6))
    x = list(range(1, len(gecikme_values) + 1))  
    y = gecikme_values 

    plt.plot(x, y, marker='o', linestyle='-', color='g', label='Gecikme')
    plt.xlabel('Çalışma Sayısı')
    plt.ylabel('Gecikme Süresi (milisaniye)')
    plt.title('Gecikme Süresi Grafiği')
    plt.xticks(x)  
    plt.grid(True)

    # Y ekseninin sınırlarını belirleme
    y_min = min(gecikme_values)
    y_max = max(gecikme_values)
    y_padding = 0.05 * (y_max - y_min)  # 5% padding
    plt.ylim(y_min - y_padding, y_max + y_padding)

    # Y ekseninin değerlerini belirleme
    y_tick_min = int(y_min - y_padding)
    y_tick_max = int(y_max + y_padding)
    plt.yticks(np.arange(y_tick_min, y_tick_max, 1000))  

    plt.legend()
    plt.show()

root_directory_path = "C:\\Users\\Dell\\Desktop\\period_600"
gecikme_values = get_gecikme_values(root_directory_path)
plot_gecikme_values(gecikme_values)


