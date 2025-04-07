import os
import open3d as o3d
import numpy as np

def ply_to_contact_graspnet_npy(ply_path, npy_path, add_camera_matrix=False, in_millimeters=False):
    """
    Converts a .ply point cloud to a .npy file compatible with Contact-GraspNet.
    
    :param ply_path: Path to the input PLY file
    :param npy_path: Path to the output NPY file
    :param add_camera_matrix: If True, adds a 3x3 camera matrix (K) to the saved data
    :param in_millimeters: If True, scales the loaded points from mm to m
    """
    # Load the point cloud from the PLY file
    pcd = o3d.io.read_point_cloud(ply_path)
    points = np.asarray(pcd.points, dtype=np.float32)

    # If your PLY is in millimeters, convert to meters
    if in_millimeters:
        points /= 1000.0

    data_dict = {"xyz": points}

    # If color information is available, add it as xyz_color
    if pcd.has_colors():
        colors = np.asarray(pcd.colors, dtype=np.float32)
        data_dict["xyz_color"] = colors

    # Optionally add the camera matrix if your pipeline needs it
    if add_camera_matrix:
        data_dict["K"] = np.array([
            [383.432861, 0.0,       322.729065],
            [0.0,        383.432861, 240.311951],
            [0.0,        0.0,        1.0]
        ], dtype=np.float32)

    # Save the dictionary as an NPY file
    np.save(npy_path, data_dict)
    print(f"Saved {npy_path} with keys: {list(data_dict.keys())}")

if __name__ == "__main__":
    # Define the directory containing the PLY files
    input_directory = "point_cloud_files"
    
    # Adjust these flags based on your setup
    ADD_CAMERA_MATRIX = False
    PLY_IS_IN_MILLIMETERS = False

    # Loop through all files in the directory
    for file_name in os.listdir(input_directory):
        if file_name.lower().endswith(".ply"):
            ply_path = os.path.join(input_directory, file_name)
            # Create output file name by replacing .ply with .npy
            npy_path = os.path.join(input_directory, file_name.replace(".ply", ".npy"))
            print(f"Processing file: {ply_path}")
            ply_to_contact_graspnet_npy(
                ply_path=ply_path,
                npy_path=npy_path,
                add_camera_matrix=ADD_CAMERA_MATRIX,
                in_millimeters=PLY_IS_IN_MILLIMETERS
            )
