#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>


#include "dictionary.h"


typedef struct node
{
    char word[LENGTH];
    struct node *next;
}
node;


const unsigned int N = 26;

node *table[N];
int total = 0;


bool check(const char *word)
{
    node *pointer = table[hash(word)];

    if (strcasecmp(pointer->word, word) == 0)
    {
        return true;
    }

    //keep looking throughout list
    while (pointer->next != NULL)
    {
        pointer = pointer->next;
        if (strcasecmp(pointer->word, word) == 0)
        {
            return true;
        }
    }

    return false;
}

//hashes a word to a bucket
unsigned int hash(const char *word)
{
    int n = (int) tolower(word[0]) - 97;
    return n;
}


bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    char *dictword = malloc(LENGTH);
    if (dictword == NULL)
    {
        return false;
    }

    while (fscanf(file, "%s", dictword) != EOF)
    {
        // allocates memory
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        // copies the word in the chunk of memory allocated and then updates the words count
        strcpy(n->word, dictword);
        total++;

        // set next to point at beginning of list
        n->next = table[hash(dictword)];

        // set array to point at n which becomes new beginning of the list
        table[hash(dictword)] = n;
    }

    fclose(file);
    free(dictword);
    return true;
} 


unsigned int size(void)
{
    return total;
}


bool unload(void)
{
    
    node *tmp;
    node *pointer;

    // repeats for every index in the table
    for (int i = 0; i < N; i++)
    {
        if (table[i] == NULL)
        {
            continue;
        }

        pointer = table[i];
        tmp = pointer;

        // until the end of the list keeps freeing the memory allocated in load
        while (pointer->next != NULL)
        {
            pointer = pointer->next;
            free(tmp);
            tmp = pointer;
        }
        free(pointer);
    }
    return true;
}