import numpy as np
import os
import sys

'''
This is used mainly to understand the architecture of the npy files that are used as input for UOIS and COntact-GraspNet
'''

def read_and_display_npy(file_path):
    # Load the .npy file
    data = np.load(file_path, allow_pickle=True)
    
    # Display basic information about the data
    print(f"Loaded .npy file: {file_path}")
    print(f"Data type: {type(data)}")
    print(f"Shape of data: {data.shape}")
    print(f"Data type (dtype): {data.dtype}")

    # If the data is a large array, avoid printing the entire contents
    # and instead show the first few entries
    if data.size > 1000000000:  # Adjust this value if necessary
        print("Displaying the first few elements of the array:")
        print(data[:5])  # Print the first 5 rows/values
    else:
        print("Displaying entire contents of the array:")
        print(data)
    
    # If the data is 3D (e.g., a depth map), we can print a small section of it
    if len(data.shape) == 3:
        print("Displaying a small section of the 3D array:")
        print(data[:2, :2, :2])  # Display a small 2x2x2 part of the array

if __name__ == "__main__":
    npy_dir = 'npy_files'
    if not os.path.exists(npy_dir):
        print(f'No npy_file directory')
        sys.exit()

    npy_file = 'file.npy' # Change to specific file name
    file_path = os.path.join(npy_dir, npy_file)
    
    read_and_display_npy(file_path)
