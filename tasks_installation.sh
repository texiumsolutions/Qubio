#!/bin/bash

# Set error handling
set -e
set -o pipefail

# Define installation paths
ROOT_DIR="$HOME/BioTasks"
ANTIFOLD_DIR="$ROOT_DIR/AntiFold"
LIGANDMPNN_DIR="$ROOT_DIR/LigandMPNN"
PROTEINMPNN_DDG_DIR="$ROOT_DIR/proteinmpnn_ddg"
TS_DIR="$ROOT_DIR/ThompsonSampling"
FREEWILSON_DIR="$ROOT_DIR/Free-Wilson"
COLABDOCK_DIR="$ROOT_DIR/ColabDock"
REINVENT_DIR="$ROOT_DIR/REINVENT4"
THERMOMPNN_DIR="$ROOT_DIR/ThermoMPNN-D"  # New path for ThermoMPNN-D

# Ensure ROOT_DIR exists
mkdir -p $ROOT_DIR

# Activate Conda
echo "=========================="
echo "Activating Conda..."
echo "=========================="
source ~/miniconda3/bin/activate || { echo "Conda activation failed"; exit 1; }
echo "Conda activated."

echo "=========================="
echo "Cloning Repositories..."
echo "=========================="

cd $ROOT_DIR
[[ ! -d "AntiFold" ]] && git clone https://github.com/oxpig/AntiFold.git
[[ ! -d "LigandMPNN" ]] && git clone https://github.com/dauparas/LigandMPNN.git
[[ ! -d "proteinmpnn_ddg" ]] && git clone https://github.com/PeptoneLtd/proteinmpnn_ddg.git
[[ ! -d "ThompsonSampling" ]] && git clone https://github.com/PatWalters/TS.git
[[ ! -d "Free-Wilson" ]] && git clone https://github.com/PatWalters/Free-Wilson.git
[[ ! -d "ColabDock" ]] && git clone https://github.com/JeffSHF/ColabDock
[[ ! -d "REINVENT4" ]] && git clone https://github.com/MolecularAI/REINVENT4.git REINVENT4
[[ ! -d "ThermoMPNN-D" ]] && git clone https://github.com/your_repo/ThermoMPNN-D.git  # Clone ThermoMPNN-D

echo "Repositories cloned successfully."

####### AntiFold Setup ########
echo "=========================="
echo "Setting up AntiFold..."
echo "=========================="
cd $ANTIFOLD_DIR
if ! conda info --envs | grep -q "antifold_cpu"; then
    conda create --name antifold_cpu python=3.10 -y
fi
conda activate antifold_cpu
pip install -U pip
conda install -c conda-forge pytorch -y
pip install .
echo "AntiFold setup complete."

####### LigandMPNN Setup ########
echo "=========================="
echo "Setting up LigandMPNN..."
echo "=========================="
cd $LIGANDMPNN_DIR
if ! conda info --envs | grep -q "ligandmpnn_env"; then
    conda create -n ligandmpnn_env python=3.11 -y
fi
conda activate ligandmpnn_env
pip install -U pip
pip install -r requirements.txt
bash get_model_params.sh "./model_params"
echo "LigandMPNN setup complete."

####### ProteinMPNN-ddG Setup ########
echo "=========================="
echo "Setting up ProteinMPNN-ddG..."
echo "=========================="
cd $PROTEINMPNN_DDG_DIR
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Please install Docker before proceeding."
    exit 1
fi
docker pull ghcr.io/peptoneltd/proteinmpnn_ddg:1.0.0_base
echo "ProteinMPNN-ddG setup complete."

####### Thompson Sampling Setup ########
echo "=========================="
echo "Setting up Thompson Sampling..."
echo "=========================="
cd $TS_DIR
if ! conda info --envs | grep -q "ts_env"; then
    conda create --name ts_env python=3.10 -y
fi
conda activate ts_env
pip install -U pip
conda install -c conda-forge rdkit -y
pip install -r requirements.txt
echo "Thompson Sampling setup complete."

