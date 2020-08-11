import pickle
import uuid
import functools
import ntpath

from .history.command_manager import CommandManager, TerminalCommand
from .factory.node_manager import *

from .graph.nenodegraph import *

from .plugin_manager import *

from .nescene_ext import *
from .nescene_commands import *




class NESceneManager:

    def __init__( self ):

        # Nodegraph data
        self.__m_refNEScene = None
        
        self.__m_CommandManager = CommandManager()
        self.__m_DuplicationSnapshot = SnapshotCommand()
        self.__m_CopySnapshot = SnapshotCommand()

        self.__m_Filepath = 'Untitled'
        
        self.__m_CallbackFuncs = {
            'CreateNodeByID': self.__CreateNodeByID_Exec,
            'CreateCustomNodeByID': self.__CreateCustomNodeByID_Exec,
            #'RemoveNodeByID', self.__RemoveNodeByID_Exec, # DeleteByID経由で呼び出す
            'ConnectByID': self.__ConnectByID_Exec,
            #'DisconnectByID': self.__DisconnectByID_Exec, # DeleteByID経由で呼び出す
            'SetAttributeByID': self.__SetAttributeByID_Exec,
            'RenameByID': self.__RenameByID_Exec,
            'RenameAttributeByID': self.__RenameAttributeByID_Exec,
            'GroupByID': self.__GroupByID_Exec,
            'UngroupByID': self.__UngroupByID_Exec,
            #'RemoveGroupByID', self.__RemoveGroupByID_Exec, # DeleteByID経由で呼び出す
            'DeleteByID': self.__DeleteByID_Exec,
            'SelectByID': self.__SelectByID_Exec,# オブジェクト選択操作.編集履歴に含めない
            'DuplicateByID': self.__DuplicateByID_Exec,
            'CutByID': self.__CutByID_Exec,
            'CopyByID': self.__CopyByID_Exec,
            'PasteByID': self.__PasteByID_Exec,
            'TranslateByID': self.__TranslateByID_Exec,
            'HideByID': self.__SetVisibleByID_Exec,
            'ShowHiddenByID': self.__SetVisibleByID_Exec,
            'CreateSymbolicLink': self.__CreateSymbolicLinkByID_Exec,
            #'RemoveSymbolicLinkByID': self.__RemoveSymbolicLinkByID_Exec,# DeleteByID経由で呼び出す
            'SetSymbolicLinkSlotIndexByID': self.__SetSymbolicLinkSlotIndexByID_Exec,
            #'ParentByID': self.__ParentByID_Exec,
            'Import': self.Import,
            'Undo': self.Undo,
            'Redo': self.Redo,
            'CheckConnectivityByID': self.__CheckConnectivityByID,
            'IsSymbolizableByID': self.__IsSymbolizableByID,

            'CreateGroupByID': self.__CreateGroupByID_Exec,

            'EditGroupByID': self.__EditGroupByID, # Open node edit window for group

            #'LockAttributeByID': __LockAttributeByID_Exec,# Disabled because of confliction with __ConnectByID_Exec/__DisconnectByID_Exec
        }

        self.__m_refDataChangedCallback = None
        self.__m_refEditGroupCallback = None
        self.__m_refUpdateProcedure = None




    def Release( self ):
        self.UnbindNEScene()
        self.__m_Filepath = 'Untitled'

        self.__m_CommandManager.Release()
        self.__m_DuplicationSnapshot.Release()
        self.__m_CopySnapshot.Release()

        self.__m_CallbackFuncs.clear()



    #====================== SceneManager Setup ==============================#
    def BindNEScene( self, nescene, datachanged, editgroup, updateProcedure ):

        self.__m_refNEScene = nescene
        self.__m_refNEScene.BindCommandCallbacks( self.ExecCommandCallback )
        
        self.__m_refEditGroupCallback = editgroup
        self.__m_refUpdateProcedure = updateProcedure
        self.__m_refDataChangedCallback = lambda : updateProcedure(modified=True)#datachanged



    def UnbindNEScene( self ):

        self.__m_refNEScene.UnbindCallbackFuncs()
        self.__m_refNEScene = None
        
        self.__m_refDataChangedCallback = None
        self.__m_refEditGroupCallback = None
        self.__m_refUpdateProcedure = None



    def GetFilePath( self ):
        return self.__m_Filepath



    def CheckGraph( self ):
        self.__m_refNEScene.CheckGraph()



    def EvaluateSelected( self ):
        self.__m_refNEScene.EvaluateSelected()



    def ExecCommandCallback( self, func_name='', *args, **kwargs ):
        return self.__m_CallbackFuncs[ func_name ]( *args, **kwargs )

    

    def CreateNode_Exec( self, nodetype, *args, **kwargs ):
        
        pos = kwargs['pos'] if 'pos' in kwargs else (0, 0)
        size = None
        name = kwargs['name'] if 'name' in kwargs else None
        parent_id = self.__m_refNEScene.GetObjectID( kwargs['parent'], (NERootObject, NEGroupObject,) ) if 'parent' in kwargs else None

        return self.__CreateNodeByID_Exec( nodetype, pos=pos, size=size, name=name, parent_id=parent_id )



    def __CreateNodeByID_Exec( self, nodetype, *, pos=(0,0), size=None, name=None, parent_id=None, object_id=None, active_attrib_ids=None, terminate=True ):
        
        print( 'NESceneManager::__CreateNodeByID_Exec()...', nodetype, pos )
        
        if( self.__m_refNEScene.NodeTypeExists( nodetype )==False ):
            print( '    Aborting: nodetype does not exist.' )
            return False

        # Create Node
        self.__m_CommandManager.executeCmd( CreateNodeCommand( self.__m_refNEScene, nodetype, pos, size, name, parent_id, object_id, active_attrib_ids ) )
        
        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def __RemoveNodeByID_Exec( self, node_id, *, terminate=True ):
        
        if( self.__m_refNEScene.ObjectExists( node_id, ( NENodeObject, ) )==False ):
            return False

        # Break connections from NodeGraph/GraphicsScene
        conn_id_list = self.__m_refNEScene.GetConnectionIDs( node_id )
        for conn_id in conn_id_list:
            self.__m_CommandManager.executeCmd( DisconnectCommand( self.__m_refNEScene, conn_id ) )
        
        self.__m_CommandManager.executeCmd( RemoveNodeCommand( self.__m_refNEScene, node_id ) )

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )
        
        return True



