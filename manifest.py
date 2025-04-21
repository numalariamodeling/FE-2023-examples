import os
#
# This is a user-modifiable Python file designed to be a set of simple input file and directory settings that you can choose and change.

# the location of the file containing AssetCollection id for the dtk sif (singularity image)
sif_id = os.path.join(os.pardir, 'dtk_sif.id')

# The script is going to use this to store the downloaded schema file. Create 'download' directory or change to your preferred (existing) location.
schema_file=os.path.join(os.path.expanduser('~'),"download/schema.json")

# The script is going to use this to store the downloaded Eradication binary. Create 'download' directory or change to your preferred (existing) location.
eradication_path=os.path.join(os.path.expanduser('~'),"download/Eradication")

# Create 'Assets' directory or change to a path you prefer. idmtools will upload files found here.
assets_input_dir="Assets"
plugins_folder = "download/reporter_plugins"

# This is where your inputs are located
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
input_dir = os.path.join(ROOT_DIR, "inputs")


ep4_path="python_scripts"
#requirements = "./requirements.txt"

# This is where your simulations and outputs will be stored
user = os.getlogin()
user_dir= f'FE_{user}'
job_directory = os.path.join('/gpfs/projects/b1139', user_dir, 'FE-2023-examples/experiments')
os.makedirs(job_directory, exist_ok=True)

# This is the path to the sisf image used to run EMOD
SIF_PATH = "--bind /gpfs/projects /gpfs/projects/b1139/images/dtk_run_rocky_py39.sif"
