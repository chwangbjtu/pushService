#include<iostream>

#include "mongo_processor.h"


using namespace std;

int main()
{
    mongo_processor * pmp = new mongo_processor();
    pmp->init();

    return 0;
}
