#include <stdio.h>
#include <cs50.h>

int main(void){

    // 1. Prompt the user for their name using the get_string function
    // The prompt text is "whats your name? "
    string name = get_string("whats your name? ");

    // 2. Print the personalized greeting, matching the required output format.
    printf("hello, %s\n", name);
}
/*
:) hello.c exists
Log
checking that hello.c exists...
:) hello.c compiles
Log
running clang hello.c -o hello -std=c11 -ggdb -lm -lcs50...
:) responds to name Mario
Log
running ./hello...
sending input Mario...
:) responds to name Peach
Log
running ./hello...
sending input Peach...
:) responds to name Bowser
Log
running ./hello...
sending input Bowser...
*/
