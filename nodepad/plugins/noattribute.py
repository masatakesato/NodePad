from nodepad.factory.pluginbase import *


class NoAttribute(PluginBase):

    def __init__(self):
        super(NoAttribute, self).__init__( 'NoAttribute' )


    def Initialize( self ):
        print( 'NoAttribute::Initialize()...' )
        
        # Set Classname
        #self.SetClassName( 'NoAttribute' )

        # Add attributes


    def Compute( self, dataBlock ):
        pass
