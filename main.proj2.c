#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

// expression tree data structure
struct ExpTreeNode {
    char data[10];
    struct ExpTreeNode *leftNode;
    struct ExpTreeNode *rightNode;
};

// takes a string and creates a node using it to append to tree
struct ExpTreeNode *createTreeNewNode(char data[]) {
    struct ExpTreeNode *newNode = (struct ExpTreeNode *) malloc(sizeof(struct ExpTreeNode));
    strcpy(newNode->data, data);// copy dfta to the node data
    newNode->leftNode = newNode->rightNode = NULL;// set right and left node to NULL for possible leaf node
    return newNode;// return the allocated newNOde
}

// checks if the given character is an arethmatic operator(-, +, /, *, %) and return true if so, false otherwise
bool isArithmeticOperator(char character) {
    // list of valid arithmetic operators
    char arithmeticOperators[] = {'+', '-', '*', '/', '%'};

    // determine if the character is one of the valid operators
    for (int i = 0; i < sizeof(arithmeticOperators) / sizeof(arithmeticOperators[0]); ++i) {
        if (character == arithmeticOperators[i]) {
            // the character is a valid arithmetic operator
            return true;
        }
    }

    // the character is not valid
    return false;
}

// takes a postfix and loads it in the expression tree
struct ExpTreeNode *loadPostfixToTree(char *equationPostfix) {
    struct ExpTreeNode *stack[100];// stack to manipulate the nodes
    int top = -1;// initialize stack empty
    // loop in postfix until the end
    for (int i = 0; i < strlen(equationPostfix); ++i) {
        if(equationPostfix[i] == '\0')
            break;// if we reached the end of equation break
        int j = 0;// index for data string
        if (isalnum(equationPostfix[i])) {
            char data[10] = "";// reset the stored data string
            while (isalnum(equationPostfix[i])) {
                data[j] = equationPostfix[i];// create data
                j++;// update indexes
                i++;// index for equations post
            }
            i--;// correct the extra 1 to continue the loop
            stack[++top] = createTreeNewNode(data);
        } else if (isArithmeticOperator(equationPostfix[i])) {// check if the char is an operator
            char data[] = {equationPostfix[i],
                           '\0'};// if so create a node with the operand as the only character in the data string
            struct ExpTreeNode *curr = createTreeNewNode(data);
            curr->rightNode = stack[top];// right node gets the right part of the equation
            top--;
            curr->leftNode = stack[top];// left node gets the left part of the equation
            top--;
            stack[++top] = curr;// append the opperand to stack to be appended to the tree
        }
    }
    return stack[top];// raturn the tree head node
}
// returns the percednce value of the arethmatic operand
int prec(char c) {
    if (c == '+' || c == '-')
        return 1;
    if (c == '/' || c == '*' || c == '%') {
        return 2;
    }
    return 0;
}

// takes the equation from a line in the file and converts it to post fix
char *convertInfixPostfix(char equationInfix[]) {
    char stack[128];// stack to handle the characters
    int top = -1;
    char *equationPostfix = (char *) malloc(128 * sizeof(char));// allocate this array because we want to return it
    // we can't return a normal array because it will be freed at the end of the function
    // i is for the infix equation, j is for postfix
    int i, j;
    for (i = 0, j = 0; i < strlen(equationInfix); i++) {
        if (equationInfix[i] == ' ')
            continue;
        if (isdigit(equationInfix[i])) {// if it is a digit the keep looping until we get all the numbers
            while (isalnum(equationInfix[i])) {
                // append all digit chars to post fix
                equationPostfix[j] = equationInfix[i];
                j++;
                i++;
            }
            i--;// correct the extra 1 because it will be incremented in the loop
            equationPostfix[j++] = ' ';
        } else if (equationInfix[i] == '(') {// if an open bracket the we append it to stack
            top++;// top + 1 because we start from -1
            stack[top] = equationInfix[i];
        } else if (equationInfix[i] == ')') {// if close bracket then pop all elements until
            // the open bracket or end of stack
            while (top > -1 && stack[top] != '(') {
                equationPostfix[j] = stack[top];// everything is added to postfix
                j++;
                top--;
                equationPostfix[j++] = ' ';// seperate all elements with a white space
            }
            top--;// correct the extra 1 because it will be incremented in the loop
        } else if (isArithmeticOperator(equationInfix[i])) {
            while (top > -1 && prec(stack[top]) >= prec(equationInfix[i])) {// append every thing with lower prec to post fix
                equationPostfix[j] = stack[top];
                top--;
                j++;
            }
            top++;
            // top of the stack will be the character with the highest prec
            stack[top] = equationInfix[i];
            equationPostfix[j++] = ' ';
        }

    }
    // if we reached the end and still some operators in stack append every thing to postfix
    // and if there is an open bracket which wasnt closed then the equation is inoprable and invalid
    while (top > -1) {
        if (stack[top] == '(') {
            return "equation is ivalid";
        }
        equationPostfix[j] = stack[top];
        top--;
        j++;
        equationPostfix[j] = ' ';
        j++;

    }
    equationPostfix[j] = '\0';

    return equationPostfix;
}
// evaluate the result using expression tree
int findTreeResult(struct ExpTreeNode *treeHead) {
    if (treeHead == NULL) {
        puts("Some error in tree(NULL)");
        return 0;
    }
    // if the string is a number then we reach a node without any left and riht nodes so we dont traverse any further
    if (isdigit(treeHead->data[0])) {
        return strtol(treeHead->data, NULL, 10);
    }
    // get the value using recursion of each child
    int leftValue = findTreeResult(treeHead->leftNode);
    int rightValue = findTreeResult(treeHead->rightNode);
// if the operation is division or modulo then if the right node VALUE = 0 (denominator = 0) we cant continue
    if (treeHead->data[0] == '/' || treeHead->data[0] == '%') {
        if (rightValue == 0)
            return 0;
    }
    // return value based on operation
    switch (treeHead->data[0]) {
        case '-':
            return leftValue - rightValue;
        case '+':
            return leftValue + rightValue;
        case '*':
            return leftValue * rightValue;
        case '%':
            return leftValue % rightValue;
        case '/':
            return leftValue / rightValue;
        default:
            exit(EXIT_FAILURE);
    }
}

