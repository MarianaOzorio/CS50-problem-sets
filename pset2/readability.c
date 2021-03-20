#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int main(void)
{
    string text = get_string("Text: ");

    float letter = 0;
    float word = 1;
    float sentence = 0;

    int n = strlen(text);

    for (int i = 0; i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letter++;
        }

        if (isspace(text[i]))
        {
            word++;
        }

        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentence++;
        }
    }

    float colemanLiauIndex = 0.0588 * (100 * letter / word) - 0.296 * (100 * sentence / word) - 15.8;
    int index = round(colemanLiauIndex);

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
