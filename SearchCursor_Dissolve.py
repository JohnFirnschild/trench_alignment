# Step 6: GIves a list of Objectids for finding spans or routes in 3gis based on step 5

# Specify the feature class and field you want to get unique values from
feature_class = input("Which FC do you want a query for?: ")
field_name = "OBJECTID"

# Create an empty list to store the unique values
unique_values = []

# Use SearchCursor to get the unique values
with arcpy.da.SearchCursor(feature_class, [field_name]) as cursor:
    for row in cursor:
        value = row[0]
        if value not in unique_values:
            unique_values.append(value)

# Print the list of unique values
print(unique_values)