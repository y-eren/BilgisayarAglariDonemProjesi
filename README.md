# Bilgisayar Ağları Dönem Projesi
Proje kapsamında kablosuz haberleşme teknolojilerinden bir tanesi olan LoraWAN modülünün performansının hareketlilikten nasıl etkilendiği incelenmiştir. Performans metrikleri olarak PDR(packet delivery rate) ve gecikme değerleri belirlenmiş olup ölçümler bu metriklere göre yapılmıştır. 

# Ana Özellikler 
Proje içerisinde SUMO uygulaması ile gerçekçi bir trafik senaryosu oluşturulmuş ve bu senaryo üzerinde LoraWAN teknolojisinin hareketlilikten nasıl etkilendiği değerlendirilmiştir. Gerçekçi trafik senaryosu oluşturulduktan sonra NS2 uyumlu hareket dosyası oluşturulmuş ve NS3 üzerinde kodlar yazılmıştır. Bu kodlar belirli bir betik üzerinde performans metriğinin istatiki açıdan daha gerçekçi olması için 30 kere farklı periyot değerleri için çalıştırılmış ve daha sonra çıktılar rahat gözlem yapabilmek için görselleştirilmiştir. 

# Örnek bir kod NS3 kodu
![image](https://github.com/y-eren/BilgisayarAglariDonemProjesi/assets/84980503/9b603bc5-ccd9-4d53-8291-3346fe0676d6)

# Deney sonucu PDR metriğinin period sayısına göre görselleştirilmesi

![ORTALAMAPDR](https://github.com/y-eren/BilgisayarAglariDonemProjesi/assets/84980503/64895a01-2b1d-474b-8607-5719d006dc45)


# Deney sonucu ortalama gecikme metriğinin period sayısına göre görselleştirilmesi 
![ORTALAMAGECİKME](https://github.com/y-eren/BilgisayarAglariDonemProjesi/assets/84980503/a7a99dd9-c433-4158-b1d2-fe90b5f3374b)


# Sonuç

Sonuç olarak kısa period aralıklarının genellikle daha düşük PDR'ye yol açtığı
periyotların değişmesinin ağ gecikmesi üzerinde belirgin bir etkiye sahip olduğunun anlaşılması,
Gateway ve düğümler arasındaki uzaklığın ağ gecikmesini etkileyen önemli faktörlerden bir tanesi olduğu incelenmiştir.
