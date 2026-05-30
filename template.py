import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')




list_of_files = [
    f"agents/__init__.py",
    f"agents/code_executor_agent.py",
    f"agents/data_analyzer_agent.py",
    f"config/__init__.py",
    f"config/constants.py",
    f"utils/__init__.py",
    f"utils/docker_util.py",
    f"models/__init__.py",
    f"models/groq_model_client.py",
    f"teams/__init__.py",
    f"teams/data_analyst.py",
    "streamlit_app.py"
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory:{filedir} for the file {filename}")

    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,'w') as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    
    else:
        logging.info(f"{filename} is already exists")