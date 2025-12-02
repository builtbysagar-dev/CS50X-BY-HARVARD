#include <cs50.h>
#include <stdio.h>

void build(int n);

int main(void)
{
    int height;

    // Get height (1-8)
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Call build function to build the wall of given height
    build(height);
}

void build(int n)
{
    for (int i = 1; i < (n + 1); i++)
    {
        for (int j = 1; j < (n + 1); j++)
        {
            if (j <= (n - i))
            {
                //Print blank spaces
                printf(" ");
            }
            else
            {
                // Print brick
                printf("#");
            }
        }

        printf("  ");

        for (int k = n; k >= 1; k--)
        {
            if (k <= (n - i))
            {
                // Skip for no character at all

            }
            else
            {
                // Print the bricks
                printf("#");
            }
        }

        // next line
        printf("\n");
    }
}