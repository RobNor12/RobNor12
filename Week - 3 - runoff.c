#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct{

    string name;
    int votes;
    bool eliminated;

} candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);

void tabulate(void);

bool print_winner(void);

int find_min(void);

bool is_tie(int min);

void eliminate(int min);

int main(int argc, string argv[]){

    // Check for invalid usage
    if (argc < 2){

        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES){

        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }

    for (int i = 0; i < candidate_count; i++){

        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");

    if (voter_count > MAX_VOTERS){

        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++){

        // Query for each rank
        for (int j = 0; j < candidate_count; j++){

            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name)){

                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true){

        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won){

            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie){

            for (int i = 0; i < candidate_count; i++){

                if (!candidates[i].eliminated){

                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++){

            candidates[i].votes = 0;
        }
    }
    return 0;
}

// Record preference if vote is valid
bool vote(int voter, int rank, string name){

    for(int i = 0; i < candidate_count; i++){

        if(strcmp(candidates[i].name, name) == 0){

            preferences[voter][rank] = i;

            return true;
        }
    }

    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void){

    for(int i = 0; i < voter_count; i++){

        for(int j = 0; j < candidate_count; j++){

            int candidate_index = preferences[i][j];

            if(candidates[candidate_index].eliminated == false){
                candidates[candidate_index].votes++;
                break;
            }
        }
    }
    return;
}

// Print the winner of the election, if there is one
bool print_winner(void){

    int majority = voter_count / 2;

    for(int i = 0; i < candidate_count; i++){

        if(candidates[i].votes > majority){

            printf("%s\n", candidates[i].name);

            return true;
        }
    }
    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void){

    int min_votes = voter_count;

    for(int i = 0; i < candidate_count; i++){

        if((!candidates[i].eliminated) && candidates[i].votes < min_votes){

            min_votes = candidates[i].votes;
        }
    }
    return min_votes;
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min){

    for(int i = 0; i < candidate_count; i++){

        if(!candidates[i].eliminated){

            if(candidates[i].votes != min){

                return false;
            }
        }
    }
    return true;
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min){

    for(int i = 0; i < candidate_count; i++){

        if((!candidates[i].eliminated && candidates[i].votes == min)){

            candidates[i].eliminated = true;
        }
    }
    return;
}
/*
cs50/problems/2025/x/runoff

:) runoff.c exists
Log
checking that runoff.c exists...

:) runoff compiles
Log
running clang runoff.c -o runoff -std=c11 -ggdb -lm -lcs50...
running clang runoff_test.c -o runoff_test -std=c11 -ggdb -lm -lcs50...

:) vote returns true when given name of candidate
:) vote returns false when given name of invalid candidate
:) vote correctly sets first preference for first voter
:) vote correctly sets third preference for second voter
:) vote correctly sets all preferences for voter
:) tabulate counts votes when all candidates remain in election
:) tabulate counts votes when one candidate is eliminated
:) tabulate counts votes when multiple candidates are eliminated
:) tabulate handles multiple rounds of preferences
:) print_winner prints name when someone has a majority
:) print_winner returns true when someone has a majority
:) print_winner returns false when nobody has a majority
:) print_winner returns false when leader has exactly 50% of vote
:) find_min returns minimum number of votes for candidate
:) find_min returns minimum when all candidates are tied
:) find_min ignores eliminated candidates
:) is_tie returns true when election is tied
:) is_tie returns false when election is not tied
:) is_tie returns false when only some of the candidates are tied
:) is_tie detects tie after some candidates have been eliminated
:) eliminate eliminates candidate in last place
:) eliminate eliminates multiple candidates in tie for last
:) eliminate eliminates candidates after some already eliminated
*/
