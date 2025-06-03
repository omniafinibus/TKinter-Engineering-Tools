from _directory import *

pipDir = os.path.join(VENV_DIRECTORY, "Scripts", "pip.exe")
os.chdir(os.path.join(MAIN_DIRECTORY))
os.system(f"{pipDir} install .")
    
print("Done!")