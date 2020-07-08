import uuid

from .factory import builder
from .factory.node_manager import *

from .graph.nenodegraph import *


from .plugin_manager import *
from .selectionlist import SelectionList


class NESceneBase:

    def __init__( self ):

        self.__m_NodeTypeManager = NodeTypeManager()

        # Nodegraph data
        self.__m_NodeGraph = NENodeGraph()
        #self.__m_Scene = GraphicsScene( self.__m_NodeGraph.GetRootID(), self.__m_NodeTypeManager )
        #self.__m_AttributeEditor = AttributeEditorWidget()

        # temporary cached data
        self.__m_SelectionList = SelectionList( uuid.UUID )


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
        #self.__m_Scene.Release()



    def Clear( self ):
        self.__m_NodeGraph.Init()
        #self.__m_Scene.Init( self.__m_NodeGraph.GetRootID() )
        #self.__m_AttributeEditor.DeinitializeWidget()



    # GUI-dependent function. nescene_managerでのみ使用.
    def BindCommandCallbacks( self, func ):
        pass
        #self.__m_Scene.BindCallbackFunc( func )
        #self.__m_AttributeEditor.BindCallbackFunc( func )



    # GUI-dependent function. nescene_managerでのみ使用.
    def UnbindCallbackFuncs( self ):
        pass
        #self.__m_Scene.UnbindCallbackFunc()
        #self.__m_AttributeEditor.UnbindCallbackFunc()

        

    def NodeTypeManager( self ):
        return self.__m_NodeTypeManager



    def NodeGraph( self ):
        return self.__m_NodeGraph



    # GUI-dependent function. mainwidgetでのみ使用.
    def GraphicsScene( self ):
        return None
        #return self.__m_Scene



    def AttributeEditor( self ):
        return None
        #return self.__m_AttributeEditor



    def EvaluateSelected( self ):
        for obj_id in self.__m_SelectionList.Iter():
            self.__m_NodeGraph.Evaluate( obj_id )



    def GetSnapshot( self, object_id ):
        return self.__m_NodeGraph.GetSnapshot( object_id )



    def GetSelectedObjectIDs( self ):
        return self.__m_SelectionList.Iter()


    
    def FilterObjectIDs( self, obj_id_list, *, typefilter, parent_id ):
        return self.__m_NodeGraph.FilterObjects( obj_id_list, typefilter=typefilter, parent_id=parent_id )



    def GetRoot( self ):
        return self.__m_NodeGraph.GetRoot()



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



    def ObjectExists( self, object_id, typefilter ):
        return self.__m_NodeGraph.ExistsByID( object_id, typefilter )



    def GetParentID( self, object_id ):
        return self.__m_NodeGraph.GetParentID( object_id )



    def ValidateVisibilityUpdate( self, object_id, visibility ):
        return self.__m_NodeGraph.ValidateVisibilityUpdate( object_id, visibility )



    def GetConnectionID( self, attrib_name1, attrib_name2 ):
        return self.__m_NodeGraph.GetConnectionIDByAttribute( attrib_name1, attrib_name2 )



    def GetConnectionIDs( self, object_id ):
        return self.__m_NodeGraph.GetConnectionIDs( object_id )



    def GetAttribConnectionIDs( self, attrib_id ):
        return self.__m_NodeGraph.GetAttribConnectionIDs( attrib_id )



    def GetOverlappedConnections( self, attrib_ids ):
        return self.__m_NodeGraph.CollectOverlappedConnectionsByID( attrib_ids )



    def GetAttribute( self, attrib_id ):
        return self.__m_NodeGraph.GetAttributeByID( attrib_id )



    def GetAttributeID( self, name ):
        return self.__m_NodeGraph.GetAttributeID( name )



    def AttributeExisits( self, attrib_id ):
        return self.__m_NodeGraph.AttributeExisitsByID( attrib_id )



    def ValidateAttributeUpdate( self, attrib_id, new_value ):
        return self.__m_NodeGraph.ValidateAttributeUpdate( attrib_id, new_value )



    def IsAttributeLocked( self, attrib_id ):
        return self.__m_NodeGraph.IsLockedByID( attrib_id )



    def IsConnectable( self, attrib_id1, attrib_id2, checkloop ):
        return self.__m_NodeGraph.IsConnectableByID( attrib_id1, attrib_id2, checkloop )



    def ExtractSymbolicLinkConnections( self, object_id ):
        return self.__m_NodeGraph.ExtractSymbolicLinkConnections( object_id )



    def ValidateConnections( self, attrib_id ):
        return self.__m_NodeGraph.ValidateConnections( attrib_id )



    def CanBeSymbolized( self, attrib_id ):
        return self.__m_NodeGraph.CanBeSymbolized( attrib_id )



    def GetSymboliclinkIDs( self, object_id ):
        return self.__m_NodeGraph.GetSymboliclinkIDs( object_id )



    def ValidateSymboliclinkUpdate( self, object_id, new_slot ):
        return self.__m_NodeGraph.ValidateSymboliclinkUpdate( object_id, new_slot )



    def GetExposedAttribs( self, object_ids ):
        return self.__m_NodeGraph.CollectExposedAttribs( object_ids )



    def GetGroupIOIDs( self, object_id ):
        return self.__m_NodeGraph.GetGroupIOIDs( object_id )



    # GUI-dependent function.
    def GetGroupIOPosition( self, object_id ):
        return None#return self.__m_Scene.CalcGroupIOOffsets( object_id )



    def GetGroupMemberIDs( self, group_id ):
        return self.__m_NodeGraph.GetGroupMemberIDs( group_id )



    def GetInternalConnections( self, obj_id_list ):
        return self.__m_NodeGraph.GetInternalConnections( obj_id_list )



    def ResolveChildNames( self, object_id ):
        return self.__m_NodeGraph.ResolveUnparentNameConflicts( object_id )



    def GetType( self, object_id ):
        return self.__m_NodeGraph.GetObjectTypeByID( object_id )



    def IsType( self, object_id, typefilter ):
        return self.__m_NodeGraph.GetObjectTypeByID( object_id ) == typefilter



    def PositionChanged( self, object_id, translate, relative ):
        return self.__m_NodeGraph.PositionChanged( object_id, translate, relative )



    # GUI-dependent function.
    def CurrentEditSpaceID( self ):
        return None# self.__m_FocusViewID# return self.__m_Scene.FocusViewID()



    def CheckGraph( self ):
        self.__m_NodeGraph.CheckGraph()



    def CenterPosition( self, object_ids ):
        return self.__m_NodeGraph.GetCentroid( object_ids )



    def IsValidNewName( self, object_id, newname ):
        return self.__m_NodeGraph.IsValidNewName( object_id, newname )



    def UpdateSelection( self ):
        print( 'NESceneBase::UpdateSelection()...' )
        pass#self.__m_Scene.UpdateSelection( self.__m_SelectionList.Iter() )



