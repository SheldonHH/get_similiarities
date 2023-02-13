#include <iostream>
#include <array>
using namespace std;

int foo(int i)
{
    return i + 5;
}

int main()
{
    int i = 10;
    std::array<int, foo(5)> arr; // OK
    
    foo(i); // Call is Ok
    
    // But...
    // std::array<int, foo(i)> arr1; // Error
   
}
 