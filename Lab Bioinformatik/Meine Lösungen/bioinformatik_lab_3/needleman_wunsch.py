from Bio import SeqIO


with open("lambda_ref.fasta") as in_handle:
    record_iterator = SeqIO.parse(in_handle, "fasta")
    seq_one = next(record_iterator).seq

with open("reads.fasta") as in_handle:
    record_iterator = SeqIO.parse(in_handle, "fasta")
    seq_two = next(record_iterator).seq














# wie man eine Matrix erstellt
matrix = []
# befüllt zeile 0
matrix.append([1, 3, 5, 7])
# befüllt zeile 1
matrix.append([2, 3, 4, 5])
# befüllt zeile 2
matrix.append([5, 2, 20, 3])


def print_matrix(mat):
    #schleife über die zeilen
    for i in range(0, len(mat)):
        print("[", end = "")
        # schleife über die spalten
        for j in range(0, len(mat[i])):
            print(mat[i][j], end = "")
            #schreibe eine tap zwischen den Zahlen
            if j != len(mat[i]) - 1:
                print("\t", end = "")
        print("]\n")


# To retrieve the value from the 2nd row, in the 0th column, is relatively simple:
print("The value in the 2nd row and the 0th column is:", matrix[2][0])

# das Format ist immer  my_matrix[teile][Spalte].


# Use these values to calculate scores
gap_penalty = -1
match_award = 1
mismatch_penalty = -1


# erstmal erstellen wir eine Matrix aus Nullen
def nMatrix(zeile, spalte):
    # eine leere Liste
    retval = []
    for x in range(zeile):
        # für jede zeile addieren wir eine leehre liste
        retval.append([])
        # dann die spalten
        for y in range(spalte):
            # addiere eine null zu an jeder stelle
            retval[-1].append(0)
    #returne die null matrix
    return retval

# eine Funktion um den score zwischen zwei basen in dem Alignment zu rechnen
def match_score(b1, b2):
    if b1 == b2:
        return match_award
    elif b1 == '-' or b2 == '-':
        return gap_penalty
    else:
        return mismatch_penalty


def needleman_wunsch(seq1, seq2):
    #speichere die länge der seq
    n = len(seq1)
    m = len(seq2)

    #erstelle eine null matrix
    score = nMatrix(m + 1, n + 1)


    # befülle die erste Spalte
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i

    #befülle die erste Reihe
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j

    # nun befülle die matrix mit den restwerten
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # rechne den Score nach needleman_wunsch (Nachbarn: links , Oben , Diagonal)
            match = score[i - 1][j - 1] + match_score(seq1[j - 1], seq2[i - 1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            # scheibe den grösten score in das nächste Feld
            score[i][j] = max(match, delete, insert)


    align1 = ""
    align2 = ""

    #wir starten in der Matrix von unten links
    i = m
    j = n

    #wir gehen die Matrix rückwerts durch
    while i > 0 and j > 0:
        score_aktuell = score[i][j]
        score_diagonal = score[i - 1][j - 1]
        score_oben = score[i][j - 1]
        score_links = score[i - 1][j]

        # wir suchen die Zelle, aus der der aktuelle Score erstellt ist
        # dann aktualisiere j i um den index auf die richtige Zelle zu setzen
        if score_aktuell == score_diagonal + match_score(seq1[j - 1], seq2[i - 1]):
            align1 += seq1[j - 1]
            align2 += seq2[i - 1]
            i -= 1
            j -= 1
        elif score_aktuell == score_oben + gap_penalty:
            align1 += seq1[j - 1]
            align2 += '-'
            j -= 1
        elif score_aktuell == score_links + gap_penalty:
            align1 += '-'
            align2 += seq2[i - 1]
            i -= 1

    # Beenden wir die Verfolgung bis zur oberen linken Zelle
    while j > 0:
        align1 += seq1[j - 1]
        align2 += '-'
        j -= 1
    while i > 0:
        align1 += '-'
        align2 += seq2[i - 1]
        i -= 1

    # Da wir die Matrix von unten rechts durchlaufen haben, werden unsere beiden Sequenzen umgekehrt sein.
    # Diese beiden Zeilen kehren die Reihenfolge der Zeichen in jeder Sequenz um.

    align1 = align1[::-1]
    align2 = align2[::-1]

    return (align1, align2)

refernce, alignment = needleman_wunsch("AAGGCCTTTTTAAACG", "TTAAACGACG")
print(refernce + "\n" + alignment)

refernce, alignment = needleman_wunsch(seq_one[0:200], seq_two[0:200])

# Das Richtige alignment, braucht ewig !!!
#refernce, alignment = needleman_wunsch(seq_one, seq_two)

print(refernce + "\n" + alignment)


