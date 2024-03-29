import sys
from tools import read_file, write_file

ASCII_SIZE = 128
NAN = -1


def z_algorithm(text: str) -> list[int]:
    """
    Applying Z algorithm to a string. Computes the Z array of a string
    efficiently and computes the Z array of a string and returns the 
    length of the longest substring that matches the prefix

    Parameters:
    text (str): String to perform z algorithm on

    Returns:
    list[int]: A list containing the length of longest match of 
               substring to prefix

    Note:
    - Z array is computed in linear time O(n) where n is the length of the text


    """
    # Left and right pointers of Z algorithm
    l = 0
    r = 0

    z_array = [0] * len(text)
    z_array[0] = NAN

    for i in range(1, len(text)):
        # If current iteration is inside rightmost Z box
        if i <= r:
            offset_i = i - l
            offset_i_zbox = z_array[offset_i]
            remaining_length = r - i + 1

            # If the offset z box is 0 then just skip
            if not offset_i_zbox:
                continue

            # Case 1: if offset Z box value < remaining length of current Z box
            if offset_i_zbox < remaining_length:
                # Set current Z box to the offset Z box value
                z_array[i] = offset_i_zbox
                continue
            # Case 2: if offset Z box value == remaining length of current Z box
            elif offset_i_zbox == remaining_length:
                # Set current Z box to offset Z box value
                z_array[i] = offset_i_zbox
                # Perform explicit comparison starting at r + 1, comparing with r + 1 - i

            # Case 3: if offset Z box value > remaining length
            else:
                # Set Z box value to length of remaining Z box, can't compare anymore
                z_array[i] = remaining_length
                continue

        # Explicitly comparing character from starting point to second last character in string
        for j in range(z_array[i], len(text) - 1):
            if (i + z_array[i] >= len(text)):
                break
            if (text[j] == text[i + z_array[i]]):
                z_array[i] += 1
            else:
                break

        # Calculate mismatch
        mismatch_point = i + z_array[i]
        # Update l and r if current iteration has a bigger rightmost box and z array value is not 0
        if z_array[i] and mismatch_point > r:
            r = mismatch_point - 1
            l = i

    return z_array


def extended_bad_char(pat: str) -> list[list[int]]:
    """
    Extended version of the bad character rule, using a 2-D array of |N| x m
    where N is the constant number of ASCII characters and m is the size of the
    pattern.
    For every character in the pattern, we copy the previous 1-D array of length |N| and
    change the corresponding character in the array to current index

    Parameters:
    pat (str): pattern to create extended bad character array for

    Returns:
    list[list[int]]: 2-D array of the left rightmost occurrence of each constant number of 
                     ASCII characters

    Note:
    - Complexity of O(m * |N|): m is the size of the pattern and |N| is the constant number
      of ASCII characters existing, however, since |N| is a constant size, we can omit treat
      it as constant time therefore O(m * 1) = O(m)
    """
    num_of_char = ASCII_SIZE
    ext_bad_char_arr = [[NAN] * num_of_char]

    # Start from the second char of pat
    for i in range(1, len(pat)):
        bad_char_for_i = ext_bad_char_arr[i - 1].copy()
        # Set the position of the character in the previous location to the previous location
        bad_char_for_i[ord(pat[i - 1])] = i - 1
        # Populate the 2-D bad character array
        ext_bad_char_arr.append(bad_char_for_i)

    return ext_bad_char_arr


def reversed_ext_bad_char(pat: str) -> list[int]:
    """
    Applying the reversed version of bad character, the suffix of a
    string is now the prefix, then reverse the reversed bad char arr
    back, since our pat will be matched in the normal direction.

    Parameters:
    pat (str): Pattern to apply reversed version of bad character

    Returns:
    list[int]: Bad character array with reversed index

    Note:
    - When accessing the bad char array with reversed index = len(pat) - 1 - bc[mismatch][char] - mismatch
    - Instead of mismatch - bc index, reverse does it by bc index - mismatch, since now we need the right-leftmost 
      occ of mismatch char instead of left-rightmost occ
    """
    reversed_bad_char_arr = extended_bad_char(pat[::-1])
    return reversed_bad_char_arr[::-1]


