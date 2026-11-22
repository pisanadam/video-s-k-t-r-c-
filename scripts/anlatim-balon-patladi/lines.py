N=['bir','iki','üç','dört','beş','altı']; NM=['Sınıf','Doğum günü','Asansör','Park','Lunapark','Dev balon']
C=[[(.3,"Abdullah balonun üstüne oturdu."),(2.0,"Biraz sıkıştı..."),(3.2,"Osuruk!"),(5.4,"Hoca silah sesi sandı."),(7.6,"Hoca masanın altında.")],
[(.1,"Mehmet'in doğum günü. Abdullah balon şişiriyor."),(2.8,"Osuruk!"),(5.0,"Yeşil balon hazır."),(6.3,"Mum..."),(7.6,"Doğum günü: osuruk aromalı.")],
[(.3,"Asansör. Onbeş balon. Bir Abdullah."),(3.3,"Osuruk!"),(5.1,"Zincirleme patlama."),(7.6,"Sıfır balon hayatta kaldı.")],
[(.3,"Abdullah balonlarla uçuyor."),(2.0,"Daha yükseğe çıkmak için..."),(3.6,"Osuruk!"),(5.4,"Ağaç."),(6.3,"İniş..."),(7.6,"Gölet.")],
[(.3,"Lunapark. Üç dart, sıfır isabet."),(3.0,"Sonra..."),(3.6,"Osuruk!"),(5.4,"Yirmidört balonun hepsi patladı."),(7.6,"Ödül: dev ayıcık.")],
[(.3,"Ve final: dev balon."),(1.5,"Osuruk!"),(4.4,"Abdullah okulun üstünde uçuyor."),(6.8,"Bayrak direği..."),(9.4,"Okul üç gün tatil.")]]
L=[(0.3,"Abdullah'ın balonları patladı. Altı senaryo.")]
for n in range(6):
    cs=3.2+n*12.2; vs=cs+2.2
    L.append((cs+.3,f"Senaryo {N[n]}. {NM[n]}."))
    for off,tx in C[n]: L.append((vs+off,tx))
L.append((78.7,"Patlayan balon: elliiki. Osuruk: altı."))
