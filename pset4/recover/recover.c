#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *f;
    unsigned char buffer[512];

    f = fopen(argv[1], "r");

    if (f == NULL)
    {
        printf("Error\n");
        return 2;
    }

    FILE *img = NULL;
    bool jpeg = false;
    int counter = 0;
    char name[8];

    while (fread(buffer, 512, 1, f) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpeg == true)
            {
                fclose(img);
            }

            sprintf(name, "%03i.jpg", counter++);
            img = fopen(name, "w");
            fwrite(buffer, 512, 1, img);
            jpeg = true;
        }
        else
        {
            if (jpeg == true)
            {
                fwrite(buffer, 512, 1, img);
            }
        }
    }

    fclose(f);
    fclose(img);
    return 0;
}
