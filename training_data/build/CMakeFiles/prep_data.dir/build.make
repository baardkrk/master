# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/baard/master/training_data

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/baard/master/training_data/build

# Include any dependencies generated for this target.
include CMakeFiles/prep_data.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/prep_data.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/prep_data.dir/flags.make

CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o: CMakeFiles/prep_data.dir/flags.make
CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o: ../src/bvh2cam_origin.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/baard/master/training_data/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o -c /home/baard/master/training_data/src/bvh2cam_origin.cpp

CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/baard/master/training_data/src/bvh2cam_origin.cpp > CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.i

CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/baard/master/training_data/src/bvh2cam_origin.cpp -o CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.s

CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o.requires:

.PHONY : CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o.requires

CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o.provides: CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o.requires
	$(MAKE) -f CMakeFiles/prep_data.dir/build.make CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o.provides.build
.PHONY : CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o.provides

CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o.provides.build: CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o


# Object files for target prep_data
prep_data_OBJECTS = \
"CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o"

# External object files for target prep_data
prep_data_EXTERNAL_OBJECTS =

prep_data: CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o
prep_data: CMakeFiles/prep_data.dir/build.make
prep_data: CMakeFiles/prep_data.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/baard/master/training_data/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable prep_data"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/prep_data.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/prep_data.dir/build: prep_data

.PHONY : CMakeFiles/prep_data.dir/build

CMakeFiles/prep_data.dir/requires: CMakeFiles/prep_data.dir/src/bvh2cam_origin.cpp.o.requires

.PHONY : CMakeFiles/prep_data.dir/requires

CMakeFiles/prep_data.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/prep_data.dir/cmake_clean.cmake
.PHONY : CMakeFiles/prep_data.dir/clean

CMakeFiles/prep_data.dir/depend:
	cd /home/baard/master/training_data/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/baard/master/training_data /home/baard/master/training_data /home/baard/master/training_data/build /home/baard/master/training_data/build /home/baard/master/training_data/build/CMakeFiles/prep_data.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/prep_data.dir/depend

