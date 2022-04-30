# Segmentation To Vector Conversion

Convert a segmented image into a vector.

## Steps
1. Find segmentations (i.e. find contours)
   * If there bounding box around a contour is very large, just ignore it
2. Group contours into "superlines" (i.e. group dashed lines)
3. Approximate these superlines as vectors

## Brain Storm with Jason
* High-Level Problem
	* Fit segmentation to vector
* Questions for ROS
	* What outputs do they want? Vectorized data of all contours? Or group certain contours and treat them as one thing. E.g. dashed lines.
	* Just provide polynomials of _each_ contour? And maybe domain of x? (a b c lower_x upper_x)
	* TODO just ask KJ. Polyn fit of each or contour bounding box?
* Random thoughts
	* Horizontal lines/splotches - TODO filter lines that are too square
	* Horizontal vs non-horizontal line - TODO filter bounding boxes that are nearly horizontal
	* Histogram approach to fitting line - TODO look into this???
	* Maybe no grouping. Just return polynomial in a package of contours + polynomial fits
