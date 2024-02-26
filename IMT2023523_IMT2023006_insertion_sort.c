#include <stdio.h>

int main()
{
    int array[] = {-2, 1, 0, 3, 2, -8, 6, 10, 9}; // Initial array to be sorted
    int size = 9;                                 // 9 elements in the array

    int i = 0, j, temp;
    while (i < size)
    {
        j = i;

        while (j > 0 && array[j] < array[j - 1])
        {

            temp = array[j];
            array[j] = array[j - 1];
            array[j - 1] = temp;
            j--;
        }
        i++;
    }

    printf("Sorted array: ");
    for (i = 0; i < size; i++)
    {
        printf("%d ", array[i]);
    }
    printf("\n");

    return 0;
}