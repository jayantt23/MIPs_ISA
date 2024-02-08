#include <iostream>

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
    std::cout << "Input array size ([0,5000]): ";
    std::cin >> n;

    int arr[n];
    for (int i = 0; i < n; ++i)
    {
        std::cout << "Input value " << i + 1 << ": ";
        std::cin >> arr[i];
    }

    std::cout << "Unsorted array given as input: ";

    for (int i = 0; i < n; ++i)
    {
        std::cout << arr[i] << " ";
    }

    std::cout << std::endl;

    insertionSort(arr, n);

    for (int i = 0; i < n; ++i)
    {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;

    return 0;
}
