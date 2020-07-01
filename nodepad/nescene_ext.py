﻿#import uuid
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
        
        self.__m_Scene = GraphicsScene( self.GetRootID(), self.NodeTypeManager() )
        self.__m_AttributeEditor = AttributeEditorWidget()


    def Release( self ):
        super(NESceneExt, self).Release()
        self.__m_Scene.Release()


    def Clear( self ):
        super(NESceneExt, self).Clear()

        self.__m_Scene.Init( self.GetRootID() )
        self.__m_AttributeEditor.DeinitializeWidget()


    # GUI-dependent function. nescene_managerでのみ使用.
    def BindCommandCallbacks( self, func ):
        #super(NESceneExt, self).BindCommandCallbacks( func )  <- Do nothing
        self.__m_Scene.BindCallbackFunc( func )
        self.__m_AttributeEditor.BindCallbackFunc( func )


    # GUI-dependent function. nescene_managerでのみ使用.
    def UnbindCallbackFuncs( self ):
        #super(NESceneExt, self).BindCommandCallbacks( func )  <- Do nothing
        self.__m_Scene.UnbindCallbackFunc()
        self.__m_AttributeEditor.UnbindCallbackFunc()
        

    # Implemented in NESceneBase
    #def NodeTypeManager( self ):
    #    return self.__m_NodeTypeManager


    # Implemented in NESceneBase
    #def NodeGraph( self ):
    #    return self.__m_NodeGraph


    # GUI-dependent function. mainwidgetでのみ使用. 
    def GraphicsScene( self ):
        #super(NESceneExt, self).GraphicsScene()  <- Do nothing
        return self.__m_Scene


    # GUI-dependent function.
    def AttributeEditor( self ):
        #super(NESceneExt, self).AttributeEditor()  <- Do nothing
        return self.__m_AttributeEditor


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
    #    return self.__m_NodeGraph.ExistsByID( object_id, typefilter )

    # Implemented in NESceneBase
    #def ValidateVisibilityUpdate( self, object_id, visibility ):
    #    return self.__m_NodeGraph.ValidateVisibilityUpdate( object_id, visibility )

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
    #def AttributeExisits( self, attrib_id ):
    #    return self.__m_NodeGraph.AttributeExisitsByID( attrib_id )

    # Implemented in NESceneBase
    #def ValidateAttributeUpdate( self, attrib_id, new_value ):
    #    return self.__m_NodeGraph.ValidateAttributeUpdate( attrib_id, new_value )

    # Implemented in NESceneBase
    #def IsAttributeLocked( self, attrib_id ):
    #    return self.__m_NodeGraph.IsLockedByID( attrib_id )

    # Implemented in NESceneBase
    #def IsConnectable( self, attrib_id1, attrib_id2, checkloop ):
    #    return self.__m_NodeGraph.IsConnectableByID( attrib_id1, attrib_id2, checkloop )

    # Implemented in NESceneBase
    #def ExtractSymbolicLinkConnections( self, object_id ):
    #    return self.__m_NodeGraph.ExtractSymbolicLinkConnections( object_id )

    # Implemented in NESceneBase
    #def ValidateConnections( self, attrib_id ):
    #    return self.__m_NodeGraph.ValidateConnections( attrib_id )

    # Implemented in NESceneBase
    #def CanBeSymbolized( self, attrib_id ):
    #    return self.__m_NodeGraph.CanBeSymbolized( attrib_id )

    # Implemented in NESceneBase
    #def GetSymboliclinkIDs( self, object_id ):
    #    return self.__m_NodeGraph.GetSymboliclinkIDs( object_id )

    # Implemented in NESceneBase
    #def ValidateSymboliclinkUpdate( self, object_id, new_slot ):
    #    return self.__m_NodeGraph.ValidateSymboliclinkUpdate( object_id, new_slot )

    # Implemented in NESceneBase
    #def GetExposedAttribs( self, object_ids ):
    #    return self.__m_NodeGraph.CollectExposedAttribs( object_ids )

    # Implemented in NESceneBase
    #def GetGroupIOIDs( self, object_id ):
    #    return self.__m_NodeGraph.GetGroupIOIDs( object_id )


    # GUI-dependent function.
    def GetGroupIOPosition( self, object_id ):
        #super(NESceneExt, self).GetGroupIOPosition( object_id )  <- Do nothing
        return self.__m_Scene.CalcGroupIOOffsets( object_id )


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
        return self.__m_Scene.FocusViewID()# self.__m_FocusViewID


    # Implemented in NESceneBase
    #def CheckGraph( self ):
    #    self.__m_NodeGraph.CheckGraph()


    # Implemented in NESceneBase
    #def CenterPosition( self, object_ids ):
    #    return self.__m_NodeGraph.GetCentroid( object_ids )


    # Implemented in NESceneBase
    #def ValidateName( self, object_id, newname ):
    #    return self.__m_NodeGraph.ValidateName( object_id, newname )


    # GUI-dependent function.
    def UpdateSelection( self ):
        super(NESceneExt, self).UpdateSelection()#  <- Do nothing
        self.__m_Scene.UpdateSelection( self._NESceneBase__m_SelectionList.Iter() )


    # GUI-dependent function.
    def __UpdateAttributeEditor( self, object_id=None ):
        #super(NESceneExt, self).__UpdateAttributeEditor( object_id )  <- Do nothing
        try:
            # get object and desc from obj_id
            obj_id = object_id if object_id else self.__m_AttributeEditor.ActiveObjectID()
            if( obj_id==None ):
                return False

            obj = self.GetObjectByID( obj_id, c_EditableTypes )
            if( obj==None ):
                return False

            desc = obj.GetDesc()
            if( desc==None ):
                return False

            self.__m_AttributeEditor.DeinitializeWidget()

            # initialize attribute editor widget
            self.__m_AttributeEditor.InitializeWidget( obj_id, desc, obj.Key() )
        
            # set values to widget
            for attrib in obj.Attributes().values():
                self.__m_AttributeEditor.SetValue_Exec( attrib.AttributeID(), attrib.Value() )

            return True


        except:
            return False


    ################################### Operations ###################################

    def CreateNode_Operation( self, nodetype, pos, size, name, object_id, parent_id, attrib_ids ):
        newNode = super(NESceneExt, self).CreateNode_Operation( nodetype, pos, size, name, object_id, parent_id, attrib_ids )
        # Create Node in NodeGraph
        #nodeDesc = self.__m_NodeTypeManager.GetNodeDesc( nodetype )
        #computeFunc = self.__m_NodeTypeManager.GetComputeFunc( nodetype )
        #newNode = self.__m_NodeGraph.AddNode( nodeDesc, computeFunc, pos, size, name, object_id, attrib_ids, parent_id )
        
        newsize = newNode.GetSize()
        # Create Node in GraphicsScene
        self.__m_Scene.CreateNode_Exec( newNode.Key(), newNode.ID(), newNode.GetDesc(), newNode.GetPosition(), newNode.ParentID() )                    

        return newNode


    def RemoveNode_Operation( self, node_id ):
        super(NESceneExt, self).RemoveNode_Operation( node_id )
        # Remove node in NodeGraph
        #result = self.__m_NodeGraph.RemoveNodeByID( node_id )

        # Remove node in GraphicsScene
        self.__m_Scene.RemoveNode_Exec( node_id )


    def Connect_Operation( self, attrib1_id, attrib2_id, object_id ):
        newConn = super(NESceneExt, self).Connect_Operation( attrib1_id, attrib2_id, object_id )
        # Create Connection in NodeGraph
        #newConn = self.__m_NodeGraph.AddConnectionByID( attrib1_id, attrib2_id, object_id )
        
        # Set Attribute's Lock/Unlock state in NodeGraph
        #self.__m_NodeGraph.LockAttributeByID( newConn.DestinationAttribID(), False )
        
        # Create Connection in GraphicsScene
        self.__m_Scene.Connect_Exec( newConn.Key(), newConn.ID(), newConn.SourceAttribID(), newConn.DestinationAttribID(), newConn.ParentID() )

        # Update AttributeEditorWidget
        self.__m_AttributeEditor.SetEnabled_Exec( newConn.DestinationAttribID(), False )


        return newConn


    def Disconnect_Operation( self, conn_id ):
        super(NESceneExt, self).Disconnect_Operation( conn_id )
        # Disconnect in NodeGraph
        #dest_attrib_id = self.__m_NodeGraph.RemoveConnectionByID( conn_id )

        # Set Attribute's Lock/Unlock state in NodeGraph
        #self.__m_NodeGraph.LockAttributeByID( dest_attrib_id, True )

        # Disconnect in GraphicsScene
        self.__m_Scene.Disconnect_Exec( conn_id )

        # Update AttributeEditorWidget.
        #self.__m_AttributeEditor.SetEnabled_Exec( dest_attrib_id, True )


    def Reconnect_Operation( self, conn_id, attrib1_id, attrib2_id ):
        conn = super(NESceneExt, self).Reconnect_Operation( conn_id, attrib1_id, attrib2_id )
        # Reconnect in NodeGraph
        #conn, prev_src_attrib_id, prev_dest_attrib_id = self.__m_NodeGraph.ReconnectByID( conn_id, attrib1_id, attrib2_id )

        # Set Attribute's Lock/Unlock state in NodeGraph
        #prev_state = self.__m_NodeGraph.LockAttributeByID( conn.DestinationAttribID(), False )

        # Reconnect in GraphicsScene
        self.__m_Scene.Reconnect_Exec( conn.ID(), ( conn.Source().ParentID(), conn.SourceID() ), ( conn.Destination().ParentID(), conn.DestinationID() ), conn.ParentID() )

        # TODO: NESceneBase::Reconnect_Operation()内でLockAttributeOperationを呼び出せばいいのでは？
        # Update AttributeEditorWidget
        #self.__m_AttributeEditor.SetEnabled_Exec( conn.DestinationAttribID(), False )

        # return previous connection
        #return (prev_src_attrib_id, prev_dest_attrib_id)
        return conn


