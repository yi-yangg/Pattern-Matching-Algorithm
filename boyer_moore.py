LOWEST_ASCII = ord('!')
LARGEST_ASCII = ord('~')


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
    z_array[0] = None

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


def get_index_from_char(c: str) -> int:
    """
    Get the char index after offsetting with the lowest ascii value

    Parameters:
    c (str): Character to find index for

    Returns:
    int: Index representing the position of the char after offset

    Note:
    O(1) time complexity
    """
    return ord(c) - LOWEST_ASCII


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
    num_of_char = LARGEST_ASCII - LOWEST_ASCII
    ext_bad_char_arr = [[-1] * num_of_char]

    # Start from the second char of pat
    for i in range(1, len(pat)):
        bad_char_for_i = ext_bad_char_arr[i - 1].copy()
        # Set the position of the character in the previous location to the previous location
        bad_char_for_i[get_index_from_char(pat[i - 1])] = i - 1
        # Populate the 2-D bad character array
        ext_bad_char_arr.append(bad_char_for_i)

    return ext_bad_char_arr


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
    good_suffix = [-1] * (m + 1)

    # From first character to second last character (len(pat) - 2)
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
    """
    good_prefix = good_suffix(pat[::-1])
    return good_prefix[::-1]


if __name__ == "__main__":
    pat = "abacaba"
    print(good_suffix("acababacaba"))
