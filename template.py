import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(acstime)s]: %(message)s')

project_name = 'WaferFaultDetection'

list_of_files = [
    ".github/main.yml",
    "config/model.yml",
    f"{project_name}/component/__init__.py",
    f"{project_name}/component/data_ingestion.py",
    f"{project_name}/component/data_transformation.py",
    f"{project_name}/component/model_trainer.py",
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/configuration/mongo_db_connection.py",
    f"{project_name}/constant/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/prediction_pipeline.py",
    f"{project_name}/pipeline/train_pipeline.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    f"{project_name}/__init__.py",
    f"{project_name}/exception.py",
    f"{project_name}/logger.py",
    "static/css/style.css",
    "templates/upload_file.html",
    ".gitignore",
    "Dockerfile",
    'README.md',
    'app.py',
    '__init__.py',
    'requirements.txt',
    'setup.py',
    'upload_data.py'
]

for file_path in list_of_files:
    file_path = Path(file_path)

    file_dir, file_name = os.path.split(file_path)

    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Creating Directory :{file_dir} for the file {file_name}")
    
    if (not os.path.exists(file_name)) or (os.path.getsize(file_name) == 0):
       with open(file_path, 'w') as f:
        pass
        logging.info(f"Creating empty file: {file_name}") 
    
    else:
        logging.info(f"{file_name} is already created.")