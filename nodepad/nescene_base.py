import uuid

from .factory import builder
from .factory.node_manager import *

from .graph.nenodegraph import *


from .plugin_manager import *
from .selector import Selector


class NESceneBase:

    def __init__( self ):

        self.__m_NodeTypeManager = NodeTypeManager()

        # Nodegraph data
        self.__m_NodeGraph = NENodeGraph()

        # temporary cached data
        self.__m_SelectionList = Selector( uuid.UUID )


        # Register TestNode
        LoadNodePlugin( self.__m_NodeTypeManager )


        CUSTOM_CODE = '''

def Initialize( self ):
    print( 'custom_code::Initialize()...' )
    self.AddAttribute( 'Attribute', DataFlow.Output, int, True, True, 'Output', 0 )

def Compute( self, dataBlock ):
    print( 'custom_code::Compute()...' )

'''
        builder.Build( 'CLASS1', CUSTOM_CODE )

        classObj = builder.CLASS1()
        classObj.Register( self.__m_NodeTypeManager )



    def Release( self ):
        self.__m_NodeTypeManager.Release()
        self.__m_NodeGraph.Release()



    def Clear( self ):
        self.__m_NodeGraph.Init()



    # GUI-dependent function. nescene_managerでのみ使用.
    def BindCommandCallbacks( self, func ):
        pass



    # GUI-dependent function. nescene_managerでのみ使用.
    def UnbindCallbackFuncs( self ):
        pass

        

    def NodeTypeManager( self ):
        return self.__m_NodeTypeManager



    def NodeGraph( self ):
        return self.__m_NodeGraph



    # GUI-dependent function. mainwidgetでのみ使用.
    def GraphEditor( self ):
        return None



    # GUI-dependent function. mainwidgetでのみ使用.
    def AttributeEditor( self ):
        return None



    def NodeTypeExists( self, nodetype ):
        return self.__m_NodeTypeManager.Exists( nodetype )



    def EvaluateSelected( self ):
        for obj_id in self.__m_SelectionList.Iter():
            self.__m_NodeGraph.Evaluate( obj_id )



    def GetSnapshot( self, object_id ):
        return self.__m_NodeGraph.GetSnapshot( object_id )



    def GetSelectedObjectIDs( self ):
        return self.__m_SelectionList.Iter()


    
    def FilterObjectIDs( self, obj_id_list, *, typefilter, parent_id ):
        return self.__m_NodeGraph.FilterObjects( obj_id_list, typefilter=typefilter, parent_id=parent_id )



    def GetRootID( self ):
        return self.__m_NodeGraph.GetRootID()



    def GetChildrenIDs( self, object_id, typefilter=c_IDMapSupportTypes ):
        return self.__m_NodeGraph.GetObjectByID( object_id, typefilter ).ChildrenID()



    def GetDescendantIDs( self, object_id ):
        return self.__m_NodeGraph.CollectAllDescendantIDsByID( object_id )



    def FilterDescendants( self, obj_id_list, parent_id ):
        return self.__m_NodeGraph.FilterDescendants( obj_id_list, parent_id )



    def GetObjectByID( self, object_id, typefilter=c_IDMapSupportTypes ):
        return self.__m_NodeGraph.GetObjectByID( object_id, typefilter )



    def GetObjectByName( self, name, typefilter=c_KeyMapSupportTypes ):
        return self.__m_NodeGraph.GetObjectByName( object_id, typefilter )



    def GetObjectID( self, name, typefilter=c_KeyMapSupportTypes ):
        return self.__m_NodeGraph.GetObjectID( name, typefilter )



    def GetObjectIDs( self, names, typefilter=c_KeyMapSupportTypes ):
        return [ self.__m_NodeGraph.GetObjectID( name, typefilter ) for name in names ]



    def GetObjectName( self, object_id ):
        return self.__m_NodeGraph.GetObjectNameByID( object_id )



    def GetType( self, object_id ):
        return self.__m_NodeGraph.GetObjectTypeByID( object_id )



    def ObjectExists( self, object_id, typefilter ):
        return self.__m_NodeGraph.ObjectExistsByID( object_id, typefilter )



    def GetParentID( self, object_id ):
        return self.__m_NodeGraph.GetParentID( object_id )



    def GetConnectionID( self, attrib_name1, attrib_name2 ):
        return self.__m_NodeGraph.GetConnectionIDByAttribute( attrib_name1, attrib_name2 )



    def GetConnectionIDs( self, object_id ):
        return self.__m_NodeGraph.GetConnectionIDs( object_id )



    def GetOverlappedConnections( self, attrib_ids ):
        return self.__m_NodeGraph.CollectOverlappedConnectionsByID( attrib_ids )



    #def GetAttribute( self, attrib_id ):
    #    return self.__m_NodeGraph.GetAttributeByID( attrib_id )



    def GetAttributeID( self, name ):
        return self.__m_NodeGraph.GetAttributeID( name )



    def AttributeExists( self, attrib_id ):
        return self.__m_NodeGraph.AttributeExistsByID( attrib_id )



    def IsLocked( self, attrib_id ):
        return self.__m_NodeGraph.IsLocked( attrib_id )



    # Gather attribute parameters for symboliclink generation
    def GetSymbolocLinkInitialParams( self, attrib_id ):
        return self.__m_NodeGraph.GetSymbolocLinkInitialParams( attrib_id )



    def IsValidNewName( self, object_id, newname ):
        return self.__m_NodeGraph.IsValidNewName( object_id, newname )



    def IsNewVisibility( self, object_id, visibility ):
        return self.__m_NodeGraph.IsNewVisibility( object_id, visibility )



    def IsNewAttributeValue( self, attrib_id, new_value ):
        return self.__m_NodeGraph.IsNewAttributeValue( attrib_id, new_value )



    def IsNewSymboliclinkSlot( self, object_id, new_slot ):
        return self.__m_NodeGraph.IsNewSymboliclinkSlot( object_id, new_slot )



    def IsConnectable( self, attrib_id1, attrib_id2, checkloop ):
        return self.__m_NodeGraph.IsConnectableByID( attrib_id1, attrib_id2, checkloop )



    def IsSymbolizable( self, attrib_id ):
        return self.__m_NodeGraph.IsSymbolizable( attrib_id )



    def IsGroupable( self, obj_id_list, parent_id ):
        return self.__m_NodeGraph.IsGroupable( obj_id_list, parent_id )



    def ExtractSymbolicLinkConnections( self, object_id ):
        return self.__m_NodeGraph.ExtractSymbolicLinkConnections( object_id )



    def GetSymboliclinkIDs( self, object_id ):
        return self.__m_NodeGraph.GetSymboliclinkIDs( object_id )



    def GetGroupIOIDs( self, object_id ):
        return self.__m_NodeGraph.GetGroupIOIDs( object_id )



    # GUI-dependent function.
    def GetGroupIOPosition( self, object_id ):
        return None#return self.__m_GraphEditor.CalcGroupIOOffsets( object_id )



    def GetGroupMemberIDs( self, group_id ):
        return self.__m_NodeGraph.GetGroupMemberIDs( group_id )



    def CollectConnections( self, obj_id_list, parend_id ):
        return self.__m_NodeGraph.CollectConnections( obj_id_list, parend_id )



    def ResolveChildNames( self, object_id ):
        return self.__m_NodeGraph.ResolveUnparentNameConflicts( object_id )



    def PositionChanged( self, object_id, translate, relative ):
        return self.__m_NodeGraph.PositionChanged( object_id, translate, relative )



    # GUI-dependent function.
    def CurrentEditSpaceID( self ):
        return None# self.__m_FocusViewID# return self.__m_GraphEditor.FocusViewID()



    def CheckGraph( self ):
        self.__m_NodeGraph.CheckGraph()



    def CenterPosition( self, object_ids ):
        return self.__m_NodeGraph.GetCentroid( object_ids )





    ################################### Operations ###################################

    def CreateNode_Operation( self, nodetype, pos, size, name, object_id, parent_id, attrib_ids ):
        # Create Node in NodeGraph
        nodeDesc = self.__m_NodeTypeManager.GetNodeDesc( nodetype )
        computeFunc = self.__m_NodeTypeManager.GetComputeFunc( nodetype )
        newNode = self.__m_NodeGraph.AddNode( nodeDesc, computeFunc, pos, size, name, object_id, attrib_ids, parent_id )
        return newNode



    def RemoveNode_Operation( self, node_id ):
        # Remove node in NodeGraph
        result = self.__m_NodeGraph.RemoveNodeByID( node_id )



    def Connect_Operation( self, attrib1_id, attrib2_id, object_id ):
        # Create Connection in NodeGraph
        newConn = self.__m_NodeGraph.AddConnectionByID( attrib1_id, attrib2_id, object_id )
        return newConn



    def Disconnect_Operation( self, conn_id ):
        # Disconnect in NodeGraph
        dest_attrib = self.__m_NodeGraph.RemoveConnectionByID( conn_id )
        return dest_attrib



