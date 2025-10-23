#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct{

    string name;
    int votes;
} candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[]){

    // Check for invalid usage
    if (argc < 2){

        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX){

        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }

    for (int i = 0; i < candidate_count; i++){

        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++){

        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name)){
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name){

    // Iterate over each candidate
    for(int i = 0; i < candidate_count; i++){
        if(strcmp(candidates[i].name, name) == 0){
            candidates[i].votes++;

            return true;
        }
    }

        // Check if candidate's name matches given name
            // If yes, increment candidate's votes and return true

    // If no match, return false
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void){
// Find the maximum number of votes
    int max_votes = 0;

    for(int i = 0; i < candidate_count; i++){

        if(candidates[i].votes > max_votes)

        max_votes = candidates[i].votes;
    }
    // Print the candidate (or candidates) with maximum votes

    for(int i = 0; i < candidate_count; i++){

        if(candidates[i].votes == max_votes){

            printf("%s\n", candidates[i].name);
        }
    }
}

/*
cs50/problems/2025/x/plurality

:) plurality.c exists
Log
checking that plurality.c exists...

:) plurality compiles
Log
running clang plurality.c -o plurality -std=c11 -ggdb -lm -lcs50...
running clang plurality_test.c -o plurality_test -std=c11 -ggdb -lm -lcs50...

:) vote returns true when given name of first candidate

:) vote returns true when given name of middle candidate

:) vote returns true when given name of last candidate

:) vote returns false when given name of invalid candidate

:) vote produces correct counts when all votes are zero

:) vote produces correct counts after some have already voted

:) vote leaves vote counts unchanged when voting for invalid candidate

:) print_winner identifies Alice as winner of election
Log
running ./plurality_test 0 7...

:) print_winner identifies Bob as winner of election
Log
running ./plurality_test 0 8...

:) print_winner identifies Charlie as winner of election
Log
running ./plurality_test 0 9...

:) print_winner prints multiple winners in case of tie

:) print_winner prints all names when all candidates are tied
*/
