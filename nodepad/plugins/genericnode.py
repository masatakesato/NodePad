from nodepad.factory.pluginbase import *


class GenericNode(PluginBase):

    def __init__(self):
        super(GenericNode, self).__init__( 'Generic' )


    def Initialize( self ):
        print( 'GenericNode::Initialize()...' )
        
        # Set Classname
        #self.SetClassName( 'Generic' )

        # Add attributes
        self.AddAttribute( 'Attribute', DataFlow.Output, object, True, True, 'Output', 1.0 )


    def Compute( self, dataBlock ):
        pass
