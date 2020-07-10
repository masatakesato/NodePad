import copy
import traceback


from ..component.descriptors import *

from .negraphobject import *
from .neattributeobject import NEAttributeObject
from .nerootobject import NERootObject




class NESymbolicLink(NEGraphObject):

    __key = { 'ProtectedSymbolicLink':'Internal', 'ExposedSymbolicLink':'External' }

    def __init__( self, key, nodeType, attribDesc, value, obj_id, attrib_ids ):
        super(NESymbolicLink, self).__init__( key, nodeType, obj_id=obj_id )

        self.__m_LayoutDesc = AttribLayoutDesc()
        self.__m_Desc = NodeDesc( nodeType, self.__m_LayoutDesc )
        self.__m_SlotIndex = -1# Group's SymbolicLink Intex

        self.__m_Attributes = {}
        self.__m_refInputs = {}
        self.__m_refOutputs = {}

        self.__m_ExposedID = None
        self.__m_ProtectedID = None
        self.__m_KeyMap = {}

        self.__m_Desc._NodeDesc__m_ObjectID = self.ID()

        if( attribDesc.IsInputFlow() ):
            in_attribDesc = AttribDesc( 'ExposedSymbolicLink', DataFlow.Input, attribDesc.DataType(), attribDesc.MultipleConnectAllowed(), attribDesc.IsEditable(), key, value, attribDesc.ConnectableTypes() )#'In'
            self.__m_ExposedID = self.__AddAttribute( in_attribDesc, attrib_ids[0] )

            out_attribDesc = AttribDesc( 'ProtectedSymbolicLink', DataFlow.Output, attribDesc.DataType(), True, False, key, value, attribDesc.ConnectableTypes() )#'Out'
            self.__m_ProtectedID = self.__AddAttribute( out_attribDesc, attrib_ids[1] )

            self.__m_refInputs[ self.__m_ExposedID ] = self.__m_Attributes[ self.__m_ExposedID ]
            self.__m_refOutputs[ self.__m_ProtectedID ] = self.__m_Attributes[ self.__m_ProtectedID ]

        elif( attribDesc.IsOutputFlow() ):
            in_attribDesc = AttribDesc( 'ProtectedSymbolicLink', DataFlow.Input, attribDesc.DataType(), False, False, key, value, attribDesc.ConnectableTypes() )#'In'
            self.__m_ProtectedID = self.__AddAttribute( in_attribDesc, attrib_ids[0] )

            out_attribDesc = AttribDesc( 'ExposedSymbolicLink', DataFlow.Output, attribDesc.DataType(), attribDesc.MultipleConnectAllowed(), attribDesc.IsEditable(), key, value, attribDesc.ConnectableTypes() )#'Out'
            self.__m_ExposedID = self.__AddAttribute( out_attribDesc, attrib_ids[1] )

            self.__m_refInputs[ self.__m_ProtectedID ] = self.__m_Attributes[ self.__m_ProtectedID ]
            self.__m_refOutputs[ self.__m_ExposedID ] = self.__m_Attributes[ self.__m_ExposedID ]

        # self.__m_Attributes[ self.__m_ProtectedID ]._NEAttributeObject__m_bLock = False # コネクションロックなし。


    def Release( self ):
        self.__m_refInputs.clear()
        self.__m_refOutputs.clear()
        self.__m_Attributes.clear()
        self.__m_KeyMap.clear()
        super(NESymbolicLink, self).Release()


    def SetSlotIndex( self, index ):
        self.__m_SlotIndex = index


    def SlotIndex( self ):
        return self.__m_SlotIndex


    # override SetParent
    def SetParent( self, parent, bRegisterAsChild=True ):
        super(NESymbolicLink, self).SetParent(parent, False)


    def HasAttribute( self, attr_id ):
        return attr_id in self.__m_Attributes


    def Attributes( self ):
        return self.__m_Attributes


    #def Attribute( self, attribname ):

    #    if( isinstance(attribname,str) ):
    #        if( attribname in self.__m_KeyMap ):
    #            return self.__m_Attributes[ self.__m_KeyMap[attribname] ]
    #        return None

    #    elif( isinstance(attribname,uuid.UUID) ):
    #        if( attribname in self.__m_Attributes ):
    #            return self.__m_Attributes[ attribname ]
    #        return None

    #    return None


    def AttributeByID( self, query ):
        try:
            return self.__m_Attributes[ query ]
        except:
            traceback.print_exc()
            return None


    def AttributeByName( self, query ):
        try:
            return self.__m_Attributes[ self.__m_KeyMap[query] ]
        except:
            traceback.print_exc()
            return None



    def InputAttributes( self ):
        return self.__m_refInputs



    def InputAttribute( self ):
        return set(self.__m_refInputs.values())[0]



    def OutputAttributes( self ):
        return self.__m_refOutputs



    def OutputAttribute( self ):
        return set(self.__m_refOutputs.values())[0]



    def ExposedAttribute( self ):
        return self.__m_Attributes[ self.__m_ExposedID ]



    def ProtectedAttribute( self ):
        return self.__m_Attributes[ self.__m_ProtectedID ]



    def RenameAttribute( self, newkey ):
        try:
            self.SetKey( newkey )
            self.__m_Attributes[ self.__m_ExposedID ].GetDesc().SetName( newkey )
            self.__m_Attributes[ self.__m_ProtectedID ].GetDesc().SetName( newkey )      
            return True

        except:
            traceback.print_exc()
            return False



    def __AddAttribute( self, attribDesc, attr_id ):

        attrib = NEAttributeObject( attribDesc, attr_id, self.ID() )
        attrib.SetParent( self, False )

        self.__m_Attributes[ attrib.ID() ] = attrib
        self.__m_KeyMap[ self.__key[ attribDesc.AttributeType() ] ] = attrib.ID()
        self.__m_LayoutDesc.AddAttribDesc( attrib.GetDesc() )

        return attrib.ID()



    def ReferredAttributeID( self ):
        try:
            return self.ProtectedAttribute().GetConnectedAttributeIDs()[0]
        except:
            traceback.print_exc()
            return (None, None)



    def IDSet( self ):
        return ( self.ID(), next(iter(self.__m_refInputs)), next(iter(self.__m_refOutputs)) )



    def DataFlow( self ):
        return self.__m_Attributes[ self.__m_ExposedID ].DataFlow()



    def GetDesc( self ):
        return  self.__m_Desc



    def FullKey( self, suffix='' ):
        if( self._NEGraphObject__m_Parent ):
            return self._NEGraphObject__m_Parent.FullKey('|') + self._NEObject__m_Key + suffix
        return self._NEObject__m_Key + suffix



    def ExtractConnections( self ):

        direct_connect_list = []# [ (source_id, dest_id), (source_id, dest_id)... ]
        #direct_connect_dict = {}# [ conn_id:(source_id, dest_id), conn_id:(source_id, dest_id)... ]

        if( self.__m_Attributes[ self.__m_ProtectedID ].HasConnections()==False ):# protectedコネクションがある場合だけ、コネクション接続情報を収集する
            return direct_connect_list

        exposedAttr = self.__m_Attributes[ self.__m_ExposedID ]
        protectedAttr = self.__m_Attributes[ self.__m_ProtectedID ]

        if( self._NEObject__m_ObjectType=='InputSymbolicLink' ):
            for source_id in exposedAttr.GetConnectedAttributeIDs():
                for dest_id in protectedAttr.GetConnectedAttributeIDs():
                    direct_connect_list.append( (source_id, dest_id) )

        elif( self._NEObject__m_ObjectType=='OutputSymbolicLink' ):
            for source_id in protectedAttr.GetConnectedAttributeIDs():
                for dest_id in exposedAttr.GetConnectedAttributeIDs():
                    direct_connect_list.append( (source_id, dest_id) )

        return direct_connect_list



    def IsInputSymbolicLink( self ):
        return self._NEObject__m_ObjectType=='InputSymbolicLink'



    def IsOutputSymbolicLink( self ):
        return self._NEObject__m_ObjectType=='OutputSymbolicLink'



    def GetSnapshot( self ):
        return NESymbolicLinkSnapshot( self )




