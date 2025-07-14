cmake_minimum_required(VERSION 3.14)

# Enable testing
enable_testing()

find_package(yaml-cpp REQUIRED)

target_link_libraries(graphlang_lib PRIVATE yaml-cpp)



# Include FetchContent module
include(FetchContent)

# Download GTest
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/release-1.12.1.zip
)

# Make it available
FetchContent_MakeAvailable(googletest)

# Add test executable
add_executable(graphlang_tests
    test_node_store.cpp
)

# Link against gtest and your library
target_link_libraries(graphlang_tests
    PRIVATE
        graphlang_lib
        GTest::gtest
        GTest::gtest_main
        yaml-cpp
        )  # <--- this closing parenthesis was missing

# Add tests to CTest
include(GoogleTest)
gtest_discover_tests(graphlang_tests)
