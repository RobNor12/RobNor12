// Implements a spell-checker

#include <ctype.h>
#include <stdio.h>
#include <sys/resource.h>
#include <sys/time.h>

#include "dictionary.h"

// Undefine any definitions
#undef calculate
#undef getrusage

// Default dictionary
#define DICTIONARY "dictionaries/large"

// Prototype
double calculate(const struct rusage *b, const struct rusage *a);

int main(int argc, char *argv[]){

    // Check for correct number of args
    if (argc != 2 && argc != 3){

        printf("Usage: ./speller [DICTIONARY] text\n");
        return 1;
    }

    // Structures for timing data
    struct rusage before, after;

    // Benchmarks
    double time_load = 0.0, time_check = 0.0, time_size = 0.0, time_unload = 0.0;

    // Determine dictionary to use
    char *dictionary = (argc == 3) ? argv[1] : DICTIONARY;

    // Load dictionary
    getrusage(RUSAGE_SELF, &before);
    bool loaded = load(dictionary);
    getrusage(RUSAGE_SELF, &after);

    // Exit if dictionary not loaded
    if (!loaded){

        printf("Could not load %s.\n", dictionary);
        return 1;
    }

    // Calculate time to load dictionary
    time_load = calculate(&before, &after);

    // Try to open text
    char *text = (argc == 3) ? argv[2] : argv[1];
    FILE *file = fopen(text, "r");
    if (file == NULL){

        printf("Could not open %s.\n", text);
        unload();
        return 1;
    }

    // Prepare to report misspellings
    printf("\nMISSPELLED WORDS\n\n");

    // Prepare to spell-check
    int index = 0, misspellings = 0, words = 0;
    char word[LENGTH + 1];

    // Spell-check each word in text
    char c;
    while (fread(&c, sizeof(char), 1, file)){

        // Allow only alphabetical characters and apostrophes
        if (isalpha(c) || (c == '\'' && index > 0)){

            // Append character to word
            word[index] = c;
            index++;

            // Ignore alphabetical strings too long to be words
            if (index > LENGTH){

                // Consume remainder of alphabetical string
                while (fread(&c, sizeof(char), 1, file) && isalpha(c));

                // Prepare for new word
                index = 0;
            }
        }

        // Ignore words with numbers (like MS Word can)
        else if (isdigit(c)){

            // Consume remainder of alphanumeric string
            while (fread(&c, sizeof(char), 1, file) && isalnum(c));

            // Prepare for new word
            index = 0;
        }

        // We must have found a whole word
        else if (index > 0){

            // Terminate current word
            word[index] = '\0';

            // Update counter
            words++;

            // Check word's spelling
            getrusage(RUSAGE_SELF, &before);
            bool misspelled = !check(word);
            getrusage(RUSAGE_SELF, &after);

            // Update benchmark
            time_check += calculate(&before, &after);

            // Print word if misspelled
            if (misspelled){

                printf("%s\n", word);
                misspellings++;
            }

            // Prepare for next word
            index = 0;
        }
    }

    // Check whether there was an error
    if (ferror(file)){

        fclose(file);
        printf("Error reading %s.\n", text);
        unload();
        return 1;
    }

    // Close text
    fclose(file);

    // Determine dictionary's size
    getrusage(RUSAGE_SELF, &before);
    unsigned int n = size();
    getrusage(RUSAGE_SELF, &after);

    // Calculate time to determine dictionary's size
    time_size = calculate(&before, &after);

    // Unload dictionary
    getrusage(RUSAGE_SELF, &before);
    bool unloaded = unload();
    getrusage(RUSAGE_SELF, &after);

    // Abort if dictionary not unloaded
    if (!unloaded){

        printf("Could not unload %s.\n", dictionary);
        return 1;
    }

    // Calculate time to unload dictionary
    time_unload = calculate(&before, &after);

    // Report benchmarks
    printf("\nWORDS MISSPELLED:     %d\n", misspellings);
    printf("WORDS IN DICTIONARY:  %d\n", n);
    printf("WORDS IN TEXT:        %d\n", words);
    printf("TIME IN load:         %.2f\n", time_load);
    printf("TIME IN check:        %.2f\n", time_check);
    printf("TIME IN size:         %.2f\n", time_size);
    printf("TIME IN unload:       %.2f\n", time_unload);
    printf("TIME IN TOTAL:        %.2f\n\n",
           time_load + time_check + time_size + time_unload);

    // Success
    return 0;
}

