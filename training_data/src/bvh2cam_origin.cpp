/***
 * Takes a bvh-file, depth-image and timestamp as input, and creates a
 * pair of ground truth keypoints and depth maps that will be used when
 * training the network.
 */

//コメントは日本語にできるよう!

#include "terminal_colors.h"

#define INCORRECT_USAGE_MSG "Incorrect usage. Please use the format:"
#define HELP_MSG "./prep_data PATH_TO_BerkeleyMHAD"
#define CORRECT_ARG_NUM 2

#define PRINT_ERR() fprintf(stderr, RED "%s\n%s\n" RESET, INCORRECT_USAGE_MSG, HELP_MSG)


#include <stdio.h>

int
main(int argc, char *argv[])
{

  if (argc != CORRECT_ARG_NUM) { PRINT_ERR(); return 0; }

  
  
  return 0;
}

