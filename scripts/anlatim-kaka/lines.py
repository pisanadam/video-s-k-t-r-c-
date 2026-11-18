NAMES=['Yazılı sınav','Arızalı tuvalet','Bahçe','Sifon','Kamp']
C=[["Yazılı sınavın tam ortası.","Hocam, tuvalete gidebilir miyim? Hayır.","Abdullah dayanıyor... dayanıyor...","Hoca: Tamam git. Abdullah: Artık gerek yok."],
["Sokakta acil durum!","Tek umut, kamu tuvaleti.","Kapıda yazıyor: arızalı.","Belediyeye şikâyet edildi."],
["Bahçede, ağacın arkasında...","Kimse görmüyor sanıyor.","Ama creeper görüyor.","Bahçe gübrelendi. Çiçekler açtı."],
["Evde, nihayet tuvalet.","Abdullah sifonu çekti...","Sifon geri tepti!","Tesisatçı çağrıldı. Gelen kim? Hoca."],
["Kamp gecesi. Tuvalet kâğıdı bitti.","Abdullah bir yaprak buldu.","Yumuşacık görünüyor...","Isırgan otuymuş!"]]
L=[(0.3,"Abdullah her yerde osurup sıçıyor. Bu sefer daha kötü.")]
for n in range(5):
    cs=3.2+n*12.7; vs=cs+2.2
    L.append((cs+.3,f"Senaryo {['bir','iki','üç','dört','beş'][n]}. {NAMES[n]}."))
    for k,off in enumerate([.3,2.6,5.0,8.3]): L.append((vs+off,C[n][k]))
L.append((66.9,"Kaka sayacı beş. Abdullah'tan uzak durun."))
