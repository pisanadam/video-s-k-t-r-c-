NAMES=['Asansör','Hediye kutusu','Müdürün ayakkabısı','Fotokopi makinesi','Vantilatör']
C=[["Asansör. Abdullah tek başına.","Bıraktı, üçüncü katta indi.","İkinci kat: kimse binmedi.","Müdür bindi. Telefonda.","Dokuzuncu kata kadar yalnız kaldı."],
["Mehmet'in doğum günü.","Bıraktı, paketledi, hediye etti.","Mehmet hediyeye bayıldı...","Mehmet hiçbir şey demedi.","Paketi kapatıp hocaya hediye etti."],
["Öğretmenler odasının kapısı.","Müdürün ayakkabısına bıraktı.","Müdür telefonla çıktı...","Müdür fark etmedi.","Yeni halıya onüç iz bıraktı."],
["Teneffüs. Fotokopi makinesi boş.","Bıraktı, kapağı kapattı.","Hoca sınav kağıdını getirdi...","Yüz kopya.","Hepsinde kaka var. Sınav iptal."],
["Sınav günü. Koridor sessiz.","Bıraktı, vantilatörü açtı.","Koku koridora yayılıyor...","Yangın alarmı!","Okul tahliye edildi. Sınav ertelendi."]]
L=[(0.3,"Abdullah sıçıp bırakıyor, iki. Beş yeni yer.")]
for n in range(5):
    cs=3.2+n*14.2; vs=cs+2.2
    L.append((cs+.3,f"Senaryo {['bir','iki','üç','dört','beş'][n]}. {NAMES[n]}."))
    for k,off in enumerate([.3,3.9,5.6,7.7 if n==4 else 7.8,9.9]): L.append((vs+off,C[n][k]))
L.append((74.5,"Bırakılan kaka: beş. Abdullah yine yakalanmadı."))
