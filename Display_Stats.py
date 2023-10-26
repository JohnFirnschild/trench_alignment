# Step 2: Displays statistics of file and makes a copy named *IN_PROGRESS
# 
# Add ST_County Trench data to working .aprx
# data is located in J:\Heather\LVLT_DUCT\SHP_OUT_original

# The follwing will derive unique values 
# from the working file to identify 
# valid/invalid input details.


arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"J:\Heather\LVLT_DUCT\Span_Project.gdb"
workspace = arcpy.env.workspace

# Get name of input file
working_file = input("What is the working file?: ")
wf_record_count = arcpy.management.GetCount(working_file)
print (f'Working File Record Count: {wf_record_count}')
# stats = arcpy.analysis.Statistics(fr"{working_file}", f"{working_file}_stats", "INSTALLATI UNIQUE;DEPTH_OF_C UNIQUE;SURFACE_RE UNIQUE;DUCT_COUNT UNIQUE;LEGACY_OWN UNIQUE;CONDUIT_DE UNIQUE;DUCT_MATER UNIQUE", "DEPTH_OF_C;DUCT_COUNT;INSTALLATI;LEGACY_OWN;CONDUIT_DE;SURFACE_RE;DUCT_MATER")
stats = arcpy.analysis.Statistics(fr"{working_file}", f"{working_file}_stats", "LEGACY_OWN UNIQUE;CONDUIT_DE UNIQUE", "CONDUIT_DE;LEGACY_OWN")
unique_record_count = arcpy.management.GetCount(stats)
print (f'Unique Value count: {unique_record_count}')
# structured_arr = arcpy.da.FeatureClassToNumPyArray(stats, ['INSTALLATI','DEPTH_OF_C','SURFACE_RE','DUCT_COUNT','LEGACY_OWN','CONDUIT_DE','DUCT_MATER'])
structured_arr = arcpy.da.FeatureClassToNumPyArray(stats, ['CONDUIT_DE', 'LEGACY_OWN'])

# Getting the field names
field_names = structured_arr.dtype.names
# Converting the structured array to a regular NumPy array
arr = np.array([tuple(row) for row in structured_arr.tolist()], dtype=object)
# I want this output to be more verbose and informative
df = pd.DataFrame(arr, columns=field_names)
print(df.to_string(index=False))
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# '''
# Create IN_PROGRESS version of the working file to calc fields and dissolve
# 
# '''
test_file = arcpy.conversion.FeatureClassToFeatureClass(working_file, workspace, f"{working_file}_IN_PROGRESS", '', '', '')

# Step 2a: Use this to make a feature layer to isolate records to dissolve
# Input value detail attributions based on the result of step 2
# Example: if you have 10 ducts and 12 ducts, create feature layers and dissolve with the next steps.

# duct_count = input("Number of ducts: ")

# arcpy.management.MakeFeatureLayer(test_file, f"{test_file}_{duct_count}_ducts", f"CONDUIT_DE LIKE '{duct_count}%'", None, "")