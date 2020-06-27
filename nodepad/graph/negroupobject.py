from collections import defaultdict
import traceback

from ..component.neobjectarray import *

from ..config.figure_params import *

from .neattributeobject import *
from .nenodeobject import *
from .nesymboliclink import *
from .neconnectionobject import *
from .negroupioobject import *




class NEGroupObject(NEGraphObject):

    def __init__( self, name, obj_id=None ):
        super(NEGroupObject, self).__init__( name, 'Group', obj_id=obj_id )

        self.__m_LayoutDesc = AttribLayoutDesc()
        self.__m_Desc = NodeDesc( 'Group', self.__m_LayoutDesc )
        self.__m_refGroupIOs = {}
        self.__m_refAttributes = {}


    def Release( self ):
        self.__m_refAttributes.clear()
        self.__m_refGroupIOs.clear()

        super(NEGroupObject, self).Release()


    def AddMember( self, obj ):

        if( isinstance( obj, NEGroupIOObject ) ):
            self.__m_refGroupIOs[ obj.DataFlow() ] = obj
        
        obj.SetParent(self)
        
        # TODO: 座標変換の動作検証用コード.リファクタリング必要. objをワールド座標系からselfのローカル座標系へ変換する. 2017.09.23
        space = self
        pos_stack = []
        while( space != None ):
            pos_stack.append( space.GetPosition() )
            space = space.Parent()

        obj_pos = list(obj.GetPosition())

        for pos in reversed(pos_stack):
            obj_pos[0] -= pos[0]
            obj_pos[1] -= pos[1]

        obj.SetTranslation( ( obj_pos[0], obj_pos[1] ) )




    def RemoveMember( self, obj_id ):

        obj = self.Child(obj_id)

        if( isinstance( obj, NEGroupIOObject ) ):
            self.__m_refGroupIOs[ obj.DataFlow() ] = None
            del self.__m_refGroupIOs[ obj.DataFlow() ]

        obj.SetParent(None)

        # TODO: 座標変換の動作検証用コード.リファクタリング必要. objをselfのローカル座標系からワールド座標系へ変換する. 2017.09.23
        space = self
        pos_stack = []
        while( space != None ):
            pos_stack.append( space.GetPosition() )
            space = space.Parent()

        obj_pos = list(obj.GetPosition())

        for pos in pos_stack:
            obj_pos[0] += pos[0]
            obj_pos[1] += pos[1]

        obj.SetTranslation( ( obj_pos[0], obj_pos[1] ) )



    def GetMemberIDs( self ):
        connection_ids = set()
        object_ids = set()
        for child in self.Children().values():
            connection_ids.add( child.ID() ) if isinstance(child, NEConnectionObject) else object_ids.add( child.ID() )
 
        return connection_ids, object_ids


    def HasAttribute( self, attr_id ):
        return attr_id in self.__m_refAttributes


    def NumAttributes( self ):
        return len(self.__m_refAttributes)


    def Attributes( self ):
        return self.__m_refAttributes 

    
    def AttributeByID( self, query ):
        try:
            return self.__m_refAttributes[ query ] 
        except:
            traceback.print_exc()
            return None


    def AttributeByName( self, query ):
        attrib = self.__m_refGroupIOs[ DataFlow.Input ].Attribute( query )
        if( attrib ): return attrib
        return self.__m_refGroupIOs[ DataFlow.Output ].Attribute( query )


    def NumInputAttributes( self ):
        return self.__m_refGroupIOs[ DataFlow.Input ].NumAttributes() if DataFlow.Input in self.__m_refGroupIOs else 0

    def InputAttributes( self ):
        try:
            return self.__m_refGroupIOs[ DataFlow.Input ]._NEGroupIOObject__m_refAttributes
        except:
            traceback.print_exc()
            return {}

    def InputAttribute( self, query ):
        return self.__m_refGroupIOs[ DataFlow.Input ].Attribute( query )


    def NumOutputAttributes( self ):
        return self.__m_refGroupIOs[ DataFlow.Output ].NumAttributes() if DataFlow.Output in self.__m_refGroupIOs else 0

    def OutputAttributes( self ):
        try:
            return self.__m_refGroupIOs[ DataFlow.Output ]._NEGroupIOObject__m_refAttributes
        except:
            traceback.print_exc()
            return {}

    def OutputAttribute( self, query ):
        return self.__m_refGroupIOs[ DataFlow.Output ].Attribute( query )


    def RenameAttribute( self, attr_id, newkey ):
        try:
            self.__m_refGroupIOs[ self.__m_refAttributes[ attr_id ].DataFlow() ].RenameAttribute( attr_id, newkey )
            return True
        except:
            traceback.print_exc()
            return False
    

    def GroupIOs( self ):
        return list( self.__m_refGroupIOs.values() )


    def GroupIOIDs( self ):
        return [ v.ID() for v in self.__m_refGroupIOs.values() ]



    def GetDesc( self ):
        return  self.__m_Desc


    def FullKey( self, suffix='' ):
        if( self._NEGraphObject__m_Parent ):
            return self._NEGraphObject__m_Parent.FullKey('|') + self._NEObject__m_Key + suffix
        else:
            return self._NEObject__m_Key + suffix


    def UngroupChildren( self ):
        for key in self.ChildrenID():
            self.Children()[key].SetParent( self.Parent() )


    def GroupInput( self ):
        try:
            return self.__m_refGroupIOs[ DataFlow.Input ]
        except:
            traceback.print_exc()
            return None


    def GroupOutput( self ):
        try:
            return self.__m_refGroupIOs[ DataFlow.Output ]
        except:
            traceback.print_exc()
            return None


    # シンボリックリンク化できるかどうかチェック.
    def CanSymbolize( self, attrib ):
        
        # アトリビュートの親ノードがグループ内に存在しない場合はFalse
        parent_id = attrib.ParentNode().ID()
        if( not parent_id in self.Children() ):
            return False
        
        attrib_id = attrib.ID()

        # アトリビュート自体がグループ内に存在しない場合もFalse
        if( self.Child(parent_id).HasAttribute(attrib_id)==False ):
            return False

        # 既にシンボリックリンクノードが存在する場合も、重複作成防止のためFalse
        if( self.__m_refGroupIOs[ DataFlow.Input ].SymbolicLinkExists( attrib )==True ):
            return False

        if( self.__m_refGroupIOs[ DataFlow.Output ].SymbolicLinkExists( attrib )==True ):
            return False


        return True


    def BindSymbolicLink( self, refSymbolicLink, reserved_slot_index=-1 ):
        
        refAttrib = refSymbolicLink.ExposedAttribute()
        slot_index = self.__m_refGroupIOs[ refSymbolicLink.DataFlow() ].NumAttributes() if reserved_slot_index==-1 else reserved_slot_index

        self.__m_refAttributes[ refAttrib.ID() ] = refAttrib
        self.__m_LayoutDesc.AddAttribDesc( refAttrib.GetDesc(), slot_index )

        self.__m_refGroupIOs[ refSymbolicLink.DataFlow() ].BindSymbolicLink( refSymbolicLink, slot_index )


    def UnbindSymbolicLink( self, refSymbolicLink ):
        
        refAttrib = refSymbolicLink.ExposedAttribute()

        self.__m_refGroupIOs[ refSymbolicLink.DataFlow() ].UnbindSymbolicLink( refSymbolicLink )

        self.__m_refAttributes[ refAttrib.ID() ] = None
        del self.__m_refAttributes[ refAttrib.ID() ]
        self.__m_LayoutDesc.RemoveAttribDesc( refAttrib.GetDesc() )


    def UnbindAllSymbolicLinks( self ):
        try:
            self.__m_refGroupIOs[ DataFlow.Input ].UnbindAllSymbolicLinks()
            self.__m_refGroupIOs[ DataFlow.Output ].UnbindAllSymbolicLinks()
        except:
            traceback.print_exc()


    def SetSymbolicLinkSlotIndex( self, refSymbolicLink, slot_index ):
        try:
            src_idx = refSymbolicLink.SlotIndex()
            self.__m_refGroupIOs[ refSymbolicLink.DataFlow() ].SetSymbolicLinkSlotIndex( src_idx, slot_index )
            self.__m_LayoutDesc.ChangeOrder( src_idx, slot_index, refSymbolicLink.DataFlow() )
            return True
        except:
            traceback.print_exc()
            return False


    def CollectInternalConnections( self ):

        internal_connections = []

        for obj in self.Children().values():
            for attrib in obj.OutputAttributes().values():
                internal_connections += [ conn.ID() for conn in attrib.Connections().values() if( conn.Source().ParentNode().ID() in self.Children() ) ]

        return internal_connections


    def Info( self ):
        print( '//------------- Group: ' + self.FullKey() + ' -------------//' )
        if( self.Parent() ):
            print( 'Parent: %s' % self.Parent().Key() )

        print( 'Group Members:' )
        for child in self.Children().values():
            print( '    %s' % child.Key() )

        if( DataFlow.Input in self.__m_refGroupIOs ):
            print( 'Input SymbolicLinks:' )
            for v in self.__m_refGroupIOs[ DataFlow.Input ].SymbolicLinks().values():
                print( '    %s' % v.Key() )

        if( DataFlow.Output in self.__m_refGroupIOs ):
            print( 'Output SymbolicLinks:' )
            for v in self.__m_refGroupIOs[ DataFlow.Output ].SymbolicLinks().values():
                print( '    %s' % v.Key() )


    def GetSnapshot( self ):
        return NEGroupSnapshot( self )



