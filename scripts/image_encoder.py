# ==================================================================== #
#  File name:      image_encoder.py             #        _.==._        #
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #
#  Date:           02-Jun-2023                  #    *= #        =*    #
# ============================================= #   #/  #         \#   #
#  Description:    Scripts which converts       #  |#   #   $      #|  #
#                  all images in the assets     #  |#   #   #      #|  #
#                  folder to python source      #   #\  #   #     /#   #
#                  code.                        #    *= #   #    =+    #
#  Rev:            1.0                          #     *++######++*     #
#                                               #        *-==-*        #
# ==================================================================== #
#  Revision history:                                                   #
#  Date        Description                                             #
#  02-Jun-2023 File created                                            #
# ==================================================================== #
#  To-Do: !=Priority, ~=Bug, ?=Idea/nice to have                       #
#                                                                      #
# ==================================================================== #

import os, sys, base64, datetime
from _directory import *

ASSETS_FOLDER = os.path.join(MAIN_DIRECTORY, "assets")
OUTPUT_FILE = os.path.join(PROJECT_DIRECTORY, "resources", "_encoded_images.py")

# Clear the previous files
if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

original_stdout = sys.stdout # Save a reference to the original standard output

# Create a new file
with open(OUTPUT_FILE, "w+") as outputFile:
    sys.stdout = outputFile
    
    print(f"# ==================================================================== #\n\
#  File name:      _encoded_images.py           #        _.==._        #\n\
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #\n\
#  Date:           {datetime.datetime.today()}  #    *= #        =*    #\n\
# ============================================= #   #/  #         \#   #\n\
#  Description:    Embedded data for images in  #  |#   #   $      #|  #\n\
#                  ./assets/                    #  |#   #   #      #|  #\n\
#                  This file is automatically   #   #\  #   #     /#   #\n\
#                  generated using the          #    *= #   #    =+    #\n\
#                  _image_encoder.py script.    #     *++######++*     #\n\
#                                               #        *-==-*        #\n\
# ==================================================================== #\n\n"
    )
    
    # Name of the file to encode
    for filename in [name for name in os.listdir(ASSETS_FOLDER) if name.endswith(".png")]: # Only embed png files
        varName = filename.replace(".png", "")
        print(f"{varName} = {base64.b64encode(open(os.path.join(ASSETS_FOLDER, filename),'rb').read())}\n")


sys.stdout = original_stdout # Reset the standard output to its original value