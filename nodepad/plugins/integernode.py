from nodepad.factory.pluginbase import *


class IntegerNode(PluginBase):

    def __init__(self):
        super(IntegerNode, self).__init__( 'Integer' )


    def Initialize( self ):
        print( 'IntegerNode::Initialize()...' )
        
        # Set Classname
        #self.SetClassName( 'Integer' )

        # Add attributes
        self.AddAttribute( 'Attribute', DataFlow.Output, int, True, True, 'Output', 0 )


    def Compute( self, dataBlock ):
        pass
