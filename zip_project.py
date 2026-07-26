import os
import zipfile

def create_zip():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    zip_filename = os.path.join(base_dir, 'Online_Quiz_Application.zip')

    # Ignore unnecessary patterns
    ignore_dirs = {'__pycache__', '.git', '.venv', 'venv', '.idea', '.vscode'}
    ignore_files = {'Online_Quiz_Application.zip', 'online_quiz.db'}

    print(f"Creating ZIP archive: {zip_filename}")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            # Exclude ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if file in ignore_files or file.endswith('.pyc'):
                    continue
                
                file_path = os.path.join(root, file)
                # Compute relative path under root zip directory "Online_Quiz_Application/"
                rel_path = os.path.relpath(file_path, base_dir)
                arcname = os.path.join('Online_Quiz_Application', rel_path)
                
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")

    print("ZIP archive created successfully!")

if __name__ == '__main__':
    create_zip()
