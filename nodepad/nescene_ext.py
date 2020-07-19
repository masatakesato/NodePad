#import uuid
import traceback

#from .factory import builder
#from .factory.node_manager import *

from .graph.nenodegraph import *


#from .plugin_manager import *
#from .selectionlist import SelectionList

from .ui.graphicsscene import GraphicsScene
from .ui.attributeeditorwidget import AttributeEditorWidget

from .nescene_base import NESceneBase




class NESceneExt(NESceneBase):

    def __init__( self ):
        super(NESceneExt, self).__init__()
        
        self.__m_GraphEditor = GraphicsScene( self.GetRootID(), self.NodeTypeManager() )
        self.__m_AttribEditor = AttributeEditorWidget()



    def Release( self ):
        super(NESceneExt, self).Release()
        self.__m_GraphEditor.Release()



    def Clear( self ):
        super(NESceneExt, self).Clear()

        self.__m_GraphEditor.Init( self.GetRootID() )
        self.__m_AttribEditor.DeinitializeWidget()



    # GUI-dependent function. nescene_managerでのみ使用.
    def BindCommandCallbacks( self, func ):
        #super(NESceneExt, self).BindCommandCallbacks( func )  <- Do nothing
        self.__m_GraphEditor.BindCallbackFunc( func )
        self.__m_AttribEditor.BindCallbackFunc( func )



    # GUI-dependent function. nescene_managerでのみ使用.
    def UnbindCallbackFuncs( self ):
        #super(NESceneExt, self).BindCommandCallbacks( func )  <- Do nothing
        self.__m_GraphEditor.UnbindCallbackFunc()
        self.__m_AttribEditor.UnbindCallbackFunc()

        

    # Implemented in NESceneBase
    #def NodeTypeManager( self ):
    #    return self.__m_NodeTypeManager



    # Implemented in NESceneBase
    #def NodeGraph( self ):
    #    return self.__m_NodeGraph



    # GUI-dependent function. mainwidgetでのみ使用. 
    def GraphEditor( self ):
        #super(NESceneExt, self).GraphEditor()  <- Do nothing
        return self.__m_GraphEditor



    # GUI-dependent function.
    def AttributeEditor( self ):
        #super(NESceneExt, self).AttributeEditor()  <- Do nothing
        return self.__m_AttribEditor



    # Implemented in NESceneBase
    #def NodeTypeExists( self, nodetype ):
    #    return self.__m_NodeTypeManager.Exists( nodetype )



    # Implemented in NESceneBase
    #def EvaluateSelected( self ):
    #    for obj_id in self.__m_SelectionList.Iter():
    #        self.__m_NodeGraph.Evaluate( obj_id )



    # Implemented in NESceneBase
    #def GetSnapshot( self, object_id ):
    #    return self.__m_NodeGraph.GetSnapshot( object_id )



    # Implemented in NESceneBase
    #def GetSelectedObjectIDs( self ):
    #    return self.__m_SelectionList.Iter()



    # Implemented in NESceneBase
    #def FilterObjectIDs( self, obj_id_list, *, typefilter, parent_id ):
    #    return self.__m_NodeGraph.FilterObjects( obj_id_list, typefilter=typefilter, parent_id=parent_id )



    # Implemented in NESceneBase
    #def GetRoot( self ):
    #    return self.__m_NodeGraph.GetRoot()



    # Implemented in NESceneBase
    #def GetRootID( self ):
    #    return self.__m_NodeGraph.GetRootID()



    # Implemented in NESceneBase
    #def GetChildrenIDs( self, object_id ):
    #    return self.__m_NodeGraph.GetObjectByID( object_id, c_IDMapSupportTypes ).ChildrenID()



    # Implemented in NESceneBase
    #def GetDescendantIDs( self, object_id ):
    #    return self.__m_NodeGraph.CollectAllDescendantIDsByID( object_id )



    # Implemented in NESceneBase
    #def GetObjectByID( self, object_id, typefilter=c_IDMapSupportTypes ):
    #    return self.__m_NodeGraph.GetObjectByID( object_id, typefilter )



    # Implemented in NESceneBase
    #def GetObjectByName( self, name, typefilter=c_KeyMapSupportTypes ):
    #    return self.__m_NodeGraph.GetObjectByName( object_id, typefilter )



    # Implemented in NESceneBase
    #def GetObjectID( self, name, typefilter=c_KeyMapSupportTypes ):
    #    return self.__m_NodeGraph.GetObjectID( name, typefilter )



    # Implemented in NESceneBase
    #def GetObjectIDs( self, names, typefilter=c_KeyMapSupportTypes ):
    #    return [ self.__m_NodeGraph.GetObjectID( name, typefilter ) for name in names ]



    # Implemented in NESceneBase
    #def ObjectExists( self, object_id, typefilter ):
    #    return self.__m_NodeGraph.ObjectExistsByID( object_id, typefilter )



    # Implemented in NESceneBase
    #def GetConnectionID( self, attrib_name1, attrib_name2 ):
    #    return self.__m_NodeGraph.GetConnectionIDByAttribute( attrib_name1, attrib_name2 )



    # Implemented in NESceneBase
    #def GetConnectionIDs( self, object_id ):
    #    return self.__m_NodeGraph.GetConnectionIDs( object_id )



    # Implemented in NESceneBase
    #def GetOverlappedConnections( self, attrib_ids ):
    #    return self.__m_NodeGraph.CollectOverlappedConnectionsByID( attrib_ids )



    # Implemented in NESceneBase
    #def GetAttribute( self, attrib_id ):
    #    return self.__m_NodeGraph.GetAttributeByID( attrib_id )



    # Implemented in NESceneBase
    #def GetAttributeID( self, name ):
    #    return self.__m_NodeGraph.GetAttributeID( name )



    # Implemented in NESceneBase
    #def AttributeExists( self, attrib_id ):
    #    return self.__m_NodeGraph.AttributeExistsByID( attrib_id )



    #def IsLocked( self, attrib_id ):
    #    return self.__m_NodeGraph.IsLocked( attrib_id )



    # Implemented in NESceneBase
    #def IsNewVisibility( self, object_id, visibility ):
    #    return self.__m_NodeGraph.IsNewVisibility( object_id, visibility )



    # Implemented in NESceneBase
    #def IsNewAttributeValue( self, attrib_id, new_value ):
    #    return self.__m_NodeGraph.IsNewAttributeValue( attrib_id, new_value )



    # Implemented in NESceneBase
    #def IsNewSymboliclinkSlot( self, object_id, new_slot ):
    #    return self.__m_NodeGraph.IsNewSymboliclinkSlot( object_id, new_slot )



    # Implemented in NESceneBase
    #def AttribHasConnections( self, attrib_id ):
    #    return self.__m_NodeGraph.AttribHasConnections( attrib_id )



    # Implemented in NESceneBase
    #def IsConnectable( self, attrib_id1, attrib_id2, checkloop ):
    #    return self.__m_NodeGraph.IsConnectableByID( attrib_id1, attrib_id2, checkloop )



    # Implemented in NESceneBase
    #def IsSymbolizable( self, attrib_id ):
    #    return self.__m_NodeGraph.IsSymbolizable( attrib_id )



    # Implemented in NESceneBase
    #def ExtractSymbolicLinkConnections( self, object_id ):
    #    return self.__m_NodeGraph.ExtractSymbolicLinkConnections( object_id )



    # Implemented in NESceneBase
    #def GetSymboliclinkIDs( self, object_id ):
    #    return self.__m_NodeGraph.GetSymboliclinkIDs( object_id )



    # Implemented in NESceneBase
    #def GetGroupIOIDs( self, object_id ):
    #    return self.__m_NodeGraph.GetGroupIOIDs( object_id )



    # GUI-dependent function.
    def GetGroupIOPosition( self, object_id ):
        #super(NESceneExt, self).GetGroupIOPosition( object_id )  <- Do nothing
        return self.__m_GraphEditor.CalcGroupIOOffsets( object_id )



    # Implemented in NESceneBase
    #def ResolveChildNames( self, object_id ):
    #    return self.__m_NodeGraph.ResolveUnparentNameConflicts( object_id )



    # Implemented in NESceneBase
    #def GetType( self, object_id ):
    #    return self.__m_NodeGraph.GetObjectTypeByID( object_id )



    # Implemented in NESceneBase
    #def IsType( self, object_id, typefilter ):
    #    return self.__m_NodeGraph.GetObjectTypeByID( object_id ) == typefilter



    # Implemented in NESceneBase
    #def PositionChanged( self, object_id, translate, relative ):
    #    return self.__m_NodeGraph.PositionChanged( object_id, translate, relative )



    # GUI-dependent function.
    def CurrentEditSpaceID( self ):
        #super(NESceneExt, self).CurrentEditSpaceID()  <- Do nothing
        return self.__m_GraphEditor.FocusViewID()# self.__m_FocusViewID



    # Implemented in NESceneBase
    #def CheckGraph( self ):
    #    self.__m_NodeGraph.CheckGraph()



    # Implemented in NESceneBase
    #def CenterPosition( self, object_ids ):
    #    return self.__m_NodeGraph.GetCentroid( object_ids )



    # GUI-dependent function.
    def __UpdateAttributeEditor( self, object_id=None ):
        try:
            print( 'NESceneExt::__UpdateAttributeEditor()...' )

            # get object and desc from obj_id
            obj_id = object_id if object_id else self.__m_AttribEditor.ActiveObjectID()
            if( obj_id==None ):
                return False

            obj = self.GetObjectByID( obj_id, c_EditableTypes )
            if( obj==None ):
                return False

            desc = obj.GetDesc()
            if( desc==None ):
                return False

            #print( 'NESceneExt::__UpdateAttributeEditor()...', obj.FullKey() )

            self.__m_AttribEditor.DeinitializeWidget()

            # initialize attribute editor widget
            self.__m_AttribEditor.InitializeWidget( obj_id, desc, obj.Key() )
        
            # set values to widget
            for attrib in obj.Attributes().values():
                self.__m_AttribEditor.SetValue_Exec( attrib.AttributeID(), attrib.Value() )

            return True

        except:
            traceback.print_exc()
            return False


    ################################### Operations ###################################

    def CreateNode_Operation( self, nodetype, pos, size, name, object_id, parent_id, attrib_ids ):
        newNode = super(NESceneExt, self).CreateNode_Operation( nodetype, pos, size, name, object_id, parent_id, attrib_ids )
        
        newsize = newNode.GetSize()
        # Create Node in GraphEditor
        self.__m_GraphEditor.CreateNode_Exec( newNode.Key(), newNode.ID(), newNode.GetDesc(), newNode.GetPosition(), newNode.ParentID() )                    

        return newNode



    def RemoveNode_Operation( self, node_id ):
        super(NESceneExt, self).RemoveNode_Operation( node_id )
        
        # Remove node in GraphEditor
        self.__m_GraphEditor.RemoveNode_Exec( node_id )



    def Connect_Operation( self, attrib1_id, attrib2_id, object_id ):
        newConn = super(NESceneExt, self).Connect_Operation( attrib1_id, attrib2_id, object_id )
        
        # Create Connection in GraphEditor
        self.__m_GraphEditor.Connect_Exec( newConn.Key(), newConn.ID(), newConn.SourceAttribID(), newConn.DestinationAttribID(), newConn.ParentID() )

        # Update AttributeEditorWidget
        self.__m_AttribEditor.Lock_Exec( newConn.DestinationAttribID(), self.IsLocked( newConn.DestinationAttribID() ) )

        return newConn



    def Disconnect_Operation( self, conn_id ):
        dest_attrib_id = super(NESceneExt, self).Disconnect_Operation( conn_id )
        
        # Disconnect in GraphEditor
        self.__m_GraphEditor.Disconnect_Exec( conn_id )

        # Update AttributeEditorWidget.
        if( dest_attrib_id ):
            self.__m_AttribEditor.Lock_Exec( dest_attrib_id, self.IsLocked( dest_attrib_id ) )



