from .nedata import NEData
from .neobjectarray import NEObjectArray



class NEDataBuffer:

    def __init__( self ):
        self.__m_Inputs = NEObjectArray()
        self.__m_Outputs = NEObjectArray()
        self.__m_Constants = NEObjectArray()


    def Release( self ):
        self.__m_Inputs.clear()
        self.__m_Outputs.clear()
        self.__m_Constants.clear()
        

    def AllocateInput( self, attribDesc ):
        self.__m_Inputs.append( NEData( attribDesc ), attribDesc.Name() )


    def AllocateOutput( self, attribDesc ):
        self.__m_Outputs.append( NEData( attribDesc ), attribDesc.Name() )


    def AllocateConstant( self, attribDesc ):
        self.__m_Constants.append( NEData( attribDesc ), attribDesc.Name() )


    def Inputs( self ):
        return self.__m_Inputs


    def Outputs( self ):
        return self.__m_Outputs


    def Constants( self ):
        return self.__m_Constants


    def Input( self, query ):
        return self.__m_Inputs[ query ]


    def Output( self, query ):
        return self.__m_Outputs[ query ]


    def Constant( self, query ):
        return self.__m_Constants[ query ]


    def SetClean( self ):
        for data in self.__m_Inputs.values():
            data.SetClean()

        for data in self.__m_Outputs.values():
            data.SetClean()
