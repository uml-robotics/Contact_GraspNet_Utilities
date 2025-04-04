import pyrealsense2 as rs
import numpy as np
import cv2
import os

object_name = input("Please enter the object's name for file naming purposes.\n")
print("Click on the camera preview window and press enter to take an image.")

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Enable streams
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

# Create an align object to align depth to color
align_to = rs.stream.color
align = rs.align(align_to)

# Create a directory to save the images if it doesn't exist
if not os.path.exists('scenes'):
    os.makedirs('scenes')

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        # Align the frames
        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not aligned_depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image for visualization
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)

        # Wait for key press (non-blocking)
        key = cv2.waitKey(1) & 0xFF

        # If the Enter key (13) is pressed, save images
        if key == 13:  # Enter key
            timestamp = int(cv2.getTickCount())  # Use a unique timestamp for file names

            # Save RGB image
            rgb_filename = os.path.join('scenes', f'rgb_{object_name}_{timestamp}.png')
            cv2.imwrite(rgb_filename, color_image)

            # Save depth image
            depth_filename = os.path.join('scenes', f'depth_{object_name}_{timestamp}.png')
            cv2.imwrite(depth_filename, depth_image)

            print(f"Images saved: {rgb_filename}, {depth_filename}")

        # Exit loop on 'Esc' key press
        if key == 27:  # Escape key
            break

finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
