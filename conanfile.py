from conans import ConanFile, CMake, tools
from conans.tools import os_info


class MyGUIConan(ConanFile):
    name = "MyGUI"
    version = "3.2.3"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-MyGUI"
    description = "Fast, flexible and simple GUI."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def requirements(self):
        self.requires.add('OGRE/[1.x]@anotherfoxguy/stable')
        if os_info.is_windows:
            self.requires.add('zlib/[1.x]@conan/stable')
            self.requires.add('freetype/[2.x]@bincrafters/stable')

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/MyGUI/mygui.git")
        git.checkout("0726ed4ae70b3479677a794a6a3dd5d6cc48ed62")

        tools.replace_in_file("CMake/InstallResources.cmake", "if (MYGUI_RENDERSYSTEM EQUAL 3)", "if (FALSE)")

        tools.replace_in_file("CMakeLists.txt", "# Find dependencies",
                              "find_library(ZLIB_LIBRARY NAMES zlib zlib_d PATH_SUFFIXES lib)")

        tools.replace_in_file("CMakeLists.txt", "set(CMAKE_MODULE_PATH", "set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR}")

        if os_info.is_windows:
            tools.replace_in_file("CMakeLists.txt", "# Set up the basic build environment", '''  
                                    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                                    conan_basic_setup(TARGETS)''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions['MYGUI_BUILD_DEMOS'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_DOCS'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_TEST_APP'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_PLUGINS'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_TOOLS'] = 'OFF'
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ['include/MYGUI']
        self.cpp_info.libdirs = ['lib', 'lib/release', 'lib/debug']  # Directories where libraries can be found
        self.cpp_info.libs = tools.collect_libs(self)