def good_suffix(pat: str) -> list[int]:
    """
    Applying the good suffix rule to the pattern where it will produce a 
    good suffix array which contains information on the longest substring 
    that matches the prefix

    Parameters:
    pat (str): Pattern string to apply good suffix on

    Returns:
    list[int]: A good suffix array

    Note:
    - Complexity of O(m) where m is the pattern size
    """
    # Pass reverse pattern into z algorithm to get z suffix array
    z_suffix_array = z_algorithm(pat[::-1])[::-1]
    m = len(pat)
    good_suffix = [NAN] * (m + 1)

    # From first character to second last character in pat
    for i in range(m - 1):

        j = m - z_suffix_array[i]
        good_suffix[j] = i

    return good_suffix


def reversed_good_suffix(pat: str) -> list[int]:
    """
    Applying good suffix on a reversed pattern. Essentially finding the good prefix
    of the pattern, then reverse and return the result. Will be used on the implementation
    of reversed Boyer Moore algorithm

    Parameters:
    pat (str): Pattern string to find good "prefix"

    Returns:
    list[int]: Reversed good "prefix" array

    Note:
    - When accessing the reversed good suffix array len(pat) - 1 - goodsuffix(mismatch - 1)
    """
    good_prefix = good_suffix(pat[::-1])
    return good_prefix[::-1]


def matched_prefix(pat: str) -> list[int]:
    """
    Applying matched prefix to pattern preprocessing, find the longest suffix that matches the
    prefix of pattern. The first index of the matched prefix array will always to the size of
    the string (prefix == suffix). Apply Z algorithm then checks if i + zbox == len(pat) if it is 
    then store the size of the zbox. Matched prefix array at k index contains the length of the longest
    suffix that matches the prefix of given pattern

    Parameter:
    pat (str): Pattern string to apply matched prefix on

    Returns:
    list[int]: A list of integer containing the length of the longest suffix that matches prefix

    Note:
    - Require O(m) time complexity. Applies Z algorithm which takes O(m) time and process the z array
      to obtain the matched prefix array O(m), O(m + m) = O(2m) = O(m)
    """
    # Apply Z algorithm
    z_matched_array = z_algorithm(pat)
    m = len(pat)

    # Create matched prefix array with m + 1 size, the m + 1 index stores the info on shift when
    # first index of pat unmatch with text
    matched_prefix_arr = [0] * (m+1)

    # Find the largest suffix that matches the prefix, loops from back to front, largest suffix will be on the left
    for i in range(m-1, -1, -1):
        # If the z box reaches the end of the string, meaning matched prefix
        if i + z_matched_array[i] == m:
            matched_prefix_arr[i] = z_matched_array[i]

        else:
            matched_prefix_arr[i] = matched_prefix_arr[i+1]

    # First index of matched prefix is always length of string
    matched_prefix_arr[0] = m

    return matched_prefix_arr


def reversed_matched_prefix(pat: str) -> list[int]:
    """
    Applying matched prefix rule in reversed. To be used in the reverse implementation
    of Boyer Moore. The suffix of the string is now the prefix, vice versa. Input the 
    reversed pattern into the original matched prefix function then reversed the output
    so that it matches the original pattern indexes

    Parameters:
    pat (str): Pattern string that reversed matched prefix is applied on

    Returns:
    list[int]: A list of int containing the largest suffix that matches prefix in the reversed direction

    Note:
    - When accessing reversed matched prefix array len(pat) - matchedprefix(mismatch)
    - Since matchedprefix is reversed when returned, m + 1 will now be 0, so if mismatch occurs at 
      position 0 then we want to take m + 1, thus matchedprefix(0)
    """
    reversed_mp_arr = matched_prefix(pat[::-1])
    return reversed_mp_arr[::-1]


