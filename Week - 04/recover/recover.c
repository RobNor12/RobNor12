#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL) // Error check
    {
        printf("Could not open file.\n");
        return 1;
    }

    // File pointer for the current output JPEG, initialized to NULL
    FILE *img = NULL;

    // Create a buffer for a block of data (using the specified uint8_t from stdint.h)
    uint8_t buffer[512];

    // Character array to hold the dynamic filename (000.jpg + \0 needs 8 bytes total)
    char filename[8]; // Changed size back to the correct minimum of 8

    // Counter for sequential filenames
    int jpeg_count = 0;


    // While there's still data left to read from the memory card
    while (fread(buffer, 1, 512, card) == 512)
    {
        // Check for New JPEG Signature (State 1)
        // Explicitly cast buffer elements to (int) during comparison
        if ( (int)buffer[0] == 0xff && (int)buffer[1] == 0xd8 && (int)buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0 )
        {
            // A. Close the old file (if one was open)
            if (img != NULL)
            {
                fclose(img);
            }

            // C. Generate the new filename (CORRECTED FORMATTING: %03i for zero-padding)
            sprintf(filename, "%03i.jpg", jpeg_count);

            // D. Open the new file and update the img pointer
            img = fopen(filename, "w");
            if (img == NULL)
            {
                fclose(card);
                return 1; // Handle file opening error
            }


            fwrite(buffer, 1, 512, img);

            // F. Increment the counter
            jpeg_count++;
        }

        // Check if we are currently writing a JPEG file (State 2)
        else if (img != NULL)
        {
            // Write the current block to the open file
            fwrite(buffer, 1, 512, img);
        }
    }

    // --- Final Cleanup ---
    // Close the last JPEG output file, if one was ever opened
    if (img != NULL)
    {
        fclose(img);
    }

    // Close the input file
    fclose(card);

    return 0;
}
