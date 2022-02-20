
import numpy as np
import cv2

#The following collection of pixel locations and corresponding relative
#ground plane locations are used to compute our homography matrix

# PTS_IMAGE_PLANE units are in pixels
######################################################
## DUMMY POINTS -- ENTER YOUR MEASUREMENTS HERE
PTS_IMAGE_PLANE = [[240, 372],
                    [2, 372],
                    [332, 192],
                    [258, 192],
                    [189, 192],
		    [403, 192],
		    [476, 192],
                    [332, 207],
                    [235, 207],
                    [142, 207],
                    [432, 207],
                    [532, 207],
                    [332, 238],
                    [173, 238],
                    [9, 238],
                    [499, 238],
                    [658, 238]] # dummy points
######################################################

# PTS_GROUND_PLANE units are in inches
# camera looks along positive x axis with positive y axis to left

######################################################
## DUMMY POINTS -- ENTER YOUR MEASUREMENTS HERE
PTS_GROUND_PLANE = [[0, 0],
		    [0, -13],
		    [-60, 0],
                    [-60, -15],
                    [-60, -30],
                    [-60, 15],
		    [-60, 30],
		    [-40, 0],
		    [-40, -15],
                    [-40, -30],
                    [-40, 15],
                    [-40, 30],
		    [-20, 0],
                    [-20, -15],
                    [-20, -30],
                    [-20, 15],
                    [-20, 30]]
 # dummy points
######################################################

METERS_PER_INCH = 0.0254


class HomographyTransformer:
    def __init__(self):

        if not len(PTS_GROUND_PLANE) == len(PTS_IMAGE_PLANE):
            print("ERROR: PTS_GROUND_PLANE and PTS_IMAGE_PLANE should be of same length")

        #Initialize data into a homography matrix

        np_pts_ground = np.array(PTS_GROUND_PLANE)
        np_pts_ground = np_pts_ground * METERS_PER_INCH
        np_pts_ground = np.float32(np_pts_ground[:, np.newaxis, :])

        np_pts_image = np.array(PTS_IMAGE_PLANE)
        np_pts_image = np_pts_image * 1.0
        np_pts_image = np.float32(np_pts_image[:, np.newaxis, :])

        self.h, err = cv2.findHomography(np_pts_image, np_pts_ground)



    def transformUvToXy(self, u, v):
        """
        u and v are pixel coordinates.
        The top left pixel is the origin, u axis increases to right, and v axis
        increases down.
        Returns a normal non-np 1x2 matrix of xy displacement vector from the
        camera to the point on the ground plane.
        Camera points along positive x axis and y axis increases to the left of
        the camera.
        Units are in meters.
        """
        homogeneous_point = np.array([[u], [v], [1]])
        xy = np.dot(self.h, homogeneous_point)
        scaling_factor = 1.0 / xy[2, 0]
        homogeneous_xy = xy * scaling_factor
        x = homogeneous_xy[0, 0]
        y = homogeneous_xy[1, 0]
        return x, y

transformer = HomographyTransformer()

# ex//
print(transformer.transformUvToXy(50, 50))