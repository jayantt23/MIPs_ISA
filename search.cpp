#include <iostream>
#include <vector>
using namespace std;

int main()
{
    vector<int> array = {1, 4, 3, 2, 7, 6};
    int search_value = 5;
    int index_result = -1;

    for (int i = 0; i < array.size(); ++i)
    {
        if (array[i] == search_value)
        {
            index_result = i;
            break;
        }
    }

    cout << "Index of " << search_value << " in the array is: " << index_result << endl;

    return 0;
}
