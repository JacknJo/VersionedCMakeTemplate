#!/usr/bin/python3

import sys
import datetime
import subprocess
import os
import re
import getpass

def generate(debugFlag):
    now = datetime.datetime.now()

    vMajor = '0'
    vMinor = '0'
    vPatch = '0'
    vRevision = '0'
    vHash = '0'
    vBuild = 0

    try:
        f = open('.version', 'r')
        vBuild = int(f.read())
        f.close()
    except FileNotFoundError:
        vBuild = 0

    vBuild+=1

    f = open('.version', 'w')
    f.write(str(vBuild))
    f.close()

    FNULL = open(os.devnull, 'w')
    ######### GIT VERSION CONTROL
    try:
        retString = subprocess.check_output(["git", "describe", "--tags", "--long", "--always"], stderr=FNULL)
    except subprocess.CalledProcessError:
        retString = None

    if retString:
        info = re.search("v(\d*).(\d*).(\d*)-(\d*)-(\w*)\\n", retString.decode("ascii")).groups()
        vMajor = info[0]
        vMinor = info[1]
        vPatch = info[2]
        vRevision = info[3]
        vHash = info[4]
    else:
        ######### SVN VERSION CONTROL
        try:
            retString = subprocess.check_output(["svn", "info"], stderr=FNULL)
        except subprocess.CalledProcessError:
            retString = None

        if retString:
            print(retString)
            vRevision = re.search("Revision: (\d*)", retString.decode("utf8")).groups()[0]
            info = re.search("URL: (\S*)", retString.decode("utf8")).groups()
            url = re.sub("/trunk", "/tags", info[0])

            retString = subprocess.check_output(["svn", "ls", url], stderr=FNULL)
            tags=retString.decode("ascii").split('\n')
            info = re.search("v(\d*).(\d*).(\d*)", tags[len(tags) - 2]).groups()
            vMajor = info[0]
            vMinor = info[1]
            vPatch = info[2]

    print("### generateHeader.py")
    print("    Generated Header for v" + vMajor + "." + vMinor + "." + vPatch + "-" + vRevision + " " + vHash)
    FNULL.close()
    with open(str(sys.argv[2]), 'w') as f:
        projectName = str(sys.argv[1])
        f.write("// #############################################################################\n")
        f.write("// GENERATED FILE! DO NOT CHANGE! CHANGES WILL BE OVERWRITTEN!                 #\n")
        f.write("// This file was generated:                                                    #\n")
        f.write("//  - with: " + '{:67}'.format(__file__) +                                    "#\n")
        f.write("//  - by:   " + '{:67}'.format(getpass.getuser()) +                           "#\n")
        f.write("//  - on:   " + '{:67}'.format(str(now.time())) +                             "#\n")
        f.write("//  - at:   " + '{:67}'.format(str(now.date())) +                             "#\n")
        f.write("// Due to the it's structure the file can only be included once. This is in-   #\n")
        f.write("// teded to be the library or the main class that is under version control. To #\n")
        f.write("// extract the version information defined herein in the code it's recommended #\n")
        f.write("// to use a static wrapper method which calls the here defined PrintVersion.   #\n")
        f.write("// This header allows to search for symbols in the generated binary with the   #\n")
        f.write("// 'getVersion.sh' script to obtain it's version contents without running it.  #\n")
        f.write("// #############################################################################\n")
        f.write("#pragma once\n")
        f.write("#include <stdint.h>\n")
        f.write("#include <iostream>\n")
        f.write("#include <cstdio>\n")
        f.write("\n")
        f.write("namespace Tools\n")
        f.write("{\n")
        f.write("    namespace JVersion\n")
        f.write("    {\n")
        f.write("        class " + projectName + "\n")
        f.write("        {\n")
        f.write("        public:\n")
        f.write("            static const uint32_t VERSION_MAJOR_REF;\n")
        f.write("            static const uint32_t VERSION_MINOR_REF;\n")
        f.write("            static const uint32_t VERSION_PATCH_REF;\n")
        f.write("            static const uint32_t VERSION_REVISION_REF;\n")
        f.write("            static const uint32_t BUILD_YEAR_REF;\n")
        f.write("            static const uint32_t BUILD_MONTH_REF;\n")
        f.write("            static const uint32_t BUILD_DAY_REF;\n")
        f.write("            static const uint32_t BUILD_HOUR_REF;\n")
        f.write("            static const uint32_t BUILD_MINUTE_REF;\n")
        f.write("            static const uint32_t BUILD_SECOND_REF;\n")
        f.write("            static const uint32_t BUILD_NUMBER_REF;\n")
