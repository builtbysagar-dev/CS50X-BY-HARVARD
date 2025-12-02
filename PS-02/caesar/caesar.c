#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        for (int l = 0; l < strlen(argv[1]); l++)
        {
            if (isalpha(argv[1][l]))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    int key = atoi(argv[1]);
    string text = get_string("plaintext: ");
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                text[i] = (((text[i] - 65) + key) % 26) + 65;
            }
            if (islower(text[i]))
            {
                text[i] = (((text[i] - 97) + key) % 26) + 97;
            }
        }
    }
    printf("ciphertext: %s\n", text);
}
