# Step 5: Selecting Live data and used to define the Spans to delete and the route to create the new span.

arcpy.management.SelectLayerByLocation("Span_Owner_Like_Level3;Span_Owner_NOT_Like_Level3;Route_NB_Like_Level3;Route_NB_NOT_Like_Level3", "SHARE_A_LINE_SEGMENT_WITH", working_dissolve, None, "NEW_SELECTION", "NOT_INVERT")