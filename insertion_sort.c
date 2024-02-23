#include <stdio.h>

void insertionSort(int arr[], int n)
{
    for (int i = 1; i < n; ++i)
    {
        int value = arr[i];
        int j = i - 1;

        while (j >= 0 && arr[j] > value)
        {
            arr[j + 1] = arr[j];
            --j;
        }
        arr[j + 1] = value;
    }
}

int main()
{
    int n;
    printf("Input array size ([0,5000]): ");
    scanf("%d", &n);

    int arr[n];
    for (int i = 0; i < n; ++i)
    {
        printf("Input value %d: ", i + 1);
        scanf("%d", &arr[i]);
    }

    printf("Unsorted array given as input: ");

    for (int i = 0; i < n; ++i)
    {
        printf("%d ", arr[i]);
    }

    printf("\n");

    insertionSort(arr, n);

    for (int i = 0; i < n; ++i)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
