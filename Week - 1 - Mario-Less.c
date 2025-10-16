Mario-less
// mario
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // ask for user imput
    //  if user imput is not vaild 1-8 ask again for user imput again and again until the imput is
    //  vaild
    // once the imput is vaild make a prompt to calcualt the height of the pyrmade
    // after the calculations print out the pyramid with the correct number of hashes
    int n;
    do{
        n = get_int("Pyrimid height: ");
    }

    while(n < 1 || n > 8);

    for(int i = 0; i < n; i++){

        for (int j = 0; j < n - (i + 1); j++){
            printf(" ");
        }

        for (int b = 0; b < i + 1; b++){
            printf("#");
        }
        printf("\n");
    }
}
