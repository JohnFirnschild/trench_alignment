"""
If you think that wasn't worth it, here is the abbreviated version!

Identify the owned fibercables by OBJECTID below in the
list: fc_oid_list.  Alternatively, you could utilize
the list: unique_values above in Step 6.

The script will create the following:

!!Beta testing Not currently pointing to EDIT!!
Feature Layers of the FiberCables in fc_oid_list
so you can easily manipulate the specific object from GIS_EDIT
while keeping the map as read only for the most part.

"""
import required_libraries

# rest of your code goes here
# Track overall time
start_time = time.time()

# fc_oid_list = unique_values
fc_oid_list = [323365, 493534, 337906]

# Create an empty list
cable_name_list = []
# Create a list of fLayers to easily delete later
fLayer_list = []

# If this makes sense and we're ready to roll, switch it to NXPRD3_GIS_EDIT
# fiber = r"\\nadnp1b_cifs.corp.intranet\NNSGIS3\ArcMap\Connections\NXPRD3_GIS_EDIT.sde\NX_DATA.TelecomDatasetProjection\NX_DATA.FiberCable"
fiber = r"\\nadnp1b_cifs.corp.intranet\NNSGIS3\ArcMap\Connections\NXPRD3_GISREAD.sde\NX_DATA.TelecomDatasetProjection\NX_DATA.FiberCable"
            
# Use a Search Cursor to extract the CABLE_NAME values
with arcpy.da.SearchCursor(fiber, ["OBJECTID", "CABLE_NAME"]) as cursor:
    for row in cursor:
        object_id, cable_name = row
        if object_id in fc_oid_list:
            cable_name_list.append(cable_name)
            
            
# print(fc_oid_name)
# print(cable_name_list)

# Iterate through the cable_name_list and create feature layers
for cable_name in cable_name_list:
    # Define the SQL Expression to select the features with the current CABLE_NAME
    sql_expression = f"CABLE_NAME = '{cable_name}'"
    
    # Create a feature layer for the current CABLE_NAME
    feature_layer_name = f"EDIT{cable_name}" # add replace steps to fix punctuation in FC Name 
    feature_layer_name = feature_layer_name.replace(" ","").replace("(","_").replace(")","_").replace(".","_")
    arcpy.MakeFeatureLayer_management(fiber, feature_layer_name, sql_expression)
    fLayer_list.append(feature_layer_name)
    # call the result with print
    print(f"Feature Layer for CABLE_NAME: {cable_name} created as: {feature_layer_name}")
    
end_time = time.time()
elapsed_time = round((end_time-start_time) / 60, 2)
print(f"Overall processing time: {elapsed_time} minutes")
print("Happy hunting!")