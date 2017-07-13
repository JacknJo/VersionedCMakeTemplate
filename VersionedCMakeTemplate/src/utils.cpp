#include "utils.hpp"

#include "testlibrary_jversion.hpp"

int Utils::Add(int a, int b)
{
    return a + b;
}

void Utils::PrintVersion()
{
    Tools::JVersion::TestLibrary::PrintVersion();
}
