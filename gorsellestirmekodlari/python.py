import os
import re

def extract_values_from_file(file):
    ranX, ranY, ranZ = None, None, None
    gonderilen_paket, ulasan_paket, kaybolan_paket, packet_delivery_rate, gecikme, ort_gecikme = None, None, None, None, None, None

    for line in file:
        if ranX is None:
            ranX_match = re.search(r'ranX:\s*(\d+)', line)
            if ranX_match:
                ranX = int(ranX_match.group(1))
        
        if ranY is None:
            ranY_match = re.search(r'ranY:\s*(\d+)', line)
            if ranY_match:
                ranY = int(ranY_match.group(1))

        if ranZ is None:
            ranZ_match = re.search(r'ranZ:\s*(\d+)', line)
            if ranZ_match:
                ranZ = int(ranZ_match.group(1))
        
        if gonderilen_paket is None:
            gonderilen_paket_match = re.search(r'Gonderilen Paket:\s*(\d+)', line)
            if gonderilen_paket_match:
                gonderilen_paket = int(gonderilen_paket_match.group(1))
        
        if ulasan_paket is None:
            ulasan_paket_match = re.search(r'Ulasan Paket\s*:\s*(\d+)', line)
            if ulasan_paket_match:
                ulasan_paket = int(ulasan_paket_match.group(1))
        
        if kaybolan_paket is None:
            kaybolan_paket_match = re.search(r'Kaybolan Paket:\s*(\d+)', line)
            if kaybolan_paket_match:
                kaybolan_paket = int(kaybolan_paket_match.group(1))

        if packet_delivery_rate is None:
            packet_delivery_rate_match = re.search(r'Packet Delivery Rate:\s*(\d+\.\d+)', line)
            if packet_delivery_rate_match:
                packet_delivery_rate = float(packet_delivery_rate_match.group(1))

        if gecikme is None:
            gecikme_match = re.search(r'Gecikme:\s*(\d+)', line)
            if gecikme_match:
                gecikme = int(gecikme_match.group(1))
        
        if ort_gecikme is None:
            ort_gecikme_match = re.search(r'Ortalama Gecikme:\s*(\d+)', line)
            if ort_gecikme_match:
                ort_gecikme = int(ort_gecikme_match.group(1))

        if (ranX is not None and ranY is not None and ranZ is not None and 
            gonderilen_paket is not None and ulasan_paket is not None and 
            kaybolan_paket is not None and packet_delivery_rate is not None and 
            gecikme is not None and ort_gecikme is not None):
            return ranX, ranY, ranZ, gonderilen_paket, ulasan_paket, kaybolan_paket, packet_delivery_rate, gecikme, ort_gecikme

    return None

def calculate_averages(directory):
    total_ranX = total_ranY = total_ranZ = 0
    total_gonderilen_paket = total_ulasan_paket = total_kaybolan_paket = 0
    total_packet_delivery_rate = 0.0
    total_gecikme = total_ort_gecikme = 0
    file_count = 0

    for i in range(1, 31):  
        subdir = os.path.join(directory, f'run{i}')
        log_file_path = os.path.join(subdir, 'log.txt')
        
        if os.path.isfile(log_file_path):
            with open(log_file_path, 'r') as file:
                values = extract_values_from_file(file)
                if values:
                    (ranX, ranY, ranZ, gonderilen_paket, ulasan_paket, 
                     kaybolan_paket, packet_delivery_rate, gecikme, ort_gecikme) = values
                    total_ranX += ranX
                    total_ranY += ranY
                    total_ranZ += ranZ
                    total_gonderilen_paket += gonderilen_paket
                    total_ulasan_paket += ulasan_paket
                    total_kaybolan_paket += kaybolan_paket
                    total_packet_delivery_rate += packet_delivery_rate
                    total_gecikme += gecikme
                    total_ort_gecikme += ort_gecikme
                    file_count += 1

    if file_count == 0:
        return None

    average_ranX = total_ranX / file_count
    average_ranY = total_ranY / file_count
    average_ranZ = total_ranZ / file_count
    average_gonderilen_paket = total_gonderilen_paket / file_count
    average_ulasan_paket = total_ulasan_paket / file_count
    average_kaybolan_paket = total_kaybolan_paket / file_count
    average_packet_delivery_rate = total_packet_delivery_rate / file_count
    average_gecikme = total_gecikme / file_count
    average_ort_gecikme = total_ort_gecikme / file_count

    return (average_ranX, average_ranY, average_ranZ, average_gonderilen_paket,
            average_ulasan_paket, average_kaybolan_paket, average_packet_delivery_rate, average_gecikme, average_ort_gecikme)

root_directory_path = "C:\\Users\\Dell\\Desktop\\period_600"  
averages = calculate_averages(root_directory_path)

if averages:
    (average_ranX, average_ranY, average_ranZ, average_gonderilen_paket, average_ulasan_paket, average_kaybolan_paket, 
     average_packet_delivery_rate, average_gecikme, average_ort_gecikme) = averages
    
    print(f"Ortalama ranX: {average_ranX}")
    print(f"Ortalama ranY: {average_ranY}")
    print(f"Ortalama ranZ: {average_ranZ}")
    print(f"Ortalama Gönderilen Paket: {average_gonderilen_paket}")
    print(f"Ortalama Ulaşan Paket: {average_ulasan_paket}")
    print(f"Ortalama Kaybolan Paket: {average_kaybolan_paket}")
    print(f"Ortalama Packet Delivery Rate: {average_packet_delivery_rate}")
    print(f"Ortalama Gecikme: {average_gecikme}")
    print(f"Ortalama Ortalama Gecikme: {average_ort_gecikme}")
else:
    print("No valid data found in the files.")
