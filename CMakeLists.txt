cmake_minimum_required(VERSION 3.15)

if(DEFINED ENV{VCPKG_ROOT} AND NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake")
endif()


# Turn off yaml-cpp testing and tools
set(YAML_CPP_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(YAML_CPP_BUILD_TOOLS OFF CACHE BOOL "" FORCE)

# Optionally suppress build output
set(FETCHCONTENT_QUIET ON)  # This will suppress most of the build output


project(graphlang VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(/usr/include)

find_package(OpenSSL REQUIRED)

enable_testing()

add_library(graphlang_lib
    src/node_store.cpp
    src/node.cpp
)

target_include_directories(graphlang_lib PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

include(FetchContent)
FetchContent_Declare(
    yaml-cpp
    GIT_REPOSITORY https://github.com/jbeder/yaml-cpp.git
    GIT_TAG yaml-cpp-0.7.0
)
FetchContent_MakeAvailable(yaml-cpp)

FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG release-1.12.1  # or whatever version you prefer
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)
# find_package(GTest REQUIRED)

target_link_libraries(graphlang_lib 
    # PRIVATE
    PUBLIC
      yaml-cpp
      OpenSSL::Crypto
      GTest::gtest
      GTest::gtest_main
)
add_executable(graphlang src/main.cpp)
target_link_libraries(graphlang PRIVATE graphlang_lib)

add_subdirectory(tests)