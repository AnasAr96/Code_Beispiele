from enum import IntEnum
import numpy as np


# setzte die scores
class Score(IntEnum):
    MATCH = 1
    MISMATCH = -2
    GAP = -1


# erstelle ein Enum für die Nachbar elemente eines Element
class Trace(IntEnum):
    STOP = 0
    LEFT = 1
    UP = 2
    DIAGONAL = 3


#lese die Fasta datein
def fasta_reader(sequence_file):
    lines = open(sequence_file).readlines()
    sequence_name_row = lines[0][1:]
    sequence = lines[1]
    return sequence_name_row.replace(" ", "").strip(), sequence.strip()



def smith_waterman(seq1, seq2):
    # generiere eine leere Matrix
    zeile = len(seq1) + 1
    cspalte = len(seq2) + 1
    matrix = np.zeros(shape=(zeile, cspalte), dtype=np.int64)
    tracing_matrix = np.zeros(shape=(zeile, cspalte), dtype=np.int64)

    # installiere die Variablen um die höchsten score zu finder
    max_score = -1
    max_index = (-1, -1)

    # Calculating the scores for all cells in the matrix
    #calculiere den score für alle werte in der matrix
    for i in range(1, zeile):
        for j in range(1, cspalte):
            # calculiete den diagonalen score
            match_value = Score.MATCH if seq1[i - 1] == seq2[j - 1] else Score.MISMATCH
            diagonal_score = matrix[i - 1, j - 1] + match_value

            # calculiere den  verticalen gap score
            vertical_score = matrix[i - 1, j] + Score.GAP

            # calculiere den horizontalen gap score
            horizontal_score = matrix[i, j - 1] + Score.GAP

            # finde den höchsten score
            matrix[i, j] = max(0, diagonal_score, vertical_score, horizontal_score)

            # finde raus wo der Zellwert herkommt
            if matrix[i, j] == 0:
                tracing_matrix[i, j] = Trace.STOP

            elif matrix[i, j] == horizontal_score:
                tracing_matrix[i, j] = Trace.LEFT

            elif matrix[i, j] == vertical_score:
                tracing_matrix[i, j] = Trace.UP

            elif matrix[i, j] == diagonal_score:
                tracing_matrix[i, j] = Trace.DIAGONAL

                # Tracking the cell with the maximum score
            if matrix[i, j] >= max_score:
                max_index = (i, j)
                max_score = matrix[i, j]

    # Initialisierung der Variablen für die Rückverfolgung
    aligned_seq1 = ""
    aligned_seq2 = ""
    current_aligned_seq1 = ""
    current_aligned_seq2 = ""
    (max_i, max_j) = max_index

    #Verfolgen und Berechnen des Weges mit der lokalen Ausrichtung
    while tracing_matrix[max_i, max_j] != Trace.STOP:
        if tracing_matrix[max_i, max_j] == Trace.DIAGONAL:
            current_aligned_seq1 = seq1[max_i - 1]
            current_aligned_seq2 = seq2[max_j - 1]
            max_i = max_i - 1
            max_j = max_j - 1

        elif tracing_matrix[max_i, max_j] == Trace.UP:
            current_aligned_seq1 = seq1[max_i - 1]
            current_aligned_seq2 = '-'
            max_i = max_i - 1

        elif tracing_matrix[max_i, max_j] == Trace.LEFT:
            current_aligned_seq1 = '-'
            current_aligned_seq2 = seq2[max_j - 1]
            max_j = max_j - 1

        aligned_seq1 = aligned_seq1 + current_aligned_seq1
        aligned_seq2 = aligned_seq2 + current_aligned_seq2

    # Reversing the order of the sequences
    aligned_seq1 = aligned_seq1[::-1]
    aligned_seq2 = aligned_seq2[::-1]

    return aligned_seq1, aligned_seq2


if __name__ == "__main__":
    # lese die Datein
    file_1_name, file_1 = fasta_reader("lambda_ref.fasta")
    file_2_name, file_2 = fasta_reader("reads.fasta")

    #führe den Alghorithmus aus
    output_1, output_2 = smith_waterman(file_1, file_2)

    print(  output_1 + '\n'  + output_2)


