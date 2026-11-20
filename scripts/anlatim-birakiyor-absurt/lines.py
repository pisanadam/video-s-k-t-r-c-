NAMES=['Hocanın sandalyesi','Otobüs durağı','Piknik','Oyun koltuğu','Okul merdiveni']
C=[["Teneffüs. Sınıf bomboş.","Bıraktı ve gitti.","Hoca geldi...","Ama kaka ayağa kalktı.","Kaka artık öğretmen. Hoca öğrenci."],
["Durakta kimse yok.","Bıraktı, otobüse atladı.","Geç kalan yolcu koşuyor...","Belediye başkanı geldi.","Kaka tarihi eser ilan edildi."],
["Piknik örtüsü hazır.","Bıraktı, ıslık çalarak gitti.","Mehmet sepetle geldi...","Mehmet mum dikti.","Kakanın yaş günü kutlandı."],
["Ali mutfakta.","Bıraktı, pencereden çıktı.","Ali geri geldi, oturdu...","Kaka modu yüklendi.","Ali'nin FPS'i dokuzbin oldu."],
["Teneffüs bitti.","Bıraktı, ıslık çalarak indi.","Müdür telefonla iniyor...","Müdür kaydı...","Strike! Üçyüz puan."]]
L=[(0.3,"Abdullah sıçıp bırakıyor, iki. Bu sefer olaylar kontrolden çıktı.")]
for n in range(5):
    cs=3.2+n*14.2; vs=cs+2.2
    L.append((cs+.3,f"Senaryo {['bir','iki','üç','dört','beş'][n]}. {NAMES[n]}."))
    for k,off in enumerate([.3,3.9,5.6,7.8,9.35 if n==4 else 9.9]): L.append((vs+off,C[n][k]))
L.append((74.5,"Bırakılan kaka: beş. Abdullah yine yakalanmadı."))
