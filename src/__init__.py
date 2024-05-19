from os.path import join, dirname, abspath
import json

with open( join( dirname( abspath( __file__ ) ), "CONFIG.json" ), "r" ) as pfile:
    CONFIG_FILE = json.load( pfile )

