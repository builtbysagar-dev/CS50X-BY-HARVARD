#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    for(int i = 0; i < height; i++){ 
        //iterates through every column
        for(int j = 0; j < width; j++){ 
            //iterates through every row

            int x = image[i][j].rgbtRed; 
            //assigning the value of red in pixel to variable x
            int y = image[i][j].rgbtBlue;
             //assigning the value of blue in pixel to variable y
            int z = image[i][j].rgbtGreen;
            
            //assigning the value of green inpixel to variable z
            int grey = (x + y + z)/3; 
            //assigning the grey sum of RGB to variable grey
            image[i][j].rgbtRed = grey; 
            //assigning value of grey to red in the pixel
            image[i][j].rgbtGreen = grey; 
            //assigning value of grey to green in the pixel
            image[i][j].rgbtBlue = grey;
             //assigning value of grey to blue in the pixel

        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < height; i++){
        for(int j = 0; j < width; j++){
            int x = image[i][j].rgbtRed; 
            //assigning the value of red in pixel to variable x
            int y = image[i][j].rgbtBlue;
             //assigning the value of blue in pixel to variable y
            int z = image[i][j].rgbtGreen; 
            //assigning the value of green inpixel to variable z
            int sepiaRed = roundf((.393 * x) + (.769 * z) + (.189 * y));
             //sepiaRed algorithm and rounding off to nearest integer
            int sepiaGreen = roundf((.349 * x) + (.686 * z) + (.168 * y)); 
            //sepiaGreen algorithm and rounding off to nearest integer
            int sepiaBlue = roundf((.272 * x) + (.534 * z) + (.131 + y)); 
            //sepiaBlue algorithm and rounding off to nearest integer

            if (sepiaRed > 255){ 
                //checks whether the value of sepiaRed exceeds the 8 bit color value(255)
                sepiaRed = 255;
            };
            if (sepiaGreen > 255){
                //checks whether the value of sepiaGreen exceeds the 8 bit color value(255)
                sepiaGreen = 255;
            };
            if (sepiaBlue > 255){ 
                //checks whether the value of sepiaBlue exceeds the 8 bit color value(255)
                sepiaBlue = 255;
            };

            image[i][j].rgbtRed = sepiaRed; 
            //assigning value of sepiaRed to red in the pixel
            image[i][j].rgbtGreen = sepiaGreen; 
            //assigning value of sepiaGreen to green in the pixel
            image[i][j].rgbtBlue = sepiaBlue; 
            //assigning value of sepiaBlue to blue in the pixel
        }
    }
    return;
}

// Reflect image horizontally
void swap(int *x, int *y);
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < height; i++){
        if (width % 2 == 0){    
            //swapping algorithm if the image has even number of pixels
            for(int j = 0; j < width / 2; j++){
                RGBTRIPLE temp[height][width];
                temp[i][j] = image[i][j];
                image[i][j] = image[i][(width - 1) - j];
                image[i][(width - 1) - j] = temp[i][j];
            }
        }
        else if(width % 2 == 1){   
             //swapping algorithm if image has an odd number of pixels
            for(int j = 0; j < (width - 1) / 2; j++){
                RGBTRIPLE temp[height][width];
                temp[i][j] = image[i][j];
                image[i][j] = image[i][(width - 1) - j];
                image[i][(width - 1) - j] = temp[i][j];
            }
        }
    }
    return;
}



// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
     RGBTRIPLE temp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sumBlue = 0;
            float sumGreen = 0;
            float sumRed = 0;
            float counter = 0;

            for (int r = -1; r < 2; r++)
            {
                for (int c = -1; c < 2; c++)
                {
                    if (i + r < 0 || i + r > height - 1)
                    {
                        continue;
                    }

                    if (j + c < 0 || j + c > width - 1)
                    {
                        continue;
                    }

                    sumBlue += image[i + r][j + c].rgbtBlue;
                    sumGreen += image[i + r][j + c].rgbtGreen;
                    sumRed += image[i + r][j + c].rgbtRed;
                    counter++;
                }
            }

            temp[i][j].rgbtBlue = round(sumBlue / counter);
            temp[i][j].rgbtGreen = round(sumGreen / counter);
            temp[i][j].rgbtRed = round(sumRed / counter);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }

    }
    return;
}