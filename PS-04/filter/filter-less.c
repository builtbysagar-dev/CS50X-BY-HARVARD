#include "helpers.h"
#include <math.h>

#define RED 0
#define GREEN 1
#define BLUE 2

int getBlur(int i, int j, int height, int width, RGBTRIPLE image[height][width], int color_position);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int newCol = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // grayscale
            newCol = round((image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen) / 3.0);
            image[i][j].rgbtBlue = newCol;
            image[i][j].rgbtRed = newCol;
            image[i][j].rgbtGreen = newCol;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed, sepiaGreen, sepiaBlue;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // sepia
            sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            // check if capped or not
            // red
            if (sepiaRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sepiaRed;
            }
            // blue
            if (sepiaBlue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sepiaBlue;
            }
            // green
            if (sepiaGreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sepiaGreen;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    int i, j;

    for (i = 0; i < height; i++)
    {
        for (j = 0; j < width / 2; j++)
        {
            temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }

    return;
}

// custom blur function
int getBlur(int i, int j, int height, int width, RGBTRIPLE image[height][width], int color_position)
{
    float count = 0;
    int sum = 0;
    for (int row = i - 1; row <= (i + 1); row++)
    {
        for (int column = j - 1; column <= (j + 1); column++)
        {
            if (row < 0 || row >= height || column < 0 || column >= width)
            {
                continue;
            }

            if (color_position == RED)
            {
                sum += image[row][column].rgbtRed;
            }
            else if (color_position == GREEN)
            {
                sum += image[row][column].rgbtGreen;
            }
            else
            {
                sum += image[row][column].rgbtBlue;
            }
            count++;
        }
    }
    return round(sum / count);
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int i, j;
    RGBTRIPLE temp[height][width];

    // copy to temp
    for (i = 0; i < height; i++)
    {
        for (j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    // find average and blur
    for (i = 0; i < height; i++)
    {

        for (j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = getBlur(i, j, height, width, temp, RED);
            image[i][j].rgbtGreen = getBlur(i, j, height, width, temp, GREEN);
            image[i][j].rgbtBlue = getBlur(i, j, height, width, temp, BLUE);
        }
    }
    return;
}