# TODO: グループを跨いで選択したノード群はどうやってグループ化する?
    def CreateGroup_Operation( self, pos, size, name, object_id, parent_id ):
        newGroup = super(NESceneExt, self).CreateGroup_Operation( pos, size, name, object_id, parent_id )

        # Create Group in NodeGraph
        #newGroup = self.__m_NodeGraph.AddGroup( pos, size, name, object_id, parent_id )

        # Create Group in GraphicsScene
        self.__m_Scene.CreateGroup_Exec( newGroup.Key(), newGroup.ID(), newGroup.GetPosition(), newGroup.ParentID() )
        
        return newGroup
        

    def RemoveGroup_Operation( self, group_id ):
        result = super(NESceneExt, self).RemoveGroup_Operation( group_id )
        #print( 'NESceneExt::RemoveGroup_Operation()...' )
        # Remove group in NodeGraph
        #result = self.__m_NodeGraph.RemoveGroupByID( group_id )

        # Remove group in GraphicsScene
        self.__m_Scene.RemoveGroup_Exec( group_id )    


# Implemented in NESceneBase
    #def Group_Operation( self, obj_id_list, pos, size, name, object_id, parent_id ):

    #    #-------------------------------- グループノード本体を作るオペレーション ---------------------------#
    #    group = self.CreateGroup_Operation( pos, size, name, object_id, parent_id )

    #    #--------------------------- グループに子ノードを追加するオペレーション ---------------------------#
    #    for obj_id in obj_id_list:
    #        self.Parent_Operation( obj_id, group.ID() )

    #    #--------------------- グループに内包されるコネクションも子供状態にするオペレーション ------------#
    #    for conn_id in group.CollectInternalConnections():
    #        self.Parent_Operation( conn_id, group.ID() )
        
    #    return group.ID()


