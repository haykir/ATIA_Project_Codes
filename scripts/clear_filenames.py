import os

# Replace 'root_directory' with the path to your main directory
root_directory = 'leftImg8bit'

# Strings to replace
strings_to_remove = [
    "_leftImg8bit_foggy_beta_0.02",
    "_leftImg8bit_foggy_beta_0.01",
    "_leftImg8bit_foggy_beta_0.005"
]

# Traverse the directory
for subdir, dirs, files in os.walk(root_directory):
    for file in files:
        old_file_path = os.path.join(subdir, file)

        # Check if any of the strings to remove are in the filename
        for string in strings_to_remove:
            if string in file:
                # Create the new filename by replacing the string
                new_file_name = file.replace(string, "")
                new_file_path = os.path.join(subdir, new_file_name)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")
                break  # Exit loop to avoid multiple replacements for the same file

print("File renaming completed successfully!")
