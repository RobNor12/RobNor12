// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Choose number of buckets in hash table
const unsigned int N = 5000;

unsigned int loaded_words = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word){

    unsigned int index = hash(word);

    node *cursor = table[index];

    while(cursor != NULL){

        if(strcasecmp(cursor -> word, word) == 0){

            return true;
        }
        cursor = cursor -> next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word){

        //Improve this hash function
    long sum = 0;

    //Loop through the word and add character values to the sum, normalizing to lower case
    for (int i = 0; word[i] != '\0'; i++){

        // Use the lowercased version of the character for consistent hashing
        sum += tolower(word[i]);
    }

    // 3. Use the modulo operator to map the large sum to an index between 0 and N-1
    return sum % N;
}


// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary){

    FILE *source = fopen(dictionary, "r");

    if(source == NULL){

        return false;
    }

    char current_word[LENGTH + 1];

    while(fscanf(source, "%s", current_word) == 1){

        node *new_node = malloc(sizeof(node));

        if(new_node == NULL){

            return false;
        }
        strcpy(new_node -> word, current_word);

        unsigned int index = hash(new_node -> word);

        new_node -> next = table[index];

        table[index] = new_node;

        loaded_words++;
    }

    fclose(source);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void){

    return loaded_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void){

    for(int i = 0; i < N; i++){

        node *cursor = table[i];

        while(cursor != NULL){

            node *tmp = cursor -> next;

            free(cursor);

            cursor = tmp;
        }
    }

    return true;
}