# Implemented in NESceneBase
    #def Ungroup_Operation( self, group_id ):
        
    #    group = self.__m_NodeGraph.GetObjectByID( group_id, (NEGroupObject,) )
    #    group_parent_id = group.ParentID()
    #    connection_ids, object_ids = group.GetMemberIDs()
        
    #    # グループ内オブジェクトの親をもとに戻す
    #    for obj_id in object_ids:
    #        self.Parent_Operation( obj_id, group_parent_id )

    #    # グループ内コネクションの親をもとに戻す
    #    for conn_id in connection_ids:
    #        self.Parent_Operation( conn_id, group_parent_id )

    #    # グループを削除する
    #    self.RemoveGroup_Operation( group_id )


    def Rename_Operation( self, node_id, newname ):
        new_name, prev_name = super(NESceneExt, self).Rename_Operation( node_id, newname )
        # Rename in NodeGraph
        #new_name, prev_name = self.__m_NodeGraph.RenameByID( node_id, newname )

        # Rename in GraphicsScene
        self.__m_Scene.Rename_Exec( node_id, new_name )

        # Update AttributeEditorWidget
        self.__m_AttributeEditor.Rename_Exec( node_id, new_name )

        return new_name, prev_name


    def RenameAttribute_Operation( self, attrib_id, newname ):
        new_name, prev_name = super(NESceneExt, self).RenameAttribute_Operation( attrib_id, newname )
        # Rename in NodeGraph
        #new_name, prev_name = self.__m_NodeGraph.RenameAttributeByID( attrib_id, newname ) 

        # Rename in GraphicsScene
        self.__m_Scene.RenameAttribute_Exec( attrib_id, new_name )
        
        # Update AttributeEditorWidget
        self.__m_AttributeEditor.RenameAttribute_Exec( attrib_id, new_name )
        
        return new_name, prev_name


    def SetAttribute_Operation( self, attrib_id, new_value ):
        prev_value = super(NESceneExt, self).SetAttribute_Operation( attrib_id, new_value )
        # Set Attribute in NodeGraph
        #prev_value = self.__m_NodeGraph.SetAttributeByID( attrib_id, new_value )

        # Update AttributeEditorWidget
        self.__m_AttributeEditor.SetValue_Exec( attrib_id, new_value )

        return prev_value


    def LockAttribute_Operation( self, attrib_id, new_state ):
        prev_state = super(NESceneExt, self).LockAttribute_Operation( attrib_id, new_state )
        # Set Attribute's Lock/Unlock state in NodeGraph
        #prev_state = self.__m_NodeGraph.LockAttributeByID( attrib_id, new_state )

        # Update AttributeEditorWidget
        self.__m_AttributeEditor.SetEnabled_Exec( attrib_id, new_state )

        return prev_state


    def Translate_Operation( self, object_id, new_pos, realative ):
        translation = super(NESceneExt, self).Translate_Operation( object_id, new_pos, realative )
        # Set Translation in NodeGraph
        #translation = self.__m_NodeGraph.TranslateByID( object_id, new_pos, realative )

        # Set Translation in GraphicsScene
        self.__m_Scene.Translate_Exec( object_id, new_pos, realative )

        return translation


    def SetVisible_Operation( self, object_id, flag ):
        prev_flag = super(NESceneExt, self).SetVisible_Operation( object_id, flag )
        # Set Visibility in NodeGraph
        #prev_flag = self.__m_NodeGraph.SetVisibleByID( object_id, flag )

        # Set Visibility in GraphicsScene
        self.__m_Scene.SetVisible_Exec( object_id, flag )

        return prev_flag


    def Parent_Operation( self, object_id, parent_id ):
        obj = super(NESceneExt, self).Parent_Operation( object_id, parent_id )# prev_parent_id, new_pos
        # Set parent in NodeGraph
        #prev_parent_id, new_pos = self.__m_NodeGraph.ParentByID( object_id, parent_id )

        # Set parent in GraphicsScene
        self.__m_Scene.Parent_Exec( object_id, parent_id )

        # Set new position on parent space
        self.__m_Scene.Translate_Exec( object_id, obj.GetPosition(), False )# new_pos

        return obj#prev_parent_id


    def CreateSymbolicLink_Operation( self, group_id, attribdesc, value, name=None, symboliclink_idset=(None,None,None), slot_index=-1 ):
        symboliclink = super(NESceneExt, self).CreateSymbolicLink_Operation( group_id, attribdesc, value, name, symboliclink_idset, slot_index )
        # Create Symboliclink in NodeGraph
        #symboliclink = self.__m_NodeGraph.ActivateSymbolicLinkByID( group_id, attribdesc, value, name, symboliclink_idset, slot_index )
        
        # Create Symboliclink in GraphicsScene
        self.__m_Scene.ActivateSymbolicLink_Exec( symboliclink.ParentID(), symboliclink.Key(), symboliclink.GetDesc(), symboliclink.SlotIndex() )# slot_index )
        
        # Update AttributeEditorWidget
        self.__UpdateAttributeEditor()

        return symboliclink


    def RemoveSymbolicLink_Operation( self, symboliclink_id ):
        super(NESceneExt, self).RemoveSymbolicLink_Operation( symboliclink_id )
        # Remove symboliclink in NodeGraph
        #self.__m_NodeGraph.DeactivateSymbolicLinkByID( symboliclink_id )

        # Remove symboliclink in GraphicsScene
        self.__m_Scene.DeactivateSymbolicLink_Exec( symboliclink_id )

        # Update AttributeEditorWidget
        self.__UpdateAttributeEditor()


    def SetSymbolicLinkSlotIndex_Operation( self, object_id, index ):
        prev_index = super(NESceneExt, self).SetSymbolicLinkSlotIndex_Operation( object_id, index )
        #print( 'NESceneExt::SetSymbolicLinkSlotIndex_Operation()...' )
        # Set symbolicLink order in NodeGraph
        #prev_index = self.__m_NodeGraph.SetSymbolicLinkSlotIndexByID( object_id, index )

        # Set symbolicLink order in GraphicsScene
        self.__m_Scene.SetSymbolicLinkSlotIndex_Exec( object_id, index )

        # Update AttributeEditorWidget
        self.__UpdateAttributeEditor()

        return prev_index    


    def CreateGroupIO_Operation( self, dataflow, pos, object_id, group_id ):
        groupio = super(NESceneExt, self).CreateGroupIO_Operation( dataflow, pos, object_id, group_id )
        #print( 'NESceneExt::CreateGroupIO_Operation()...' )
        # Create GroupIO in NodeGraph
        #groupio = self.__m_NodeGraph.CreateGroupIO( dataflow, pos, group_id, object_id )

        # Create GroupIO in GraphicsScene
        self.__m_Scene.CreateGroupIO_Exec( groupio.Key(), dataflow, groupio.GetPosition(), group_id, groupio.ID() )
        
        return groupio


    def RemoveGroupIO_Operation( self, object_id ):
        super(NESceneExt, self).RemoveGroupIO_Operation( object_id )
        #print( 'NESceneExt::RemoveGroupIO_Operation()...' )
        # Remove GroupIO in NodeGraph
        #self.__m_NodeGraph.RemoveGroupIOByID( object_id )

        # Remove GroupIO in GraphicsScene
        self.__m_Scene.RemoveGroupIO_Exec( object_id )



    def Select_Operation_Multi( self, obj_id_list, option ):
        try:
            #print( 'NESceneExt::Select_Operation_Multi()...' )
            #self.__m_SelectionList.Exec( *obj_id_list, **option )

            #if( self.__m_SelectionList.Changed()==False ):
            #    return False
            result = super(NESceneExt, self).Select_Operation_Multi( obj_id_list, option )
            if( result==False ):
                return False

            self.__m_AttributeEditor.DeinitializeWidget()

            obj_ids_editable = self.FilterObjectIDs( self.GetSelectedObjectIDs(), typefilter=c_EditableTypes, parent_id=None )
            # self.__m_NodeGraph.FilterObjects( self.GetSelectedObjectIDs(), typefilter=c_EditableTypes, parent_id=None )

            if( not obj_ids_editable ):
                return False

            # get object and desc from selected id
            obj_id = obj_ids_editable[0]
            obj = self.GetObjectByID( obj_id, c_EditableTypes )
            desc = obj.GetDesc()
            if( desc==None ):    return False

            # initialize attribute editor widget
            self.__m_AttributeEditor.InitializeWidget( obj_id, desc, obj.Key() )
        
            # set values to widget
            for attrib in obj.Attributes().values():
                self.__m_AttributeEditor.SetValue_Exec( attrib.AttributeID(), attrib.Value() )

            return True

        except:
            traceback.print_exc()
            return False