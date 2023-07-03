import re
import os
# for getting file name
def get_file_name(file_path):
    pattern = r'([^\\/]+)$'  # Regex pattern to match the file name at the end of the path
    match = re.search(pattern, file_path)
    
    if match:
        return match.group(1)  # Return the matched file name
    else:
        return None  # Return None if no match is found
    
def get_dir(directory):
    try:
    # Check if the directory exists
        if os.path.exists(directory):
            return directory
        else:
            try:
                os.makedirs(directory)
                return directory
            except FileExistsError:
                print(f"Directory '{directory}' already exists.")

            except OSError as e:
                print(f"An error occurred while creating directory '{directory}': {str(e)}")
        

    except FileNotFoundError as e:
        print(e)  # Output the error message
        # Handle the case where the directory does not exist

