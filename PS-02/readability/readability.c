#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int words(string s);
int letters(string s);
int sentences(string s);

int main(void)
{
    string text = get_string("Text: ");
    int W = words(text);
    int L = letters(text);
    int S = sentences(text);

    int index;
    index = round(0.0588 * (L / (float) W * 100.0) - 0.296 * (S / (float) W * 100.0) - 15.8);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int words(string s)
{
    int w = 0;
    int a = strlen(s);
    for (int i = 0; i < a; i++)
    {
        if (s[i] == ' ')
        {
            w++;
        }
    }
    return (w + 1);
}

int letters(string s)
{
    int l = 0;
    int a = strlen(s);
    for (int i = 0; i < a; i++)
    {
        if (isupper(s[i]) || islower(s[i]))
        {
            l++;
        }
    }
    return l;
}

int sentences(string s)
{
    int l = 0;
    int a = strlen(s);
    for (int i = 0; i < a; i++)
    {
        if (s[i] == '.' || s[i] == '!' || s[i] == '?')
        {
            l++;
        }
    }
    return l;
}
