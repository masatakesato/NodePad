from nodepad.factory.pluginbase import *


class Plugin3(PluginBase):

    def __init__(self):
        super(Plugin3, self).__init__( 'TestNode3' )


    def Initialize( self ):
        print( 'Plugin3::Initialize()...' )
        
        # Set Classname
        #self.SetClassName( 'TestNode3' )

        # Add attributes
        self.AddAttribute( 'Attribute', DataFlow.Input, str, False, True, 'In', 'Value', {str} )
        self.AddAttribute( 'Attribute', DataFlow.Input, int, False, True, 'In2', 0, {int} )
        self.AddAttribute( 'Attribute', DataFlow.Output, float, True, False, 'Out', 2.5 )
        self.AddAttribute( 'Attribute', DataFlow.Output, float, True, False, 'Out2', 2.5 )


    def Compute( self, dataBlock ):
        print( 'Plugin3::Compute()...' )
