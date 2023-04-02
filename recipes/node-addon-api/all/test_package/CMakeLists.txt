cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(node-addon-api REQUIRED CONFIG)

add_library(${PROJECT_NAME} SHARED test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE node-addon-api::node-addon-api)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
set_target_properties(${PROJECT_NAME} PROPERTIES PREFIX "" SUFFIX ".node")

if(APPLE)
  # not using "LINKER:" in the options below, the XCode 12 new buildsystem has issues handling -XLinker options
  target_link_options(${PROJECT_NAME} PRIVATE "-Wl,-undefined,dynamic_lookup")
elseif(LINUX)
  target_link_options(${PROJECT_NAME} PRIVATE "LINKER:--export-dynamic")
elseif(WIN32)
  # On windows, we need to use extra glue code to intercept the loading: the following is copied
  # from node-gyp, see node_modules\npm\node_modules\node-gyp\src in the NodeJS distribution.
  # The HOST_BINARY refers to the symbols in node.exe referenced by the node.lib link library.
  set(HOST_BINARY "node.exe")
  set_property(TARGET ${PROJECT_NAME} APPEND PROPERTY SOURCES win32/win_delay_load_hook.cc)
  target_compile_definitions(${PROJECT_NAME} PRIVATE "BUILDING_NODE_EXTENSION" "HOST_BINARY=\"${HOST_BINARY}\"")
  # tell the linker to delay loading for the symbols referenced in the node.lib link library.
  target_link_options(${PROJECT_NAME} PRIVATE "LINKER:/DELAYLOAD:${HOST_BINARY}")
  target_link_options(${PROJECT_NAME} PRIVATE "LINKER:/SUBSYSTEM:CONSOLE")
  target_link_libraries(${PROJECT_NAME} PRIVATE DelayImp.lib)
endif()
