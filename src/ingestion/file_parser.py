import os
import pandas as pd

def get_raw_files_from_source(path):
    """List all valid files in the source directory."""
    return [f for f in os.listdir(path) if not f.startswith('.')]

def parse_raw_files(path: str) -> list[dict]:
    """ Parse files in the source directory."""
    files = get_raw_files_from_source(path)
    knowledge_base = []

    for file in files:
        if file.endswith(('xls', 'xlsx')):
            df = pd.read_excel(os.path.join(path, file))
            content = df.to_csv(index=False)
            knowledge_base.append({
                "content": content,
                "metadata": {
                    "file_name": file,
                    "file_type": "excel_sheet"
                }
            })

    return knowledge_base