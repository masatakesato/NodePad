from nodepad.factory.pluginbase import *


class Plugin2(PluginBase):

    def __init__(self):
        super(Plugin2, self).__init__( 'TestNode2' )


    def Initialize( self ):
        print( 'Plugin2::Initialize()...' )
        
        # Set Classname
        #self.SetClassName( 'TestNode2' )

        # Add attributes
        self.AddAttribute( 'Attribute', DataFlow.Input, float, False, True, 'In', 0.0, {float, int, bool} )
        self.AddAttribute( 'Attribute', DataFlow.Output, float, True, False, 'Out', 2.5 )


    def Compute( self, dataBlock ):
        print( 'Plugin2::Compute()...' )