# TODO: GUI-specific method. Should be removed from NESceneBase
    #def __UpdateAttributeEditor( self, object_id=None ):
    #    try:
    #        # get object and desc from obj_id
    #        obj_id = object_id if object_id else self.__m_AttributeEditor.ActiveObjectID()
    #        if( obj_id==None ):
    #            return False

    #        obj = self.__m_NodeGraph.GetObjectByID( obj_id, c_EditableTypes )
    #        if( obj==None ):
    #            return False

    #        desc = obj.GetDesc()
    #        if( desc==None ):
    #            return False

    #        self.__m_AttributeEditor.DeinitializeWidget()

    #        # initialize attribute editor widget
    #        self.__m_AttributeEditor.InitializeWidget( obj_id, desc, obj.Key() )
        
    #        # set values to widget
    #        for attrib in obj.Attributes().values():
    #            self.__m_AttributeEditor.SetValue_Exec( attrib.AttributeID(), attrib.Value() )

    #        return True

    #    except:

    #        return False


    ################################### Operations ###################################

    def CreateNode_Operation( self, nodetype, pos, size, name, object_id, parent_id, attrib_ids ):
        # Create Node in NodeGraph
        nodeDesc = self.__m_NodeTypeManager.GetNodeDesc( nodetype )
        computeFunc = self.__m_NodeTypeManager.GetComputeFunc( nodetype )
        newNode = self.__m_NodeGraph.AddNode( nodeDesc, computeFunc, pos, size, name, object_id, attrib_ids, parent_id )
        
        # Create Node in GraphicsScene
        #newsize = newNode.GetSize()
        #self.__m_Scene.CreateNode_Exec( newNode.Key(), newNode.ID(), newNode.GetDesc(), newNode.GetPosition(), newNode.ParentID() )                    

        return newNode



    def RemoveNode_Operation( self, node_id ):
        # Remove node in NodeGraph
        result = self.__m_NodeGraph.RemoveNodeByID( node_id )

        # Remove node in GraphicsScene
        #self.__m_Scene.RemoveNode_Exec( node_id )



    def Connect_Operation( self, attrib1_id, attrib2_id, object_id ):
        # Create Connection in NodeGraph
        newConn = self.__m_NodeGraph.AddConnectionByID( attrib1_id, attrib2_id, object_id )
        
        # Set Attribute's Lock/Unlock state in NodeGraph
        self.__m_NodeGraph.LockAttributeByID( newConn.DestinationAttribID(), False )
        
        # Create Connection in GraphicsScene
        #self.__m_Scene.Connect_Exec( newConn.Key(), newConn.ID(), newConn.SourceAttribID(), newConn.DestinationAttribID(), newConn.ParentID() )

        # Update AttributeEditorWidget
        #self.__m_AttributeEditor.SetEnabled_Exec( newConn.DestinationAttribID(), False )

        return newConn



    def Disconnect_Operation( self, conn_id ):
        # Disconnect in NodeGraph
        dest_attrib_id = self.__m_NodeGraph.RemoveConnectionByID( conn_id )

        # Set Attribute's Lock/Unlock state in NodeGraph
        #self.__m_NodeGraph.LockAttributeByID( dest_attrib_id, True )
        self.LockAttribute_Operation( dest_attrib_id, True )

        # Disconnect in GraphicsScene
        #self.__m_Scene.Disconnect_Exec( conn_id )

        # Update AttributeEditorWidget
        #self.__m_AttributeEditor.SetEnabled_Exec( dest_attrib_id, True )



    def Reconnect_Operation( self, conn_id, attrib1_id, attrib2_id ):
        print( 'NESceneBase::Reconnect_Operation()...' )
        # Reconnect in NodeGraph
        conn = self.__m_NodeGraph.ReconnectByID( conn_id, attrib1_id, attrib2_id )

        # Set Attribute's Lock/Unlock state in NodeGraph
        #prev_state = self.__m_NodeGraph.LockAttributeByID( conn.DestinationAttribID(), False )
        self.LockAttribute_Operation( conn.DestinationAttribID(), False )

        # Reconnect in GraphicsScene
        #self.__m_Scene.Reconnect_Exec( conn_id, ( conn.Source().ParentID(), conn.SourceID() ), ( conn.Destination().ParentID(), conn.DestinationID() ), conn.ParentID() )

        # Update AttributeEditorWidget
        #self.__m_AttributeEditor.SetEnabled_Exec( conn.DestinationAttribID(), False )

        # return previous connection
        return conn



