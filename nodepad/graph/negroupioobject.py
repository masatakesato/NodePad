from collections import defaultdict
import traceback


from ..component.neobjectarray import *

from .neattributeobject import *
from .nenodeobject import *
from .nesymboliclink import *
from .neconnectionobject import *



class NEGroupIOObject(NEGraphObject):

    def __init__( self, dataflow, obj_id=None ):
        super(NEGroupIOObject, self).__init__( 'Group Input' if dataflow==DataFlow.Input else 'Group Output', 'GroupIO', obj_id=obj_id )
        
        self.__m_LayoutDesc = AttribLayoutDesc()
        self.__m_Desc = NodeDesc( 'GroupIO', self.__m_LayoutDesc )
        self.__m_Desc.SetEnable( False )
        self.__m_DataFlow = dataflow
        self.__m_refAttributes = {}

        self.__m_SymbolicLinkArray = NEObjectArray()# key: uuid/name/index, value: NESymbolicLink


    def Release( self ):
        for linknode in self.__m_SymbolicLinkArray.values(): linknode.Release()
        self.__m_SymbolicLinkArray.clear()

        super(NEGroupIOObject, self).Release()


    #def HasAttribute( self, attr_id ):
    #    return len(self.__m_SymbolicLinkArray) > 0


    def NumAttributes( self ):
        return len(self.__m_refAttributes)


    def Attributes( self ):
        return self.__m_refAttributes 

    
    def Attribute( self, query ):
        if( query in self.__m_SymbolicLinkArray ):
            return self.__m_SymbolicLinkArray[ query ].ExposedAttribute()
        return None


    def RenameAttribute( self, attr_id, newkey ):

        if( not attr_id in self.__m_refAttributes ):
            return False

        refAttrib = self.__m_refAttributes[ attr_id ]
        self.__m_SymbolicLinkArray.setname( refAttrib.ParentKey(), newkey )# Update self.__m_SymbolicLinkArray's key
        self.__m_SymbolicLinkArray[ attr_id ].RenameAttribute(newkey)# Update Attribute's key
        
        return True


    def DataFlow( self ):
        return self.__m_DataFlow


    def GetDesc( self ):
        return  self.__m_Desc


    def FullKey( self, suffix='' ):
        if( self._NEGraphObject__m_Parent ):
            return self._NEGraphObject__m_Parent.FullKey('|') + self._NEObject__m_Key + suffix
        else:
            return self._NEObject__m_Key + suffix


    def NumSymbolicLinks( self ):
        return len(self.__m_SymbolicLinkArray)


    def SymbolicLink( self, query ):
        try:
            return self.__m_SymbolicLinkArray[ query ]
        except:
            traceback.print_exc()
            return None


    def SymbolicLinks( self ):
        return self.__m_SymbolicLinkArray


    # シンボリックリンクが既に存在するかどうかチェック
    def SymbolicLinkExists( self, attrib ):
        for linknode in self.__m_SymbolicLinkArray.values():# 既にシンボリックリンクノードが存在する場合も、重複作成防止のため中止
            if( attrib.AttributeID() in linknode.ProtectedAttribute().GetConnectedAttributeIDs() ):
                return True
        return False


    def BindSymbolicLink( self, refSymbolicLink, reserved_slot_index=-1 ):
        
        refAttrib = refSymbolicLink.ExposedAttribute()
        slot_index = len(self.__m_SymbolicLinkArray) if reserved_slot_index==-1 else reserved_slot_index

        refSymbolicLink.SetParent( self.Parent(), False )
        refSymbolicLink.SetSlotIndex( slot_index )
        
        self.__m_refAttributes[ refAttrib.ID() ] = refAttrib
        self.__m_LayoutDesc.AddAttribDesc( refAttrib.GetDesc(), slot_index )# ここで要素番号を指定できるようにする？

        self.__m_SymbolicLinkArray[ refAttrib.ID() ] = refSymbolicLink
        self.__m_SymbolicLinkArray.setindex( len(self.__m_SymbolicLinkArray)-1, slot_index )

        # Update indices
        for i in range( slot_index+1, len(self.__m_SymbolicLinkArray) ):
            self.__m_SymbolicLinkArray[i].SetSlotIndex(i)
            #print( i, self.__m_SymbolicLinkArray[i].SlotIndex() )


    def UnbindSymbolicLink( self, refSymbolicLink ):
        
        refAttrib = refSymbolicLink.ExposedAttribute()
        slot_index = refSymbolicLink.SlotIndex()
        
        refSymbolicLink.SetParent( self.Parent().Parent(), False )
        refSymbolicLink.SetSlotIndex(-1)

        del self.__m_SymbolicLinkArray[ refAttrib.ID() ]

        self.__m_refAttributes[ refAttrib.ID() ] = None
        del self.__m_refAttributes[ refAttrib.ID() ]
        self.__m_LayoutDesc.RemoveAttribDesc( refAttrib.GetDesc() )

        # update indices
        for i in range( slot_index, len(self.__m_SymbolicLinkArray) ):
            self.__m_SymbolicLinkArray[i].SetSlotIndex(i)
            #print( i, self.__m_SymbolicLinkArray[i].SlotIndex() )


    def UnbindAllSymbolicLinks( self ):
        keys = set(self.__m_SymbolicLinkArray.keys())
        for k in keys:
            self.UnbindSymbolicLink(self.__m_SymbolicLinkArray[k])


    def SetSymbolicLinkSlotIndex( self, src_idx, dst_idx ):

        self.__m_SymbolicLinkArray.setindex( src_idx, dst_idx )

        start = min( src_idx, dst_idx )
        count = max( src_idx, dst_idx ) + 1

        for i in range( start, count ):
            self.__m_SymbolicLinkArray[i].SetSlotIndex(i)
            #print( i, self.__m_SymbolicLinkArray[i].SlotIndex() )

        self.__m_LayoutDesc.ChangeOrder( src_idx, dst_idx, self.__m_SymbolicLinkArray[ dst_idx ].ExposedAttribute().DataFlow() )


    def Info( self ):
        print( '//------------- GroupIO: ' + self.FullKey() + ' -------------//' )
        self.__m_SymbolicLinkArray.Info()
        #for attrib in self.__m_refAttributes.values():
        #    print( '    ' + attrib.Key() )


    def GetSnapshot( self ):
        return NEGroupIOSnapshot( self )


    def SetKey( self, key ):
        print( 'Rename forbidden...' )
        return False


class NEGroupIOSnapshot():

    def __init__( self, refObj ):
        self.__m_NodeArgs = (refObj.ObjectType(), refObj.GetPosition(), refObj.ID(), refObj.Key(), refObj.ParentID(), refObj.DataFlow() )


    def ObjectType( self ):
        return self.__m_NodeArgs[0]


    def Translation( self ):
        return self.__m_NodeArgs[1]


    def ObjectID( self ):
        return self.__m_NodeArgs[2]


    def Key( self ):
        return self.__m_NodeArgs[3]


    def ParentID( self ):
        return self.__m_NodeArgs[4]


    def DataFlow( self ):
        return self.__m_NodeArgs[5]
