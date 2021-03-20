#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv [])
{
    if (argc != 2)
    {
        printf("Please type it a key\n");
        return 1;
    }

    if (!isdigit(*argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        int key = atoi(argv[1]);

        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");

        int inputText = strlen(plaintext);

        for (int j = 0; j < inputText; j++)
        {
            if (islower(plaintext[i]))
            {
                printf("%c", (plaintext[i] - 'a' + key) % 26 + 'a');
            }
            else if (isupper(plaintext[i]))
            {
                printf("%c", (plaintext[i] - 'A' + key) % 26 + 'A');
            }
            else
            {
                printf("%c", plaintext[i]);
            }
        }
    }

    printf("\n");
    return 0;
}
