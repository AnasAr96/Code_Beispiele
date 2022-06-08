import random
import matplotlib.pyplot as plt

basen = ["A", "C", "G", "T"]
#markov-ketten 0.Ordnung
sequenzen = ''.join(random.choices(basen, weights=(400, 100, 100, 400), k=1000))



#die Anzah jeder Base
a = sequenzen.count("A")
c = sequenzen.count("C")
g = sequenzen.count("G")
t = sequenzen.count("T")

xWerte = ["A","C","G","T"] #ausgabe der verteilung der Basen
yWerte = [a,c,g,t]
plt.bar(xWerte,yWerte)
plt.xlabel("Basen")
plt.ylabel("Anzahl Basen in der Sequenz")
plt.show()

#zählen der 2-mere
aa = sequenzen.count("AA")
ac = sequenzen.count("AC")
at = sequenzen.count("AT")
ag = sequenzen.count("AG")

ca = sequenzen.count("CA")
cc = sequenzen.count("CC")
ct = sequenzen.count("CT")
cg = sequenzen.count("CG")

ta = sequenzen.count("TA")
tc = sequenzen.count("TC")
tt = sequenzen.count("TT")
tg = sequenzen.count("TG")

ga = sequenzen.count("GA")
gc = sequenzen.count("GC")
gt = sequenzen.count("GT")
gg = sequenzen.count("GG")


#Plotten der  verteilung der 2-mere
xValues = ["AA","AC","AT","AG","CC","CA","CT","CG","TT","TC","TA","TG","GA","GC","GT","GG"]
yValues = [aa/1000,ac/1000,at/1000,ag/1000,cc/1000,ca/1000,ct/1000,cg/1000,tt/1000,tc/1000,ta/1000,tg/1000,ga/1000,gc/1000,gt/1000,gg/1000]
plt.bar(xValues,yValues)
plt.xlabel("2er Segment")
plt.ylabel("Wahrscheinlichkeit")
plt.show()

