#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_WORD_LENGTH 30
#define ALPHABET_SIZE 26

// function to get index of a character ('a' = 0, 'z' = 25)
int getCharIndex(char c) {
    return c - 'a';
}

typedef struct Node {
    char word[MAX_WORD_LENGTH + 1];
    struct Node *prev, *next;
} Node;

Node *head = NULL; // head pointer for the doubly linked list

// forward declarations of functions
void loadStringsFromFile(char *filename);
void printStrings();
void radixSort();
void addWord(char *word);
void deleteWord(char *word);
void saveToFile(char *filename);
void freeList();
void showMenu();

int main() {
    showMenu();
    return 0;
}

void showMenu() {
    int choice;
    char filename[100];
    char word[MAX_WORD_LENGTH + 1];

    do {
        // display options menu
        printf("\nMenu:\n");
        printf("1. Load the strings from file\n");
        printf("2. Print the strings before sorting\n");
        printf("3. Sort the strings\n");
        printf("4. Print the sorted strings\n");
        printf("5. Add a new word to the list\n");
        printf("6. Delete a word from the list\n");
        printf("7. Save to output file\n");
        printf("8. Exit\n");
        printf("Enter your choice: ");
        scanf(" %d", &choice);
        puts("");
        switch (choice) {
            case 1:
                printf("Enter filename to load: ");
                scanf(" %s", filename);
                puts("");
                loadStringsFromFile(filename);
                break;
            case 2:
                printStrings();
                break;
            case 3:
                radixSort();
                puts("Sorted Successfully");
                break;
            case 4:
                printStrings();
                break;
            case 5:
                printf("Enter a new word: ");
                scanf(" %s", word);
                puts("");
                addWord(word);
                radixSort();
                puts("Added Successfully");
                break;
            case 6:
                printf("Enter a word to delete: ");
                scanf(" %s", word);
                puts("");
                deleteWord(word);
                break;
            case 7:
                printf("Enter filename to save: ");
                scanf(" %s", filename);
                puts("");
                saveToFile(filename);
                puts("Saved Successfully");
                break;
            case 8:
                // free all allocated memory
                freeList();
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 8);
}

void addWord(char *word) {
    // create a new node and add it to the front of the list
    Node *newNode = (Node *)malloc(sizeof(Node));
    if (!newNode) {
        perror("Unable to allocate memory for new node");
        exit(EXIT_FAILURE);
    }
    strcpy(newNode->word, word);
    newNode->next = head;
    newNode->prev = NULL;
    if (head != NULL) {
        head->prev = newNode;
    }
    head = newNode;
}

void deleteWord(char *word) {
    // delete a word from the list if it exists
    Node *temp = head;
    while (temp != NULL) {
        if (strcmp(temp->word, word) == 0) {
            if (temp->prev != NULL) {
                temp->prev->next = temp->next;
            } else {
                head = temp->next;
            }
            if (temp->next != NULL) {
                temp->next->prev = temp->prev;
            }
            free(temp);
            puts("Deleted Successfully");
            return;
        }
        temp = temp->next;
    }
    printf("Word not found.\n");
}

void printStrings() {
    // print all strings in the list
    Node *current = head;
    while (current != NULL) {
        printf("%s\n", current->word);
        current = current->next;
    }
}

void saveToFile(char *filename) {
    // save the list of words to a file
    FILE *file = fopen(filename, "w");
    if (!file) {
        perror("Error opening file");
        return;
    }
    Node *current = head;
    while (current != NULL) {
        fprintf(file, "%s\n", current->word);
        current = current->next;
    }
    fclose(file);
}

void freeList() {
    // free all nodes in the list
    Node *current = head;
    while (current != NULL) {
        Node *next = current->next;
        free(current);
        current = next;
    }
    head = NULL;
}

int findMaxStringLength() {
    // find the length of the longest string in the list
    int maxLen = 0;
    Node *current = head;
    while (current != NULL) {
        int len = strlen(current->word);
        if (len > maxLen) {
            maxLen = len;
        }
        current = current->next;
    }
    return maxLen;
}

int tolower(int ch) {
    // convert character to lowercase if uppercase
    if (ch >= 'A' && ch <= 'Z') {
        return ch - 'A' + 'a';
    }
    return ch;
}

void radixSort() {
    // implementation of radix sort for sorting the strings
    int maxLen = findMaxStringLength();
    Node *buckets[ALPHABET_SIZE + 1], *tailBuckets[ALPHABET_SIZE + 1]; // +1 for the 'empty' character bucket

    for (int i = maxLen - 1; i >= 0; i--) {
        // initialize buckets for each character
        for (int j = 0; j <= ALPHABET_SIZE; j++) {
            buckets[j] = NULL;
            tailBuckets[j] = NULL;
        }

        // distribute strings into buckets based on their characters
        Node *temp = head;
        while (temp) {
            int index;
            if (i < strlen(temp->word)) {
                index = getCharIndex(tolower(temp->word[i])); // convert to lowercase
            } else {
                index = ALPHABET_SIZE; // bucket for 'empty' character
            }

            // adding node to the appropriate bucket
            if (buckets[index] == NULL) {
                buckets[index] = temp;
            } else {
                tailBuckets[index]->next = temp;
            }
            temp->prev = tailBuckets[index]; // linking previous pointer
            tailBuckets[index] = temp;
            temp = temp->next;
        }

        // reconstruct the list from the buckets
        head = NULL;
        Node *last = NULL;
        for (int j = 0; j <= ALPHABET_SIZE; j++) {
            if (buckets[j]) {
                if (!head) {
                    head = buckets[j];
                } else {
                    last->next = buckets[j];
                    buckets[j]->prev = last;
                }
                last = tailBuckets[j];
            }
        }
        if (last) {
            last->next = NULL; // ensure the last node's next is null
        }
    }
}

void loadStringsFromFile(char *filename) {
    // load strings from a file and add them to the list
    FILE *file = fopen(filename, "r");
    char buffer[MAX_WORD_LENGTH + 1];

    if (file == NULL) {
        perror("Error opening file");
        return;
    }

    while (fgets(buffer, MAX_WORD_LENGTH + 1, file)) {
        // remove newline character if present
        buffer[strcspn(buffer, "\n")] = 0;
        addWord(buffer);
    }
    puts("Read Successfully");
    fclose(file);
}
