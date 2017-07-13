set(PROJECT_NAME TestLibrary)

cmake_minimum_required(VERSION 3.7)
# set(CMAKE_VERBOSE_MAKEFILE 1)

# Set variables
string(TOLOWER ${CMAKE_BUILD_TYPE} LOWERCASE_TYPE)
string(TOLOWER ${PROJECT_NAME} LOWERCASE_PROJECT_NAME)

# Define the sources to be compiled here.
set(SOURCES
    src/utils.cpp
)

execute_process(COMMAND issue.sh
    OUTPUT_VARIABLE ISSUE
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

add_custom_command(OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/include/${LOWERCASE_PROJECT_NAME}_jversion.hpp
    # COMMAND generateHeader.py ${PROJECT_NAME} include/${LOWERCASE_PROJECT_NAME}_jversion.hpp ${LOWERCASE_TYPE}
    COMMAND generateHeader.py ${PROJECT_NAME} include/${LOWERCASE_PROJECT_NAME}_jversion.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS ${SOURCES}
)

add_custom_target(CODE_GENERATION
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/include/${LOWERCASE_PROJECT_NAME}_jversion.hpp
)

# Add custom include directories here.
include_directories(
    include
    ../include
)

# Add library with project name as target.
add_library(${PROJECT_NAME} STATIC ${SOURCES})
add_dependencies(${PROJECT_NAME} CODE_GENERATION)

# Create symbolic links post build.
add_custom_command(TARGET ${PROJECT_NAME}
    POST_BUILD
    COMMAND mkdir -p lib/${ISSUE}
    COMMAND mkdir -p lib/${LOWERCASE_TYPE}
    COMMAND unlink lib/${ISSUE}/$<TARGET_FILE_NAME:${PROJECT_NAME}> > /dev/null 2>&1 | true
    COMMAND unlink lib/${LOWERCASE_TYPE}/$<TARGET_FILE_NAME:${PROJECT_NAME}> > /dev/null 2>&1 | true
    COMMAND ln -s ../../build/${LOWERCASE_TYPE}/$<TARGET_FILE_NAME:${PROJECT_NAME}> lib/${ISSUE}
    COMMAND ln -s ../../build/${LOWERCASE_TYPE}/$<TARGET_FILE_NAME:${PROJECT_NAME}> lib/${LOWERCASE_TYPE}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
