#!/bin/bash

# This script creates a list of wget commands and downloads them in parallel:
# ./getParallel.sh -n [numThreads] -s "sequence1 sequence2 sequence3 ..."
numThreads=1
numKinectViews=10
sequences="none"
currDir=$(pwd)

if command -v wget >/dev/null 2>&1; then
    WGET="wget -c"
    mO="-O"
else
    echo "This script requires wget to download files."
    echo "Aborting."
    exit 1;
fi


while getopts "n:s:k:" args
do
    case $args in
	n)
	    numThreads=$OPTARG
	    ;;
	s)
	    IFS=', ' read -r -a sequences <<< $OPTARG
	    echo "Downloading ${#sequences[@]} sequences"
	    ;;
	k)
	    numKinectViews=$OPTARG
	    if [ $numKinectViews -gt 10 ] || [ $numKinectViews -lt 1 ]; then
		echo "Invalid number of kinect views. Must be in interval [1,10]"
		echo "Aborting"
		exit 1;
	    fi
	    ;;
	*)
	    echo "Did not understand input arguments."
	    exit 0
    esac
done

declare -a wgetURIList

if [ ${#sequences[@]} == 0 ]; then
    echo "need input sequences"
    exit 0
fi

for name in "${sequences[@]}"
do
    mkdir "$name" ##################################
    # Adding download for panoptic calibration data
    wgetURIList+=("$WGET $mO $name/calibration_$name.json http://domedb.perception.cs.cmu.edu/webdata/dataset/$name/calibration_$name.json")
    # Adding download for kinect calibration data
    wgetURIList+=("$WGET $mO $name/kcalibration_$name.json http://domedb.perception.cs.cmu.edu/webdata/dataset/$name/kinect_shared_depth/kcalibration_$name.json")
    # Download synctables data
    wgetURIList+=("$WGET $mO $name/synctables_$name.json http://domedb.perception.cs.cmu.edu/webdata/dataset/$name/kinect_shared_depth/synctables.json")
    wgetURIList+=("$WGET $mO $name/ksynctables_$name.json http://domedb.perception.cs.cmu.edu/webdata/dataset/$name/kinect_shared_depth/ksynctables.json")
    
    # Skipping download RGB videos
    ######################
    # Download kinect depth videos
    ######################
    nodes=(1 2 3 4 5 6 7 8 9 10)
    for (( c=0; c<$numKinectViews; c++ ))
    do
	# Create subfolder
	mkdir -p $name/kinect_shared_depth/KINECTNODE${nodes[c]} #################################
	fileName="kinect_shared_depth/KINECTNODE${nodes[c]}/depthdata.dat"
	wgetURIList+=("$WGET $mO $name/$fileName http://domedb.perception.cs.cmu.edu/webdata/dataset/$name/$fileName || rm -v $name/$fileName")
	# Delete if file is blank: || rm -v $name/$filename"
    done

    ######################
    # Download skeleton data
    # Coco 19 keypoint definition
    # by VGA index
    ######################
    wgetURIList+=("$WGET $mO $name/hdPose3d_stage1_coco19.tar http://domedb.perception.cs.cmu.edu/webdata/dataset/$name/hdPose3d_stage1_coco19.tar || rm -v $name/hdPose3d_stage1_coco19.tar")
    # Delete if file is blank: || rm -v $name/hdPose3d_stage1_coco19.tar
done


# Downloading all files.
# printf "%s\n" "${FILES[@]}" | xargs -i mv '{}' /path/to/destination
echo "Num Threads: $numThreads"
parallel --bar -P $numThreads ::: "${wgetURIList[@]}"
