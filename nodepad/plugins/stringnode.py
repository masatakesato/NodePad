from nodepad.factory.pluginbase import *


class StringNode(PluginBase):

    def __init__(self):
        super(StringNode, self).__init__( 'String' )


    def Initialize( self ):
        print( 'StringNode::Initialize()...' )

        # Set Classname
        #self.SetClassName( 'String' )

        # Add attributes
        self.AddAttribute( 'Attribute', DataFlow.Output, str, True, True, 'Out', 'ggg' )


    def Compute( self, dataBlock ):
        pass
