#import pycon as pycon
from Bio import SeqIO

with open("gi7305369.fasta") as in_handle:
    record_iterator = SeqIO.parse(in_handle, "fasta")
    rec_one = next(record_iterator)

with open("gi12643549.fasta") as in_handle:
    record_iterator = SeqIO.parse(in_handle, "fasta")
    rec_two = next(record_iterator)

window = 15
dict_one = {}
dict_two = {}
for (seq, section_dict) in [
    (rec_one.seq.upper(), dict_one),
    (rec_two.seq.upper(), dict_two),
]:
    for i in range(len(seq) - window):
        section = seq[i : i + window]
        try:
            section_dict[section].append(i)
        except KeyError:
            section_dict[section] = [i]
# Now find any sub-sequences found in both sequences
matches = set(dict_one).intersection(dict_two)
print("%i unique matches" % len(matches))
#In order to use the pylab.scatter() we need separate lists for the x and y co-ordinates:

# Create lists of x and y co-ordinates for scatter plot
x = []
y = []
for section in matches:
    for i in dict_one[section]:
        for j in dict_two[section]:
            x.append(i)
            y.append(j)
#We are now ready to draw the revised dot plot as a scatter plot:

import pylab

pylab.cla()  # clear any prior graph
pylab.gray()
pylab.scatter(x, y)
pylab.xlim(0, len(rec_one) - window)
pylab.ylim(0, len(rec_two) - window)
pylab.xlabel("Datei: %s (length %i bp)" % (rec_one.id, len(rec_one)))
pylab.ylabel("Datei: %s (length %i bp)" % (rec_two.id, len(rec_two)))
pylab.title("Dot plot using window size %i" % window)
pylab.show()