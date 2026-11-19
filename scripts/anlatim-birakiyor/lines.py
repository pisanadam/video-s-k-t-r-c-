NAMES=['Hocanın sandalyesi','Otobüs durağı','Piknik','Oyun koltuğu','Okul merdiveni']
C=[["Teneffüs. Sınıf bomboş.","Bıraktı ve gitti.","Zil çaldı. Hoca geldi...","Hoca oturdu."],
["Durakta kimse yok.","Bıraktı, otobüse atladı.","Geç kalan yolcu koşuyor...","Yolcu kaydı. Otobüs gitti."],
["Piknik örtüsü hazır.","Bıraktı, ıslık çalarak gitti.","Mehmet sepetle geldi...","Mehmet puding sandı. Yemedi."],
["Ali mutfakta.","Bıraktı, pencereden çıktı.","Ali geri geldi...","Koltuk artık kahverengi edisyon."],
["Teneffüs bitti.","Bıraktı, ıslık çalarak indi.","Müdür telefonla konuşarak iniyor...","Müdür merdivenden kızak gibi kaydı."]]
L=[(0.3,"Abdullah sıçıp bırakıyor. Nereye bastığına dikkat et.")]
for n in range(5):
    cs=3.2+n*12.7; vs=cs+2.2
    L.append((cs+.3,f"Senaryo {['bir','iki','üç','dört','beş'][n]}. {NAMES[n]}."))
    for k,off in enumerate([.3,3.9,5.6,8.3]): L.append((vs+off,C[n][k]))
L.append((66.9,"Bırakılan kaka: beş. Abdullah bugün de yakalanmadı."))
