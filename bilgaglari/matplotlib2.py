
import os
import re
import matplotlib.pyplot as plt

def extract_pdr_from_file(file):
    for line in file:
        gecikme_match = re.search(r'Gecikme:\s*(\d+\.\d+)', line)
        if gecikme_match:
            return float(gecikme_match.group(1))
    return None

def get_gecikme_values(directory):
   
    gecikme_values = []

    for i in range(1, 31): 
        subdir = os.path.join(directory, f'run{i}')
        log_file_path = os.path.join(subdir, 'log.txt')
        
        if os.path.isfile(log_file_path):
            with open(log_file_path, 'r') as file:
                gecikme = extract_pdr_from_file(file)
                if gecikme is not None:
                    gecikme_values.append(gecikme)
                else:
                    gecikme_values.append(0)  
        else:
            gecikme_values.append(0)  

    return gecikme_values

def plot_gecikme_values(gecikme_values):
    
    x = list(range(1, 31))  
    y = gecikme_values  

    plt.figure(figsize=(12, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='g', label='Gecikme')
    plt.xlabel('Çalışma Sayısı')
    plt.ylabel('Gecikme suresi milisaniye')
    plt.title('Gecikme Süresi Metrigi ')
    plt.xticks(x)  
    plt.ylim(0, 110) 
    for i, value in enumerate(y):
        plt.text(x[i], y[i], f'{value:.1f}', ha='center', va='bottom',fontsize=8)
    plt.grid(True)
    plt.legend()
    plt.show()

root_directory_path = "C:\\Users\\Dell\\Desktop\\period_600"  
gecikme_values = get_gecikme_values(root_directory_path)
plot_gecikme_values(gecikme_values)