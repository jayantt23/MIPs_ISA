#include <stdio.h>

int main()
{
    int array[] = {1, 4, 3, 2, 7, 6};
    int array_size = sizeof(array) / sizeof(array[0]);
    int search_value = 7;
    int index_result = -1;

    for (int i = 0; i < array_size; ++i)
    {
        if (array[i] == search_value)
        {
            index_result = i;
            break;
        }
    }

    printf("Index of %d in the array is: %d\n", search_value, index_result);

    return 0;
}