######################### TODO: 試験実装. QGraphicsItemの外部で形状パラメータを保持したい ############################

    # Overriding NEGraphObject::SetSize
    def SetSize( self, size=None ):
        if( size ):
            super(NEGroupObject, self).SetSize(size)
        else:
            numslots = max( 1, max( self.NumInputAttributes(), self.NumOutputAttributes() ) )
            width = g_GroupMinWidth + g_GroupFrameWidth * 2
            height = ( g_GroupMinHeight + numslots * g_AttribAreaHeight ) + g_GroupFrameWidth * 2
            super(NEGroupObject, self).SetSize( [ width, height ] )









class NEGroupSnapshot():

    def __init__( self, refObj ):

        self.__m_NodeArgs = None
        self.__m_MemberIDs = None
        
        self.__CollectNodeArgs( refObj )


    def ObjectType( self ):
        return self.__m_NodeArgs[0]


    def Translation( self ):
        return self.__m_NodeArgs[1]


    def Size( self ):
        return self.__m_NodeArgs[2]


    def ObjectID( self ):
        return self.__m_NodeArgs[3]


    def Key( self ):
        return self.__m_NodeArgs[4]


    def ParentID( self ):
        return self.__m_NodeArgs[5]


    def MemberIDs( self ):
        return self.__m_MemberIDs


    def __CollectNodeArgs( self, refObj ):

        excludetypes = ( NEConnectionObject, NEGroupIOObject )
        object_id = refObj.ID()

        self.__m_NodeArgs = (refObj.ObjectType(), refObj.GetPosition(), refObj.GetSize(), object_id, refObj.Key(), refObj.ParentID() )
        self.__m_MemberIDs = [ obj.ID() for obj in refObj.Children().values() if not type(obj) in excludetypes ]# ConnectionObject, GroupIOObjectはスナップショットから除外