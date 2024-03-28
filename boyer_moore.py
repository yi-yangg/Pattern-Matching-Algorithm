LOWEST_ASCII = ord('!')
LARGEST_ASCII = ord('~')
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
    ext_bad_char_arr = [[NAN] * num_of_char]

    # Start from the second char of pat
    for i in range(1, len(pat)):
        bad_char_for_i = ext_bad_char_arr[i - 1].copy()
        # Set the position of the character in the previous location to the previous location
        bad_char_for_i[get_index_from_char(pat[i - 1])] = i - 1
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
    - When accessing the bad char array with reversed index len(pat) - 1 - bc[row][char]
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
    Require O(m) time complexity. Applies Z algorithm which takes O(m) time and process the z array
    to obtain the matched prefix array O(m), O(m + m) = O(2m) = O(m)
    """
    # Apply Z algorithm
    z_matched_array = z_algorithm(pat)
    m = len(pat)

    # Create matched prefix array with m + 1 size, the m + 1 index stores the info on shift when
    # first index of pat unmatch with text
    matched_prefix_arr = [-1] * (m+1)

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
    """
    reversed_mp_arr = matched_prefix(pat[::-1])
    return reversed_mp_arr[::-1]


if __name__ == "__main__":
    pat = "abacaba"
    print(matched_prefix("acababacaba"[::-1])[::-1])
