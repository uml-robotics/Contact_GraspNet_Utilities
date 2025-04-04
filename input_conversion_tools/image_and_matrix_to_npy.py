import numpy as np
import cv2
import os
import sys

def load_camera_matrix(filename):
    """
    Loads a 3x3 camera matrix from a text file.
    :param filename: Path to the camera matrix text file.
    :return: A 3x3 numpy array of type float32.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    start_index = None
    for i, line in enumerate(lines):
        if "Camera Matrix (K) in 3x3 format:" in line:
            start_index = i + 1
            break
    if start_index is None:
        raise ValueError("Camera matrix section not found in the file.")
    
    matrix_lines = lines[start_index:start_index+3]
    matrix = []
    for l in matrix_lines:
        # Split the line on whitespace and convert each element to float
        matrix.append([float(x) for x in l.strip().split()])
    return np.array(matrix, dtype=np.float32)

def depth2pc(depth, K, rgb):
    """
    Converts a depth image into a point cloud using the pinhole camera model.
    :param depth: Depth map (in meters) as a 2D numpy array.
    :param K: Camera matrix (3x3 numpy array).
    :param rgb: RGB image as a 3D numpy array.
    :return: (pc_full, pc_colors) where pc_full is an (N x 3) point cloud and
             pc_colors is an (N x 3) array of corresponding RGB values.
    """
    # Get image dimensions
    height, width = depth.shape

    # Create grid of pixel coordinates
    x, y = np.meshgrid(np.arange(width), np.arange(height))

    # Compute normalized coordinates (u-cx)/fx, (v-cy)/fy
    normalized_x = (x - K[0, 2]) / K[0, 0]
    normalized_y = (y - K[1, 2]) / K[1, 1]

    # Flatten arrays
    normalized_x = normalized_x.flatten()
    normalized_y = normalized_y.flatten()
    depth_flat = depth.flatten()

    # Compute 3D coordinates in camera coordinate system
    world_x = normalized_x * depth_flat
    world_y = normalized_y * depth_flat
    world_z = depth_flat

    # Stack to form the (N x 3) point cloud
    pc_full = np.vstack((world_x, world_y, world_z)).T

    # Reshape pc_full to match the original image resolution (height, width, 3)
    pc_full_reshaped = pc_full.reshape((height, width, 3))

    # Flatten the RGB image to match the point cloud (one color per pixel)
    rgb_flat = rgb.reshape(-1, 3)
    pc_colors = rgb_flat.reshape((height, width, 3))

    return pc_full_reshaped, pc_colors

def process_and_save_depth_images(input_folder, output_folder, camera_matrix):
    """
    Processes each pair of RGB and depth images in the input folder and saves a .npy file
    with the structure containing rgb, xyz, and label data.
    :param input_folder: Folder containing images (files starting with 'rgb' and 'depth').
    :param output_folder: Folder where processed files will be saved.
    :param camera_matrix: 3x3 camera intrinsic matrix as a numpy array.
    """
    os.makedirs(output_folder, exist_ok=True)

    # List image files (assumes matching order for rgb and depth images)
    rgb_images = [f for f in os.listdir(input_folder) if f.startswith('rgb')]
    depth_images = [f for f in os.listdir(input_folder) if f.startswith('depth')]

    for rgb_image, depth_image in zip(rgb_images, depth_images):
        # Load images
        rgb = cv2.imread(os.path.join(input_folder, rgb_image))
        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

        # Use IMREAD_UNCHANGED to preserve the original depth bit-depth (e.g., 16-bit)
        depth = cv2.imread(os.path.join(input_folder, depth_image), cv2.IMREAD_UNCHANGED)
        if depth is None:
            print(f"Warning: Unable to load depth image {depth_image}")
            continue

        # Normalize depth from mm to meters (assuming the depth image is in mm)
        depth = depth.astype(np.float32) / 1000.0

        # Convert depth to point cloud and get corresponding RGB colors
        pc_full, pc_colors = depth2pc(depth, camera_matrix, rgb)
        print(f'PC_Full = {pc_full.shape}\nPC_Colors = {pc_colors.shape}')

        # Prepare data dictionary
        processed_data = {
            'rgb': rgb,                                      # Original RGB image
            'xyz': pc_full,                                  # Precomputed point cloud (height x width x 3)
            'label': np.zeros(depth.shape, dtype=np.float32) # Placeholder segmentation map (height x width)
        }

        # Save as a .npy file
        output_path = os.path.join(output_folder, f"{rgb_image}_data.npy")
        np.save(output_path, processed_data)

        print(f"Processed and saved: {rgb_image}")

if __name__ == "__main__":

    input_dir = "input_data"
    if not os.path.exists(input_dir):
        print("No input data")
        sys.exit()

    scene_folder = 'scenes' # change to the specific folder containing RGB and RGB-D for specific scenes (rgb_*.png and depth_*.png)
    input_folder = os.path.join(input_dir, scene_folder)

    output_folder = "processed_data" 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
 
    camera_matrix_file = os.path.join(input_dir, 'camera_matrix.txt')

    # Load the camera matrix from the text file
    camera_matrix = load_camera_matrix(camera_matrix_file)
    print("Loaded Camera Matrix:")
    print(camera_matrix)

    # Process all images and save the processed files in the expected format
    process_and_save_depth_images(input_folder, output_folder, camera_matrix)
    print("All images have been processed and saved.")
