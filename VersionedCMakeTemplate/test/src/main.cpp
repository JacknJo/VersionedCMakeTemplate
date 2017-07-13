#include <iostream>

#include "utils.hpp"
#include "testexecutable_jversion.hpp"

int main()
{
    std::cout << "Testing library with cmake." << std::endl;

    Utils::PrintVersion();
    Tools::JVersion::testExecutable::PrintVersion();

    std::cout << " Utils result = " << Utils::Add(5, 3) << std::endl;

    return 0;
}
