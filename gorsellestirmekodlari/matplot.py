import os
import re
import matplotlib.pyplot as plt

def extract_pdr_from_file(file):
    
    for line in file:
        pdr_match = re.search(r'Packet Delivery Rate:\s*(\d+\.\d+)', line)
        if pdr_match:
            return float(pdr_match.group(1))
    return None

def get_pdr_values(directory):
   
    pdr_values = []

    for i in range(1, 31): 
        subdir = os.path.join(directory, f'run{i}')
        log_file_path = os.path.join(subdir, 'log.txt')
        
        if os.path.isfile(log_file_path):
            with open(log_file_path, 'r') as file:
                pdr = extract_pdr_from_file(file)
                if pdr is not None:
                    pdr_values.append(pdr)
                else:
                    pdr_values.append(0)  
        else:
            pdr_values.append(0)  

    return pdr_values

def plot_pdr_values(pdr_values):
    
    x = list(range(1, 31))  
    y = pdr_values  

    plt.figure(figsize=(12, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='g', label='PDR')
    plt.xlabel('Çalışma Sayısı')
    plt.ylabel('Packet Delivery Rate')
    plt.title('Packet Delivery Rate (PDR) Metrigi ')
    plt.xticks(x)  
    plt.ylim(95, 100) 
    # plt.yticks(range(98, 99,2)) 
    plt.grid(True)
    plt.legend()
    plt.show()

root_directory_path = "C:\\Users\\Dell\\Desktop\\period_1800"  
pdr_values = get_pdr_values(root_directory_path)
plot_pdr_values(pdr_values)