############################################# TODO: CustomNode experiments ####################################
    def __CreateCustomNodeByID_Exec( self, nodetype, *, pos=(0,0), name=None, parent_id=None, object_id=None, active_attrib_ids=None, terminate=True ):
        
        print( 'NESceneManager::__CreateCustomNodeByID_Exec()...', nodetype, pos )
        
        # Create Custom Node
        self.__m_CommandManager.executeCmd( CreateCustomNodeCommand( self.__m_refNEScene, nodetype, pos, name, parent_id, object_id, active_attrib_ids ) )
        
        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def __RemoveCustomNodeByID_Exec( self, node_id, *, terminate=True ):
        
        if( self.__m_refNEScene.ObjectExists( node_id, ( NENodeObject, ) )==False ):
            return False

        # Break connections from NodeGraph/GraphicsScene
        conn_id_list = self.__m_refNEScene.GetConnectionIDs( node_id )
        for conn_id in conn_id_list:
            self.__m_CommandManager.executeCmd( DisconnectCommand( self.__m_refNEScene, conn_id ) )
        
        self.__m_CommandManager.executeCmd( RemoveCustomNodeCommand( self.__m_refNEScene, node_id ) )

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )
        
        return True
###################################################################################################################



    def Connect_Exec( self, name_source, name_dest ):

        source_id = self.__m_refNEScene.GetAttributeID( name_source )
        dest_id = self.__m_refNEScene.GetAttributeID( name_dest )
        
        if( source_id==None or dest_id==None ):
            return False
        
        return self.__ConnectByID_Exec( source_id, dest_id, check=True )



    def __ConnectByID_Exec( self, attrib1_id, attrib2_id, *, object_id=None,  check=False, terminate=True ):
        
        if( check==True ):
            if( self.__m_refNEScene.IsConnectable( attrib1_id, attrib2_id, checkloop=True )==False ):
                return False

        # Disconnect overlapped connections
        overlapped_conn_ids = self.__m_refNEScene.GetOverlappedConnections( [attrib1_id, attrib2_id] )
        for conn_id in overlapped_conn_ids:
            self.__m_CommandManager.executeCmd( DisconnectCommand( self.__m_refNEScene, conn_id ) )

        # Create Connection
        self.__m_CommandManager.executeCmd( ConnectCommand( self.__m_refNEScene, (attrib1_id, attrib2_id), object_id ) )

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def Disconnect_Exec( self, attrib1_name, attrib2_name ):

        conn_id = self.__m_refNEScene.GetConnectionID( attrib1_name, attrib2_name )

        if( conn_id == None ):
            return False

        return self.__DisconnectByID_Exec( conn_id )



    def __DisconnectByID_Exec( self, conn_id, *, terminate=True ):

        if( self.__m_refNEScene.ObjectExists( conn_id, ( NEConnectionObject, ) )==False ):
            return False
        
        snapshot = self.__m_CommandManager.executeCmd( DisconnectCommand( self.__m_refNEScene, conn_id ) )._DisconnectCommand__m_Snapshot# Remove Connection
        src_attrib_id = snapshot.SourceAttribID()
        dest_attrib_id = snapshot.DestinationAttribID()

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )
        
        return True



    def SetAttribute_Exec( self, attrib_name, value ):
        
        attrib_id = self.__m_refNEScene.GetAttributeID( attrib_name )

        if( attrib_id==None ):
            return False

        return self.__SetAttributeByID_Exec( attrib_id, value )



    def __SetAttributeByID_Exec( self, attrib_id, value, *, terminate=True ):

        if( self.__m_refNEScene.IsNewAttributeValue( attrib_id, value )==False ):
            return False

        #print( 'NESceneManager::__SetAttributeByID_Exec()...', attrib.FullKey(), value )

        self.__m_CommandManager.executeCmd( SetAttributeCommand( self.__m_refNEScene, attrib_id, value ) )

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def LockAttribute_Exec( self, attrib_name, state ):

        attrib_id = self.__m_refNEScene.GetAttributeID( attrib_name )

        if( attrib_id==None ):
            return False

        return self.__LockAttributeByID_Exec( attrib_id, state )



    def __LockAttributeByID_Exec( self, attrib_id, state, *, terminate=True ):

        if( self.__m_refNEScene.AttributeExists( attrib_id )==False ):
            return False
        print( 'NESceneManager::__LockAttributeByID_Exec()...' )
        self.__m_CommandManager.executeCmd( LockAttributeCommand( self.__m_refNEScene, attrib_id, state ) )

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def Rename_Exec( self, currname, newname ):

        object_id = self.__m_refNEScene.GetObjectID( currname, ( NENodeObject, NEGroupObject, NESymbolicLink ) )
        if( object_id==None ):
            return False

        return self.__RenameByID_Exec( object_id, newname )



    def __RenameByID_Exec( self, object_id, newname, *, terminate=True ):
        
        if( self.__m_refNEScene.ObjectExists( object_id, ( NENodeObject, NEGroupObject, NESymbolicLink ) )==False ):
            return False

        if( self.__m_refNEScene.IsValidNewName( object_id, newname )==False ):# Avoid renaming with current name.
            return False

        #print( 'NESceneManager::__RenameByID_Exec()...', obj.Key(), newname )
        self.__m_CommandManager.executeCmd( RenameCommand( self.__m_refNEScene, object_id, newname ) )
        
        # Terminate command sequence
        #if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )
        
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( lambda: self.__m_refUpdateProcedure( renamed=object_id ) ) )

        return True



    def RenameAttribute_Exec( self, currname, newname ):

        attrib_id = self.__m_refNEScene.GetAttributeID( currname )
        if( attrib_id==None ):
            return False

        return self.__RenameAttributeByID_Exec( attrib_id, newname )



    def __RenameAttributeByID_Exec( self, attrib_id, newname, *, terminate=True ):

        print( 'NESceneManager::__RenameAttributeByID_Exec()...' )
        if( self.__m_refNEScene.AttributeExists( attrib_id )==False ):
            print( '    Aborting: Attribute does not exist.' )
            return False

        #attrib = self.__m_refNEScene.GetAttribute( attrib_id )
        #print( attrib.AttributeID()[0] == attrib.Parent().ID() )
        #print( attrib.ParentID() == attrib.Parent().ID() )

        # SymbolicLinkの場合はself.__RenameByID_Execを使うように処理を切り替える
        if( self.__m_refNEScene.GetType(attrib_id[0])==NESymbolicLink ):
            return self.__RenameByID_Exec( attrib_id[0], newname, terminate=terminate )
        
        self.__m_CommandManager.executeCmd( RenameAttributeCommand( self.__m_refNEScene, attrib_id, newname ) )
        
        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def Select_Exec( self, *args, **kwargs ):
        obj_name_list = [ arg for arg in args if isinstance(arg, str) ]
        option = kwargs
        obj_id_list = self.__m_refNEScene.GetObjectIDs( obj_name_list, typefilter=c_SelectableTypes )

        if( not obj_id_list ):
            SelectCommand( self.__m_refNEScene, [], {'clear':True} ).execute()
            return False

        SelectCommand( self.__m_refNEScene, obj_id_list, option ).execute()

        return True



    def __SelectByID_Exec( self, obj_id_list, option ):
        #print( 'NESceneManager::__SelectByID_Exec()...' )
        obj_id_list = self.__m_refNEScene.FilterObjectIDs( obj_id_list, typefilter=c_SelectableTypes, parent_id=None )
        
        if( not obj_id_list ):
            SelectCommand( self.__m_refNEScene, [], {'clear':True} ).execute()
            return False

        SelectCommand( self.__m_refNEScene, obj_id_list, option ).execute()

        # Evaluate Selected Objects.
        self.__m_refNEScene.EvaluateSelected()

        return True



    def __CheckConnectivityByID( self, attrib1_id, attrib2_id ):
        return self.__m_refNEScene.IsConnectable( attrib1_id, attrib2_id, checkloop=False )



    def __IsSymbolizableByID( self, attrib_id ):
        return self.__m_refNEScene.IsSymbolizable( attrib_id )



    def Group_Exec( self, *args, **kwargs ):

        # Gather object ids
        obj_name_list = [ arg for arg in args if isinstance(arg, str) ]
        obj_id_list = self.__m_refNEScene.GetObjectIDs( obj_name_list, (NENodeObject, NEGroupObject) )

        # Check parent space argument
        parent_id = self.__m_refNEScene.GetObjectID( kwargs['parent'], (NERootObject, NEGroupObject) ) if 'parent' in kwargs else None

        return self.__GroupByID_Exec( obj_id_list, parent_id=None )



    def __GroupByID_Exec( self, obj_id_list, parent_id, *, pos=None, size=None, name=None, object_id=None, groupio_ids=(None, None), align_groupios=True, terminate=True ):

        print( 'NESceneManager::__GroupByID_Exec()...' )

        obj_id_list = self.__m_refNEScene.FilterObjectIDs( obj_id_list, typefilter=(NENodeObject, NEGroupObject), parent_id=None )#parent_id )
        if( not obj_id_list ):
            print( '    Aborting: No valid objects specified.' )
            return False

        # Abort grouping if obj_id_list contains invalid objects.
        if( self.__m_refNEScene.IsGroupable( obj_id_list, parent_id )==False ):
            print( '    Aborting: Unable to group ancestor node/group.' )
            return False

        # CreateGroup
        group_pos = pos if pos else self.__m_refNEScene.CenterPosition( obj_id_list )
        group_id, groupin_id, groupout_id = self.__CreateGroupByID_Exec( pos=group_pos, size=size, name=name, parent_id=parent_id, object_id=object_id,
                                                                  groupio_ids=groupio_ids, terminate=False )
        
        # Parent NENodeObjects NEGroupObjects, and relevant NEConnectionObjects
        self.__ParentByID_Exec( obj_id_list, group_id, terminate=False )

        # Align GroupIO positions
        if( align_groupios ):
            groupio_pos = self.__m_refNEScene.GetGroupIOPosition( group_id )# Generate GroupIOs' default position
            self.__TranslateByID_Exec( (groupin_id,), groupio_pos[0], relative=False, terminate=False )
            self.__TranslateByID_Exec( (groupout_id,), groupio_pos[1], relative=False, terminate=False )

        # Clear selection
        SelectCommand( self.__m_refNEScene, [], {'clear':True} ).execute()

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def Ungroup_Exec( self, group_name ):
        # Do Ungrouping in NodeGraph
        group_id = self.__m_refNEScene.GetObjectID( group_name, (NEGroupObject,) )
        return self.__UngroupByID_Exec( group_id )



    def __UngroupByID_Exec( self, group_id, *, terminate=True ):

        print( 'NESceneManager::__UngroupByID_Exec()...' )

        if( self.__m_refNEScene.GetType(group_id)!=NEGroupObject ):
            print( '    Aborting: No valid objects specified.' )
            return False

        parent_id = self.__m_refNEScene.GetParentID( group_id )# get parent space id after ungrouping
        symboliclink_id_list = self.__m_refNEScene.GetSymboliclinkIDs( group_id )# gather symboliclink ids

        conn_info_restore = []
        for symboliclink_id in symboliclink_id_list:# extract symboliclinks' actual from/to attribute id
            conn_info_restore += self.__m_refNEScene.ExtractSymbolicLinkConnections( symboliclink_id )

        # Resolve node name confliction caused by ungrouping
        rename_dict = self.__m_refNEScene.ResolveChildNames( group_id )
        for obj_id, newname in rename_dict.items():
            self.__m_CommandManager.executeCmd( RenameCommand( self.__m_refNEScene, obj_id, newname ) )

        # Unparent child Nodes/Groups. Relevant Connections are also removed.
        # print( '#==================== Unparent child Nodes/Groups ====================#' )
        connection_ids, object_ids = self.__m_refNEScene.GetGroupMemberIDs( group_id )
        self.__ParentByID_Exec( object_ids, parent_id, terminate=False )

        # Remove SymbolicLinks and their direct Connections
        #print( '#================ Remove SymbolicLinks and their direct Connections ===============#' )
        for symboliclink_id in symboliclink_id_list:
            self.__RemoveSymbolicLinkByID_Exec( symboliclink_id, terminate=False )

        # Remove GroupIOs
        #print( '#============================== Remove GroupIO ====================================#' )
        groupio_ids = self.__m_refNEScene.GetGroupIOIDs( group_id )
        for gio_id in groupio_ids:
            self.__m_CommandManager.executeCmd( RemoveGroupIOCommand( self.__m_refNEScene, gio_id ) )

        # Remove Group
        #print( '#============================== Remove Group ====================================#' )
        self.__m_CommandManager.executeCmd( RemoveGroupCommand( self.__m_refNEScene, group_id ) )

        # Restore Connections of unparented Node/Groups
        #print( '#================= Restore Connections of unparented Node/Groups ================#' )
        for attrib_ids in conn_info_restore:
            self.__m_CommandManager.executeCmd( ConnectCommand( self.__m_refNEScene, attrib_ids, None ) )

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def CreateGroup_Exec( self, *args, **kwargs ):
        # Check arguments
        pos = kwargs['pos'] if 'pos' in kwargs else (0, 0)
        name = kwargs['name'] if 'name' in kwargs else None
        parent_id = self.__m_refNEScene.GetObjectID( kwargs['parent'], (NERootObject, NEGroupObject) ) if 'parent' in kwargs else None

        return self.__CreateGroupByID_Exec( pos=pos, name=name, parent_id=parent_id )



    def __CreateGroupByID_Exec( self, *, pos=(0,0), size=None, name=None, parent_id=None, object_id=None, groupio_ids=(None, None), terminate=True ):

        # Group Createion Command
        group_id = self.__m_CommandManager.executeCmd( CreateGroupCommand( self.__m_refNEScene, pos, size, name, parent_id, object_id ) )._CreateGroupCommand__m_Snapshot.ObjectID()

        # GroupIO Creation Command
        group_io_pos = ( (-150, 0), (150, 0) )# Generate GroupIOs' default position
        group_in_id = self.__m_CommandManager.executeCmd( CreateGroupIOCommand( self.__m_refNEScene, DataFlow.Input, group_io_pos[0], groupio_ids[0], group_id ) )._CreateGroupIOCommand__m_Snapshot.ObjectID()
        group_out_id = self.__m_CommandManager.executeCmd( CreateGroupIOCommand( self.__m_refNEScene, DataFlow.Output, group_io_pos[1], groupio_ids[1], group_id ) )._CreateGroupIOCommand__m_Snapshot.ObjectID()
        
        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return group_id, group_in_id, group_out_id



    # Use Delete_Exec instead.
    #def RemoveGroup_Exec( self, group_name ):
    #    group_id = self.__m_refNEScene.GetObjectID( group_name, (NEGroupObject,) )
    #    return self.__RemoveGroupByID_Exec( group_id )



    def __RemoveGroupByID_Exec( self, group_id, *, terminate=True ):
        
        # Collect Groups and Nodes to delete
        subgroup_ids, subnode_ids = self.__m_refNEScene.GetDescendantIDs( group_id )
        
        # Ungroup all group objects inside descendant_list
        for group_id in subgroup_ids:
            self.__UngroupByID_Exec( group_id, terminate=False )

        # Then Remove all child objects
        for node_id in subnode_ids:
            self.__RemoveNodeByID_Exec( node_id, terminate=False )

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def CreateSymbolicLink_Exec( self, attrib_name ):
        attrib_id = self.__m_refNEScene.GetAttributeID( attrib_name )

        self.__CreateSymbolicLinkByID_Exec( attrib_id )



    def __CreateSymbolicLinkByID_Exec( self, attrib_id, *, symboliclink_idset=(None,None,None), conn_id=None, slot_index=-1, terminate=True ):

        if( self.__m_refNEScene.IsSymbolizable( attrib_id )==False ):
            return False

        # Collect attribute's exsiting connections (for symboliclink bypassing)
        parent_id, desc, value, name = self.__m_refNEScene.GetSymbolocLinkInitialParams( attrib_id )
        
        # Create SymbolicLink( and ProtectedAttribute's Connection )
        command = self.__m_CommandManager.executeCmd( CreateSymbolicLinkCommand( self.__m_refNEScene, parent_id, desc, value, name, symboliclink_idset, slot_index ) )
        snapshot = command._CreateSymbolicLinkCommand__m_Snapshot

        # Create ProtectedAttribute Connection
        self.__m_CommandManager.executeCmd( ConnectCommand( self.__m_refNEScene, (snapshot.ProtectedAttribID(), attrib_id), conn_id ) )

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def CreateSymbolicLinkByDesc_Exec( self, group_id, attrib_desc, value, name, *, symboliclink_idset=(None,None,None), slot_index=-1, terminate=True ):
  
        # Create SymbolicLink( and ProtectedAttribute's Connection )
        command = self.__m_CommandManager.executeCmd( CreateSymbolicLinkCommand( self.__m_refNEScene, group_id, attrib_desc, value, name, symboliclink_idset, slot_index ) )
        snapshot = command._CreateSymbolicLinkCommand__m_Snapshot

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return snapshot.ProtectedAttribID(), snapshot.ExposedAttribID()



    # Use Delete_Exec instead.
    #def RemoveSymbolicLink_Exec( self, symboliclink_name ):
    #    symboliclink_id = self.__m_refNEScene.GetObjectByName( symboliclink_name, (NESymbolicLink,) )

    #    self.__RemoveSymbolicLinkByID_Exec( symboliclink_id )



    def __RemoveSymbolicLinkByID_Exec( self, symboliclink_id, *, terminate=True ):
        
        # Remove all connections
        #print( '#=================== __RemoveSymbolicLinkByID_Exec::Remove all connections ====================#' )
        for conn_id in self.__m_refNEScene.GetConnectionIDs( symboliclink_id ):
            self.__m_CommandManager.executeCmd( DisconnectCommand( self.__m_refNEScene, conn_id ) )

        # Remove SymbolicLink Node( and ProtectedAttribute's connection)
        #print( '#=================== Remove SymbolicLink Node( and ProtectedAttribute\'s connection) ====================#' )
        self.__m_CommandManager.executeCmd( RemoveSymbolicLinkCommand( self.__m_refNEScene, symboliclink_id ) )
        
        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def __SetSymbolicLinkSlotIndexByID_Exec( self, symboliclink_id, index, terminate=True ):
        
        if( self.__m_refNEScene.IsNewSymboliclinkSlot(symboliclink_id, index)==False ):
            return False

        print( 'NESceneManager::__SetSymbolicLinkSlotIndexByID_Exec()...', index  )

        self.__m_CommandManager.executeCmd( SetSymbolicLinkSlotIndexCommand( self.__m_refNEScene, symboliclink_id, index ) )

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def Delete_Exec( self, *args, **kwargs ):
        obj_name_list = [ arg for arg in args if isinstance(arg, str) ]
        self.__DeleteByID_Exec( self.__m_refNEScene.GetObjectIDs( obj_name_list ) )



    def __DeleteByID_Exec( self, obj_id_list, *, terminate=True ):

        #print( 'NESceneManager::__DeleteByID_Exec()...' )

        for obj_id in obj_id_list:#sorted( set(obj_id_list), key=obj_id_list.index ):
            obj_type = self.__m_refNEScene.GetType( obj_id )

            if( obj_type==None ):
                continue

            if( obj_type is NENodeObject ):
                self.__RemoveNodeByID_Exec( obj_id, terminate=False )

            elif( obj_type is NEGroupObject ):
                self.__RemoveGroupByID_Exec( obj_id, terminate=False )

            elif( obj_type is NEConnectionObject ):
                self.__DisconnectByID_Exec( obj_id, terminate=False )

            elif( obj_type is NESymbolicLink ):
                self.__RemoveSymbolicLinkByID_Exec( obj_id, terminate=False )

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )



    def Duplicate_Exec( self, *args, **kwargs ):
        # Gather object ids
        obj_name_list = [ arg for arg in args if isinstance(arg, str) ]
        obj_id_list = self.__m_refNEScene.GetObjectIDs( obj_name_list )

        # Check options
        parent_id = self.__m_refNEScene.GetObjectID( kwargs['parent'], (NERootObject, NEGroupObject) ) if 'parent' in kwargs else None

        return self.__DuplicateByID_Exec( obj_id_list, parent_id )


    
