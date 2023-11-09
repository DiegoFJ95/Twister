from os.path import join, dirname, abspath
import json

with open( join( dirname( abspath( __file__ ) ), "CONFIG.json" ), "r" ) as pfile:
    CONFIG_FILE = json.load( pfile )


# Sobreescribir CONFIG FILE
#CONFIG_FILE["MAXIMUM_NODES"] = 9
#
#with open( "src\CONFIG.json", "w" ) as pFile:
#    json.dump( CONFIG_FILE,  pFile, indent=4  )