# TODO: グループを跨いで選択したノード群はどうやってグループ化する?
    def CreateGroup_Operation( self, pos, size, name, object_id, parent_id ):

        # Create Group in NodeGraph
        newGroup = self.__m_NodeGraph.AddGroup( pos, size, name, object_id, parent_id )

        # Create Group in GraphicsScene
        #self.__m_Scene.CreateGroup_Exec( newGroup.Key(), newGroup.ID(), newGroup.GetPosition(), newGroup.ParentID() )
        
        return newGroup

        

    def RemoveGroup_Operation( self, group_id ):
        print( 'NESceneBase::RemoveGroup_Operation()...' )
        # Remove group in NodeGraph
        result = self.__m_NodeGraph.RemoveGroupByID( group_id )

        # Remove group in GraphicsScene
        #self.__m_Scene.RemoveGroup_Exec( group_id )



    def Rename_Operation( self, node_id, newname ):
        # Rename in NodeGraph
        new_name, prev_name = self.__m_NodeGraph.RenameByID( node_id, newname )

        # Rename in GraphicsScene
        #self.__m_Scene.Rename_Exec( node_id, new_name )

        # Update AttributeEditorWidget
        #self.__m_AttributeEditor.Rename_Exec( node_id, new_name )

        return new_name, prev_name


    def RenameAttribute_Operation( self, attrib_id, newname ):
        # Rename in NodeGraph
        new_name, prev_name = self.__m_NodeGraph.RenameAttributeByID( attrib_id, newname ) 

        # Rename in GraphicsScene
        #self.__m_Scene.RenameAttribute_Exec( attrib_id, new_name )
        
        # Update AttributeEditorWidget
        #self.__m_AttributeEditor.RenameAttribute_Exec( attrib_id, new_name )
        
        return new_name, prev_name


    def SetAttribute_Operation( self, attrib_id, new_value ):
        # Set Attribute in NodeGraph
        prev_value = self.__m_NodeGraph.SetAttributeByID( attrib_id, new_value )

        # Update AttributeEditorWidget
        #self.__m_AttributeEditor.SetValue_Exec( attrib_id, new_value )

        return prev_value


    def LockAttribute_Operation( self, attrib_id, new_state ):
        # Set Attribute's Lock/Unlock state in NodeGraph
        prev_state = self.__m_NodeGraph.LockAttributeByID( attrib_id, new_state )

        # Update AttributeEditorWidget
        #self.__m_AttributeEditor.SetEnabled_Exec( attrib_id, new_state )

        return prev_state


    def Translate_Operation( self, object_id, new_pos, realative ):
        # Set Translation in NodeGraph
        translation = self.__m_NodeGraph.TranslateByID( object_id, new_pos, realative )

        # Set Translation in GraphicsScene
        #self.__m_Scene.Translate_Exec( object_id, new_pos, realative )

        return translation#prev_pos


    def SetVisible_Operation( self, object_id, flag ):
        # Set Visibility in NodeGraph
        prev_flag = self.__m_NodeGraph.SetVisibleByID( object_id, flag )

        # Set Visibility in GraphicsScene
        #self.__m_Scene.SetVisible_Exec( object_id, flag )

        return prev_flag


    def Parent_Operation( self, object_id, parent_id ):
        print( 'NESceneBase::Parent_Operation()...' )
        # Set parent in NodeGraph
        #prev_parent_id, new_pos = self.__m_NodeGraph.ParentByID( object_id, parent_id )
        obj = self.__m_NodeGraph.ParentByID( object_id, parent_id )

        # Set parent in GraphicsScene
        #self.__m_Scene.Parent_Exec( object_id, parent_id )

        # Set new position on parent space
        #self.__m_Scene.Translate_Exec( object_id, new_pos, False )

        return obj#prev_parent_id, new_pos


    def CreateSymbolicLink_Operation( self, group_id, attribdesc, value, name=None, symboliclink_idset=(None,None,None), slot_index=-1 ):
        # Create Symboliclink in NodeGraph
        symboliclink = self.__m_NodeGraph.ActivateSymbolicLinkByID( group_id, attribdesc, value, name, symboliclink_idset, slot_index )
        
        # Create Symboliclink in GraphicsScene
        #self.__m_Scene.ActivateSymbolicLink_Exec( symboliclink.ParentID(), symboliclink.Key(), symboliclink.GetDesc(), symboliclink.SlotIndex() )# slot_index )
        
        # Update AttributeEditorWidget
        #self.__UpdateAttributeEditor()

        return symboliclink


    def RemoveSymbolicLink_Operation( self, symboliclink_id ):
        # Remove symboliclink in NodeGraph
        self.__m_NodeGraph.DeactivateSymbolicLinkByID( symboliclink_id )

        # Remove symboliclink in GraphicsScene
        #self.__m_Scene.DeactivateSymbolicLink_Exec( symboliclink_id )

        # Update AttributeEditorWidget
        #self.__UpdateAttributeEditor()


    def SetSymbolicLinkSlotIndex_Operation( self, object_id, index ):
        print( 'NESceneBase::SetSymbolicLinkSlotIndex_Operation()...' )
        # Set symbolicLink order in NodeGraph
        prev_index = self.__m_NodeGraph.SetSymbolicLinkSlotIndexByID( object_id, index )

        # Set symbolicLink order in GraphicsScene
        #self.__m_Scene.SetSymbolicLinkSlotIndex_Exec( object_id, index )

        # Update AttributeEditorWidget
        #self.__UpdateAttributeEditor()

        return prev_index    


    def CreateGroupIO_Operation( self, dataflow, pos, object_id, group_id ):
        print( 'NESceneBase::CreateGroupIO_Operation()...' )
        # Create GroupIO in NodeGraph
        groupio = self.__m_NodeGraph.CreateGroupIO( dataflow, pos, group_id, object_id )

        # Create GroupIO in GraphicsScene
        #self.__m_Scene.CreateGroupIO_Exec( groupio.Key(), dataflow, groupio.GetPosition(), group_id, groupio.ID() )
        
        return groupio


    def RemoveGroupIO_Operation( self, object_id ):
        print( 'NESceneBase::RemoveGroupIO_Operation()...' )
        # Remove GroupIO in NodeGraph
        self.__m_NodeGraph.RemoveGroupIOByID( object_id )

        # Remove GroupIO in GraphicsScene
        #self.__m_Scene.RemoveGroupIO_Exec( object_id )



    # returns True if selection changed, else False.
    def Select_Operation( self, obj_id_list, option ):
        try:
            print( 'NESceneBase::Select_Operation()...' )

            self.__m_SelectionList.Exec( *obj_id_list, **option )

            return self.__m_SelectionList.Changed()

            #if( self.__m_SelectionList.Changed()==False ):
            #    return False

            #self.__m_AttributeEditor.DeinitializeWidget()

            #obj_ids_editable = self.__m_NodeGraph.FilterObjects( self.__m_SelectionList.Iter(), typefilter=c_EditableTypes, parent_id=None )

            #if( not obj_ids_editable ):
            #    return False

  
            ## get object and desc from selected id
            #obj_id = obj_ids_editable[0]
            #obj = self.__m_NodeGraph.GetObjectByID( obj_id, c_EditableTypes )
            #desc = obj.GetDesc()
            #if( desc==None ):    return False

            ## initialize attribute editor widget
            #self.__m_AttributeEditor.InitializeWidget( obj_id, desc, obj.Key() )
        
            ## set values to widget
            #for attrib in obj.Attributes().values():
            #    self.__m_AttributeEditor.SetValue_Exec( attrib.AttributeID(), attrib.Value() )

            #return True

        except:
            traceback.print_exc()
            return False