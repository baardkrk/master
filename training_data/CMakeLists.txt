cmake_minimum_required( VERSION 2.6 )

project( bvh_and_depth_pairer )

include_directories( include )

add_executable( prep_data src/bvh2cam_origin.cpp )
