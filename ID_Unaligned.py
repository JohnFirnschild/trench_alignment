"""
Now that you have your Span created from the Route let's take this opportunity to make sure everything is snappd.

You could just trace the Fibercables against the Span but let's overcomplicate it 

( ͡° ͜ʖ ͡°)

Identify the owned fibercables by OBJECTID below in the list: fc_oid_list.  
Alternatively, you could utilize the list: unique_values above in Step 6.

Once you have that sorted, run the script. 
You will be prompted to provide the OBJECTID of the Span we're working from.

The script will create the following:

!!Beta testing Not currently pointing to EDIT!!

Feature Layers of the FiberCables in fc_oid_list so you can easily manipulate the specific
object from GIS_EDIT while keeping the map as read only for the most part.

Polygon outputs used to identify where the Span and Fibercable are not snapped.

At this point, you could zip around with Topology enabled and align edge from the results, 
or you may find tracing is a better option.

"""

# Track overall time
start_time = time.time()

# Use List extract method above to pull Object ID's of Features
fc_oid_list = unique_values
# fc_oid_list = [323365, 493534, 337906, 478998, 362335, 308005]

# Create an empty list
cable_name_list = []
# Create a list of fLayers to easily delete later
fLayer_list = []
# Create a list of buffers to easily delete later
buffer_list = []
# Create a list of erased buffers to easily delete later
erase_list = []
# Create a list of exploded features to easily delete later
explode_list = []

# If this makes sense and we're ready to roll, switch it to NXPRD3_GIS_EDIT
# fiber = r"\\nadnp1b_cifs.corp.intranet\NNSGIS3\ArcMap\Connections\NXPRD3_GIS_EDIT.sde\NX_DATA.TelecomDatasetProjection\NX_DATA.FiberCable"
fiber = r"\\nadnp1b_cifs.corp.intranet\NNSGIS3\ArcMap\Connections\NXPRD3_GISREAD.sde\NX_DATA.TelecomDatasetProjection\NX_DATA.FiberCable"
span = r"\\nadnp1b_cifs.corp.intranet\NNSGIS3\ArcMap\Connections\NXPRD3_GISREAD.sde\NX_DATA.TelecomDatasetProjection\NX_DATA.span"
explode_style = r"J:\Heather\LVLT_DUCT\EXPLODE_STYLE.lyrx"

span_oid = input("What is the OBJECTID of Span related to the Fibercables being reshaped?: ")
span_sql = f"OBJECTID = {span_oid}"
span_name = "Working_Span"
arcpy.management.MakeFeatureLayer(span, span_name, span_sql)
# arcpy.management.MakeFeatureLayer(r"J:\ArcMap\Connections\NXPRD3_GISREAD.sde\NX_DATA.TelecomDatasetProjection\NX_DATA.span", "Working_Span", "OBJECTID = 1264337", None, "")
fLayer_list.append(span_name)
print(f"Area defined by Span OBJECTID: {span_oid}")
span_buff_name = "SPAN_BUFF"
arcpy.analysis.Buffer(span_name, span_buff_name, "10 Feet", "FULL", "ROUND", "NONE", None, "PLANAR")
buffer_list.append(span_buff_name)
print(f"This may take a while...")
print("----------------------------------------------------------------------------------------------------")
            
# Use a Search Cursor to extract the CABLE_NAME values
with arcpy.da.SearchCursor(fiber, ["OBJECTID", "CABLE_NAME"]) as cursor:
    for row in cursor:
        object_id, cable_name = row
        if object_id in fc_oid_list:
            cable_name_list.append(cable_name)
            
# print(cable_name_list)

# Iterate through the cable_name_list and create feature layers
for cable_name in cable_name_list:
    # Track geoprocessing time
    gp_start_time = time.time()
    # Define the SQL Expression to select the features with the current CABLE_NAME
    sql_expression = f"CABLE_NAME = '{cable_name}'"
    
    # Create a feature layer for the current CABLE_NAME
    feature_layer_name = f"EDIT{cable_name}" # add replace steps to fix punctuation in FC Name 
    feature_layer_name = feature_layer_name.replace(" ","").replace("(","_").replace(")","_").replace(".","_")
    feature_layer_name = feature_layer_name.replace("_001","")
    arcpy.MakeFeatureLayer_management(fiber, feature_layer_name, sql_expression)
    fLayer_list.append(feature_layer_name)
    # call the result with print
    # print(f"Feature Layer for CABLE_NAME: {cable_name} created as: {feature_layer_name}")
    
    # Create Buffers for each Feature Layer
    buffer_name = f"{feature_layer_name}_buff"
    arcpy.analysis.Buffer(feature_layer_name, buffer_name, "10 Feet", "FULL", "ROUND", "NONE", None, "PLANAR")
    buffer_list.append(buffer_name)
    # call the result with print
    # print(f"Buffer created for {buffer_name}")
    
    # Erase FiberCable Buffers from Span Buffer
    # To identify areas where geometry needs attention
    erase_output_name = buffer_name
    erase_output_name = erase_output_name.replace("EDIT", "ERASE").replace("_buff", "")
    arcpy.analysis.Erase(buffer_name, span_buff_name, erase_output_name, None)
    erase_list.append(erase_output_name)
    # call the result with print
    # print(f"Buffer {buffer_name} erased by {erase_output_name}")
    
    # Multipart to Singlepart
    explode_output_name = erase_output_name
    explode_output_name = explode_output_name.replace("ERASE", "EXPLODE")
    arcpy.management.MultipartToSinglepart(erase_output_name, explode_output_name)
    explode_list.append(explode_output_name)
    
    # Apply Layer symbology for easy visibility
    arcpy.management.ApplySymbologyFromLayer(explode_output_name, explode_style, None, "DEFAULT")
    
    # Get Count
    count = arcpy.management.GetCount(explode_output_name)
    print(f"You have {count} locations to investigate for {cable_name}")    
    gp_end_time = time.time()
    gp_elapsed_time = round((gp_end_time-gp_start_time) / 60, 2)
    print(f"Elapsed time for {explode_output_name}: {gp_elapsed_time} minutes")
    print("----------------------------------------------------------------------------------------------------")
    
# print (fLayer_list)
arcpy.Delete_management(buffer_list)
arcpy.Delete_management(erase_list)
arcpy.Delete_management(span_name)

end_time = time.time()
elapsed_time = round((end_time-start_time) / 60, 2)
print(f"Overall processing time: {elapsed_time} minutes")
print("Happy hunting!")