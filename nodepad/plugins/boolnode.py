from nodepad.factory.pluginbase import *


class BoolNode(PluginBase):

    def __init__(self):
        super(BoolNode, self).__init__( 'Bool' )


    def Initialize( self ):
        print( 'BoolNode::Initialize()...' )
        
        # Set Classname
        #self.SetClassName( 'Bool' )

        # Add attributes
        self.AddAttribute( 'Attribute', DataFlow.Output, bool, True, True, 'Bool', True )


    def Compute( self, dataBlock ):
        pass
