#include "helpers.h"
#include <math.h>

// Convert image to grayscale (Averages R, G, B values)
void grayscale(int height, int width, RGBTRIPLE image[height][width]){

    for (int i = 0; i < height; i++){

        for (int j = 0; j < width; j++){
            // Use floats to prevent integer division
            float r = image[i][j].rgbtRed;
            float g = image[i][j].rgbtGreen;
            float b = image[i][j].rgbtBlue;

            // Calculate the rounded average
            int avg = round((r + b + g) / 3.0);

            // Set all three color channels to the new average
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }

    return;
}

// Reflect image horizontally (Swaps left half with right half)
void reflect(int height, int width, RGBTRIPLE image[height][width]){

    for (int i = 0; i < height; i++){

        // Loop through HALF of the columns to avoid swapping back!
        for (int j = 0; j < width / 2; j++){
            // Calculate the mirror column index
            int mirror_j = width - 1 - j;

            // Perform the three-step swap using a temporary pixel structure
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][mirror_j];
            image[i][mirror_j] = temp;
        }
    }
    
    return;
}

// Blur image (Averages 3x3 surrounding pixels)
void blur(int height, int width, RGBTRIPLE image[height][width]){

    //Create a temporary copy to read original pixel values
    RGBTRIPLE temp_image[height][width];

    for (int i = 0; i < height; i++){

        for (int j = 0; j < width; j++){

            temp_image[i][j] = image[i][j];
        }
    }

    // Main loop to calculate blur for every pixel
    for (int i = 0; i < height; i++){

        for (int j = 0; j < width; j++){
            float total_red = 0;
            float total_green = 0;
            float total_blue = 0;
            int count = 0;

            // Inner loops to check the 3x3 neighborhood (k=row offset, l=col offset)
            for (int k = -1; k <= 1; k++){

                for (int l = -1; l <= 1; l++){

                    int neighbor_i = i + k;
                    int neighbor_j = j + l;

                    // Boundary Check: Ensure the neighbor is within bounds
                    if (neighbor_i >= 0 && neighbor_i < height && neighbor_j >= 0 && neighbor_j < width){
                        total_red += temp_image[neighbor_i][neighbor_j].rgbtRed;
                        total_green += temp_image[neighbor_i][neighbor_j].rgbtGreen;
                        total_blue += temp_image[neighbor_i][neighbor_j].rgbtBlue;
                        count++;
                    }
                }
            }

            // Calculate the final average and assign to the original image
            image[i][j].rgbtRed = round(total_red / count);
            image[i][j].rgbtGreen = round(total_green / count);
            image[i][j].rgbtBlue = round(total_blue / count);
        }
    }
    
    return;
}

// Detect edges (Sobel Filter)
void edges(int height, int width, RGBTRIPLE image[height][width]){

    // 1. Define the Sobel Kernels
    int Gx[3][3] = {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };

    int Gy[3][3] = {
        {-1, -2, -1},
        { 0,  0,  0},
        { 1,  2,  1}
    };

    // 2. Create a temporary copy (mandatory for using original values)
    RGBTRIPLE temp_image[height][width];

    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){

            temp_image[i][j] = image[i][j];
        }
    }

    // Main loop to calculate edges for every pixel
    for (int i = 0; i < height; i++){

        for (int j = 0; j < width; j++){
            // Accumulators for Gx and Gy for all three colors
            long Gx_red = 0;
            long Gx_green = 0;
            long Gx_blue = 0;
            long Gy_red = 0;
            long Gy_green = 0;
            long Gy_blue = 0;

            // Inner loops to check the 3x3 box (k=row offset, l=col offset)
            for (int k = -1; k <= 1; k++){

                for (int l = -1; l <= 1; l++){
                    int neighbor_i = i + k;
                    int neighbor_j = j + l;

                    // Boundary Check
                    if (neighbor_i >= 0 && neighbor_i < height && neighbor_j >= 0 && neighbor_j < width){
                        // Accumulate Gx values
                        Gx_red += (long) Gx[k + 1][l + 1] * temp_image[neighbor_i][neighbor_j].rgbtRed;
                        Gx_green += (long) Gx[k + 1][l + 1] * temp_image[neighbor_i][neighbor_j].rgbtGreen;
                        Gx_blue += (long) Gx[k + 1][l + 1] * temp_image[neighbor_i][neighbor_j].rgbtBlue;

                        // Accumulate Gy values
                        Gy_red += (long) Gy[k + 1][l + 1] * temp_image[neighbor_i][neighbor_j].rgbtRed;
                        Gy_green += (long) Gy[k + 1][l + 1] * temp_image[neighbor_i][neighbor_j].rgbtGreen;
                        Gy_blue += (long) Gy[k + 1][l + 1] * temp_image[neighbor_i][neighbor_j].rgbtBlue;
                    }
                }
            }

            // FINAL MAGNITUDE CALCULATION (OUTSIDE of k and l loops)
            // Magnitude = round(sqrt(Gx^2 + Gy^2))

            // Red Channel
            int final_red = round(sqrt((Gx_red * Gx_red) + (Gy_red * Gy_red)));

            // Green Channel
            int final_green = round(sqrt((Gx_green * Gx_green) + (Gy_green * Gy_green)));

            // Blue Channel
            int final_blue = round(sqrt((Gx_blue * Gx_blue) + (Gy_blue * Gy_blue)));

            // Cap the values at 255 and assign them
            image[i][j].rgbtRed = (final_red > 255) ? 255 : final_red;
            image[i][j].rgbtGreen = (final_green > 255) ? 255 : final_green;
            image[i][j].rgbtBlue = (final_blue > 255) ? 255 : final_blue;
        }
    }
    
    return;
}
