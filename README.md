# Contact-GraspNet-Utilities

Utilities for working with [Contact-GraspNet](https://github.com/NVlabs/contact_graspnet), a deep learning model for generating 6-DoF grasps from RGB-D input. 

These utilities are also helpful for getting started with creating segmentation masks with the [Unseen Object Instance Segmentation for Robotic Enviroments](https://github.com/chrisdxie/uois) framework. These segmentation masks improve the quality of grasps generated from Contact-GraspNet.

## Overview

Both Contact-Graspnet and UOIS require additional setup which is specified in their own respective repositories. 

This repo provides helper tools for:
- Collecting RGB and RGB-D data from an Intel RealSense Depth Camera D435
- Converting RGB and RGB-D data into .npy format for Contact-GraspNet (and UOIS)
- Installation scripts for Contact-Graspnet (in progress)

## Getting Started
1. Installation requirements (in progress)

2. If you do not already have a camera intrinsics matrix for your current camera setup. Generate by running: 
    ```bash
    python image_capture_intel_realsense/camera_intrinsics.py
    mv image_capture_intel_realsense/camera_matrix.txt input_conversion_tools/input_data

3. Capture RGB and RGB-D data:
    ```bash
    python image_capture_intel_realsense/capture_depth_and_rgb_images.py
    mv image_capture_intel_realsense/scenes input_conversion_tools/input_data

4. Convert scenes into .npy files. This is the file type expected from Contact-GraspNet and UOIS
    ```bash
    python input_conversion_tools/image_and_matrix_to_npy.py
  Files in processed data can the be use in Contact-GraspNet and UOIS

