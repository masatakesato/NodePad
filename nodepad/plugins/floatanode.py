from nodepad.factory.pluginbase import *


class FloatNode(PluginBase):

    def __init__(self):
        super(FloatNode, self).__init__( 'Float' )


    def Initialize( self ):
        print( 'FloatNode::Initialize()...' )
        
        # Set Classname
        #self.SetClassName( 'Float' )

        # Add attributes
        self.AddAttribute( 'Attribute', DataFlow.Output, float, True, True, 'Output', 1.0 )# 


    def Compute( self, dataBlock ):
        pass
