NAMES=['Market','Kütüphane','Spor salonu','Okul servisi','Otopark']
C=[[(.3,"Market. Üçüncü reyon."),(3.0,"Kamera her şeyi kaydetti."),(5.0,"Abdullah tuvalet kağıtlarının altında."),(7.6,"Bir teyze arabayı alıp gitti."),(10.0,"Kaçtı.")],
[(.3,"Kütüphane. Sessizlik."),(3.4,"Kütüphaneci gördü!"),(4.6,"Ama kütüphanede bağırmak yasak."),(7.8,"Parmak ucunda..."),(10.0,"Sessizce kaçtı.")],
[(.3,"Beden dersi."),(3.5,"Düdük!"),(4.3,"Abdullah halata tırmanıyor."),(6.0,"Beden hocası tırmanamadı."),(7.6,"Pencereden çıktı. Kaçtı.")],
[(.3,"Okul servisi. Sabah yedikırk."),(3.4,"Şoför dikiz aynasından gördü!"),(5.4,"Acil çıkış kapısı..."),(7.4,"Atladı. Kaçtı.")],
[(.3,"Okul otoparkı."),(3.3,"Alarm!"),(4.2,"Müdür koşuyor."),(6.0,"Abdullah bisikletle kaçtı."),(7.4,"Müdür ise... bastı.")]]
L=[(0.3,"Abdullah yakalandı. Ama hep kaçtı.")]
for n in range(5):
    cs=3.2+n*14.2; vs=cs+2.2
    L.append((cs+.3,f"Senaryo {['bir','iki','üç','dört','beş'][n]}. {NAMES[n]}."))
    for off,tx in C[n]: L.append((vs+off,tx))
L.append((74.5,"Final."))
B=76.4
for off,tx in [(.3,"Birleşmiş Milletler acil toplandı."),(2.6,"Karar: Abdullah aranacak."),(4.2,"Arama ekibi sahada."),(6.5,"Bulundu! Çember daralıyor..."),(8.0,"Ama Abdullah osurdu."),(11.8,"Uzaya kadar."),(13.6,"Aşağı baktı..."),(15.0,"Ve bıraktı."),(17.0,"Arama ekibi yukarı baktı..."),(18.6,"Tam isabet."),(20.0,"Birleşmiş Milletler sıfır, Abdullah bir.")]: L.append((B+off,tx))
L.append((98.6,"Abdullah hâlâ uzayda."))
