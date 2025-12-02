#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512
typedef uint8_t BYTE;

void ArgumentCount(int argc);
void doesFileExists(FILE *file);
int JPEG_check(BYTE tempb[]);

int main(int argc, char *argv[])
{
    ArgumentCount(argc);
    FILE *raw = fopen(argv[1], "r");
    doesFileExists(raw);

    BYTE tempb[BLOCK_SIZE];

    char fName[8];
    FILE *img;
    int counter = 0;

    while (fread(tempb, BLOCK_SIZE, 1, raw) == 1)
    {
        if (JPEG_check(tempb) == 1)
        {
            if (counter != 0)
            {
                fclose(img);
            }
            sprintf(fName, "%03i.jpg", counter++);
            img = fopen(fName, "w");
            fwrite(tempb, BLOCK_SIZE, 1, img);
        }
        else if (counter > 0)
        {
            fwrite(tempb, BLOCK_SIZE, 1, img);
        }
    }
    fclose(raw);
    fclose(img);
}

void ArgumentCount(int argc)
{
    if (argc != 2)
    {
        printf("Usage: /recover image\n");
        exit(1);
    }
}

void doesFileExists(FILE *file)
{
    if (file == NULL)
    {
        printf("File could not be opened. \n");
        exit(1);
    }
}

int JPEG_check(BYTE tempb[])
{
    if (tempb[0] == 0xff && tempb[1] == 0xd8 && tempb[2] == 0xff && (tempb[3] & 0xf0) == 0xe0)
    {
        return 1;
    }

    return 0;
}
