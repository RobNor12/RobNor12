#include <stdio.h>
#include <cs50.h>

int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennys(int cents);

int main(void){
    // Prompt the user for change owed, in cents
    int cents;
    int total_coins;
    
    do {
        cents = get_int("Change owed: ");
    }
    while(cents < 0);

    // Calculate how much change you should give customer
    int quarters = calculate_quarters(cents);
    cents = cents - (quarters * 25);
    
    int dimes = calculate_dimes(cents);
    cents = cents - (dimes * 10);
    
    int nickels = calculate_nickels(cents);
    cents = cents - (nickels * 5);
    
    int pennys = calculate_pennys(cents);
    cents = cents - (pennys * 1);

    total_coins = quarters + dimes + nickels + pennys;
    printf("You are owed %i coins\n", total_coins);
}

int calculate_quarters(int cents){
    // Calculate how many quarters you should give customer
    int quarters = 0;
    while(cents >= 25){
        quarters++;
        cents = cents - 25;
    }
    
    return quarters;
}

int calculate_dimes(int cents){
    int dimes = 0;
    while(cents >= 10){
        dimes++;
        cents = cents - 10;
    }
    
    return dimes;
}

int calculate_nickels(int cents){
    int nickels = 0;
    while(cents >= 5){
        nickels++;
        cents = cents - 5;
    }
    
    return nickels;
}

int calculate_pennys(int cents){
    int pennys = 0;
    while(cents > 0){
        pennys++;
        cents = cents - 1;
    }
    
    return pennys;
}

/*
cs50/problems/2025/x/cash
:) cash.c exists
Log
checking that cash.c exists...
:) cash.c compiles
Log
running clang cash.c -o cash -std=c11 -ggdb -lm -lcs50...
:) input of 41 yields output of 4
Log
running ./cash...
sending input 41...
checking for output "4\n"...
checking that program exited with status 0...
:) input of 1 yields output of 1
Log
running ./cash...
sending input 1...
checking for output "1\n"...
checking that program exited with status 0...
:) input of 15 yields output of 2
Log
running ./cash...
sending input 15...
checking for output "2\n"...
checking that program exited with status 0...
:) input of 160 yields output of 7
Log
running ./cash...
sending input 160...
checking for output "7\n"...
checking that program exited with status 0...
:) input of 2300 yields output of 92
Log
running ./cash...
sending input 2300...
checking for output "92\n"...
checking that program exited with status 0...
:) rejects a negative input like -1
Log
running ./cash...
sending input -1...
checking that input was rejected...
:) rejects a non-numeric input of "foo"
Log
running ./cash...
sending input foo...
checking that input was rejected...
*/
:) rejects a non-numeric input of ""
Log
running ./cash...
sending input ...
checking that input was rejected...
