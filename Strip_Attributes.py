"""
Steps 3 & 4
If the CONDUIT_DE ONLY HAS one unique value
this can ue used with valid_input

If make feature layer was used to seperate data
then identify those with test_file variable above

"""
# Step 3: strip unnecessary information from the table 

# Get a list of unique values in the CONDUIT_DE field
unique_values = list(set(row[0] for row in arcpy.da.SearchCursor(test_file, "CONDUIT_DE")))

# Define the valid input
# THis is based on the reults of ste 2
valid_input = input("Define the valid input: ")

# Create a list of values to delete
values_to_delete = []
for value in unique_values:
    if valid_input in value:
        delete_string = value.replace(valid_input, "").strip()
        values_to_delete.append(delete_string)

# Create the expression for the CalculateField function
expression = "!CONDUIT_DE!"
for value in values_to_delete:
    expression = f"{expression}.replace('{value}', '')"

# Calculate the field
arcpy.management.CalculateField(test_file, "CONDUIT_DE", expression, "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")

# Step 4: After attributes have been standardized perform Dissolve

working_dissolve = arcpy.management.Dissolve(test_file, f"{test_file}_Dissolve", "CONDUIT_DE;LEGACY_OWN", None, "SINGLE_PART", "UNSPLIT_LINES")
record_count = arcpy.management.GetCount(working_dissolve)
print (record_count)