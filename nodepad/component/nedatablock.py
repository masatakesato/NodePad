from collections import defaultdict

from .descriptors import *

from .nedata import NEData
from .nedatabuffer import NEDataBuffer



class NEDataBlock:

    def __init__( self, databuffer ):
        
        self.__m_Inputs = databuffer.Inputs()# defaultdict(list)# アトリビュート実体. 接続元アトリビュートがある場合はリスト先頭は接続先への参照
        self.__m_Outputs = databuffer.Outputs()# defaultdict(list)# アトリビュート実体. 接続元アトリビュートがある場合はリスト先頭は接続先への参照
        self.__m_Constants = databuffer.Constants()


    def __del__( self ):
        self.Release()


    def Release( self ):
        self.__m_Inputs.clear()
        self.__m_Outputs.clear()
        self.__m_Constants.clear()


    def NumInputValues( self, query ):
        return self.__m_Inputs[ query ].NumReferences()

        
    def GetInput( self, query, idx=0 ):
        return self.__m_Inputs[ query ].FrontValue(idx)


    def GetOutput( self, query ):
        return self.__m_Outputs[ query ].Value()


    def SetOutput( self, query, value ):
        self.__m_Outputs[ query ].SetValue( value )


    def GetConstant( self, query ):
        self.__m_Constants[ query ].Value()


    def SetConstant( self, query, value ):
        self.__m_Constants[ query ].SetValue( value )


