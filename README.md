# Verifying-Bidirectional-Drive-Coverage-in-HVSLI-Data

## Problem Statement
The given problem was to verify the bidirectional drive coverage which refers to a road network data collected in both directions, i.e. forward and reverse, to ensure complete coverage of a route. This way of collecting data ensures that the data is not biased towards one direction of movement. The provided data contained a gps route map of the drive from the HVSLI (High Value Street Level Imagery) data.  

### Bi-directional data
Provided bidirectional data contained mapped route of the drive defined in three video_code attributes, with each route mapped with its latitude and longitude location trace (GPS trace) at each point.
<br>

![Bi-directional-data](https://github.com/user-attachments/assets/c06d1ea4-4cdf-4a81-9c15-ab50be1f3fc8)
<br>

The below segment of csv file describes the data
| Video_code            | Geometry                                                               |
| ----------------- | ------------------------------------------------------------------ |
| 1 | MULTILINESTRING ((72.55535354623741 23.058550000000004, 72.55527181564638 23.058600000000002),... |
| 2 | LINESTRING (72.58360723313228 23.066200000000006),...|
| 3 | LINESTRING (72.54353143255115 23.025300000000005),... |

## Observations from the data
1. The state of a drive is always either single drive or multiple drive.
2. Drive routes have a returning curve or route when completing a section of a bidirectional drive.
3. If bidirectional drive routes are considered as parallel lines, there may be a case where if angle between two drive lines may be close to zero.

## Arrived Conclusion from the observations
1. Check if drive is bidirectional or not.
2. Check whether two lines are nearly parallel within a given angle threshold.

## Our Solution 

### Bidirectional Drive Coverage Checker

1. **Loads and Cleans Data:**  
   - Uses GeoPandas to load a shapefile (with associated files like `.dbf`, `.shx`, etc.).
   - Explodes multipart geometries and fixes invalid ones.

2. **Computes Directional Attributes:**  
   - Calculates the orientation (angle) of each drive route.
   - Uses an angle-based function to test whether two segments are nearly parallel.

3. **Spatial Analysis:**  
   - Constructs an R-tree spatial index for efficient neighbor searches.
   - For each drive segment, it finds nearby segments within a dynamic threshold (based on geometry length) and checks for parallelism.  
   - Segments that lack a sufficiently nearby and parallel neighbor are flagged as "bidirectional errors" (i.e. potentially incomplete drive coverage).

4. **Visualization and Export:**  
   - Visualizes the valid routes (in blue) and flagged errors (in red dashed lines) on an interactive map, with centroids labeled by latitude and longitude.
   - Exports the error geometries as a new shapefile.

This enables us to quickly identify drive segments with incomplete bidirectional coverage using standard GIS file formats.

---

### After Verification of Bi-directional data
![Figure_1](https://github.com/user-attachments/assets/2f65b83f-17c6-47ce-8e77-87c6125ec0f3)
![Error1-gis](https://github.com/user-attachments/assets/81a61ce6-5b35-46f5-ba74-8c4631318e0f)
![Error1](https://github.com/user-attachments/assets/572a5cd4-9807-4e50-86eb-0aa7daa6c0b4)
![Error2-gis](https://github.com/user-attachments/assets/22c818ba-0be0-445a-bf55-ac71224b19d3)
![Error2](https://github.com/user-attachments/assets/c43e822c-1e4e-4f04-8948-8f35818467a2)
![Error3-gis](https://github.com/user-attachments/assets/21de09dd-4936-4475-9249-13ddc87e7037)
![Error3](https://github.com/user-attachments/assets/12ca222b-c9f2-4145-bc71-9a95eaba8014)
![Error4-gis](https://github.com/user-attachments/assets/37f9e205-4126-4677-b71e-63bec775371f)
![Error4](https://github.com/user-attachments/assets/551f76d7-2704-4a9b-b29c-9473aea6ec42)