####### Free-Wilson Setup ########
echo "=========================="
echo "Setting up Free-Wilson..."
echo "=========================="
cd $FREEWILSON_DIR
if ! conda info --envs | grep -q "freewilson_env"; then
    conda create --name freewilson_env python=3.9 -y
fi
conda activate freewilson_env
pip install -U pip
pip install rdkit tqdm docopt pyfancy sklearn scipy joblib
echo "Free-Wilson setup complete."

####### ColabDock Setup ########
echo "=========================="
echo "Setting up ColabDock..."
echo "=========================="
cd $COLABDOCK_DIR
if ! conda info --envs | grep -q "colabdock_env"; then
    conda create --name colabdock_env python=3.10 -y
fi
conda activate colabdock_env
pip install -U pip
pip install -r requirements.txt
pip install https://storage.googleapis.com/jax-releases/cuda11/jaxlib-0.3.8+cuda11.cudnn805-cp38-none-manylinux2014_x86_64.whl
pip install jax==0.3.8
mkdir -p "$COLABDOCK_DIR/protein"
echo "ColabDock setup complete."

####### REINVENT Setup ########
echo "=========================="
echo "Setting up REINVENT4..."
echo "=========================="
cd $REINVENT_DIR
if ! conda info --envs | grep -q "reinvent4"; then
    conda create --name reinvent4 python=3.12 -y
fi
conda activate reinvent4
pip install -U pip
pip install -r requirements.txt
pip install .
echo "REINVENT4 setup complete."

####### Download AlphaFold2 Parameters ########
echo "=========================="
echo "Downloading AlphaFold2 Parameters..."
echo "=========================="
COLABDOCK_PARAMS_DIR="$COLABDOCK_DIR/params"
mkdir -p $COLABDOCK_PARAMS_DIR
cd $COLABDOCK_PARAMS_DIR
if [[ ! -f "alphafold_params_2022-12-06.tar" && ! -d "params" ]]; then
    wget https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar
    tar -xvf alphafold_params_2022-12-06.tar
    rm alphafold_params_2022-12-06.tar
    echo "AlphaFold2 parameters downloaded and extracted."
else
    echo "AlphaFold2 parameters already exist. Skipping download."
fi


####### ParaSurf Setup ########
echo "=========================="
echo "Setting up ParaSurf..."
echo "=========================="
PARASURF_DIR="$ROOT_DIR/ParaSurf"
cd $ROOT_DIR
if [[ ! -d "ParaSurf" ]]; then
    git clone https://github.com/BeichenLi123/ParaSurf.git
fi

cd $PARASURF_DIR
if ! conda info --envs | grep -q "parasurf_env"; then
    conda create --name parasurf_env python=3.10 -y
fi
conda activate parasurf_env
pip install -U pip
pip install -r requirements.txt

# Make sure model_weights dir exists
mkdir -p "$PARASURF_DIR/model_weights"

echo "ParaSurf setup complete."

####### ThermoMPNN-D Setup ########
echo "=========================="
echo "Setting up ThermoMPNN-D..."
echo "=========================="
cd $THERMOMPNN_DIR
if ! conda info --envs | grep -q "ThermoMPNN-D"; then
    conda create --name ThermoMPNN-D python=3.10 -y
fi
conda activate ThermoMPNN-D
pip install -U pip
pip install -r requirements.txt
echo "ThermoMPNN-D setup complete."


####### LocalColabFold Setup ########
echo "=========================="
echo "Setting up LocalColabFold..."
echo "=========================="
LOCALCOLABFOLD_DIR="$ROOT_DIR/LocalColabFold"
cd $ROOT_DIR
if [[ ! -d "LocalColabFold" ]]; then
    git clone https://github.com/YoshitakaMo/localcolabfold.git LocalColabFold
fi

cd $LOCALCOLABFOLD_DIR
if ! conda info --envs | grep -q "localcolabfold"; then
    conda create --name localcolabfold python=3.10 -y
fi
conda activate localcolabfold

pip install -U pip
pip install -r requirements.txt
python3 setup.py install

# Download weights (optional, but often required)
python3 colabfold/download.py

echo "LocalColabFold setup complete."


echo "=========================="
echo "All installations completed successfully!"
echo "=========================="
