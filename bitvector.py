from bitarray import *
import sys
from tools import read_file, write_file


def bitvector_pat_match(text: str, pat: str) -> list[int]:
    """
    Using bitvectors and bit operations like left shifts and bitwise OR 
    to perform exact pattern matching on text with pattern

    Parameters:
    text (str): Text string to perform pattern matching on
    pat (str): Pattern string to be used to pattern match in text

    Returns:
    list[int]: A list of integers that states the occurrence of the pattern
    """
    m = len(pat)
    n = len(text)
    # Initialize bit array and set all to 1, at -1 index the string is unmatched in all positions
    bitvector = bitarray(m)
    bitvector.setall(1)

    # Initialize delta bit array
    delta = bitarray(m)

    occurrences = []

    # For each of the characters in the text
    for i in range(n):
        # Populate delta by comparing each char in pattern with the current char in text
        for j in range(m):
            delta[j] = text[i] != pat[m-1-j]

        # Perform bitwise operations using previous bitvector and current delta bit array
        bitvector = (bitvector << 1) | delta

        # Check if the first bit array is 0, if it is then it means theres a match
        if not bitvector[0]:
            # Append the position where the match was found
            occurrences.append((i + 1) - m + 1)

    return occurrences


if __name__ == "__main__":
    _, text_file, pat_file = sys.argv

    text = read_file(text_file)
    pat = read_file(pat_file)
    result = bitvector_pat_match(text, pat)

    result_str = "\n".join(map(str, result))

    output_file = "output_bitvector.txt"
    write_file(output_file, result_str)
