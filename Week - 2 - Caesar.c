#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

bool only_digits(string s);

char rotate(char c, int n);

int main(int argc, string argv[]){
    // Make sure program was run with just one command-line argument

    // Make sure every character in argv[1] is a digit

    // Convert argv[1] from a `string` to an `int`

    // Prompt user for plaintext

    // For each character in the plaintext:

        // Rotate the character if it's a letter
    if(argc != 2){

        printf("Usage: ./ceaser key\n");

        return 1;
    }

    if(!only_digits(argv[1])){
        printf("Usage: ./ceaser key\n");

        return 1;
    }

    int k = atoi(argv[1]);

    string plaintext = get_string("Plaintext: ");

    printf("Ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++){

        char c = plaintext[i];

        if(isalpha(c)){
            printf("%c", rotate(c, k));
        }

        else{
            printf("%c", c);
        }
    }
    printf("\n");
    return 0;
}

bool only_digits(string s){
    for(int i = 0; i < strlen(s); i++){

        if(!isdigit(s[i])){
            return false;
        }
    }
    return true;
}

char rotate(char c, int n){

    if(isupper(c)){
        char r = (c - 'A' + n) % 26 + 'A';
        return r;
    }

    else if(islower(c)){
        char r = (c - 'a' + n) % 26 + 'a';
        return r;
    }
    return c;
}

/*
cs50/problems/2025/x/caesar

:) caesar.c exists.
Log
checking that caesar.c exists...

:) caesar.c compiles.
Log
running clang caesar.c -o caesar -std=c11 -ggdb -lm -lcs50...

:) encrypts "a" as "b" using 1 as key
Log
running ./caesar 1...
sending input a...
checking for output "ciphertext: b\n"...
checking that program exited with status 0...

:) encrypts "barfoo" as "yxocll" using 23 as key
Log
running ./caesar 23...
sending input barfoo...
checking for output "ciphertext: yxocll\n"...
checking that program exited with status 0...

:) encrypts "BARFOO" as "EDUIRR" using 3 as key
Log
running ./caesar 3...
sending input BARFOO...
checking for output "ciphertext: EDUIRR\n"...
checking that program exited with status 0...

:) encrypts "BaRFoo" as "FeVJss" using 4 as key
Log
running ./caesar 4...
sending input BaRFoo...
checking for output "ciphertext: FeVJss\n"...
checking that program exited with status 0...

:) encrypts "barfoo" as "onesbb" using 65 as key
Log
running ./caesar 65...
sending input barfoo...
checking for output "ciphertext: onesbb\n"...
checking that program exited with status 0...

:) encrypts "world, say hello!" as "iadxp, emk tqxxa!" using 12 as key
Log
running ./caesar 12...
sending input world, say hello!...
checking for output "ciphertext: iadxp, emk tqxxa!\n"...
checking that program exited with status 0...

:) handles lack of argv[1]
Log
running ./caesar...
checking that program exited with status 1...

:) handles non-numeric key
Log
running ./caesar 2x...
checking that program exited with status 1...

:) handles too many arguments
Log
running ./caesar 1 2...
checking that program exited with status 1...
*/
