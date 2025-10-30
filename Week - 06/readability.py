def count_letters(text):
    """
    Returns the number of alphabetic characters (a-z, A-Z) in the text.
    """
    return sum(c.isalpha() for c in text)

def count_words(text):
    """
    Returns the number of words in the text.

    """
    words = text.split()
    return len(words)

def count_sentences(text):
    """
    Returns the number of sentences in the text, counted by the
    presence of common terminal punctuation (. ! ?).
    """
    sentence_count = 0

    for char in text:
        if char in ['.', '!', '?']:
            sentence_count += 1

    return sentence_count

def calculate_grade(text):
    """Calculates and prints the Coleman-Liau index grade."""

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    #check if words is zero to prevent DivisionByZeroError
    if words == 0:
        return "Text is empty or contains no words."

    # L = average number of letters per 100 words
    L = (letters / words) * 100

    # S = average number of sentences per 100 words
    S = (sentences / words) * 100

    # Coleman-Liau Index formula
    index = 0.0588 * L - 0.296 * S - 15.8

    # Final grade is the index rounded to the nearest whole number
    grade = round(index)

    print(f"\n--- Counts ---")
    print(f"Letters: {letters}")
    print(f"Words: {words}")
    print(f"Sentences: {sentences}")
    print(f"Index: {index:.2f}")

    print(f"\n--- Grade Level ---")
    if grade >= 16:
        print("Grade 16+")
    elif grade < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {grade}")

text = input("enter text: ")
calculate_grade(text)

"""
check50
cs50/problems/2025/x/sentimental/readability

:) readability.py exists.
Log
checking that readability.py exists...

:) handles single sentence with multiple words
Log
running python3 readability.py...
sending input In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since....
checking for output "Grade 7\n"...
checking that program exited with status 0...

:) handles punctuation within a single sentence
Log
running python3 readability.py...
sending input There are more things in Heaven and Earth, Horatio, than are dreamt of in your philosophy....
checking for output "Grade 9\n"...
checking that program exited with status 0...

:) handles more complex single sentence
Log
running python3 readability.py...
sending input Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, "and what is the use of a book," thought Alice "without pictures or conversation?"...
checking for output "Grade 8\n"...
checking that program exited with status 0...

:) handles multiple sentences
Log
running python3 readability.py...
sending input Harry Potter was a highly unusual boy in many ways. For one thing, he hated the summer holidays more than any other time of year. For another, he really wanted to do his homework, but was forced to do it in secret, in the dead of the night. And he also happened to be a wizard....
checking for output "Grade 5\n"...
checking that program exited with status 0...

:) handles multiple more complex sentences
Log
running python3 readability.py...
sending input It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him....
checking for output "Grade 10\n"...
checking that program exited with status 0...

:) handles longer passages
Log
running python3 readability.py...
sending input When he was nearly thirteen, my brother Jem got his arm badly broken at the elbow. When it healed, and Jem's fears of never being able to play football were assuaged, he was seldom self-conscious about his injury. His left arm was somewhat shorter than his right; when he stood or walked, the back of his hand was at right angles to his body, his thumb parallel to his thigh....
checking for output "Grade 8\n"...
checking that program exited with status 0...

:) handles questions in passage
Log
running python3 readability.py...
sending input Would you like them here or there? I would not like them here or there. I would not like them anywhere....
checking for output "Grade 2\n"...
checking that program exited with status 0...

:) handles reading level before Grade 1
Log
running python3 readability.py...
sending input One fish. Two fish. Red fish. Blue fish....
checking for output "Before Grade 1\n"...
checking that program exited with status 0...

:) handles reading level at Grade 16+
Log
running python3 readability.py...
sending input A large class of computational problems involve the determination of properties of graphs, digraphs, integers, arrays of integers, finite families of finite sets, boolean formulas and elements of other countable domains....
checking for output "Grade 16+\n"...
checking that program exited with status 0...
"""
