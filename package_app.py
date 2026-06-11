import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_app_package():
    # Create a temporary directory for packaging
    temp_dir = Path("temp_build")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()

    # Copy necessary files
    files_to_copy = [
        "manage.py",
        "requirements.txt",
        "README.md",
        "download_nltk_data.py"
    ]

    dirs_to_copy = [
        "journal",
        "journal_project",
        "sentiment_analyzer",
        "templates",
        "static"
    ]

    # Copy files
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, temp_dir)

    # Copy directories
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, temp_dir / dir_name)

    # Create a launcher script
    launcher_content = """import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        app_dir = Path(sys._MEIPASS)
    else:
        app_dir = Path(__file__).parent

    # Change to the application directory
    os.chdir(app_dir)

    # Run Django development server
    subprocess.run([sys.executable, 'manage.py', 'runserver'])

if __name__ == '__main__':
    main()
"""
    
    with open(temp_dir / "launcher.py", "w") as f:
        f.write(launcher_content)

    # Create PyInstaller spec file
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=['{temp_dir}'],
    binaries=[],
    datas=[
        ('journal', 'journal'),
        ('journal_project', 'journal_project'),
        ('sentiment_analyzer', 'sentiment_analyzer'),
        ('templates', 'templates'),
        ('static', 'static'),
        ('manage.py', '.'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
        ('download_nltk_data.py', '.'),
    ],
    hiddenimports=[
        'django',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'journal',
        'sentiment_analyzer',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='JournalApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
    
    with open(temp_dir / "JournalApp.spec", "w") as f:
        f.write(spec_content)

    
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Run PyInstaller
    os.chdir(temp_dir)
    subprocess.run([sys.executable, "-m", "PyInstaller", "JournalApp.spec"])

    # Move the executable to the dist directory
    dist_dir = Path("dist")
    if not dist_dir.exists():
        dist_dir.mkdir()

    # Copy the executable and create a README
    shutil.copy2(temp_dir / "dist" / "JournalApp.exe", dist_dir)
    
    readme_content = """Journal Application

This is a standalone version of the Journal Application.

To run the application:
1. Double-click JournalApp.exe
2. The application will start and be available at http://127.0.0.1:8000

For support or issues bina soche samjhe  contact support@journalapp.com
"""
    
    with open(dist_dir / "README.txt", "w") as f:
        f.write(readme_content)

    # Clean up
    os.chdir("..")
    shutil.rmtree(temp_dir)

    print("Application packaged successfully!")
    print(f"Executable can be found in: {dist_dir.absolute()}")

if __name__ == "__main__":
    create_app_package() 