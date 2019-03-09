# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random
import numbers

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# global variables:
shifts = []
# -----------------------------------


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable

# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
    ### TODO.
	
    assert isinstance(shift, numbers.Integral), 'shift is not an integer'

    coder = {}

    chars_lower = ' ' + string.ascii_lowercase
    chars_upper = ' ' + string.ascii_uppercase
    
    for pos in range(len(chars_upper)):
        new_pos = (pos + shift) % 27
        coder[chars_upper[pos]] = chars_upper[new_pos]
    for pos in range(len(chars_lower)):
        new_pos = (pos + shift) % 27
        coder[chars_lower[pos]] = chars_lower[new_pos]
    return coder 

def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ### TODO.
    d = build_coder(shift)
    return d

def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ### TODO.
    coder = build_coder(shift)
    decoder = {}
    for k,v in coder.iteritems():
        decoder[v] = k
    return decoder

def apply_coder(text, shift):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    shift: amount to shift letters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    ### TODO.
    coder = build_coder(shift)
    coded_txt = ''
    for char in text:
        if char in coder:
            coded_txt += coder[char]
        else:
            coded_txt += char	
    return coded_txt
	
def apply_decoder(text, shift):
    """
    Applies the decoder to the text. Returns the decoded text.

    text: string (coded text)
    shift: amount to shift letters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_shift("Hello, world!", 3)
    'Khoor,czruog!'
    >>> apply_decoder("Khoor,czruog!", 3)
    'Hello, world!'
    """    
    decoder = build_decoder(shift)
    decoded_txt = ''
    for char in text:
        if char in decoder:
            decoded_txt += decoder[char]
        else:
            decoded_txt += char	
    return decoded_txt

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    ### TODO.
    return apply_coder(text, shift)

def apply_decode_shift(text, shift):
    """
    Given a encoded text, returns decoded text by given shift offset.
    """	
    return apply_decoder(text, shift)

#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: encoded string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """
    ### TODO
    matches = []
	# checks if encoded test is a single word
    if len(text) < 14: # longest word in wordlist has 13 characters
        for shift in range(27):
            sample = apply_decoder(text, shift)
            space_index = sample.find(' ')
            if space_index == -1:
                if is_word(wordlist, sample):
                    best_shift = shift
                    return best_shift			
    
	# looking for best shift assuming encoded text include more than one word
	for shift in range(27):
            counter = 0
            sample = apply_decoder(text, shift)
            temp = sample.split()
        for word in temp:
            if is_word(wordlist, word):
                counter += 1
        matches.append(counter)
    best_shift = matches.index(max(matches))
    return best_shift
	
#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to 
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.  
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """
    ### TODO.
	assert shifts, 'no tuple (position, shift) in the shifts'
	
    for i in range(len(shifts)):
        shifted_txt = text[:shifts[i][0]] + apply_shift(text[shifts[i][0]:], shifts[i][1])        
        text = shifted_txt
    return shifted_txt

def apply_decode_shifts(text, shifts):
    """
    Applies a sequence of shifts to an encoded text.
    """
    for i in range(len(shifts)):
        de_shifted_txt = text[:shifts[i][0]] + apply_decode_shift(text[shifts[i][0]:], shifts[i][1])        
        text = de_shifted_txt
    return de_shifted_txt

#
# Problem 4: Multi-level decryption.
#
def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """

def find_best_shifts_rec(wordlist, text, start = 0):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """
    global shifts

    for shift in range(27):
        # print '-----------------------------------------------'
        # print 'start', start
        # print 'shift:', shift
        # print 'shifts:', shifts
        # print 'text at the entrance:  ', text        
        sample  = apply_decoder(text, shift)
        space_index = sample.find(' ', start)
        # print 'sample at the entrance:', sample
		
		# if no spaces from the start till the end of the sample, checks if it is a valid word
		# and if it is valid word it means it is the end of text and we can return shifts
        if space_index == -1:
            # print 'NO spaces text'
            # print 'NO spaces check sample[start:]', sample[start:]
            # print 'len(sample[start:]):', len(sample[start:])
            if is_word(wordlist, sample[start:]):
                # print 'NO spaces word is valid'
                if shift != 0:
                    shifts.append((start, shift))
                return shifts
                    
		# if there is a space in the sample, checks if first word is valid
        # if the word is valid and shift != 0 it adds tuple to the shifts
        if space_index != -1:
            # print 'text with spaces'
            # print 'sample[start:space_index]:', sample[start:space_index]
            if is_word(wordlist, sample[start:space_index]):
                if shift != 0:
                    shifts.append((start, shift))
                    # print 'appending tuple for word', (start, shift), sample[start:space_index]                
                
				# if lenght of word + start index == lenght of text it means it is last word
                length_of_word = start + len(sample[start:space_index])
                # print 'len(text):', len(text)
                # print 'length_of_word:', length_of_word
                if length_of_word == len(text):
                    return shifts
                else:
                    new_start = space_index + 1
                    # print 'new_start:', new_start					
                    # print 'sample[new_start:] out:', sample[new_start:]
                    # print '***************'
                    result = find_best_shifts_rec(wordlist, sample, new_start)                 				
                    # print 'XXXXXXXXXXXXresultXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:', result
                    if result == None:
						# if result == None means it has not reached last word
						# checks and removes if improper tuple already has been added to the shifts
						# it continues with the next shift from the last start
                        if shifts:
                            last_shift = shifts[-1]
                            # print 'last_shift:', last_shift
                            # print 'last_shift[0]:', last_shift[0]
                            # print 'start:', start						
                            if last_shift[0] == start:
                                shifts.pop()
                        continue
                    else:
                        return result


def decrypt_fable():
    """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
    ### TODO.

    encoded_fable = get_fable_string()
    best_shifts = find_best_shifts_rec(wordlist, encoded_fable)
    decoded_fable = apply_decode_shifts(encoded_fable, best_shifts)
    f = open('decoded_fable.txt', 'w')
    f.write(decoded_fable)
    f.close()
    print 'The fable has been decoded and written to the "{:s}" file'.format(f.name)
	

decrypt_fable()
 
#What is the moral of the story?

"""
An Ingenious Man who had built a flying machine invited a great concourse of people to see it go up.
at the appointed moment, everything being ready, he boarded the car and turned a a he power.
the machine immediately broke through the massive substructure upon which it was builded, and sank out of sight into the earth,
the aeronaut springing out barely in time to save himself. "well," said he, "i have done enough to demonstrate the correctness of my details.
the defects," he added, with a add hat the ruined brick work, "are merely basic and fundamental."
upon this assurance the people came ox ward with subscriptions to build a second machine
"""
#The moral of the story is - Never, ever give up! ;)

