# Find GTest package
find_package(GTest CONFIG REQUIRED)

# Enable testing for this directory
enable_testing()

# Add test executable
add_executable(graphlang_tests
    test_node_store.cpp
)

# Link against gtest and our library
target_link_libraries(graphlang_tests
    PRIVATE
        graphlang_lib
        GTest::gtest
        GTest::gtest_main
)

# Add tests to CTest
include(GoogleTest)
gtest_discover_tests(graphlang_tests)