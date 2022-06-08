import pylab
import lab_1_functions

window_length = 2

first_fasta_Record = lab_1_functions.open_FastaFile_and_return_Content_as_RecordObjekt("gi7305369.fasta")
second_fasta_Record = lab_1_functions.open_FastaFile_and_return_Content_as_RecordObjekt("gi12643549.fasta")

first_seq = lab_1_functions.get_seq_of(first_fasta_Record)
second_seq = lab_1_functions.get_seq_of(second_fasta_Record)

# Es wird eine Matrix "data" mit der Breite und Länge der 2 Sequenzen erstellt, Die matrix hat boolean Werte über die Übereinstimmungen. Window length bestimmt wieviele Übereinstimmungen übereinander folgen sollen, damit es als übereinstimmung gilt
data = lab_1_functions.make_intersection_Matrix_with_bool_Values_from(first_seq, second_seq, window_length)





# Plot Configuration
#pylab.gray()
pylab.imshow(data, cmap="PuBu", aspect="auto", )
pylab.xlim(0, 450)
pylab.ylim(0, 450)
pylab.xlabel("Datei : %s (length %i bp)" % (first_fasta_Record.id, len(first_fasta_Record)))
pylab.ylabel("Datei : %s (length %i bp)" % (second_fasta_Record.id, len(second_fasta_Record)))
pylab.title("Dot plot using window size %i" % window_length)
pylab.show()