def reversed_boyer_moore(text: str, pat: str) -> list[int]:
    """
    Applying a reversed version of Boyer Moore algorithm on a text and pattern. Similar to the
    regular Boyer Moore algorithm, but the reversed version starts from right and shifts to the
    left every iteration and scans on the pattern from left to right. The reversed version also
    included optimizations where it will avoid repeated comparison on text and pattern when a 
    bad character, good suffix or matched prefix shift happens, however, there are cases where
    the shifts doesn't give us enough information to guarantee optimization therefore explicit 
    comparison is still needed on those shifts

    Parameters:
    text (str): Text string to allow pattern to scan on
    pat (str): Pattern string that scans the text for occurrences

    Returns:
    list[int]: A list of integers that contains indices where pattern is found in text

    Note:
    - O(n) time complexity, since optimizations where considered and made sure that no repeated 
    comparisons are occuring
    """
    n = len(text)
    m = len(pat)

    bad_char_arr = reversed_ext_bad_char(pat)
    good_suffix_arr = reversed_good_suffix(pat)
    matched_prefix_arr = reversed_matched_prefix(pat)

    occurrence = []

    i = n - 1
    start = stop = NAN
    while True:
        # Get the index of the text relative to the left most index of pat
        search_index_on_text = i - (m - 1)
        # If the index is negative means that pattern exceeded the text
        if search_index_on_text < 0:
            break

        # Set text and pattern pointer
        pattern_pointer = 0

        # Loop to check pattern with text and perform shifts
        while True:
            if pattern_pointer == start:
                pattern_pointer = stop + 1

            if pattern_pointer == m:
                occurrence.append(search_index_on_text + 1)
                shift_amt = m - matched_prefix_arr[-2]

                # Optimization for matched prefix, if there's a matched prefix then optimize
                if matched_prefix_arr[-2] != 0:
                    start = shift_amt
                    stop = m - 1
                else:
                    start = stop = NAN

                # Perform shift
                i -= shift_amt
                break

            # If the text and pat char is the same then check next char in pat and text
            if text[search_index_on_text + pattern_pointer] == pat[pattern_pointer]:
                pattern_pointer += 1
                continue

            else:
                # If not the same perform shifts
                # Char mismatch in text
                char_mismatch = text[search_index_on_text + pattern_pointer]
                # Get left-rightmost mismatch character from bad character array
                bc_index = bad_char_arr[pattern_pointer][ord(char_mismatch)]
                # Calculate bad character shift, using length of pat to minus bc_index to reverse index
                bc_shift = m - 1 - bc_index - pattern_pointer

                # Good suffix and matched prefix array follows 1 based indexing, since the m + 1 index is now 0 index
                if good_suffix_arr[pattern_pointer] == NAN:
                    # Use matched prefix when good suffix is None
                    gs_shift = m - matched_prefix_arr[pattern_pointer]
                else:
                    gs_shift = m - 1 - good_suffix_arr[pattern_pointer]

                shift_amt = max(bc_shift, gs_shift)

                # Optimization
                # If my prefix length == 0 and the shift amount is the same for bc and gs then choose bc shift
                if (pattern_pointer - 1 == NAN and bc_shift == gs_shift) or bc_shift > gs_shift:
                    # If the bad character index is NAN then reset start, stop. Cant optimize
                    if bc_index == NAN:
                        start = stop = NAN
                    else:
                        start = stop = m - 1 - bc_index

                # Choosing good suffix shift, if prefix length before mismatch != 0 then optimization can be applied
                elif pattern_pointer - 1 != NAN:
                    # Match prefix shift is used, set start to gs shift value and stop to end of string
                    if good_suffix_arr[pattern_pointer] == NAN:
                        start = gs_shift
                        stop = m - 1
                    # Good suffix shift is used, set start to gs shift value and stop to start + length of good "prefix"
                    else:
                        start = gs_shift
                        stop = start + pattern_pointer - 1
                        # If shift for bc and gs are the same then we optimize the bad character by adding 1
                        # This only happens when gs and bs are side by side so we can optimize the bc as well
                        if bc_shift == gs_shift:
                            stop += 1
                else:
                    start = stop = NAN
                # Perform shift
                i -= shift_amt
                break
    return occurrence


if __name__ == "__main__":
    _, text_file, pat_file = sys.argv

    text = read_file(text_file)
    pat = read_file(pat_file)
    result = reversed_boyer_moore(text, pat)

    result_str = "\n".join(map(str, result))

    output_file = "output_boyer_moore.txt"
    write_file(output_file, result_str)
