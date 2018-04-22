#include <iostream>
#include <ctime>
#include <string>
#include <cstdlib>

using namespace std;

void afiseaza(){
    cout << "Hello world!" << endl;
}

int main()
{
    afiseaza();
    srand(time(NULL));
    unsigned int numberToGuess = rand() % 100;

    cout << "Guess a number between 0 and 99"<<endl;

    unsigned int playersNumber {};
    cin >> playersNumber;

    cout << "you guessed: "
        << playersNumber
        << " The actual number was: "
        << numberToGuess
        <<endl;
    return 0;
}
