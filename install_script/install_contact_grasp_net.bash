#!/bin/bash
cd "$HOME"
# Check if Anaconda is installed
if [ -d "$HOME/anaconda3" ] && [ -x "$HOME/anaconda3/bin/conda" ]; then
    echo "Anaconda is already installed at $HOME/anaconda3."
else
    cd "$HOME"
    echo "Installing Anaconda..."
    curl -O https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
    bash ~/Anaconda3-2024.10-1-Linux-x86_64.sh -b
    source ~/.bashrc
    source ~/anaconda3/bin/activate
    conda init --all
    source ~/.bashrc
    conda config --set auto_activate_base False
    conda list
fi

# Clone the Contact-GraspNet repository if it's not already cloned
REPO_DIR="$HOME/contact-graspnet"
if [ ! -d "$REPO_DIR" ]; then
    echo "Cloning Contact-GraspNet repository..."
    git clone https://github.com/NVlabs/contact_graspnet.git "$REPO_DIR"
    cd "$REPO_DIR"

    # Create the Conda environment
    conda env create -f contact_graspnet_env.yml
     Set up checkpoints directory and download models
    CHECKPOINTS_DIR="$REPO_DIR/checkpoints"
    mkdir -p "$CHECKPOINTS_DIR"
    cd "$CHECKPOINTS_DIR"

    # Install gdown if not already installed
    if ! command -v gdown &> /dev/null; then
    echo "Installing gdown..."
    pip install gdown
    fi

    # Download trained models
    if [ ! -d "$CHECKPOINTS_DIR/contact_graspnet_models" ]; then
    echo "Downloading trained models..."
    gdown --folder "https://drive.google.com/drive/folders/1tBHKf60K8DLM5arm-Chyf7jxkzOr5zGl"
    fi

    # Move models to the correct location
    if [ -d "$CHECKPOINTS_DIR/contact_graspnet_models" ]; then
    mv "$CHECKPOINTS_DIR/contact_graspnet_models"/* "$CHECKPOINTS_DIR"/
    rmdir "$CHECKPOINTS_DIR/contact_graspnet_models"
    fi

    # Download example test data
    cd "$REPO_DIR"
    if [ ! -d "$REPO_DIR/test_data" ]; then
    echo "Downloading test data..."
    gdown --folder "https://drive.google.com/drive/folders/1chRprUBdITSYEjrP7O2eXnC_7Zk5ZRFl?usp=sharing"
    fi

    # Ensure test_data folder exists and contains .npy files
    if [ -z "$(ls -A test_data/*.npy 2>/dev/null)" ]; then
    echo "Error: No .npy files found in test_data. Please check the download."
    exit 1
    fi
    else
    echo "Contact-GraspNet repository already exists."
    fi
fi
# Activate the Contact-GraspNet environment
source ~/.bashrc
conda activate contact_graspnet_env

# Run Contact-GraspNet inference
echo "Running Contact-GraspNet inference..."
python contact_graspnet/inference.py \
       --np_path=test_data/*.npy \
       --local_regions --filter_grasps

echo "Inference complete!"
