from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool

class MyGUIConan(ConanFile):
    name = "MyGUI"
    version = "3.2.3-OGRE-1.11.6-with-patches"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-MyGUI"
    description = "Fast, flexible and simple GUI."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths"

    def requirements(self):
        self.requires.add('OGRE/1.11.6-with-patches@anotherfoxguy/stable')
        if os_info.is_windows:
            self.requires.add('OGREdeps/[20.x]@anotherfoxguy/stable')

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/MyGUI/mygui.git")
        #git.checkout("07da0620e0d835346452b02b7b1ba7c583429736")
        tools.replace_in_file("CMake/InstallResources.cmake", "if (MYGUI_RENDERSYSTEM EQUAL 3)", "if (FALSE)")
        tools.replace_in_file("CMakeLists.txt", "set(CMAKE_MODULE_PATH", "set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR}")
        tools.replace_in_file("CMakeLists.txt", "# MYGUI BUILD SYSTEM", "include(conan_paths.cmake)")
        tools.replace_in_file("CMakeLists.txt", "# Set up the basic build environment", 
        '''
        find_library(ZLIB_LIBRARY NAMES zlib zlib_d PATH_SUFFIXES lib)
        find_library(FREETYPE_LIBRARY NAMES freetype freetype_d PATH_SUFFIXES lib)
        ''')

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
        self.cpp_info.libdirs = ['lib', 'lib/release', 'lib/debug']	 # Directories where libraries can be found
        self.cpp_info.libs = tools.collect_libs(self)
