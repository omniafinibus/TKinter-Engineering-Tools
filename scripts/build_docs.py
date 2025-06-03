from _directory import *

try:
    os.chdir(os.path.join(MAIN_DIRECTORY, "docs", "sphinx"))
    os.system(f"sphinx-apidoc -P -f -d 10 -o .\source\\auto_tocs\ {PROJECT_DIRECTORY}\.")
    os.system(f".\make.bat html")
    # os.system(f".\make.bat latex")
    os.system('pause')
except Exception as e: 
    print(e)
    os.system('pause')