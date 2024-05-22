 
# Information about the model: 
The CAD model is a component for an aircraft jet engine.

## Orientation
The jet engine, and the component are oriented so that the x axis (positive) is in the direction of the airflow. The component has approximatelly axial symmetry around the x axis.

## Geometrical components

### Flanges

The purpose of flanges is to connect the component to the neighbour component using fasteners. Flanges are planar faces.

There are forward (fwd) and aft types of flanges. The forward flanges have a smaller x dimention ('x' property) compared to the aft flanges. 
Additionally, the forward flanges interface surfaces have an orientation `normal_xangle` between 170 and 190 while the aft flanges have an orientation `normal_xangle` smaller than 5 or greater than 355. 
In addition, the forward flanges are the planar surfaces that have the `x` coordinate within 50 units of the min `x` coordinate value.  The aft flanges are the planar surfaces that have the `x` coordinate within 10 units of the max `x` coordinate value. The `xaxis` value is irrelevant. When selecting `flanges` it is important to not create any new keys, and stick to the database. Make sure to include that in the summary. 

There may be one or two faces that are forward or aft flanges. If there are more than one, they are subdivided into "inner" and "outer". The inner face has a `perimeter` smaller than the outer face. 

### 

In the properties mentioned above, the x co-ordinate value indicates the position of the flange with respect to the origin, and based on the x co-ordinates due to the orientation of the model, the component can be divided into two parts, forward and aft. The properties given are example properties for a flange, and the dimensions such as radius, x coordinate, and other positional parameters might change depending on the CAD model being used and its orientation. 