# Unused.
    #def Reconnect_Operation( self, conn_id, attrib1_id, attrib2_id ):
    #    print( 'NESceneBase::Reconnect_Operation()...' )
    #    # Reconnect in NodeGraph
    #    conn = self.__m_NodeGraph.ReconnectByID( conn_id, attrib1_id, attrib2_id )

    #    # Set Attribute's Lock/Unlock state in NodeGraph
    #    #prev_state = self.__m_NodeGraph.LockAttributeByID( conn.DestinationAttribID(), False )
    #    self.LockAttribute_Operation( conn.DestinationAttribID(), False )

    #    # Reconnect in GraphEditor
    #    #self.__m_GraphEditor.Reconnect_Exec( conn_id, ( conn.Source().ParentID(), conn.SourceID() ), ( conn.Destination().ParentID(), conn.DestinationID() ), conn.ParentID() )

    #    # Update AttributeEditorWidget
    #    #self.__m_AttribEditor.Lock_Exec( conn.DestinationAttribID(), True )

    #    # return previous connection
    #    return conn



    def CreateGroup_Operation( self, pos, size, name, object_id, parent_id ):
        # Create Group in NodeGraph
        newGroup = self.__m_NodeGraph.AddGroup( pos, size, name, object_id, parent_id )        
        return newGroup

        

    def RemoveGroup_Operation( self, group_id ):
        #print( 'NESceneBase::RemoveGroup_Operation()...' )
        # Remove group in NodeGraph
        result = self.__m_NodeGraph.RemoveGroupByID( group_id )



    def Rename_Operation( self, node_id, newname ):
        # Rename in NodeGraph
        new_name, prev_name = self.__m_NodeGraph.RenameByID( node_id, newname )
        return new_name, prev_name



    def RenameAttribute_Operation( self, attrib_id, newname ):
        # Rename in NodeGraph
        new_name, prev_name = self.__m_NodeGraph.RenameAttributeByID( attrib_id, newname )         
        return new_name, prev_name



    def SetAttribute_Operation( self, attrib_id, new_value ):
        # Set Attribute in NodeGraph
        prev_value = self.__m_NodeGraph.SetAttributeByID( attrib_id, new_value )
        return prev_value



    def LockAttribute_Operation( self, attrib_id, new_state ):
        # Set Attribute's Lock/Unlock state in NodeGraph
        prev_state = self.__m_NodeGraph.LockAttributeByID( attrib_id, new_state )
        return prev_state



    def Translate_Operation( self, object_id, new_pos, realative ):
        # Set Translation in NodeGraph
        translation = self.__m_NodeGraph.TranslateByID( object_id, new_pos, realative )
        return translation



    def SetVisible_Operation( self, object_id, flag ):
        # Set Visibility in NodeGraph
        prev_flag = self.__m_NodeGraph.SetVisibleByID( object_id, flag )
        return prev_flag



    def Parent_Operation( self, object_id, parent_id ):
        #print( 'NESceneBase::Parent_Operation()...' )
        # Set parent in NodeGraph
        obj = self.__m_NodeGraph.ParentByID( object_id, parent_id )
        return obj



    def CreateSymbolicLink_Operation( self, group_id, attribdesc, value, name=None, symboliclink_idset=(None,None,None), slot_index=-1 ):
        # Create Symboliclink in NodeGraph
        symboliclink = self.__m_NodeGraph.ActivateSymbolicLinkByID( group_id, attribdesc, value, name, symboliclink_idset, slot_index )
        return symboliclink



    def RemoveSymbolicLink_Operation( self, symboliclink_id ):
        # Remove symboliclink in NodeGraph
        self.__m_NodeGraph.DeactivateSymbolicLinkByID( symboliclink_id )



    def SetSymbolicLinkSlotIndex_Operation( self, object_id, index ):
        #print( 'NESceneBase::SetSymbolicLinkSlotIndex_Operation()...' )
        # Set symbolicLink order in NodeGraph
        prev_index = self.__m_NodeGraph.SetSymbolicLinkSlotIndexByID( object_id, index )
        return prev_index



    def CreateGroupIO_Operation( self, dataflow, pos, object_id, group_id ):
        #print( 'NESceneBase::CreateGroupIO_Operation()...' )
        # Create GroupIO in NodeGraph
        groupio = self.__m_NodeGraph.CreateGroupIO( dataflow, pos, group_id, object_id )
        return groupio



    def RemoveGroupIO_Operation( self, object_id ):
        #print( 'NESceneBase::RemoveGroupIO_Operation()...' )
        # Remove GroupIO in NodeGraph
        self.__m_NodeGraph.RemoveGroupIOByID( object_id )



    # returns True if selection changed, else False.
    def Select_Operation( self, obj_id_list, option ):
        try:
            #print( 'NESceneBase::Select_Operation()...' )
            self.__m_SelectionList.Exec( *obj_id_list, **option )
            #self.__m_SelectionList.Info()
            return self.__m_SelectionList.Changed()

        except:
            traceback.print_exc()
            return False