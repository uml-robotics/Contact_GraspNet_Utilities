import pyrealsense2 as rs
import numpy as np
import cv2
import os

object_name = input("Please enter the object's name for file naming purposes.\n")
print("Click on the camera preview window and press enter to take an image.")
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

# Create a directory to save the images if it doesn't exist
if not os.path.exists('saved_depth_and_rgb_images'):
    os.makedirs('saved_depth_and_rgb_images')

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
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
            timestamp = int(cv2.getTickCount())  # Use a unique timestamp to name the image files

            # Save RGB image
            rgb_filename = os.path.join('saved_depth_and_rgb_images', f'rgb_{object_name}_{timestamp}.png')
            cv2.imwrite(rgb_filename, color_image)

            # Save depth image
            depth_filename = os.path.join('saved_depth_and_rgb_images', f'depth_{object_name}_{timestamp}.png')
            cv2.imwrite(depth_filename, depth_colormap)

            print(f"Images saved: {rgb_filename}, {depth_filename}")

        # Exit loop on 'Esc' key press
        if key == 27:  # Escape key
            break

finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