# parent_idはコピー先の親空間
    def __DuplicateByID_Exec( self, obj_id_list, parent_id, *, terminate=True ):
        
        print( 'NESceneManager::__DuplicateByID_Exec()...' )

        # 選択オブジェクトの親空間を制限したい場合はparent_id引数を指定する
        obj_id_list = self.__m_refNEScene.FilterObjectIDs( obj_id_list, typefilter=(NENodeObject, NEGroupObject), parent_id=None )#parent_id )
        if( not obj_id_list ):
            print( '\tAborting: No valid objects specified.' )
            return
        
        # Store selected item data to snapshot
        self.__m_DuplicationSnapshot.Init( self.__m_refNEScene, obj_id_list )

        selection_id_list = self.__ExecuteSnapshot( self.__m_DuplicationSnapshot, (75.0, 75.0), parent_id )
        SelectCommand( self.__m_refNEScene, selection_id_list, {'clear':True} ).execute()

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )



    def __CutByID_Exec( self, obj_id_list, parent_id ):

        print( 'NESceneManager::__CutByID_Exec()...' )

        obj_id_list = self.__m_refNEScene.FilterObjectIDs( obj_id_list, typefilter=(NENodeObject, NEGroupObject), parent_id=None )#parent_id )
        if( not obj_id_list ):
            print( '    Aborting: No valid objects specified.' )
            return

        # Store selected item data to snapshot
        self.__m_CopySnapshot.Init( self.__m_refNEScene, obj_id_list )

        # Remove selected items
        self.__DeleteByID_Exec( obj_id_list )



    def __CopyByID_Exec( self, obj_id_list, parent_id ):

        print( 'NESceneManager::__CopyByID_Exec()...' )

        obj_id_list = self.__m_refNEScene.FilterObjectIDs( obj_id_list, typefilter=(NENodeObject, NEGroupObject), parent_id=None )#parent_id )
        if( not obj_id_list ):
            print( '    Aborting: No valid objects specified.' )
            return

        # Store selected item data to snapshot
        self.__m_CopySnapshot.Init( self.__m_refNEScene, obj_id_list )



    def __PasteByID_Exec( self, parent_id, *, terminate=True ):

        selection_id_list = self.__ExecuteSnapshot( self.__m_CopySnapshot, (75.0, 75.0), parent_id )
        SelectCommand( self.__m_refNEScene, selection_id_list, {'clear':True} ).execute()

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )



    def __TranslateByID_Exec( self, obj_id_list, translate, *, relative=False, terminate=True ):

        posChanged = False
        obj_id_list = self.__m_refNEScene.FilterObjectIDs( obj_id_list, typefilter=c_EditableTypes, parent_id=None )#parent_id )        

        for object_id in obj_id_list:
            if( self.__m_refNEScene.PositionChanged( object_id, translate, relative ) ):
                self.__m_CommandManager.executeCmd( TranslateCommand( self.__m_refNEScene, object_id, translate, relative ) )
                posChanged = True

        if( posChanged==False ):
            return False

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

        return True



    def SetVisible_Exec( self, object_name, visibility=True ):

        object_id = self.__m_refNEScene.GetObjectID( object_name, ( NENodeObject, NEGroupObject, ) )

        if( object_id==None ):
            return False

        return self.__SetVisibleByID_Exec( object_id, visibility )



    def __SetVisibleByID_Exec( self, object_id, visibility=True, *, terminate=True ):

        # Check if visible change operation is necessary
        if( self.__m_refNEScene.IsNewVisibility( object_id, visibility )==False ):
            return False

        print( 'NESceneManager::__SetVisibleByID_Exec()...', visibility )

        self.__m_CommandManager.executeCmd( SetVisibleCommand( self.__m_refNEScene, object_id, visibility ) )

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )



    def Parent_Exec( self, parent_name ):

        parent_id = self.__m_refNEScene.GetObjectID( parent_name, (NERootObject, NEGroupObject) )
        if( parent_id==None ):
            print( 'Aborting Parent Operation: No parent space specified.' )
            return False

        obj_id_list = self.__m_refNEScene.GetSelectedObjectIDs()
        if( not obj_id_list ):
            print( 'Aborting Parent Operation: No objects selected.' )
            return False
        
        self.__ParentByID_Exec( obj_id_list, parent_id )
        return True



    def __ParentByID_Exec( self, obj_id_list, parent_id, *, terminate=True ):
        print( 'NESceneManager::__ParentByID_Exec()...' )

        if( self.__m_refNEScene.ObjectExists( parent_id, (NERootObject, NEGroupObject, ) )==False ):
            print( '    Aborting: No valid parent specified.' )
            return False

        obj_id_list = self.__m_refNEScene.FilterDescendants( obj_id_list, parent_id )

        if( not obj_id_list ):
            print( '    Aborting: No parentable objects selected.' )
            return False

        closed_conn_ids, open_attrib_info, removal_conn_info = self.__m_refNEScene.CollectConnections( obj_id_list, parent_id )
        
        #print( '#=================== Remove inter-group connections =================#' )
        for conn_id in removal_conn_info:
            self.__m_CommandManager.executeCmd( DisconnectCommand( self.__m_refNEScene, conn_id ) )

        # Change Parent of Nodes/Groups and Connections
        for object_id in obj_id_list:
            self.__m_CommandManager.executeCmd( ParentCommand( self.__m_refNEScene, object_id, parent_id ) )

        for conn_id in closed_conn_ids:
            self.__m_CommandManager.executeCmd( ParentCommand( self.__m_refNEScene, conn_id, parent_id ) )

        # Create SymbolicLinks and Connections
        for attrib_id_internal, conn_info in open_attrib_info.items():
            # Create SymbolicLink
            _, desc, value, name = self.__m_refNEScene.GetSymbolocLinkInitialParams( attrib_id_internal )
            symlink_id_protected, symlink_id_exposed = self.CreateSymbolicLinkByDesc_Exec( parent_id, desc, value, name, symboliclink_idset=(None,None,None), terminate=False )

            for _, attrib_id_external in conn_info:
                # Connect external attrib and exposed symboliclink attribute
                self.__m_CommandManager.executeCmd( ConnectCommand( self.__m_refNEScene, (attrib_id_external, symlink_id_exposed), None ) )
                # Connect protected symboliclink attribute and internal attribute
                self.__m_CommandManager.executeCmd( ConnectCommand( self.__m_refNEScene, (symlink_id_protected, attrib_id_internal), None ) )

        # Terminate command sequence
        if( terminate==True ):  self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )
        
        return True



    def IsUpToDate( self ):
        return self.__m_CommandManager.IsUpToDate()



    def IsModified( self ):
        return self.__m_CommandManager.IsModified()



    def __EditGroupByID( self, *args, **kwargs ):
        self.__m_refEditGroupCallback( *args, **kwargs )



    def __ExecuteSnapshot( self, snapshotCommand, offset, dest_space_id=None ):

        refObjIDs = snapshotCommand.PublishObjectIDs()
        refSnapshots = snapshotCommand.Snapshots()
        parent_space_id = dest_space_id if dest_space_id else self.__m_refNEScene.CurrentEditSpaceID()

        # Construct NodeGraph structure from Snapshots
        for i in range( len(refSnapshots) ):

            snapshot = refSnapshots[i]
            
            if( isinstance(snapshot, NEGroupSnapshot) ):
                newObjectID = refObjIDs[snapshot.ObjectID()]
                groupIOIDs = ( refObjIDs[ refSnapshots[i+1].ObjectID() ], refObjIDs[ refSnapshots[i+2].ObjectID() ] )# GroupIO2個分のuuidを取り出す.
                #name=snapshot.Key(),
                self.__CreateGroupByID_Exec( name=str(newObjectID), parent_id=parent_space_id, object_id=newObjectID, groupio_ids=groupIOIDs, terminate=False )
                i+=2 # skip GroupIO snapshots

            elif( isinstance(snapshot, NENodeSnapshot) ):
                active_attrib_ids = [ # new attribute ids
                        [ refObjIDs[id_] for id_ in snapshot.ActiveAttribIDs()[0] ], # input attributes
                        [ refObjIDs[id_] for id_ in snapshot.ActiveAttribIDs()[1] ], ] # output attributes
                newObjectID = refObjIDs[snapshot.ObjectID()]
                #name=snapshot.Key(), 
                self.__CreateNodeByID_Exec( snapshot.ObjectType(), name=str(newObjectID), parent_id=parent_space_id, object_id=newObjectID, active_attrib_ids=active_attrib_ids, terminate=False )
                for attribName in snapshot.AttribNames():
                    self.__RenameAttributeByID_Exec( (refObjIDs[attribName[0]], refObjIDs[attribName[1]]), attribName[2], terminate=False )
                for attribArg in snapshot.AttribArgs():
                    self.__SetAttributeByID_Exec( (refObjIDs[attribArg[0]], refObjIDs[attribArg[1]]), attribArg[2], terminate=False )

            elif( isinstance(snapshot, NEConnectionSnapshot) ):
                newObjectID = refObjIDs[snapshot.ObjectID()]
                src_id = snapshot.SourceAttribID()
                newAttrib1_ID = ( refObjIDs[src_id[0]], refObjIDs[src_id[1]] )
                dst_id = snapshot.DestinationAttribID()
                newAttrib2_ID = ( refObjIDs[dst_id[0]], refObjIDs[dst_id[1]] )
                self.__ConnectByID_Exec( newAttrib1_ID, newAttrib2_ID, object_id=newObjectID, terminate=False )
                self.__SetVisibleByID_Exec( newObjectID, snapshot.Visibility(), terminate=False )

            elif( isinstance(snapshot, NESymbolicLinkSnapshot) ):
                obj_idset = snapshot.ObjectIDSet()
                newObjectIDSet = ( refObjIDs[obj_idset[0]], refObjIDs[obj_idset[1]], refObjIDs[obj_idset[2]] )
                group_id = refObjIDs[snapshot.GroupID()]
                attribdesc = snapshot.AttribDesc()
                value = snapshot.Value()
                #name=snapshot.Key()
                self.CreateSymbolicLinkByDesc_Exec( group_id, attribdesc, value, str(newObjectIDSet[0]), symboliclink_idset=newObjectIDSet, slot_index=snapshot.SlotIntex(), terminate=False )
                for attribArg in snapshot.AttribArgs():
                    self.__SetAttributeByID_Exec( (refObjIDs[attribArg[0]], refObjIDs[attribArg[1]]), attribArg[2], terminate=False )

            elif( isinstance(snapshot, NEParentSnapshot) ):
                print( 'TODO: NEParentSnapshot detected...' )
                parent_id = refObjIDs[ snapshot.ObjectID() ]
                obj_id_list = [ refObjIDs[obj_id] for obj_id in snapshot.MemberIDs() ]
                self.__ParentByID_Exec( obj_id_list, parent_id, terminate=False )

        # Apply name and translation to each node.
        root_duplicate_ids = []

        dest_space_children = self.__m_refNEScene.GetObjectByID( parent_space_id, (NERootObject, NEGroupObject,) ).Children()
        typefilter_rename = ( NENodeSnapshot, NEGroupSnapshot, NESymbolicLinkSnapshot, )
        typefilter_translate = ( NENodeSnapshot, NEGroupSnapshot, NEGroupIOSnapshot, )

        for snapshot in snapshotCommand.Snapshots():

            object_id = refObjIDs[snapshot.ObjectID()]
            
            if( type(snapshot) in typefilter_rename ):# Set actual name to Node, Group and Symboliclink
                self.__RenameByID_Exec( object_id, snapshot.Key(), terminate=False )
            
            if( type(snapshot) in typefilter_translate ):# Translate Duplicated Node/Groups to appropriate position.
                pos = snapshot.Translation()
                offsetflag = float( snapshot.ObjectID() in dest_space_children )
                newPos = ( pos[0] + offset[0] * offsetflag, pos[1] + offset[1] * offsetflag )
                self.__TranslateByID_Exec( (object_id,), newPos, relative=False, terminate=False )

            if( object_id in dest_space_children ):# Add to root_duplicate_ids list if object is a direct child of target group
                root_duplicate_ids.append( object_id )

        # Return duplicated node/group ids in target space 
        return root_duplicate_ids

