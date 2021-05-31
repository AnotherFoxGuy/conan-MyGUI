from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool

class MyGUIConan(ConanFile):
    name = "MyGUI"
    version = "3.4.1"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-MyGUI"
    description = "Fast, flexible and simple GUI."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths"
    exports_sources = "source/*"

    def requirements(self):
        self.requires.add('OGRE/[1.x]@anotherfoxguy/stable')
        if os_info.is_windows:
            self.requires.add('zlib/[1.x]')
            self.requires.add('freetype/[2.x]')

    def source(self):
        tools.replace_in_file("source/CMake/InstallResources.cmake", "if (MYGUI_RENDERSYSTEM EQUAL 3)", "if (FALSE)")
        tools.replace_in_file("source/CMakeLists.txt", "set(CMAKE_MODULE_PATH", "set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR}")
        tools.replace_in_file("source/CMakeLists.txt", "# MYGUI BUILD SYSTEM", "include(${CMAKE_BINARY_DIR}/conan_paths.cmake)")
        tools.replace_in_file("source/CMakeLists.txt", "# Set up the basic build environment", 
        '''
        find_library(ZLIB_LIBRARY NAMES zlib zlib_d PATH_SUFFIXES lib REQUIRED)
        find_library(FREETYPE_LIBRARY NAMES freetype freetype_d freetyped PATH_SUFFIXES lib REQUIRED)
        find_library(LIBPNG_LIBRARY NAMES libpng16 libpng16_d libpng16d PATH_SUFFIXES lib REQUIRED)
        find_library(BZIP2_LIBRARY NAMES bz2 bz2_d bz2d PATH_SUFFIXES lib REQUIRED)
        ''')
        tools.replace_in_file("source/MyGUIEngine/CMakeLists.txt", "target_link_libraries(${PROJECTNAME} ${FREETYPE_LIBRARIES})", 
            "target_link_libraries(${PROJECTNAME} ${FREETYPE_LIBRARIES} ${LIBPNG_LIBRARY} ${BZIP2_LIBRARY})")
        tools.replace_in_file("source/CMakeLists.txt", "# Provide CPack packaging target", 
        '''
        include(FeatureSummary)
        feature_summary(WHAT ALL)
        ''')
            

    def build(self):
        cmake = CMake(self)
        cmake.definitions['MYGUI_BUILD_DEMOS'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_DOCS'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_TEST_APP'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_PLUGINS'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_TOOLS'] = 'OFF'
        cmake.configure(source_folder="source")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ['include/MYGUI']
        self.cpp_info.libdirs = ['lib', 'lib/release', 'lib/debug']	 # Directories where libraries can be found
        self.cpp_info.libs = tools.collect_libs(self)
