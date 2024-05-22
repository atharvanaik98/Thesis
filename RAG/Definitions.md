# Information about the model: 
The CAD model is an aerospace component from an aircraft jet engine. 

# Orientation of the model 
The model is oriented in such a way that the direction of airflow is always indicated by the X-axis. 
This indicates that in the case of a circular model symmetric about the center will have its center lying on the x-axis. 

## Positional References: 
In the properties mentioned above, the x co-ordinate value indicates the position of the flange with respect to the origin, and based on the x co-ordinates due to the orientation of the model, the component can be divided into two parts, forward and aft. The properties given are example properties for a flange, and the dimensions such as radius, x coordinate, and other positional parameters might change depending on the CAD model being used and its orientation. 

## Geometrical Components 

### Boltholes
Boltholes are `cylindrical` features with small radii, especially when compared to `flanges`, and usually present on flanges which allow the flanges to be securely fastened, allowing for an airtight seal. Boltholes usually have a radius that is possibly the smallest in the model, with `normal_xangle` between 80 and 100  and `normal_yangle` also between 80 and 100. Boltholes can have positions in either the forward or aft sections of the model, depending on which flange they are present on. The boltholes in the aft have their maximum `x` co-ordinates within 10 units of the maximum `x` co-ordinate value. The xaxis value is irrelevant. For forward and aft sections of the model, the same rules and positional references apply as those used for flanges. 



### Strut-fillets 
Strut-fillets are connecting faces of the blend type that connect struts to the main body of the model. They are scattered around a space, each pointing in a different direction. Some are tilted, some are upright. Each corner piece has a number on it to identify it. We can describe each corner piece by its size, its exact location in the space, and the direction it's pointing. These usually have similar `radius` and `radius_minor` but a large `radius_major` indicating that they are sweeping curves. Strut fillets are usually positioned such that they have a `normal_xangle` somewhere between 100 and 180, and `normal_yangle` between 0 and 90 along with a `zaxis` value that is between 100 and 200. These faces have a `yzangle` between 0 and 360, which means they are spread out about the x axis. Consider a tolerance of 10 units in the properties.  

### Leading Edges 
Leading Edges of a geometrical feature are the edges that are position directly in the airflow, in this case edges that are perpendicular to the direction of airflow, in the forward section of the CAD model. 

### Trailing Edges 
Trailing Edges are the edges of a geometrical feature that face away from the direction of airflow but are still perpendicular to the direction of airflow, which means that these edges are present in the aftmost section of the CAD model. 