######################################################################################################################
#
# TODO: 形状パラメータをQtの外側で保持したい. コピペ時の形状サイズ再現性維持のため、下記スナップショット実装に機能拡張が必要
#
# TODO: Implement NESceneManager::ResizeByID_Exec(). 
# TODO: Refactor Translate/Resize operation
#  NENodeSnapshot　　　　サイズ指定、位置指定
#  NEGroupSnapshot　　　　サイズ指定、位置指定
#  NESymbolicLinkSnapshot　 -
#  NEConnectionSnapshot　　-
#  NEGroupIOSnapshot　　　位置指定
# 
######################################################################################################################



    ###################################### Menubar UI Commands ######################################

    def Clear( self ):
        self.__m_refNEScene.Clear()

        self.__m_Filepath = 'Untitled'

        self.__m_CommandManager.Clear()
        self.__m_DuplicationSnapshot.Clear()
        self.__m_CopySnapshot.Clear()



    def Open( self, filepath ):
        if( self.Import( filepath ) ):
            # Keep Filepath
            self.__m_Filepath = filepath
            # Clear history
            self.__m_CommandManager.Clear()

    

    def Save( self, filepath ):
        self.__m_Filepath = filepath
        self.Export( filepath )
        self.__m_CommandManager.SetReadout()



    def Import( self, filepath, offset=(0,0) ):
        objects = []
        with(open(filepath, 'rb')) as openfile:
            while True:
                try:
                    objects.append(pickle.load(openfile))# pickleでデシリアライズしてリストに追加する
                except EOFError:
                    break

        if( objects ):
            for obj in objects:
                self.__ExecuteSnapshot( obj, offset, self.__m_refNEScene.CurrentEditSpaceID() )
            # Terminate command sequence
            self.__m_CommandManager.executeCmd( TerminalCommand( self.__m_refDataChangedCallback ) )

            return True

        return False



    def Export( self, filepath ):
        snapshot = SnapshotCommand()
        snapshot.Init( self.__m_refNEScene, self.__m_refNEScene.GetChildrenIDs( self.__m_refNEScene.GetRootID() ) )
        snapshot.ExportCommand( filepath )
        snapshot.Release()

        

    def ExportSelection( self, filepath ):
        obj_id_list = self.__m_refNEScene.FilterObjectIDs( self.__m_refNEScene.GetSelectedObjectIDs(), typefilter=(NENodeObject, NEGroupObject), parent_id=None )# self.__m_refNEScene.CurrentEditSpaceID() )
        
        snapshot = SnapshotCommand()
        snapshot.Init( self.__m_refNEScene, obj_id_list )
        snapshot.ExportCommand( filepath )
        snapshot.Release()



    def Undo( self ):
        self.__m_CommandManager.undo()



    def Redo( self ):
        self.__m_CommandManager.redo()



    def Cut( self ):
        selected_ids = self.__m_refNEScene.GetSelectedObjectIDs()
        if( selected_ids ):
