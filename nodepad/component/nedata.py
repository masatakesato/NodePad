from .descriptors import AttribDesc
from .neobject import NEObject



class NEData(NEObject):
       
    def __init__( self, attribDesc ):
        super(NEData, self).__init__( attribDesc.Name(), 'Data', attribDesc.ObjectID()[1] )

        self.__m_DataType = attribDesc.DataType()
        self.__m_Value = attribDesc.DefaultValue()# 参照を渡したいので
        self.__m_DirtyFlag = True # True: Data is out of date(needs update), False: Data is up to date.
        self.__m_ParentID = attribDesc.ObjectID()[0]

        self.__m_References = []# コネクションされたNEData(複数可)への参照
        
        self.__m_options = { False: self, True: self.Reference }


    def __del__( self ):
        self.Release()


    def Release( self ):
        self.__m_References.clear()


    def Value( self ):
        return self.__m_Value
        

    def SetValue( self, value ):
        self.__m_Value = value


    def SetDirty( self ):
        self.__m_DirtyFlag = True


    def SetClean( self ):
        self.__m_DirtyFlag = False


    def IsDirty( self ):
        return self.__m_DirtyFlag


    def ParentID( self ):
        return self.__m_ParentID


    def BindReference( self, data ):
        #print( 'NEData::BindReference()...', data )
        self.__m_References.append( data )


    def UnbindReference( self, data ):
        #print( 'NEData::UnbindReference()...', data )
        self.__m_References.remove( data )


    def ClearReference( self ):
        #print( 'NEData::ClearReference()...' )
        self.__m_References.clear()


    def HasReference( self ):
        return bool( self.__m_References )


    def NumReferences( self ):
        return len( self.__m_References )


    def Reference( self, idx ):
        return self.__m_References[idx]


    def References( self ):
        return self.__m_References


    def FrontValue( self, idx ):
        return self.__m_References[idx].__m_Value if self.__m_References else self.__m_Value