// Returns number of seconds between b and a
double calculate(const struct rusage *b, const struct rusage *a)
{
    if (b == NULL || a == NULL)
    {
        return 0.0;
    }
    else
    {
        return ((((a->ru_utime.tv_sec * 1000000 + a->ru_utime.tv_usec) -
                  (b->ru_utime.tv_sec * 1000000 + b->ru_utime.tv_usec)) +
                 ((a->ru_stime.tv_sec * 1000000 + a->ru_stime.tv_usec) -
                  (b->ru_stime.tv_sec * 1000000 + b->ru_stime.tv_usec)))
                / 1000000.0);
    }
}


/*
check50
cs50/problems/2025/x/speller

:) dictionary.c exists
Log
checking that dictionary.c exists...

:) speller compiles
Log
running make...
checking that program exited with status 0...

:) handles most basic words properly
Log
running ./speller basic/dict basic/text...
checking for output "MISSPELLED WORDS\n\n\nWORDS MISSPELLED: 0\nWORDS IN DICTIONARY: 8\nWORDS IN TEXT: 9\n"...
checking that program exited with status 0...

:) handles min length (1-char) words
Log
running ./speller min_length/dict min_length/text...
checking for output "MISSPELLED WORDS\n\n\nWORDS MISSPELLED: 0\nWORDS IN DICTIONARY: 1\nWORDS IN TEXT: 1\n"...
checking that program exited with status 0...

:) handles max length (45-char) words
Log
running ./speller max_length/dict max_length/text...
checking for output "MISSPELLED WORDS\n\n\nWORDS MISSPELLED: 0\nWORDS IN DICTIONARY: 1\nWORDS IN TEXT: 1\n"...
checking that program exited with status 0...

:) handles words with apostrophes properly
Log
running ./speller apostrophe/without/dict apostrophe/with/text...
checking for output "MISSPELLED WORDS\n\nfoo's\n\nWORDS MISSPELLED: 1\nWORDS IN DICTIONARY: 1\nWORDS IN TEXT: 1\n"...
checking that program exited with status 0...
running ./speller apostrophe/with/dict apostrophe/without/text...
checking for output "MISSPELLED WORDS\n\nfoo\nfoO\nfOo\nFoo\nfOO\nFoO\nFOo\nFOO\n\nWORDS MISSPELLED: 8\nWORDS IN DICTIONARY: 1\nWORDS IN TEXT: 8\n"...
checking that program exited with status 0...
running ./speller apostrophe/with/dict apostrophe/with/text...
checking for output "MISSPELLED WORDS\n\n\nWORDS MISSPELLED: 0\nWORDS IN DICTIONARY: 1\nWORDS IN TEXT: 1\n"...
checking that program exited with status 0...

:) spell-checking is case-insensitive
Log
running ./speller case/dict case/text...
checking for output "MISSPELLED WORDS\n\n\nWORDS MISSPELLED: 0\nWORDS IN DICTIONARY: 1\nWORDS IN TEXT: 8\n"...
checking that program exited with status 0...

:) handles substrings properly
Log
running ./speller substring/dict substring/text...
checking for output "MISSPELLED WORDS\n\nca\ncats\ncaterpill\ncaterpillars\n\nWORDS MISSPELLED: 4\nWORDS IN DICTIONARY: 2\nWORDS IN TEXT: 6\n"...
checking that program exited with status 0...

:) handles large dictionary (hash collisions) properly
Log
running ./speller large/dict large/text...
checking for output "MISSPELLED WORDS\n\n\nWORDS MISSPELLED: 0\nWORDS IN DICTIONARY: 143091\nWORDS IN TEXT: 158\n"...
checking that program exited with status 0...

:) program is free of memory errors
Log
running valgrind --show-leak-kinds=all --xml=yes --xml-file=/tmp/tmp6e8rpwna -- ./speller substring/dict substring/text...
checking for output "MISSPELLED WORDS\n\nca\ncats\ncaterpill\ncaterpillars\n\nWORDS MISSPELLED: 4\nWORDS IN DICTIONARY: 2\nWORDS IN TEXT: 6\n"...
checking that program exited with status 0...
checking for valgrind errors...

*/
