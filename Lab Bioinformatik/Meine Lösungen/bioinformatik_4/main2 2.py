import random
import matplotlib.pyplot as plt

bases = ["A","C","G","T"]
#markov-ketten 1.Ordnung
buchstabe = random.choices(bases, weights=(0.2875, 0.2125, 0.2875, 0.2125)) #wahrscheinlichkeiten ergeben sich durch das addieren der einzelnen Spaltung und einer Teilung durch 4
sequence = ''.join(buchstabe)

i = 1
while i < 1000 :
    matching = buchstabe[0]

    if matching == 'A':
        weights = (0.6,0.1,0.1,0.2)
    elif matching == 'C':
        weights = (0.1, 0.5, 0.3, 0.1)
    elif matching ==  'G':
        weights = (0.05, 0.2, 0.7, 0.05)
    elif matching ==  'T':
        weights = (0.4,0.05,0.05,0.5)

    buchstabe = random.choices(bases, weights)
    sequence = sequence + buchstabe[0]
    i = i+1

#Anzahl der  Basen
a = sequence.count("A")
c = sequence.count("C")
g = sequence.count("G")
t = sequence.count("T")

xWerte = ["A", "C", "G", "T"] #ausgabe der verteilung der Basen
yWerte = [a, c, g, t]
plt.bar(xWerte, yWerte)
plt.xlabel("Basen")
plt.ylabel("Anzahl der Basen in der Sequence")
plt.show()

#zählen der 2-Segmente
aa = sequence.count("AA")
ac = sequence.count("AC")
at = sequence.count("AT")
ag = sequence.count("AG")

ca = sequence.count("CA")
cc = sequence.count("CC")
ct = sequence.count("CT")
cg = sequence.count("CG")

ta = sequence.count("TA")
tc = sequence.count("TC")
tt = sequence.count("TT")
tg = sequence.count("TG")

ga = sequence.count("GA")
gc = sequence.count("GC")
gt = sequence.count("GT")
gg = sequence.count("GG")
#ausgabe der  verteilung der 2-Segmente
xwert = ["AA","AC","AT","AG","CC","CA","CT","CG","TT","TC","TA","TG","GA","GC","GT","GG"]
ywert = [aa/1000,ac/1000,at/1000,ag/1000,cc/1000,ca/1000,ct/1000,cg/1000,tt/1000,tc/1000,ta/1000,tg/1000,ga/1000,gc/1000,gt/1000,gg/1000]
plt.bar(xwert,ywert)
plt.xlabel("2-mere")
plt.ylabel("Wahrscheinlichkeit")
plt.show()

