import os
import shutil

# Replace 'root_directory' with the path to your main directory
root_directory = 'leftImg8bit'

# Define target directories
low_dir = os.path.join(root_directory, "Low")
med_dir = os.path.join(root_directory, "Med")
hgh_dir = os.path.join(root_directory, "Hgh")

# Create the base target directories
os.makedirs(low_dir, exist_ok=True)
os.makedirs(med_dir, exist_ok=True)
os.makedirs(hgh_dir, exist_ok=True)

# Walk through the directory and subdirectories
for subdir, dirs, files in os.walk(root_directory):
    # Skip the target directories to avoid recursion
    if any(subdir.startswith(d) for d in [low_dir, med_dir, hgh_dir]):
        continue

    for file in files:
        file_path = os.path.join(subdir, file)
        relative_path = os.path.relpath(subdir, root_directory)

        # Check the file name for specific strings
        if "0.005" in file:
            target_dir = os.path.join(low_dir, relative_path)
        elif "0.01" in file:
            target_dir = os.path.join(med_dir, relative_path)
        elif "0.02" in file:
            target_dir = os.path.join(hgh_dir, relative_path)
        else:
            continue

        # Create the target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)

        # Move the file
        shutil.move(file_path, os.path.join(target_dir, file))

print("Files moved successfully with folder structure maintained!")
