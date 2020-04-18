import os
import shutil
import sys

SOURCE_DIR = 'src/ui/ui_source'
TARGET_DIR = 'src/ui/ui_compiled'

while not os.path.isdir(os.path.join(os.getcwd(), '.git')):
    os.chdir('..')

    if os.getcwd() == "/":
        print('Root not found')
        sys.exit(127)

shutil.rmtree(os.path.join(os.getcwd(), TARGET_DIR), ignore_errors=True)

for subdir, dirs, files in os.walk(os.path.join(os.getcwd(), SOURCE_DIR)):
    for file in files:
        source = os.path.join(subdir, file)
        source_dir_rel = os.path.relpath(subdir, SOURCE_DIR)
        target_dir = os.path.normpath(
            os.path.join(os.getcwd(), TARGET_DIR, source_dir_rel)
        )
        os.makedirs(target_dir, exist_ok=True)
        target, _ = os.path.splitext(os.path.join(target_dir, file))
        target += ".py"
        os.system(f'pyuic5 {source} >> {target}')
        print(f'Processed: {source}')
