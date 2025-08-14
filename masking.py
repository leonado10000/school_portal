import pandas as pd
from faker import Faker

fake = Faker()

# Load student.csv
students = pd.read_csv('C:\\Users\\rjdis\\OneDrive\\Desktop\\students data\\student.csv')

# Create a mapping for consistent fake names
name_mapping = {}
for name in students['name'].unique():
    name_mapping[name] = fake.first_name() + " " + fake.last_name()

# Mask student names
students['name'] = students['name'].map(name_mapping)

# Optionally mask parents' names
if 'fathers_name' in students.columns:
    name_mapping_father = {}
    for name in students['fathers_name'].dropna().unique():
        name_mapping_father[name] = fake.first_name() + " " + fake.last_name()
    students['fathers_name'] = students['fathers_name'].map(name_mapping_father)

if 'mothers_name' in students.columns:
    name_mapping_mother = {}
    for name in students['mothers_name'].dropna().unique():
        name_mapping_mother[name] = fake.first_name() + " " + fake.last_name()
    students['mothers_name'] = students['mothers_name'].map(name_mapping_mother)

# Save masked file
students.to_csv('C:\\Users\\rjdis\\OneDrive\\Desktop\\students data\\student.csv', index=False)
print("✅ student_masked.csv created with anonymized names")
