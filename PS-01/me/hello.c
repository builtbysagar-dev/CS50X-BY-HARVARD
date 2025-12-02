#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Ask for the name of the user
    string name = get_string("What's your name?");
    // Greet th euser with their name
    printf("Hello, %s\n", name);
}