// main functio that reads the files and display the menu
int main() {

    // open input file for reading
    FILE *PtrFileRead = fopen("in.txt", "r");

    // open output file for writing
    FILE *PtrFileWrite = fopen("out.txt", "w");

    // variable to store user option selection
    int c = 1;

    // character array to store user input
    char in[128];

    // 2D array to store input equations from file
    char equations[128][128];

    // variable to track number of equations read from file
    int eqSize = 0;

    // 2D array to store postfix expressions
    char postfixes[128][128];

    // display menu and get option selection in loop
    while (c >= 1 && c <= 6) {

        // print menu options
        printf("select one:\n");
        printf("1- read equations from file \n");
        printf("2- print equations from file(infix) \n");
        printf("3- find the equation result using expression tree(after converting to postfix) \n");
        printf("4- print postfix expressions (using stack)\n");
        printf("5- Save to output file (postfix and results) \n");
        printf("6- End Program\n");

        // get user selection
        scanf("%s", in);

        // convert to integer
        c = strtol(in, NULL, 10);

        // validate input
        if (c < 1 || c > 6)
            continue;

        // option 1 - read equations from file
        if (c == 1) {

            // go to start of file
            rewind(PtrFileRead);

            // read equations line by line
            int fIdx = 0;
            while (fgets(in, 128, PtrFileRead)) {
                strcpy(equations[fIdx], in);
                fIdx++;
            }

            // store number of equations
            eqSize = fIdx;

            // print success message
            printf("file read successfully");
        }

            // option 2 - print input equations
        else if (c == 2) {

            // validate equations were read
            if (eqSize == 0) {
                puts("no equations yet! you must choose option 1 first");
                continue;
            }

            // print all equations
            for (int i = 0; i < eqSize; ++i) {
                printf("%d. %s\n", i + 1, equations[i]);
            }
        }

            // option 3 - evaluate equations
        else if (c == 3) {

            // validate equations
            if (eqSize == 0) {
                puts("no equations yet! you must choose option 1 first");
                continue;
            }

            // evaluate each equation
            for (int i = 0; i < eqSize; ++i) {

                // convert to postfix
                char *equationPostfix = convertInfixPostfix(equations[i]);

                // build expression tree
                struct ExpTreeNode *treeHead = loadPostfixToTree(equationPostfix);

                // evaluate tree
                int result = findTreeResult(treeHead);

                // print original, postfix, and result
                printf("%d. infix: %s", i + 1, equations[i]);
                printf("postfix: %s\nresult = %d\n\n", equationPostfix, result);
            }

        }

            // option 4 - print postfix expressions
        else if (c == 4) {

            // validate equations
            if (eqSize == 0) {
                puts("no equations yet! you must choose option 1 first");
                continue;
            }

            // print postfix version of each
            for (int i = 0; i < eqSize; ++i) {
                char *equationPostfix = convertInfixPostfix(equations[i]);
                printf("%d. postfix: %s\n", i + 1, equationPostfix);
            }
        }

            // option 5 - write results to file
        else if (c == 5) {

            // go to start of file
            rewind(PtrFileWrite);

            // validate equations
            if (eqSize == 0) {
                puts("no equations yet! you must choose option 1 first");
                continue;
            }

            // evaluate and write each equation
            for (int i = 0; i < eqSize; ++i) {

                // convert equation
                char *equationPostfix = convertInfixPostfix(equations[i]);

                // build expression tree
                struct ExpTreeNode *treeHead = loadPostfixToTree(equationPostfix);

                // evaluate tree
                int result = findTreeResult(treeHead);

                // write postfix and result to file
                fprintf(PtrFileWrite, "%d. postfix: %s\nresult = %d\n\n", i + 1, equationPostfix, result);
            }

            // go to start of file
            rewind(PtrFileWrite);

            // print success message
            puts("written to file successfully");
        }

            // option 6 - exit program
        else {
            fclose(PtrFileRead);
            fclose(PtrFileWrite);
            exit(0);
        }
    }
}





