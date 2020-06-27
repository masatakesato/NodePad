from nodepad.factory.pluginbase import *


class Plugin1(PluginBase):

    def __init__(self):
        super(Plugin1, self).__init__( 'TestNode' )


    def Initialize( self ):
        print( 'Plugin1::Initialize()...' )
        
        # Set Classname
        #self.SetClassName( 'TestNode' )

        # Add attributes
        self.AddAttribute( 'Attribute', DataFlow.Input, bool, False, True, 'Boolean', False, {bool, int} )
        self.AddAttribute( 'Attribute', DataFlow.Input, float, True, True, 'Input1', 0.0, {float, int, bool} )
        self.AddAttribute( 'Attribute', DataFlow.Input, str, False, True, 'Input2', 'textvalue' )
        self.AddAttribute( 'Attribute', DataFlow.Output, float, True, False, 'Output', 2.5 )


    def Compute( self, dataBlock ):
        print( 'Plugin1::Compute()...' )

        print( '# of Input1 connection:', dataBlock.NumInputValues('Input1') )
        for idx in range( dataBlock.NumInputValues('Input1') ):
            print( dataBlock.GetInput( 'Input1', idx ) )