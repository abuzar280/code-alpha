import os
import shutil
import logging

# Setup logging
logging.basicConfig(filename='file_organizer.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def organize_files(path):
    try:
        files = os.listdir(path)
    except FileNotFoundError:
        logging.error(f"Path not found: {path}")
        print(f"Error: The specified path '{path}' does not exist.")
        return

    for file in files:
        filename, extension = os.path.splitext(file)
        extension = extension[1:]  # Remove the dot from the extension

        if extension:  # Only process files with an extension
            try:
                # Define the target directory path
                target_dir = os.path.join(path, extension)
                
                # Create the directory if it doesn't exist
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                # Move the file
                shutil.move(os.path.join(path, file), os.path.join(target_dir, file))
                logging.info(f"Moved file '{file}' to folder '{extension}'")

            except Exception as e:
                logging.error(f"Failed to move '{file}': {e}")
                print(f"Error moving '{file}': {e}")

if __name__ == "__main__":
    path = input("Enter Path: ")
    organize_files(path)
    print("File organization complete. Check 'file_organizer.log' for details.")
