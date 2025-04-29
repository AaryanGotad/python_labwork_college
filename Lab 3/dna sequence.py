# This program stores a DNA Sequence and reverses it with & without the spaces and outputs on the terminal
# It also counts the number of times the sequence 'TTACT' occurred in both the reversed and original sequence of dna

try:

    # storing the sequence
    dna_sequence = 'ATGTACTC ATTCGTTTCG GAAGAGACAG GTACGTTAAT AGTTAATAGC GTACTTCTTT TTCTTGCTTT CGTGGTATTC TTGCTAGTTA CACTAGCCAT CCTTACTGCG CTTCGATTGT GTGCGTACTG CTGCAATATT GTTAACGTGA GTCTTGTAAA ACCTTCTTTT TACGTTTACT CTCGTGTTAA AAATCTGAAT TCTTCTAGAG TTCCTGATCT TCTGGTCTAA'
    
    # prints the original DNA Sequence and also the number of occurrences of 'TTACT' in it
    print()
    print(f"Original DNA Sequence : {dna_sequence}")
    print()

    print(f"Total occurrences of 'TTACT' in the given DNA Sequence: {dna_sequence.count('TTACT')}")
    print()

    # storing the reversed DNA Sequence preserving spaces and printing it
    reversed_dna_sequence_no_spaces = ''
    length = len(dna_sequence)

    for i in range(length - 1, -1, -1) :
        reversed_dna_sequence_no_spaces += dna_sequence[i]

    print(f"Reversed DNA Sequence (with spcaes): {reversed_dna_sequence_no_spaces}")
    print()

    # storing the reversed DNA Sequence not preserving spaces and printing it
    reversed_dna_sequence_spaces = ''
    for i in range(length - 1, -1, -1) :
        if not dna_sequence[i].isspace() :
            reversed_dna_sequence_spaces += dna_sequence[i]

    print(f"Reversed DNA Sequence (without spcaes): {reversed_dna_sequence_spaces}")
    print()

    # printing the number of occurrences of 'TTACT' in the reversed DNA Sequence
    print(f"Total occurrences of 'TTACT' in the reversed DNA Sequence: {reversed_dna_sequence_no_spaces.count('TTACT')}")
    print()

except Exception as e:
    print(f"An unexpected error '{e}' occurred while running the program. Exiting...")