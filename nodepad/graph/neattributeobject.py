import copy

from ..component.descriptors import *
from ..component.nedata import NEData

from .negraphobject import *
from .neconnectionobject import *




class NEAttributeObject(NEGraphObject):

    def __init__( self, attribDesc, obj_id, parent_id ):
        super(NEAttributeObject, self).__init__( attribDesc.Name(), attribDesc.AttributeType(), obj_id=obj_id )
        
        self.__m_Desc = copy.deepcopy( attribDesc )
        self.__m_Desc._AttribDesc__m_ObjectID = ( parent_id, self.ID() )
        self.__m_refConnections = {}
        self.__m_bLock = False
        self.__m_refData = None

        

    def Release( self ):
        self.ClearConnection()
        super(NEAttributeObject, self).Release()

        self.__m_refData = None



    # override SetParent
    def SetParent( self, parent, bRegisterAsChild=True ):
        super(NEAttributeObject, self).SetParent(parent, bRegisterAsChild)

        self.__m_Desc._AttribDesc__m_ObjectID = ( parent.ID(), self.ID() )



    # owner node
    def ParentNode( self ):
        return self.Parent() if self._NEObject__m_ObjectType=='Attribute' else self.Parent().Parent()
        # ノードアトリビュートの場合: 自信の親(ノード)を返す.
        # それ以外(シンボリックリンク)の場合: シンボリックリンク->親(グループIO)->さらに親(グループ)を返す.



    # return opened space for connection
    def ParentSpace( self ):

        if( self._NEObject__m_ObjectType=='ExposedSymbolicLink' ):
            return self.Parent().Parent().Parent()
        elif( self._NEObject__m_ObjectType=='ProtectedSymbolicLink' ):
            return self.Parent().Parent()
        else:
            return self.Parent().Parent()
        #   'ExposedSymbolicLink': シンボリックリンクを保持するグループのさらに親をたどる
        #   'ProtectedSymbolicLink': シンボリックリンクを保持するグループのIDを返す
        #   'Attribute': アトリビュートの親ノードを保持するスペース



    def BindConnection( self, pconn ):
        self.__m_refConnections[ pconn.ID() ] = pconn


    def UnbindConnection( self, pconn ):
        try:
            self.__m_refConnections[ pconn.ID() ] = None
            del self.__m_refConnections[ pconn.ID() ]
        except:
            pass


    def ClearConnection( self ):
        self.__m_refConnections.clear()


    def GetDesc( self ):
        return  self.__m_Desc


    def DataFlow( self ):
        return self.__m_Desc.DataFlow()


    def IsInputFlow( self ):
        return self.__m_Desc.IsInputFlow()


    def IsOutputFlow( self ):
        return self.__m_Desc.IsOutputFlow()


    def MultipleConnectAllowed( self ):
        return self.__m_Desc.MultipleConnectAllowed()


    def Connections( self ):
        return self.__m_refConnections


    def ConnectionIDs( self ):
        return [ v.ID() for v in self.__m_refConnections.values() ]


    def Value( self ):
        return self.__m_refData.Value()


    def SetValue( self, value ):
        self.__m_refData.SetValue( value )


    def Data( self ):
        return self.__m_refData


    def BindData( self, data ):
        self.__m_refData = data


    def UnbindData( self ):
        self.__m_refData = None


    def DataType( self ):
        return self.__m_Desc.DataType()


    def SetEditable( self, state ):
        self.__m_Desc.SetEditale( state )

    def IsEditable( self ):
        return self.__m_Desc.IsEditable()

    def SetEnable( self, state ):
        self.__m_Desc.SetEnable( state )

    def Enabled( self ):
        return self.__m_Desc.Enabled()


    def AttributeID( self ):
        return self.__m_Desc._AttribDesc__m_ObjectID


    def FullKey( self, suffix='' ):
        if( self._NEGraphObject__m_Parent ):
            return self._NEGraphObject__m_Parent.FullKey('.') + self._NEObject__m_Key + suffix
        else:
            return self._NEObject__m_Key + suffix


    def IsConnected( self, attrib ):

        if( self.__m_Desc.IsInputFlow() ):
            for conn in self.__m_refConnections.values():
                if( conn.Source() == attrib ):
                    print( '  NEAttributeObject::IsConnected()... Detected ' + attrib.FullKey() + '->' + self.FullKey() + 'Connection.' )
                    return True

        elif( self.__m_Desc.IsOutputFlow() ):
            for conn in self.__m_refConnections.values():
                if( conn.Destination() == attrib ):
                    print( '  NEAttributeObject::IsConnected()... Detected ' + self.FullKey() + '->' + attrib.FullKey() + 'Connection.' )
                    return True

        return False


    def IsConnectedFrom( self, attrib_src ):

        if( self.__m_Desc.IsInputFlow() ):
            for conn in self.__m_refConnections.values():
                if( conn.Source() == attrib_src ):
                    print( '  NEAttributeObject::IsConnectedFrom()... Detected ' + attrib_src.FullKey() + '->' + self.FullKey() + 'Connection.' )
                    return True

        return False


    def IsConnectedTo( self, attrib_dest ):

        if( self.__m_Desc.IsOutputFlow() ):
            for conn in self.__m_refConnections.values():
                if( conn.Destination() == attrib_dest ):
                    print( '  NEAttributeObject::IsConnectedTo()... Detected ' + self.FullKey() + '->' + attrib_dest.FullKey() + 'Connection.' )
                    return True

        return False


    def GetConnectionFrom( self, attrib_src ):
        for conn in self.__m_refConnections.values():
            if( conn.Source() == attrib_src ):
                return conn
        return None


    def GetConnectionTo( self, attrib_dest ):
        for conn in self.__m_refConnections.values():
            if( conn.Destination() == attrib_dest ):
                return conn
        return None


    def GetConnectedAttributes( self ):
        return [ (conn.Source() if self.__m_Desc.IsInputFlow() else conn.Destination()) for conn in self.__m_refConnections.values() ]


    def GetSourceAttributes( self ):
        return [ conn.Source() for conn in self.__m_refConnections.values() ]


    def GetDestinationAttributes( self ):
        return [ conn.Destination() for conn in self.__m_refConnections.values() ]


    def GetConnectedAttributeIDs( self ):
        return [ (conn.Source().AttributeID() if self.__m_Desc.IsInputFlow() else conn.Destination().AttributeID()) for conn in self.__m_refConnections.values() ]


    def GetSourceAttributeIDs( self ):
        return [ conn.Source().AttributeID() for conn in self.__m_refConnections.values() ]


    def GetDestinationAttributeIDs( self ):
        return [ conn.Destination().AttributeID() for conn in self.__m_refConnections.values() ]


    def HasConnections( self ):
        return bool( self.__m_refConnections )


    def IsConnectable( self, attrib ):

        if( self.ParentSpace().ID() != attrib.ParentSpace().ID() ):
            print( 'Unable to connect: Different Node Hierarchy...' )
            return False

        if( self.__m_bLock or attrib.__m_bLock ):
            print( 'Unable to connect: Connection Operation is Frozen state...' )
            return False

        if( self.__m_Desc.DataFlow()==attrib.__m_Desc.DataFlow() ):
            print( 'Unable to connect: Incorrect DataFlow Combination...' )
            return False
        
        if( not self.__m_Desc.ConnectableTypes().intersection(attrib.__m_Desc.ConnectableTypes()) ):
        #if( not self.__m_Desc.DataType().intersection(attrib.__m_Desc.DataType()) ):
            print( 'Unable to connect: Different DataType...' )
            return False


        return True


    def IsLocked( self ):
        return self.__m_bLock


    def Info( self ):
        print( '  - ' + self.FullKey() + ' Connections:' )

        if( not self.__m_refConnections ):
            print( '     None' )
        else:
            for conn in self.__m_refConnections.values():
                print( '     ' + conn.FullKey() )
