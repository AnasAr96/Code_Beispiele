from Bio import SeqIO


def open_FastaFile_and_return_Content_as_RecordObjekt(fastaFileName):
    with open(fastaFileName) as in_handle:
        record_iterator = SeqIO.parse(in_handle, "fasta")
        rec_one = next(record_iterator)
    return rec_one


def get_seq_of(fasta_Record):
    return fasta_Record.seq.upper()


def make_intersection_Matrix_with_bool_Values_from(first_seq, second_seq, window_length):
    return [
        [
            (first_seq[i: i + window_length] != second_seq[j: j + window_length])
            for j in range(len(first_seq) - window_length)
        ]
        for i in range(len(second_seq) - window_length)
    ]
