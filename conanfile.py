from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool

class MyGUIConan(ConanFile):
    name = "MyGUI"
    version = "3.2.3"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-MyGUI"
    description = "Fast, flexible and simple GUI."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths"

    def requirements(self):
        self.requires.add('OGREdeps/2018-07@anotherfoxguy/stable')
        self.requires.add('OGRE/1.9.1@anotherfoxguy/stable')

    def source(self):
        self.run("git clone --depth 1 https://github.com/MyGUI/mygui.git . ")
        tools.download("https://raw.githubusercontent.com/OGRECave/ogre/v1.9.1/CMake/Packages/FindOGRE.cmake", "FindOGRE.cmake")
        tools.replace_in_file("CMakeLists.txt", "set(CMAKE_MODULE_PATH", "set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR}")
        tools.replace_in_file("CMakeLists.txt", "# MYGUI BUILD SYSTEM", "include(conan_paths.cmake)")

    def build(self):
        cmake = CMake(self)
        cmake.definitions['MYGUI_BUILD_DEMOS'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_DOCS'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_TEST_APP'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_TOOLS'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_PLUGINS'] = 'OFF'
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["MyGUI"]
