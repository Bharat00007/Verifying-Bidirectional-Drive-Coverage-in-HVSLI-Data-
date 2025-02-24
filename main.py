import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString, MultiLineString, Point
from rtree import index
import math


def load_data(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    gdf = gdf.explode(index_parts=False).reset_index(drop=True)
    gdf["geometry"] = gdf["geometry"].apply(lambda x: x if x.is_valid else x.buffer(0))
    return gdf


def calculate_angle(line):
    start, end = list(line.coords)[0], list(line.coords[-1])
    dx, dy = end[0] - start[0], end[1] - start[1]
    return math.degrees(math.atan2(dy, dx)) % 180  


def is_parallel(line1, line2, angle_threshold=10):
    """Check if two lines are nearly parallel within a given angle threshold."""
    angle1 = calculate_angle(line1)
    angle2 = calculate_angle(line2)
    return np.isclose(angle1, angle2, atol=angle_threshold) or np.isclose(abs(angle1 - angle2), 180, atol=angle_threshold)


def build_spatial_index(gdf):
    """Builds an R-tree spatial index for efficient nearest-neighbor searches."""
    spatial_index = index.Index()
    for i, row in gdf.iterrows():
        spatial_index.insert(i, row.geometry.bounds)
    return spatial_index


def check_bidirectional_coverage(gdf, angle_threshold=30, parallel_threshold=10, distance_factor=0.2):
    errors = []
    spatial_index = build_spatial_index(gdf)

    for i, row1 in gdf.iterrows():
        is_covered = False
        possible_neighbors = list(spatial_index.intersection(row1.geometry.bounds))

        for j in possible_neighbors:
            if i != j:
                row2 = gdf.iloc[j]
                distance = row1.geometry.distance(row2.geometry)

                
                dynamic_threshold = max(row1.geometry.length, row2.geometry.length) * distance_factor

                parallel = is_parallel(row1.geometry, row2.geometry, parallel_threshold)

                if distance <= dynamic_threshold and parallel:
                    is_covered = True
                    break 

        if not is_covered:
            errors.append(row1.geometry)
            angle = calculate_angle(row1.geometry)
            print(f"❌ Line {i} is an ERROR | Angle: {angle:.2f}°")

    return errors


def visualize_errors(gdf, bidirectional_errors):
    fig, ax = plt.subplots(figsize=(12, 8))

    error_gdf = gpd.GeoDataFrame(geometry=bidirectional_errors, crs=gdf.crs)
    non_error_gdf = gdf[~gdf.geometry.isin(bidirectional_errors)].copy()

    path_color = "blue"

    if not non_error_gdf.empty:
        non_error_gdf.plot(ax=ax, color=path_color, linewidth=1, label="Valid Paths")

    
    if not error_gdf.empty:
        error_gdf.plot(ax=ax, color=path_color, linewidth=2, linestyle="dashed", label="Bidirectional Errors")

   
    for i, row in gdf.iterrows():
        centroid = row.geometry.centroid
        lat, lon = centroid.y, centroid.x  
        print(f"Segment {i}: Latitude = {lat:.6f}, Longitude = {lon:.6f}") 
        ax.text(lon, lat, f"({lat:.4f}, {lon:.4f})", fontsize=8, ha='center', color='black')

    ax.set_title("Bidirectional Coverage Errors with Lat-Long")
   
    plt.show()





def export_errors(errors, output_path, crs):
    error_gdf = gpd.GeoDataFrame(geometry=errors, crs=crs)
    error_gdf.to_file(output_path)
    print(f"Error detection complete! Results saved as {output_path}")


shapefile_path = r"Bidirectional_drive_coverage\Drive_data.shp"
output_path = "map_errors.shp"
gdf = load_data(shapefile_path)
bidirectional_errors = check_bidirectional_coverage(gdf)
visualize_errors(gdf, bidirectional_errors)
export_errors(bidirectional_errors, output_path, gdf.crs)