# TODO: parent_id is unused at __CutByID_Exec
            self.__CutByID_Exec( selected_ids, self.__m_refNEScene.CurrentEditSpaceID() )



# TODO: 複数グループを跨ぐノード群を、階層構造を維持したままコピー可能にする方法を考える.
    def Copy( self ):
        selected_ids = self.__m_refNEScene.GetSelectedObjectIDs()
        if( selected_ids ):
# TODO: parent_id is unused at __CopyByID_Exec
            self.__CopyByID_Exec( selected_ids, self.__m_refNEScene.CurrentEditSpaceID() )



    def Paste( self ):
        self.__PasteByID_Exec( self.__m_refNEScene.CurrentEditSpaceID() )



    def Duplicate( self ):
        self.__DuplicateByID_Exec( self.__m_refNEScene.GetSelectedObjectIDs(), parent_id=self.__m_refNEScene.CurrentEditSpaceID() )



    def Delete( self ):
        self.__DeleteByID_Exec( self.__m_refNEScene.GetSelectedObjectIDs() )



    def Group( self ):
        self.__GroupByID_Exec( self.__m_refNEScene.GetSelectedObjectIDs(), parent_id=self.__m_refNEScene.CurrentEditSpaceID() )



    def Ungroup( self ):
        for group_id in self.__m_refNEScene.GetSelectedObjectIDs():  
            self.__UngroupByID_Exec( group_id )