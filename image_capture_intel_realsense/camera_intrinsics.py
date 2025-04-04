import pyrealsense2 as rs
import numpy as np

# Initialize the pipeline
pipeline = rs.pipeline()

# Configure the pipeline to stream both depth and color data
config = rs.config()
config.enable_stream(rs.stream.depth)
config.enable_stream(rs.stream.color)

# Start the pipeline
pipeline.start(config)

# Wait for a few frames to ensure the camera is ready
frames = pipeline.wait_for_frames()

# Get the depth stream
depth_stream = frames.get_depth_frame()

# Retrieve the intrinsics (camera matrix)
depth_intrinsics = depth_stream.profile.as_video_stream_profile().get_intrinsics()

# Prepare the camera matrix (K)
K = np.array([[depth_intrinsics.fx, 0, depth_intrinsics.ppx],
              [0, depth_intrinsics.fy, depth_intrinsics.ppy],
              [0, 0, 1]])

# Define the file path to save the camera matrix
file_path = 'camera_matrix.txt'

# Write the camera matrix and intrinsics to a file
with open(file_path, 'w') as f:
    f.write("Camera Matrix (K):\n")
    f.write(f"fx: {depth_intrinsics.fx}\n")
    f.write(f"fy: {depth_intrinsics.fy}\n")
    f.write(f"cx: {depth_intrinsics.ppx}\n")
    f.write(f"cy: {depth_intrinsics.ppy}\n")
    f.write("\nCamera Matrix (K) in 3x3 format:\n")
    np.savetxt(f, K, fmt='%0.6f')

print(f"Camera matrix saved to {file_path}")

# Stop the pipeline
pipeline.stop()
