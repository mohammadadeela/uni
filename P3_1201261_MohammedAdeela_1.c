/*
 * Mohammad adeela
 * 1201261
 * Section 1
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define HASH_TABLE_SIZE 100  // define the size of the hash tables

// structure representing a dictionary word with meanings
typedef struct {
    int isFilled;     // flag to check if the entry is used
    char word[30];    // the word
    char meanings[3][30]; // up to three meanings of the word
} Word;

Word table1[HASH_TABLE_SIZE]; // first hash table for words
Word table2[HASH_TABLE_SIZE]; // second hash table for words

int col_count1 = 0; // collision count for the first table
int col_count2 = 0; // collision count for the second table

// function to compare and display the number of collisions in both hash methods
void insertionCollisionsComparison() {
    // print the number of collisions for both tables
    printf("number of open addressing collisions: %d\n", col_count1);
    printf("number of open double hashing collisions: %d\n", col_count2);

    // compare and print which method had fewer collisions
    if (col_count1 < col_count2) {
        printf("open addressing here is better.\n");
    } else if (col_count1 > col_count2) {
        printf("double hashing here is better.\n");
    } else {
        printf("the two have same number of collisions\n");
    }
}

// calculate the hash index using double hashing method
int doubleHashIndex(const char *str) {
    long hashValue = 0, primePower = 1;

    // calculate the hash value for the first three characters of the string
    for (int i = 0; i < 3; i++) {
        // check if character is within valid ASCII range
        if ((int) str[i] > 127 || (int) str[i] < 0)
            break;
        hashValue += (int) str[i] * primePower;
        primePower *= 29;  // using a prime number for hash calculation
    }

    // return the calculated index within the bounds of the hash table size
    return (hashValue % HASH_TABLE_SIZE + HASH_TABLE_SIZE) % HASH_TABLE_SIZE;
}

// calculate the hash index using linear probing method
int linearProbIndex(const char *str) {
    long hashValue = 0;

    // calculate the hash value for the first three characters of the string
    for (int i = 0; i < 3; i++) {
        // check if character is within valid ASCII range
        if ((int) str[i] > 127 || (int) str[i] < 0)
            break;
        hashValue = hashValue * 29 + (int) str[i]; // using a prime number for hash calculation
    }

    // return the calculated index within the bounds of the hash table size
    return hashValue % HASH_TABLE_SIZE;
}

// insert a word into the second hash table using double hashing
void insertDoubleHashing(Word entry) {
    // calculate initial indexes
    int index1 = linearProbIndex(entry.word);
    int index2 = doubleHashIndex(entry.word);
    int i = 0;
    int index = (index1 + i * index2) % HASH_TABLE_SIZE;

    // iterate to find an empty slot, incrementing collision count
    while (table2[index].isFilled && i < HASH_TABLE_SIZE) {
        col_count2++;
        i++;
        index = (index1 + i * index2) % HASH_TABLE_SIZE;
    }

    // check if the table is full
    if (i == HASH_TABLE_SIZE) {
        printf("error, table is full '%s'\n", entry.word);
        return;
    }

    // insert the word into the table
    table2[index] = entry;
}

// insert a word into the first hash table using open addressing
void insertOpenAddressing(Word entry) {
    // calculate initial index
    int index = linearProbIndex(entry.word);
    int mainIndex = index;
    int i = 1;

    // iterate to find an empty slot, incrementing collision count
    while (table1[index].isFilled && i < HASH_TABLE_SIZE) {
        col_count1++;
        index = (mainIndex + i) % HASH_TABLE_SIZE;
        i++;
    }

    // check if the table is full
    if (i == HASH_TABLE_SIZE) {
        printf("error, table is full '%s'\n", entry.word);
        return;
    }

    // insert the word and its meanings into the table
    strcpy(table1[index].word, entry.word);
    strcpy(table1[index].meanings[0], entry.meanings[0]);
    strcpy(table1[index].meanings[1], entry.meanings[1]);
    strcpy(table1[index].meanings[2], entry.meanings[2]);
    table1[index].isFilled = entry.isFilled;
}

// read words from a file and insert them into both hash tables
void readFile(char *filename) {
    FILE *file;
    // open the file, exit if it cannot be opened
    if ((file = fopen(filename, "r")) == NULL) {
        printf("error file.\n");
        exit(1);
    }

    char line[100];
    // loop through the file line by line
    while (fgets(line, sizeof(line), file)) {

        // parse the line into word and meanings
        char word[30], meaning1[30], meaning2[30], meaning3[30];
        sscanf(line, "%[^:]:%[^#]#%[^#]#%[^\n]", word, meaning1, meaning2, meaning3);

        // create a word entry
        Word entry;
        strcpy(entry.word, word);
        strcpy(entry.meanings[0], meaning1);
        strcpy(entry.meanings[1], meaning2);
        strcpy(entry.meanings[2], meaning3);
        entry.isFilled = 1;

        // insert the word into both tables
        insertOpenAddressing(entry);
        insertDoubleHashing(entry);
    }
    // compare and display the number of collisions for both hash methods
    insertionCollisionsComparison();

    // close the file
    fclose(file);
}

// print the content of a hash table
void printTable(Word *table) {
    printf("index\tword\tmeanings\n");
    for (int i = 0; i < HASH_TABLE_SIZE; i++) {
        // print the word and its meanings if the slot is filled
        if (table[i].isFilled) {
            printf("%d\t%s\t", i, table[i].word);
            for (int j = 0; j < 3; j++) {
                // print each meaning if it's not NULL
                if (table[i].meanings[j] != NULL) {
                    printf("%s", table[i].meanings[j]);
                    if (j < 2 && table[i].meanings[j + 1] != NULL) {
                        printf(", ");
                    }
                }
            }
            printf("\n");
        } else {
            // print 'empty' for empty slots
            printf("%d\tempty\n", i);
        }
    }
}

// search for a word in the first table using linear probing
Word *searchTable1(char *word, Word *table) {
    // calculate initial index
    int index = linearProbIndex(word);
    int mainIndex = index;
    int i = 1;

    // iterate through the table to find the word
    while (!table[index].isFilled && strcmp(table[index].word, word) != 0 && i < HASH_TABLE_SIZE) {
        index = (mainIndex + i) % HASH_TABLE_SIZE;
        i++;
    }

    // return the word if found
    if (strcmp(table[index].word, word) == 0 && table[index].isFilled) {
        return &table[index];
    } else {
        return NULL; // return NULL if the word is not found
    }
}

// search for a word in the second table using double hashing
Word *searchTable2(char *word, Word *table) {
    // calculate initial indexes
    int index1 = linearProbIndex(word);
    int index2 = doubleHashIndex(word);
    int i = 0;
    int index = (index1 + i * index2) % HASH_TABLE_SIZE;

    // iterate through the table to find the word
    while (table[index].isFilled && i < HASH_TABLE_SIZE) {
        if (strcmp(table[index].word, word) == 0) {
            return &table[index]; // return the word if found
        }
        i++;
        index = (index1 + i * index2) % HASH_TABLE_SIZE;
    }

    return NULL; // return NULL if the word is not found
}

// delete a word from the first table
void deleteFromTable1(char *word, Word *table) {
    // calculate initial index
    int index = linearProbIndex(word);
    int mainIndex = index;
    int i = 1;

    // iterate through the table to find the word
    while (table[index].isFilled && i < HASH_TABLE_SIZE) {
        if (strcmp(table[index].word, word) == 0) {
            table[index].isFilled = 0; // mark the slot as empty
            printf("deleted successfully the hash table 1.\n", word);
            return;
        }
        index = (mainIndex + i) % HASH_TABLE_SIZE;
        i++;
    }

    printf("word '%s' DNE.\n", word); // print if the word does not exist
}

// delete a word from the second table using double hashing
void deleteFromTable2(char *word) {
    // calculate initial indexes
    int index1 = linearProbIndex(word);
    int index2 = doubleHashIndex(word);
    int i = 0;
    int index = (index1 + i * index2) % HASH_TABLE_SIZE;

    // iterate through the table to find the word
    while (table2[index].isFilled && i < HASH_TABLE_SIZE) {
        if (strcmp(table2[index].word, word) == 0) {
            table2[index].isFilled = 0; // mark the slot as empty
            printf("deleted successfully the hash table 2.\n", word);
            return;
        }
        i++;
        index = (index1 + i * index2) % HASH_TABLE_SIZE;
    }

    printf("word '%s' DNE.\n", word); // print if the word does not exist
}

// save the content of the second hash table into a file
void saveFile(char *filename, Word *table) {
    FILE *file = fopen(filename, "w");
    // exit if file cannot be opened
    if (!file) {
        printf("error opening file");
        exit(1);
    }

    // loop through the table and write each filled entry to the file
    for (int i = 0; i < HASH_TABLE_SIZE; i++) {
        if (table[i].isFilled) {
            fprintf(file, "%s:", table[i].word);
            for (int j = 0; j < 3; j++) {
                // write each meaning separated by '#'
                if (table[i].meanings[j] != NULL) {
                    fprintf(file, "%s", table[i].meanings[j]);
                    if (j < 2 && table[i].meanings[j + 1] != NULL) {
                        fprintf(file, "#");
                    }
                }
            }
            fprintf(file, "\n");
        }
    }

    fclose(file);
    printf("saved successfully\n");
}

// calculate the load factor of a hash table
double calcLoadFactor(Word *table) {
    int filledCount = 0;
    // count the number of filled entries
    for (int i = 0; i < HASH_TABLE_SIZE; i++) {
        if (table[i].isFilled) {
            filledCount++;
        }
    }
    // return the ratio of filled entries to total size
    return (double) filledCount / HASH_TABLE_SIZE;
}

// main function to drive the program
int main() {
    readFile("words.txt"); // read and process words from the file
    int choice;
    char word[30];
    Word entry;

    // loop to provide various operations
    do {
        puts("\nchoose an option please\n"
             "1. print tables\n"
             "2. Print out table size and the load factor. \n"
             "3. Print out the used hash functions. \n"
             "4. Insert a new record to hash table (insertion will be done on both hash tables). \n"
             "5. Search for a specific word (specify which table to search in). \n"
             "6. Delete a specific word (from both tables).\n"
             "7. Compare between the two methods in terms of number of collisions occurred. \n"
             "8. Save hash table back to a file named saved_words.txt\n"
             "9. terminate\n"
             "input your option: \n");
        scanf(" %d", &choice);

        // switch case to handle user input
        switch (choice) {
            case 1:
                printf("hash table 1:\n");
                printTable(table1); // print first hash table
                printf("\nhash table 2:\n");
                printTable(table2); // print second hash table
                break;
            case 2:
                printf("table size: %d\n", HASH_TABLE_SIZE); // print table size
                printf("load factor for table 1: %f\n", calcLoadFactor(table1)); // print load factor for table 1
                printf("load factor for table 2: %f\n", calcLoadFactor(table2)); // print load factor for table 2
                break;
            case 3:
                puts("hash1: Open Addressing\nhash2: Double Hashing");
                break;
            case 4:
                // prompt user to enter a word to insert
                printf("enter word to insert: \n");
                scanf(" %s", entry.word);

                // initialize the meanings of the word to empty strings
                for (int i = 0; i < 3; i++) {
                    strcpy(entry.meanings[i], "");
                }

                char meaning[30];
                // loop to get up to 3 meanings for the word
                for (int i = 0; i < 3; i++) {
                    printf("enter meaning %d (or -1 to skip): \n", i + 1);
                    scanf("%s", meaning);
                    // break the loop if user enters '-1'
                    if (0 == strcmp(meaning, "-1"))
                        break;
                    // copy the entered meaning to the entry
                    strcpy(entry.meanings[i], meaning);
                }

                // mark the entry as filled
                entry.isFilled = 1;

                // insert the word into both hash tables
                insertOpenAddressing(entry);
                insertDoubleHashing(entry);
                // compare the number of collisions in both insertion methods
                insertionCollisionsComparison();
                printf("word inserted.\n");
                break;
            case 5:
                // prompt user to enter a word to search for
                printf("enter word to search for: \n");
                scanf("%s", word);
                // ask user to choose which table to search in
                printf("select Table to search in (1 or 2): \n");
                int tableChoice;
                scanf("%d", &tableChoice);

                Word *found;
                // search in the specified table
                if (tableChoice == 1) {
                    found = searchTable1(word, table1);
                } else {
                    found = searchTable2(word, table2);
                }
                // if word is found, print it and its meanings
                if (found != NULL) {
                    printf("word found: %s\n", found->word);
                    printf("meaning/s: \n");
                    for (int i = 0; i < 3; i++) {
                        if (0 == strcmp(found->meanings[i], ""))
                            break;
                        printf("%d. %s\n", i + 1, found->meanings[i]);
                    }
                } else {
                    printf("word not found.\n");
                }
                break;
            case 6:
                // prompt user to enter a word to delete
                printf("enter word to delete: \n");
                scanf("%s", word);
                // delete the word from both tables
                deleteFromTable1(word, table1);
                deleteFromTable2(word);
                break;
            case 7:
                // compare the number of collisions again
                insertionCollisionsComparison();
                break;
            case 8:
                // save the second hash table to a file
                saveFile("saved_words.txt", table2);
                break;
            case 9:
                // exit the program
                printf("exiting program.\n");
                break;
            default:
                // handle invalid choice input
                printf("invalid choice. please try again.\n");
        }
    } while (choice != 9); // loop until user chooses to exit

    return 0;
}
