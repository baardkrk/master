BIOVISION HIERARCHICAL DATA
===========================

Notes are gathered from (wisc)[1]

Developed by biovision, and is used in many motion capture applications. (Especially
games and animation applications) It lack a full definition of the basis pose (without
specific placements for the segments described in the "frames" section, the segments of
the skeleton are not fully defined.). So, if you open a bvh file without any recoreded
frames, the segments will be connected, but no meaningful basis pose will be rendered.

Parsing
-------

Begins with `HIERARCHY` keyword, followd by `ROOT <name>`. On the next line is a curly
brace, indicating the start of the information of that segment.
Next, we have the `OFFSET` from the parent segment. in the `ROOT` segment the offset will
generally be zero. (It isn't in our case, since it is defined from the world zero
coordinate .. I think...)

Behind the `OFFSET` keyword, we have the x, y and z offset of this segment from the
parent. Example:
```
HIERARCHY
ROOT hips
{
	OFFSET 0 0 0
	CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
```
The offset is also used to infer how to draw the length and direction of the *parent*
segment. In BVH files, no information is given as to *how* to draw the segments, whcih is
why we use the offset information in the child to infer this.
However, with the root and upper body segments we will have multiple children. We'll come
back to how to draw these segments later (I hope).

The next line indicates some `CHANNELS` header information. First, we have the number of
channels in this segment. Then we have a list of the labels for each channel. While
parsing the BVH file, we must keep track of how many channels we have encountered, and the
order in which these appear. For example, we first encountered the 'hip' joint with 6
channels, XYZpositions and ZXYrotations. The next segment in the hierarchy is 'spine'
which only contains 3 channels: ZXYrotations and so on.

On the next line, we will find either the keyword `JOINT <name>` or `End site`. In the
first case, we continue describing the `OFFSET` information and `CHANNELS`. We can then go
on to describe yet another child, or we get the `End site` keyword, which provides us with
the last bit of information about the parent segment.
The number of `CHANNELS` in the `JOINT` segments are different from the ones in the `ROOT`
segment. We only have the rotation information in addition to the `OFFSET`. We therefore
have to recursively infer the XYZpositions of each joint based on the offsets and the XYZ
position of the `ROOT` segment.
At the `End site` this recursion ends, and we will begin the recursion on the next `JOINT`
or we'll have a fully defined skeleton, and the recursion terminates.

In the BVH hierarchy the world coordinates are defined as a right hand coordinate system
with the Y axis as the 'up' vector.

Example of a very simple skeleton framework:
```
HIERARCHY
ROOT hip
{
	OFFSET 0 0 0
	CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
	JOINT spine
	{
		OFFSET 0 1 0
		CHANNELS 3 Zrotation Xrotation Yrotation
		JOINT neck
		{
			OFFSET 0 6 0
			CHANNELS 3 Zrotation Xrotation Yrotation
			End Site
			{
				OFFSET 0 2 0
			}
		JOINT RArm
		{
			OFFSET -3 1 0
			CHANNELS 3 Zrotation Xrotation Yrotation
			JOINT RForearm
			{
				OFFSET -6 1 0
				CHANNELS 3 Zrotation Xrotation Yrotation
				End site
				{
					OFFSET -8 1 0
				}
			}
		}
	}
}

```

The motion section of the file begins with the keyword `MOTION`. It is then followed by
the number of frames in the file, and the time (in seconds) each frame lasts. The rest of
the file is the actual motion data, with each sample (or frame) on one line each.

Interpreting the data
---------------------

First, we create a transformation matrix from the *local translation and rotation
information for that segment*. For any segment, the *translation* information will simply
be the `OFFSET` as defined in the `HIERARCHY` section. The rotation data comes from the
`MOTION` section.
For the `ROOT` object, the translation data will be the sum of the `OFFSET` data and the
translation data from the `MOTION` section. The BVH format doesn't account for scale, so
it isn't neccessary to include a scale factor for calculation.


BVH uses Tait-Bryan angles, multiplied with the YXZ configuration.
if we have rotation matrices


[1]: https://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/BVH.html
