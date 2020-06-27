from .negraphobject import *



class NEConnectionObject(NEGraphObject):

    def __init__( self, connectionType, obj_id=None ):
        super(NEConnectionObject, self).__init__( '', connectionType, obj_id=obj_id )

        self.__m_pSource = None
        self.__m_pDestination = None
        self._NEGraphObject__m_Key = 'connector_' + str(self.ID())


    def Release( self ):
        self.__m_pSource = None
        self.__m_pDestination = None
        super(NEConnectionObject, self).Release()


    def BindSource( self, source ):
        self.__m_pSource = source


    def BindDestination( self, dest ):
        self.__m_pDestination = dest


    def UnbindSource( self ):
        self.__m_pSource = None


    def UnbindDestination( self ):
        self.__m_pDestination = None


    def Source( self ):
        return self.__m_pSource

    def SourceID( self ):
        return self.__m_pSource.ID()

    def SourceKey( self ):
        return self.__m_pSource.Key()

    def SourceAttribID( self ):
        return ( self.__m_pSource.ParentID(), self.__m_pSource.ID() )


    def Destination( self ):
        return self.__m_pDestination

    def DestinationID( self ):
        return self.__m_pDestination.ID()

    def DestinationKey( self ):
        return self.__m_pDestination.Key()

    def DestinationAttribID( self ):
        return ( self.__m_pDestination.ParentID(), self.__m_pDestination.ID() )


    def Info( self ):
        print( '//------------- Connection: ' + self.FullKey() + ' -------------//' )
        if( self.__m_pSource ):
            print( '   Source Attribute: ' + self.__m_pSource.FullKey() )
        if( self.__m_pDestination ):
            print( '   Destination Attribute: ' + self.__m_pDestination.FullKey() )


    def SetTranslation( self, pos ):# Disable position assignment
        pass


    def GetSnapshot( self ):
        return NEConnectionSnapshot( self )


    def SetKey( self, key ):
        print( 'Rename forbidden at NEConnectionObject::SetKey()...' )
        return False



class NEConnectionSnapshot():

    def __init__( self, refObj ):
        self.__m_Args = [ (refObj.Source().ParentID(), refObj.SourceID()), (refObj.Destination().ParentID(), refObj.DestinationID()), refObj.ID(), refObj.Key(), refObj.Visibility() ]


    def SourceAttribID( self ):
        return self.__m_Args[0]


    def DestinationAttribID( self ):
        return self.__m_Args[1]


    def ObjectID( self ):
        return self.__m_Args[2]


    def Key( self ):
        return self.__m_Args[3]


    def Visibility( self ):
        return self.__m_Args[4]