class NESymbolicLinkSnapshot():

    def __init__( self, refObj ):

        self.__m_NodeArgs = None
        self.__m_AttribArgs = []

        self.__m_GroupID = refObj.ParentID()
        self.__m_AttribDesc = copy.deepcopy(refObj.ExposedAttribute().GetDesc())

        self.__CollectNodeArgs( refObj )



    def Translation( self ):
        return self.__m_NodeArgs[0]



    def ObjectIDSet( self ):
        return self.__m_NodeArgs[1]



    def Key( self ):
        return self.__m_NodeArgs[2]



    def SlotIntex( self ):
        return self.__m_NodeArgs[3]



    def ObjectID( self ):
        return self.__m_NodeArgs[1][0]



    def InputID( self ):
        return self.__m_NodeArgs[1][1]



    def OutputID( self ):
        return self.__m_NodeArgs[1][2]



    #def ProtectedAttribID( self ):
    #    return (self.__m_AttribArgs[0][0:2])
        


    #def ExposedAttribID( self ):
    #    return (self.__m_AttribArgs[1][0:2])



    def AttribArgs( self ):
        return self.__m_AttribArgs



    def __CollectNodeArgs( self, refObj ):

        object_id = refObj.ID()#refObj.IDSet()[0]
        
        # Node Creation params( source_attrib_id, position, object_id(self, and child attributes), name )
        self.__m_NodeArgs = ( refObj.GetPosition(), refObj.IDSet(), refObj.Key(), refObj.SlotIndex() )

        # Attribute settings
        attrib = refObj.ProtectedAttribute()
        self.__m_AttribArgs.append( (object_id, attrib.ID(), attrib.Value()) )

        attrib = refObj.ExposedAttribute()
        self.__m_AttribArgs.append( (object_id, attrib.ID(), attrib.Value()) )



    def GroupID( self ):
        return self.__m_GroupID



    def AttribDesc( self ):
        return self.__m_AttribDesc



    def Value( self ):
        return self.__m_AttribArgs[1][2]