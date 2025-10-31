import csv
import sys


def main():

    # Check for 3 arguments (script, database, sequence)
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # Store arguments for clarity
    database_filename = sys.argv[1]
    sequence_filename = sys.argv[2]

    # Variables to store data
    database = []
    str_sequences = [] # STRs (AGAT, AATG, etc.) will be stored here
    dna_sequence = ""  # Variable to hold the entire DNA sequence string

    # 1. Read database file into a variable
    with open(database_filename) as file:
        reader = csv.DictReader(file)

            # Get the list of STRs (all fieldnames EXCEPT the first one, 'name')
        str_sequences = reader.fieldnames[1:]

            # Store all the people's data into the database list
        database = list(reader)



    #Read DNA sequence file into a variable


    with open(sequence_filename) as file:
        # Read the single line of DNA sequence and remove any trailing newline
        dna_sequence = file.read().strip()



    #Find longest match of each STR in DNA sequence
    sequence_counts = {}

    # Loop over the list of required STRs (AGAT, AATG, etc.)
    for str_name in str_sequences:
        # Calculate the longest run of the current STR in the DNA sequence
        match_length = longest_match(dna_sequence, str_name)

        # Store the result: e.g., {'AGAT': 4, 'AATG': 1, ...}
        sequence_counts[str_name] = match_length


    # Check database for matching profiles (FINAL LOGIC)
    for person in database:
        # Assume the current person is a match until proven otherwise
        is_match = True

        # Loop over every required STR (e.g., AGAT, AATG)
        for str_name in str_sequences:

            # CRITICAL STEP: Convert person's count from STRING to INTEGER for comparison
            person_count = int(person[str_name])

            # Get the calculated count for the DNA sequence
            suspect_count = sequence_counts[str_name]

            # If any STR count does not match, set flag to False and stop checking this person
            if person_count != suspect_count:
                is_match = False
                break

        # If the flag is still True after checking ALL STRs, we have a match
        if is_match:
            print(person['name'])
            sys.exit(0) # Exit the program after a successful match

    # If the outer loop finishes without finding a match
    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # Ensure we don't go out of bounds before checking
            if end > sequence_length:
                break

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()

"""
check50
cs50/problems/2025/x/dna

:) dna.py exists
Log
checking that dna.py exists...

:) correctly identifies sequences/1.txt
Log
running python3 dna.py databases/small.csv sequences/1.txt...
checking for output "Bob\n"...

:) correctly identifies sequences/2.txt
Log
running python3 dna.py databases/small.csv sequences/2.txt...
checking for output "No match\n"...

:) correctly identifies sequences/3.txt
Log
running python3 dna.py databases/small.csv sequences/3.txt...
checking for output "No match\n"...

:) correctly identifies sequences/4.txt
Log
running python3 dna.py databases/small.csv sequences/4.txt...
checking for output "Alice\n"...

:) correctly identifies sequences/5.txt
Log
running python3 dna.py databases/large.csv sequences/5.txt...
checking for output "Lavender\n"...

:) correctly identifies sequences/6.txt
Log
running python3 dna.py databases/large.csv sequences/6.txt...
checking for output "Luna\n"...

:) correctly identifies sequences/7.txt
Log
running python3 dna.py databases/large.csv sequences/7.txt...
checking for output "Ron\n"...

:) correctly identifies sequences/8.txt
Log
running python3 dna.py databases/large.csv sequences/8.txt...
checking for output "Ginny\n"...

:) correctly identifies sequences/9.txt
Log
running python3 dna.py databases/large.csv sequences/9.txt...
checking for output "Draco\n"...

:) correctly identifies sequences/10.txt
Log
running python3 dna.py databases/large.csv sequences/10.txt...
checking for output "Albus\n"...

:) correctly identifies sequences/11.txt
Log
running python3 dna.py databases/large.csv sequences/11.txt...
checking for output "Hermione\n"...

:) correctly identifies sequences/12.txt
Log
running python3 dna.py databases/large.csv sequences/12.txt...
checking for output "Lily\n"...

:) correctly identifies sequences/13.txt
Log
running python3 dna.py databases/large.csv sequences/13.txt...
checking for output "No match\n"...

:) correctly identifies sequences/14.txt
Log
running python3 dna.py databases/large.csv sequences/14.txt...
checking for output "Severus\n"...

:) correctly identifies sequences/15.txt
Log
running python3 dna.py databases/large.csv sequences/15.txt...
checking for output "Sirius\n"...

:) correctly identifies sequences/16.txt
Log
running python3 dna.py databases/large.csv sequences/16.txt...
checking for output "No match\n"...

:) correctly identifies sequences/17.txt
Log
running python3 dna.py databases/large.csv sequences/17.txt...
checking for output "Harry\n"...

:) correctly identifies sequences/18.txt
Log
running python3 dna.py databases/large.csv sequences/18.txt...
checking for output "No match\n"...

:) correctly identifies sequences/19.txt
Log
running python3 dna.py databases/large.csv sequences/19.txt...
checking for output "Fred\n"...

:) correctly identifies sequences/20.txt
Log
running python3 dna.py databases/large.csv sequences/20.txt...
checking for output "No match\n"...

:) correctly identifies sequences/dynamic_1.txt
Log
running python3 generate_dynamic_test.py dynamic_1.csv dynamic_1.txt 1980 && python3 dna.py databases/dynamic_1.csv sequences/dynamic_1.txt...
checking for output "Philosopher\n"...

:) correctly identifies sequences/dynamic_2.txt
Log
running python3 generate_dynamic_test.py dynamic_2.csv dynamic_2.txt 7 && python3 dna.py databases/dynamic_2.csv sequences/dynamic_2.txt...
checking for output "Philosopher\n"...

:) correctly identifies sequences/dynamic_3.txt
Log
running python3 generate_dynamic_test.py dynamic_3.csv dynamic_3.txt 31 && python3 dna.py databases/dynamic_3.csv sequences/dynamic_3.txt...
checking for output "Philosopher\n"...

:) correctly identifies sequences/dynamic_4.txt
Log
running python3 generate_dynamic_test.py dynamic_4.csv dynamic_4.txt 4 && python3 dna.py databases/dynamic_4.csv sequences/dynamic_4.txt...
checking for output "Philosopher\n"...

:) correctly identifies sequences/dynamic_5.txt
Log
running python3 generate_dynamic_test.py dynamic_5.csv dynamic_5.txt 141 && python3 dna.py databases/dynamic_5.csv sequences/dynamic_5.txt...
checking for output "Philosopher\n"...

:) correctly identifies sequences/dynamic_6.txt
Log
running python3 generate_dynamic_test.py dynamic_6.csv dynamic_6.txt 12 && python3 dna.py databases/dynamic_6.csv sequences/dynamic_6.txt...
checking for output "Philosopher\n"...

:) correctly identifies sequences/dynamic_7.txt
Log
running python3 generate_dynamic_test.py dynamic_7.csv dynamic_7.txt 20 && python3 dna.py databases/dynamic_7.csv sequences/dynamic_7.txt...
checking for output "Philosopher\n"...

:) correctly identifies sequences/dynamic_8.txt
Log
running python3 generate_dynamic_test.py dynamic_8.csv dynamic_8.txt 206 && python3 dna.py databases/dynamic_8.csv sequences/dynamic_8.txt...
checking for output "Philosopher\n"...
"""
