from nodepad.factory.pluginbase import *


class MultNode(PluginBase):

    def __init__(self):
        super(MultNode, self).__init__( 'Multiply' )


    def Initialize( self ):
        print( 'MultNode::Initialize()...' )
        
        # Set Classname
        #self.SetClassName( 'Multiply' )

        # Add attributes
        self.AddAttribute( 'Attribute', DataFlow.Input, float, False, True, 'Value1', 5.0, {int, float, bool} )
        self.AddAttribute( 'Attribute', DataFlow.Input, float, False, True, 'Value2', 0.5, {int, float, bool} )
        self.AddAttribute( 'Attribute', DataFlow.Output, float, True, False, 'Result', 1.0 )


    def Compute( self, dataBlock ):
        print( 'MultNode::Compute()...' )
        
        value1 = dataBlock.GetInput( 'Value1' )# 複数ある場合はlistに詰めたデータがほしい
        value2 = dataBlock.GetInput( 'Value2' )# 複数ある場合はlistに詰めたデータがほしい

        dataBlock.SetOutput( 'Result', float(value1) * float(value2) )

        print( 'Value1:', value1 )
        print( 'Value2:', value2 )

        print( 'Result:', dataBlock.GetOutput('Result') )