// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

int words = 0;


// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int k = hash(word);

    node *cursor = table[k];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }

        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int result = 0;

    for (int i = 0; word[i] != '\0'; i++)
    {
        result += tolower(word[i]);
    }

    return result % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)

{
    FILE *d;
    d = fopen(dictionary, "r");

    if (d == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];

    while (fscanf(d, "%s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));

        if (new_node == NULL)
        {
            return 1;
        }

        strcpy(new_node->word, word);

        int k = hash(word);

        if (table[k] == NULL)
        {
            new_node->next = NULL;
            table[k] = new_node;
        }
        else
        {
            new_node->next = table[k];
            table[k] = new_node;
        }

        words++;
    }

    fclose(d);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