#         f.write("            static constexpr uint32_t VERSION_MAJOR_REF    = " + vMajor + ";\n")
#         f.write("            static constexpr uint32_t VERSION_MINOR_REF    = " + vMinor + ";\n")
#         f.write("            static constexpr uint32_t VERSION_PATCH_REF    = " + vPatch + ";\n")
#         f.write("            static constexpr uint32_t VERSION_REVISION_REF = " + vRevision + ";\n")
#         f.write("            static constexpr uint32_t BUILD_YEAR_REF       = " + str(now.year) + ";\n")
#         f.write("            static constexpr uint32_t BUILD_MONTH_REF      = " + str(now.month) + ";\n")
#         f.write("            static constexpr uint32_t BUILD_DAY_REF        = " + str(now.day) + ";\n")
#         f.write("            static constexpr uint32_t BUILD_HOUR_REF       = " + str(now.hour) + ";\n")
#         f.write("            static constexpr uint32_t BUILD_MINUTE_REF     = " + str(now.minute) + ";\n")
#         f.write("            static constexpr uint32_t BUILD_SECOND_REF     = " + str(now.second) + ";\n")
#         f.write("            static constexpr uint32_t BUILD_NUMBER_REF     = " + str(vBuild) + ";\n")
        if debugFlag:
            f.write("            static const uint32_t IS_DEBUG_REF;\n\n")
        else:
            f.write("\n")
        f.write("            static void PrintVersion()\n")
        f.write("            {\n")
        f.write("                std::cout << \"  Version details of " + projectName + ":\" << std::endl;\n")
        f.write("                std::cout << \"    v\" << VERSION_MAJOR_REF <<\n")
        f.write("                                 \".\" << VERSION_MINOR_REF <<\n")
        f.write("                                 \".\" << VERSION_PATCH_REF <<\n")
        f.write("                                 \" Revision: \" << VERSION_REVISION_REF << std::endl;\n")
        if not debugFlag:
            f.write("                std::printf(\"    Build #%d - %02d.%02d.%04d, %02d:%02d:%02d\\n\",\n")
        else:
            f.write("                std::printf(\"    %s build #%d - %02d.%02d.%04d, %02d:%02d:%02d\\n\",\n")
            f.write("                                 IS_DEBUG_REF ? \"Debug\" : \"Release\",\n")
        f.write("                                 BUILD_NUMBER_REF, BUILD_DAY_REF, BUILD_MONTH_REF, BUILD_YEAR_REF,\n")
        f.write("                                 BUILD_HOUR_REF, BUILD_MINUTE_REF, BUILD_SECOND_REF);\n")
        f.write("            }\n")
        f.write("        };\n\n")
        f.write("        const uint32_t " + projectName + "::VERSION_MAJOR_REF    = " + vMajor + ";\n")
        f.write("        const uint32_t " + projectName + "::VERSION_MINOR_REF    = " + vMinor + ";\n")
        f.write("        const uint32_t " + projectName + "::VERSION_PATCH_REF    = " + vPatch + ";\n")
        f.write("        const uint32_t " + projectName + "::VERSION_REVISION_REF = " + vRevision + ";\n")
        f.write("        const uint32_t " + projectName + "::BUILD_YEAR_REF       = " + str(now.year) + ";\n")
        f.write("        const uint32_t " + projectName + "::BUILD_MONTH_REF      = " + str(now.month) + ";\n")
        f.write("        const uint32_t " + projectName + "::BUILD_DAY_REF        = " + str(now.day) + ";\n")
        f.write("        const uint32_t " + projectName + "::BUILD_HOUR_REF       = " + str(now.hour) + ";\n")
        f.write("        const uint32_t " + projectName + "::BUILD_MINUTE_REF     = " + str(now.minute) + ";\n")
        f.write("        const uint32_t " + projectName + "::BUILD_SECOND_REF     = " + str(now.second) + ";\n")
        f.write("        const uint32_t " + projectName + "::BUILD_NUMBER_REF     = " + str(vBuild) + ";\n")
        if debugFlag:
            f.write("        const uint32_t " + projectName + "::IS_DEBUG_REF         = " + str(int(debugFlag)) + ";\n")
        f.write("    }\n")
        f.write("}\n")

if __name__ == "__main__":
        if len(sys.argv) == 3:
            generate(False)
        elif len(sys.argv) == 4:
            generate(True)
        else:
                print('skipped generating the version header. No output file specified!')
