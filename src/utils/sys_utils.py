from pathlib import Path


def mkdirs(folders):
  for output_folder in folders:
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    
