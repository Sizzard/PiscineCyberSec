#include <string.h>
#include <stdio.h>

int main(void) {
    char res[114];
    int cmp = 0;

    printf("Please enter key: ");
    scanf("%s", &res[14]);
    if ( !strcmp(&res[14], "__stack_check") )
        printf("Good job.\n");
    else
        printf("Nope.\n");
    return 0;
}