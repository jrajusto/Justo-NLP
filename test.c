// Online C compiler to run C program online
#include <stdio.h>

int main() {
    // Write C code here
    int firstNum;
    int secondNum;
    do{
        printf("Please enter first number: ");
        scanf("%d",&firstNum);

        if(firstNum > 1000)
        printf("Please enter a number less than 1000. \n");
    }
    while (firstNum > 1000);
    printf("Please enter second number: ");
    return 0;
    
}