# Unused.
    #def Reconnect_Operation( self, conn_id, attrib1_id, attrib2_id ):
    #    conn = super(NESceneExt, self).Reconnect_Operation( conn_id, attrib1_id, attrib2_id )
    #    # Reconnect in GraphEditor
    #    self.__m_GraphEditor.Reconnect_Exec( conn.ID(), ( conn.Source().ParentID(), conn.SourceID() ), ( conn.Destination().ParentID(), conn.DestinationID() ), conn.ParentID() )
    #    # return previous connection
    #    #return (prev_src_attrib_id, prev_dest_attrib_id)
    #    return conn



    def CreateGroup_Operation( self, pos, size, name, object_id, parent_id ):
        newGroup = super(NESceneExt, self).CreateGroup_Operation( pos, size, name, object_id, parent_id )

        # Create Group in GraphEditor
        self.__m_GraphEditor.CreateGroup_Exec( newGroup.Key(), newGroup.ID(), newGroup.GetPosition(), newGroup.ParentID() )
        
        return newGroup

        

    def RemoveGroup_Operation( self, group_id ):
        result = super(NESceneExt, self).RemoveGroup_Operation( group_id )
        #print( 'NESceneExt::RemoveGroup_Operation()...' )
        # Remove group in GraphEditor
        self.__m_GraphEditor.RemoveGroup_Exec( group_id )
        


    def Rename_Operation( self, node_id, newname ):
        new_name, prev_name = super(NESceneExt, self).Rename_Operation( node_id, newname )
        
        # Rename in GraphEditor
        self.__m_GraphEditor.Rename_Exec( node_id, new_name )

        # Update AttributeEditorWidget
        if( self.__m_AttribEditor.HasTrigerred()==False ):
            self.__m_AttribEditor.Rename_Exec( node_id, new_name )

        return new_name, prev_name



    def RenameAttribute_Operation( self, attrib_id, newname ):
        new_name, prev_name = super(NESceneExt, self).RenameAttribute_Operation( attrib_id, newname )

        # Rename in GraphEditor
        self.__m_GraphEditor.RenameAttribute_Exec( attrib_id, new_name )
        
        # Update AttributeEditorWidget
        if( self.__m_AttribEditor.HasTrigerred()==False ):
            self.__m_AttribEditor.RenameAttribute_Exec( attrib_id, new_name )
        
        return new_name, prev_name



    def SetAttribute_Operation( self, attrib_id, new_value ):
        prev_value = super(NESceneExt, self).SetAttribute_Operation( attrib_id, new_value )

        # Update AttributeEditorWidget
        if( self.__m_AttribEditor.HasTrigerred()==False ):
            self.__m_AttribEditor.SetValue_Exec( attrib_id, new_value )

        return prev_value



    def LockAttribute_Operation( self, attrib_id, new_state ):
        prev_state = super(NESceneExt, self).LockAttribute_Operation( attrib_id, new_state )
        
        # Update AttributeEditorWidget
        if( self.__m_AttribEditor.HasTrigerred()==False ):
            self.__m_AttribEditor.Lock_Exec( attrib_id, self.IsLocked( attrib_id ) )

        return prev_state



    def Translate_Operation( self, object_id, new_pos, realative ):
        translation = super(NESceneExt, self).Translate_Operation( object_id, new_pos, realative )

        # Set Translation in GraphEditor
        if( self.__m_GraphEditor.HasTriggered()==False ):
            self.__m_GraphEditor.Translate_Exec( object_id, new_pos, realative )

        return translation



    def SetVisible_Operation( self, object_id, flag ):
        prev_flag = super(NESceneExt, self).SetVisible_Operation( object_id, flag )

        # Set Visibility in GraphEditor
        self.__m_GraphEditor.SetVisible_Exec( object_id, flag )

        return prev_flag



    def Parent_Operation( self, object_id, parent_id ):
        obj = super(NESceneExt, self).Parent_Operation( object_id, parent_id )# prev_parent_id, new_pos

        # Set parent in GraphEditor
        self.__m_GraphEditor.Parent_Exec( object_id, parent_id )

        # Set new position on parent space
        self.__m_GraphEditor.Translate_Exec( object_id, obj.GetPosition(), False )# new_pos

        return obj#prev_parent_id



    def CreateSymbolicLink_Operation( self, group_id, attribdesc, value, name=None, symboliclink_idset=(None,None,None), slot_index=-1 ):
        symboliclink = super(NESceneExt, self).CreateSymbolicLink_Operation( group_id, attribdesc, value, name, symboliclink_idset, slot_index )
        
        # Create Symboliclink in GraphEditor
        self.__m_GraphEditor.ActivateSymbolicLink_Exec( symboliclink.ParentID(), symboliclink.Key(), symboliclink.GetDesc(), symboliclink.SlotIndex() )
        
        # Update AttributeEditorWidget
        self.__UpdateAttributeEditor()

        return symboliclink



    def RemoveSymbolicLink_Operation( self, symboliclink_id ):
        super(NESceneExt, self).RemoveSymbolicLink_Operation( symboliclink_id )
        
        # Remove symboliclink in GraphEditor
        self.__m_GraphEditor.DeactivateSymbolicLink_Exec( symboliclink_id )

        # Update AttributeEditorWidget
        self.__UpdateAttributeEditor()



    def SetSymbolicLinkSlotIndex_Operation( self, object_id, index ):
        prev_index = super(NESceneExt, self).SetSymbolicLinkSlotIndex_Operation( object_id, index )
        #print( 'NESceneExt::SetSymbolicLinkSlotIndex_Operation()...' )
        # Set symbolicLink order in GraphEditor
        self.__m_GraphEditor.SetSymbolicLinkSlotIndex_Exec( object_id, index )

        # Update AttributeEditorWidget
        self.__UpdateAttributeEditor()

        return prev_index



    def CreateGroupIO_Operation( self, dataflow, pos, object_id, group_id ):
        groupio = super(NESceneExt, self).CreateGroupIO_Operation( dataflow, pos, object_id, group_id )
        #print( 'NESceneExt::CreateGroupIO_Operation()...' )
        # Create GroupIO in GraphEditor
        self.__m_GraphEditor.CreateGroupIO_Exec( groupio.Key(), dataflow, groupio.GetPosition(), group_id, groupio.ID() )
        
        return groupio



    def RemoveGroupIO_Operation( self, object_id ):
        super(NESceneExt, self).RemoveGroupIO_Operation( object_id )
        #print( 'NESceneExt::RemoveGroupIO_Operation()...' )
        # Remove GroupIO in GraphEditor
        self.__m_GraphEditor.RemoveGroupIO_Exec( object_id )



    def Select_Operation( self, obj_id_list, option ):
        try:
            result = super(NESceneExt, self).Select_Operation( obj_id_list, option )
            if( result==False ):
                return False

            if( self.__m_GraphEditor.HasTriggered()==False ):
                self.__m_GraphEditor.Select_Exec( self._NESceneBase__m_SelectionList.Iter() )


            self.__m_AttribEditor.DeinitializeWidget()

            obj_ids_editable = self.FilterObjectIDs( self.GetSelectedObjectIDs(), typefilter=c_EditableTypes, parent_id=None )

            if( not obj_ids_editable ):
                return False

            # get object and desc from selected id
            obj_id = obj_ids_editable[0]
            obj = self.GetObjectByID( obj_id, c_EditableTypes )
            desc = obj.GetDesc()
            if( desc==None ):    return False

            # Init attribute editor widget
            self.__m_AttribEditor.InitializeWidget( obj_id, desc, obj.Key() )
            
            # Init individual attributes
            for attrib in obj.Attributes().values():
                self.__m_AttribEditor.SetValue_Exec( attrib.AttributeID(), attrib.Value() )
                self.__m_AttribEditor.Lock_Exec( attrib.AttributeID(), bool(attrib.LockState()) )

            return True

        except:
            traceback.print_exc()
            return False