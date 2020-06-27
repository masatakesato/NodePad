
# http://stackoverflow.com/questions/487971/is-there-a-standard-way-to-list-names-of-python-modules-in-a-package

import os
import glob
import pkgutil
import importlib
import traceback


from .factory.node_manager import AttribLayoutDesc, AttribDesc, NodeTypeManager
from .factory.pluginbase import PluginBase



def GetSubclass( module, base_class ):

    for name in dir(module):
        
        # avoid base_class - base_class comparison at issubclass()
        if( name == base_class.__name__ ):
            continue
        obj = getattr( module, name )
        try:
            if( issubclass(obj, base_class) ):
                return obj
        except TypeError:  # If 'obj' is not a class
            pass
    return None



#TODO: Refactor plugin module import process. 2020.06.27
def LoadNodePlugin( nodeTypeManager ):

    pkg_name = 'nodepad.plugins'

    # get package path
    plugin_paths = glob.glob( os.getcwd()+'/**/plugins/', recursive=True )

    # import node plugins
    for importer, modname, ispkg in pkgutil.iter_modules( plugin_paths ):

        try:
            #print( 'Found submodule %s (is a package: %s)' % (modname, ispkg) )
            module = importlib.import_module( pkg_name + '.' + modname )

            # Get PluginBase's subclass
            classObj = GetSubclass( module, PluginBase )
        
            if( classObj ):
                # Create Instance
                pluginInstance = classObj()
        
                # Initialize plugin
                pluginInstance.Register( nodeTypeManager )
            else:
                print( 'Failed creating class instance from module: %s' % modname )

        except:
            traceback.print_exc()
