# Segmentation To Vector Conversion

Convert a segmented image into a vector.

## Steps
1. Find segmentations (i.e. find contours)
   * If there bounding box around a contour is very large, just ignore it
2. Group contours into "superlines" (i.e. group dashed lines)
3. Approximate these superlines as vectors