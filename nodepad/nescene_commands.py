import pickle
import uuid

from .component.descriptors import AttribLock

from .history.commandbase import CommandBase

from .graph.neconnectionobject import NEConnectionSnapshot
from .graph.nenodeobject import NENodeObject, NENodeSnapshot
from .graph.negroupobject import NEGroupObject, NEGroupSnapshot, NEParentSnapshot
from .graph.nesymboliclink import NESymbolicLinkSnapshot
from .graph.negroupioobject import NEGroupIOSnapshot

from .nescene_ext import NESceneExt


#========================== Commands ===================================#



########################### TODO: カスタムコードノードの操作コマンド試験実装. #####################################

# TODO: Register CustomNode creation procedure at GraphicsScene::contextMenuEvent.
# TODO: Implement NESceneManager::CreateCustomNode_Exec.
# TODO: Implement NESceneManager::__RemoveCustomNodeByID_Exec.
# TODO: Implement NEScene::CreateCustomNode_Operation.
# TODO: Implement NEScene::RemoveCustomNode_Operation.
# TODO: Implement NEScene::CompileCustomNodeCommand.


class CreateCustomNodeCommand(CommandBase):

    def __init__( self ):
        super(CreateCustomNodeCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = None


    def execute( self ):
        self.__m_Snapshot = self.__m_refNEScene.GetSnapshot( self.__m_refNEScene.CreateCustomNode_Operation( self.__m_NodeType, self.__m_Position, self.__m_Name, self.__m_ObjectID, self.__m_ParentID, self.__m_ActiveAttribIDs ) )

    def undo( self ):
        print( 'CreateCustomNodeCommand::undo()...' )
        self.__m_refNEScene.RemoveCustomNode_Operation( self.__m_Snapshot.ObjectID() )

    def redo( self ):
        print( 'CreateCustomNodeCommand::redo()...' )
        


class RemoveCustomNodeCommand(CommandBase):

    def __init__( self, neScene, object_id ):
        super(RemoveCustomNodeCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = neScene.GetSnapshot( object_id )


    def execute( self ):
        self.__m_refNEScene.RemoveCustomNode_Operation( self.__m_Snapshot.ObjectID()  )
        
    def undo( self ):
        print( 'RemoveCustomNodeCommand::undo()...' )
        # resotre node
        self.__m_refNEScene.CreateCustomNode_Operation( self.__m_Snapshot.ObjectType(), self.__m_Snapshot.Translation(), self.__m_Snapshot.Key(), self.__m_Snapshot.ObjectID(), self.__m_Snapshot.ParentID(), self.__m_Snapshot.ActiveAttribIDs() )
        # restore attribute names
        for attribName in self.__m_Snapshot.AttribNames():
            self.__m_refNEScene.RenameAttribute_Operation( (attribName[0], attribName[1]), attribName[2] )
        # restore attribute values and lock-states
        for attribArg in self.__m_Snapshot.AttribArgs():
            self.__m_refNEScene.SetAttribute_Operation( (attribArg[0], attribArg[1]), attribArg[2] )
            self.__m_refNEScene.LockAttribute_Operation( (attribArg[0], attribArg[1]), attribArg[3] )

    def redo( self ):
        print( 'RemoveCustomNodeCommand::redo()...' )
        self.__m_refNEScene.RemoveCustomNode_Operation( self.__m_Snapshot.ObjectID() )



class CompileCustomNodeCommand(CommandBase):

    def __init__( self, neScene, object_id ):
        super(CompileCustomNodeCommand, self).__init__()


    def execute( self ):
        pass
        
    def undo( self ):
        print( 'CompileCustomNodeCommand::undo()...' )
        

    def redo( self ):
        print( 'CompileCustomNodeCommand::redo()...' )


###################################################################################################




class CreateNodeCommand(CommandBase):

    def __init__( self, neScene, nodetype, pos, size, name, parent_id, object_id, active_attrib_ids ):
        super(CreateNodeCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = None

        self.__m_NodeType = nodetype
        self.__m_Position = pos
        self.__m_Size = size
        self.__m_Name = name
        self.__m_ParentID = parent_id
        self.__m_ObjectID = object_id
        self.__m_ActiveAttribIDs = active_attrib_ids


    def execute( self ):
        self.__m_Snapshot = self.__m_refNEScene.CreateNode_Operation( self.__m_NodeType, self.__m_Position, self.__m_Size, self.__m_Name, self.__m_ObjectID, self.__m_ParentID, self.__m_ActiveAttribIDs ).GetSnapshot() #self.__m_refNEScene.GetSnapshot( self.__m_refNEScene.CreateNode_Operation( self.__m_NodeType, self.__m_Position, self.__m_Size, self.__m_Name, self.__m_ObjectID, self.__m_ParentID, self.__m_ActiveAttribIDs ) )

    def undo( self ):
        print( 'CreateNodeCommand::undo()...' )
        self.__m_refNEScene.RemoveNode_Operation( self.__m_Snapshot.ObjectID() )

    def redo( self ):
        print( 'CreateNodeCommand::redo()...' )
        self.__m_refNEScene.CreateNode_Operation( self.__m_Snapshot.ObjectType(), self.__m_Snapshot.Translation(), self.__m_Snapshot.Size(), self.__m_Snapshot.Key(), self.__m_Snapshot.ObjectID(), self.__m_Snapshot.ParentID(), self.__m_Snapshot.ActiveAttribIDs() )




class RemoveNodeCommand(CommandBase):

    def __init__( self, neScene, object_id ):
        super(RemoveNodeCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = neScene.GetSnapshot( object_id )


    def execute( self ):
        self.__m_refNEScene.RemoveNode_Operation( self.__m_Snapshot.ObjectID()  )
        
    def undo( self ):
        print( 'RemoveNodeCommand::undo()...' )
        # restore node
        self.__m_refNEScene.CreateNode_Operation( self.__m_Snapshot.ObjectType(), self.__m_Snapshot.Translation(), self.__m_Snapshot.Size(), self.__m_Snapshot.Key(), self.__m_Snapshot.ObjectID(), self.__m_Snapshot.ParentID(), self.__m_Snapshot.ActiveAttribIDs() )
        # restore attribute names
        for attribName in self.__m_Snapshot.AttribNames():
            self.__m_refNEScene.RenameAttribute_Operation( (attribName[0], attribName[1]), attribName[2] )
        # restore attribute values and lock-states
        for attribArg in self.__m_Snapshot.AttribArgs():
            self.__m_refNEScene.SetAttribute_Operation( (attribArg[0], attribArg[1]), attribArg[2] )
            self.__m_refNEScene.LockAttribute_Operation( (attribArg[0], attribArg[1]), attribArg[3] )

    def redo( self ):
        print( 'RemoveNodeCommand::redo()...' )
        self.__m_refNEScene.RemoveNode_Operation( self.__m_Snapshot.ObjectID() )




class ConnectCommand(CommandBase):

    def __init__( self, neScene, attrib_ids, object_id ):
        super(ConnectCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = None
        
        self.__m_ObjectID = object_id
        self.__m_AttribIDs = attrib_ids


    def execute( self ):
        self.__m_Snapshot = self.__m_refNEScene.Connect_Operation( self.__m_AttribIDs[0], self.__m_AttribIDs[1], self.__m_ObjectID ).GetSnapshot()#self.__m_refNEScene.GetSnapshot( self.__m_refNEScene.Connect_Operation( self.__m_AttribIDs[0], self.__m_AttribIDs[1], self.__m_ObjectID ) )

    def undo( self ):
        print( 'ConnectCommand::undo()...' )
        self.__m_refNEScene.Disconnect_Operation( self.__m_Snapshot.ObjectID() )

    def redo( self ):
        print( 'ConnectCommand::redo()...' )
        self.__m_refNEScene.Connect_Operation( self.__m_Snapshot.SourceAttribID(), self.__m_Snapshot.DestinationAttribID(), self.__m_Snapshot.ObjectID() )




class DisconnectCommand(CommandBase):

    def __init__( self, neScene, object_id ):
        super(DisconnectCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = neScene.GetSnapshot( object_id )


    def execute( self ):
        self.__m_refNEScene.Disconnect_Operation( self.__m_Snapshot.ObjectID() )

    def undo( self ):
        print( 'DisconnectCommand::undo()...' )
        self.__m_refNEScene.Connect_Operation( self.__m_Snapshot.SourceAttribID(), self.__m_Snapshot.DestinationAttribID(), self.__m_Snapshot.ObjectID() )
        self.__m_refNEScene.Rename_Operation( self.__m_Snapshot.ObjectID(), self.__m_Snapshot.Key() )

    def redo( self ):
        print( 'DisconnectCommand::redo()...' )
        self.__m_refNEScene.Disconnect_Operation( self.__m_Snapshot.ObjectID() )




# Unused.
#class ReconnectCommand(CommandBase):

#    def __init__( self, neScene, object_id, attrib_ids ):
#        super(ReconnectCommand, self).__init__()

#        self.__m_refNEScene = neScene
#        self.__m_Snapshot = neScene.GetSnapshot( object_id )# keep before-reconnection state for undo

#        self.__m_NewAttribIDs = attrib_ids


#    def execute( self ):
#        self.__m_refNEScene.Reconnect_Operation( self.__m_Snapshot.ObjectID(), self.__m_NewAttribIDs[0], self.__m_NewAttribIDs[1] )

#    def undo( self ):
#        print( 'ReconnectCommand::undo()...' )
#        self.__m_refNEScene.Reconnect_Operation( self.__m_Snapshot.ObjectID(), self.__m_Snapshot.SourceAttribID(), self.__m_Snapshot.DestinationAttribID() )

#    def redo( self ):
#        print( 'ReconnectCommand::redo()...' )
#        self.__m_refNEScene.Reconnect_Operation( self.__m_Snapshot.ObjectID(), self.__m_NewAttribIDs[0], self.__m_NewAttribIDs[1] )




class CreateGroupCommand(CommandBase):

    def __init__( self, neScene, pos, size, name, parent_id, object_id ):
        super(CreateGroupCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = None
        self.__m_Position = pos
        self.__m_Size = size
        self.__m_Name = name
        self.__m_ParentID = parent_id
        self.__m_ObjectID = object_id


    def execute( self ):
        self.__m_Snapshot = self.__m_refNEScene.CreateGroup_Operation( self.__m_Position, self.__m_Size, self.__m_Name, self.__m_ObjectID, self.__m_ParentID ).GetSnapshot()

    def undo( self ):
        print( 'CreateGroupCommand::undo()...' )
        self.__m_refNEScene.RemoveGroup_Operation( self.__m_Snapshot.ObjectID() )

    def redo( self ):
        print( 'CreateGroupCommand::redo()...' )
        self.__m_refNEScene.CreateGroup_Operation( self.__m_Snapshot.Translation(), self.__m_Snapshot.Size(), self.__m_Snapshot.Key(), self.__m_Snapshot.ObjectID(), self.__m_Snapshot.ParentID() )




class RemoveGroupCommand(CommandBase):

    def __init__( self, neScene, object_id ):
        super(RemoveGroupCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = neScene.GetSnapshot( object_id )


    def execute( self ):
        self.__m_refNEScene.RemoveGroup_Operation( self.__m_Snapshot.ObjectID() )

    def undo( self ):
        print( 'RemoveGroupCommand::undo()...' )
        self.__m_refNEScene.CreateGroup_Operation( self.__m_Snapshot.Translation(), self.__m_Snapshot.Size(), self.__m_Snapshot.Key(), self.__m_Snapshot.ObjectID(), self.__m_Snapshot.ParentID() )

    def redo( self ):
        print( 'RemoveGroupCommand::redo()...' )
        self.__m_refNEScene.RemoveGroup_Operation( self.__m_Snapshot.ObjectID() )




class SetAttributeCommand(CommandBase):

    def __init__( self, neScene, attrib_id, value ):
        super(SetAttributeCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_ObjectID = attrib_id
        self.__m_NewValue = value
        self.__m_PrevValue = None


    def execute( self ):
        self.__m_PrevValue = self.__m_refNEScene.SetAttribute_Operation( self.__m_ObjectID, self.__m_NewValue )

    def undo( self ):
        print( 'SetAttributeCommand::undo()...' )
        self.__m_refNEScene.SetAttribute_Operation( self.__m_ObjectID, self.__m_PrevValue )

    def redo( self ):
        print( 'SetAttributeCommand::redo()...' )
        self.__m_refNEScene.SetAttribute_Operation( self.__m_ObjectID, self.__m_NewValue )




class LockAttributeCommand(CommandBase):

    def __init__( self, neScene, attrib_id, flag ):
        super(LockAttributeCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_ObjectID = attrib_id
        self.__m_NewState = AttribLock.UserLock if flag else AttribLock.Unlock
        self.__m_PrevState = None


    def execute( self ):
        self.__m_PrevState = self.__m_refNEScene.LockAttribute_Operation( self.__m_ObjectID, self.__m_NewState )
        
    def undo( self ):
        print( 'LockAttributeCommand::undo()...' )
        self.__m_refNEScene.LockAttribute_Operation( self.__m_ObjectID, self.__m_PrevState )

    def redo( self ):
        print( 'LockAttributeCommand::redo()...' )
        self.__m_refNEScene.LockAttribute_Operation( self.__m_ObjectID, self.__m_NewState )




class RenameCommand(CommandBase):

    def __init__( self, neScene, object_id, new_name ):
        super(RenameCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_ObjectID = object_id
        self.__m_NewName = new_name
        self.__m_PrevName = None


    def execute( self ):
        self.__m_NewName, self.__m_PrevName = self.__m_refNEScene.Rename_Operation( self.__m_ObjectID, self.__m_NewName )# update self.__m_NewName to actual newname

    def undo( self ):
        print( 'RenameCommand::undo()...' )
        self.__m_refNEScene.Rename_Operation( self.__m_ObjectID, self.__m_PrevName )

    def redo( self ):
        print( 'RenameCommand::redo()...' )
        self.__m_refNEScene.Rename_Operation( self.__m_ObjectID, self.__m_NewName )




class RenameAttributeCommand(CommandBase):

    def __init__( self, neScene, object_id, new_name ):
        super(RenameAttributeCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_ObjectID = object_id
        self.__m_NewName = new_name
        self.__m_PrevName = None


    def execute( self ):
        self.__m_NewName, self.__m_PrevName = self.__m_refNEScene.RenameAttribute_Operation( self.__m_ObjectID, self.__m_NewName )

    def undo( self ):
        print( 'RenameAttributeCommand::undo()...' )
        self.__m_refNEScene.RenameAttribute_Operation( self.__m_ObjectID, self.__m_PrevName )

    def redo( self ):
        print( 'RenameAttributeCommand::redo()...' )
        self.__m_refNEScene.RenameAttribute_Operation( self.__m_ObjectID, self.__m_NewName )




class TranslateCommand(CommandBase):

    def __init__( self, neScene, object_id, new_pos, relative ):
        super(TranslateCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_ObjectID = object_id
        self.__m_NewPos = new_pos
        self.__m_Translation = None
        self.__m_Relative = relative


    def execute( self ):
        self.__m_Translation = self.__m_refNEScene.Translate_Operation( self.__m_ObjectID, self.__m_NewPos, self.__m_Relative )

    def undo( self ):
        print( 'TranslateCommand::undo()...' )
        self.__m_refNEScene.Translate_Operation( self.__m_ObjectID, (-self.__m_Translation[0], -self.__m_Translation[1]), True )

    def redo( self ):
        print( 'TranslateCommand::redo()...' )
        self.__m_refNEScene.Translate_Operation( self.__m_ObjectID, self.__m_Translation, True )




class SetVisibleCommand(CommandBase):

    def __init__( self, neScene, object_id, state ):
        super(SetVisibleCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_ObjectID = object_id
        self.__m_NewState = state
        self.__m_PrevState = None


    def execute( self ):
        self.__m_PrevState = self.__m_refNEScene.SetVisible_Operation( self.__m_ObjectID, self.__m_NewState )

    def undo( self ):
        print( 'SetVisibleCommand::undo()...' )
        self.__m_refNEScene.SetVisible_Operation( self.__m_ObjectID, self.__m_PrevState )

    def redo( self ):
        print( 'SetVisibleCommand::redo()...' )
        self.__m_refNEScene.SetVisible_Operation( self.__m_ObjectID, self.__m_NewState )




class ParentCommand(CommandBase):

    def __init__( self, neScene, object_id, parent_id ):
        super(ParentCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_ObjectID = object_id
        self.__m_NewParentID = parent_id
        self.__m_PrevParentID = neScene.GetObjectByID(object_id).ParentID()# keep current parentid before parant change


    def execute( self ):
        self.__m_refNEScene.Parent_Operation( self.__m_ObjectID, self.__m_NewParentID )

    def undo( self ):
        print( 'ParentCommand::undo()...' )
        self.__m_refNEScene.Parent_Operation( self.__m_ObjectID, self.__m_PrevParentID )

    def redo( self ):
        print( 'ParentCommand::redo()...' )
        self.__m_refNEScene.Parent_Operation( self.__m_ObjectID, self.__m_NewParentID )



class CreateSymbolicLinkCommand(CommandBase):

    def __init__( self, neScene, group_id, attribdesc, value, name, symboliclink_idset, slot_index ):
        super(CreateSymbolicLinkCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = None
        
        self.__m_GroupID = group_id
        self.__m_AttribDesc = attribdesc
        self.__m_Value = value
        self.__m_Name = name
        self.__m_ObjectIDSet = symboliclink_idset
        self.__m_SlotIndex = slot_index


    def execute( self ):
        self.__m_Snapshot = self.__m_refNEScene.CreateSymbolicLink_Operation( self.__m_GroupID, self.__m_AttribDesc, self.__m_Value, self.__m_Name, self.__m_ObjectIDSet, self.__m_SlotIndex ).GetSnapshot()
        
    def undo( self ):
        print( 'CreateSymbolicLinkCommand::undo()...' )
        self.__m_refNEScene.RemoveSymbolicLink_Operation( self.__m_Snapshot.ObjectID() )

    def redo( self ):
        print( 'CreateSymbolicLinkCommand::redo()...' )
        self.__m_refNEScene.CreateSymbolicLink_Operation( self.__m_Snapshot.GroupID(), self.__m_Snapshot.AttribDesc(), self.__m_Snapshot.Value(), self.__m_Snapshot.Key(), self.__m_Snapshot.ObjectIDSet(), self.__m_Snapshot.SlotIntex() )




class RemoveSymbolicLinkCommand(CommandBase):

    def __init__( self, neScene, object_id ):
        super(RemoveSymbolicLinkCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = neScene.GetSnapshot( object_id )


    def execute( self ):
        self.__m_refNEScene.RemoveSymbolicLink_Operation( self.__m_Snapshot.ObjectID() )
    
    def undo( self ):
        print( 'RemoveSymbolicLinkCommand::undo()...' )
        # restore symboliclink
        self.__m_refNEScene.CreateSymbolicLink_Operation( self.__m_Snapshot.GroupID(), self.__m_Snapshot.AttribDesc(), self.__m_Snapshot.Value(), self.__m_Snapshot.Key(), self.__m_Snapshot.ObjectIDSet(), self.__m_Snapshot.SlotIntex() )
        # restore attribute values and lock-states
        for attribArg in self.__m_Snapshot.AttribArgs():
            self.__m_refNEScene.SetAttribute_Operation( (attribArg[0], attribArg[1]), attribArg[2] )
            self.__m_refNEScene.LockAttribute_Operation( (attribArg[0], attribArg[1]), attribArg[3] )
 
    def redo( self ):
        print( 'RemoveSymbolicLinkCommand::redo()...' )
        self.__m_refNEScene.RemoveSymbolicLink_Operation( self.__m_Snapshot.ObjectID() )




class SetSymbolicLinkSlotIndexCommand(CommandBase):

    def __init__( self, neScene, object_id, slot_index ):
        super(SetSymbolicLinkSlotIndexCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_ObjectID = object_id
        self.__m_NewValue = slot_index
        self.__m_PrevValue = None


    def execute( self ):
        self.__m_PrevValue = self.__m_refNEScene.SetSymbolicLinkSlotIndex_Operation( self.__m_ObjectID, self.__m_NewValue )

    def undo( self ):
        print( 'SetSymbolicLinkSlotIndexCommand::undo()...' )
        self.__m_refNEScene.SetSymbolicLinkSlotIndex_Operation( self.__m_ObjectID, self.__m_PrevValue )

    def redo( self ):
        print( 'SetSymbolicLinkSlotIndexCommand::redo()...' )
        self.__m_refNEScene.SetSymbolicLinkSlotIndex_Operation( self.__m_ObjectID, self.__m_NewValue )




class CreateGroupIOCommand(CommandBase):

    def __init__( self, neScene, dataflow, pos, object_id, parent_id ):
        super(CreateGroupIOCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = None
        self.__m_Position = pos
        self.__m_DataFlow = dataflow
        self.__m_ParentID = parent_id# ParentGroupID
        self.__m_ObjectID = object_id


    def execute( self ):
        self.__m_Snapshot = self.__m_refNEScene.CreateGroupIO_Operation( self.__m_DataFlow, self.__m_Position, self.__m_ObjectID, self.__m_ParentID ).GetSnapshot()

    def undo( self ):
        print( 'CreateGroupIOCommand::undo()...' )
        self.__m_refNEScene.RemoveGroupIO_Operation( self.__m_Snapshot.ObjectID() )
 
    def redo( self ):
        print( 'CreateGroupIOCommand::redo()...' )
        self.__m_refNEScene.CreateGroupIO_Operation( self.__m_Snapshot.DataFlow(), self.__m_Snapshot.Translation(), self.__m_Snapshot.ObjectID(), self.__m_Snapshot.ParentID()  )




class RemoveGroupIOCommand(CommandBase):

    def __init__( self, neScene, object_id ):
        super(RemoveGroupIOCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = neScene.GetSnapshot( object_id )


    def execute( self ):
        self.__m_refNEScene.RemoveGroupIO_Operation( self.__m_Snapshot.ObjectID() )
    
    def undo( self ):
        print( 'RemoveGroupIOCommand::undo()...' )
        self.__m_refNEScene.CreateGroupIO_Operation( self.__m_Snapshot.DataFlow(), self.__m_Snapshot.Translation(), self.__m_Snapshot.ObjectID(), self.__m_Snapshot.ParentID() )

    def redo( self ):
        print( 'RemoveGroupIOCommand::redo()...' )
        self.__m_refNEScene.RemoveGroupIO_Operation( self.__m_Snapshot.ObjectID() )




class SelectCommand():

    def __init__( self, neScene, object_ids, option ):
        super(SelectCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_ObjectIDs = object_ids
        self.__m_Option = option


    def execute( self ):
        self.__m_refNEScene.Select_Operation( self.__m_ObjectIDs, self.__m_Option )
    
    def undo( self ):
        print( 'SelectCommand::undo()...' )
        self.__m_refNEScene.Select_Operation( [], {'clear':True} )

    def redo( self ):
        print( 'SelectCommand::redo()...' )
        self.__m_refNEScene.Select_Operation( self.__m_ObjectIDs, self.__m_Option )





class SnapshotCommand():

    def __init__( self ):
        self.__m_ObjectIDs = {}
        self.__m_Snapshots = []
        self.__m_SelectedObjectIDs = set()



    def Init( self, neScene, obj_id_list ):
        self.Clear()
        
        print('//===================== Initializing Snapshots ===================//' )
        #refObj_list = [ neScene.GetObjectByID( obj_id ) for obj_id in obj_id_list ]
        #print( 'Duplicate', [ obj.FullKey() for obj in refObj_list ] )

        #for refObj in refObj_list:

        #    if( isinstance(refObj, NENodeObject) ):
        #        self.__CollectCreateNodeArgs(refObj)

        #    elif( isinstance(refObj, NEGroupObject) ):
        #        self.__CollectGroupArgs(refObj)

        #    self.__m_SelectedObjectIDs.add( refObj.ID() )

        #self.__CollectConnectArgs( refObj_list )


################################################################################################################

        print('//===================== Initializing Snapshots(new version) ===================//' )
        snapshot_gen_list, descendants = neScene.NodeGraph().PrepareSnapshot( obj_id_list )
        refObj_list = [ neScene.GetObjectByID( obj_id ) for obj_id in snapshot_gen_list ]

        for refObj in refObj_list:
        #for obj_id in snapshot_gen_list:
            #refObj = neScene.GetObjectByID( obj_id )

            if( isinstance(refObj, NENodeObject) ):
                self.__CollectCreateNodeArgs(refObj)

            elif( isinstance(refObj, NEGroupObject) ):
                if( not descendants[ refObj.ID() ] ): # Include all children if NEGroupObject is leaf
                    self.__CollectGroupArgsRecursive( refObj )
                else:
                    self.__CollectCreateGroupArgs( refObj )
                    self.__CollectParentingSnapshots( refObj, descendants[ refObj.ID() ] )

            self.__m_SelectedObjectIDs.add( refObj.ID() )

        self.__CollectConnectArgs( refObj_list, descendants )

################################################################################################################



    def Release( self ):
        self.Clear()



    def Clear( self ):
        self.__m_ObjectIDs.clear()
        self.__m_Snapshots.clear()
        self.__m_SelectedObjectIDs.clear()



    def PublishObjectIDs( self ):
        for k in self.__m_ObjectIDs.keys():
            self.__m_ObjectIDs[k] = uuid.uuid1()

        return self.__m_ObjectIDs



    def Snapshots( self ):
        return self.__m_Snapshots



    def SellectedIDs( self ):
        return self.__m_SelectedObjectIDs



    def __CollectCreateNodeArgs( self, refObj ):

        # Reserve ObjectID space for node
        self.__m_ObjectIDs[refObj.ID()] = None

        # Reserve ObjectID space for attributes
        for attrib in refObj.Attributes().values():
            self.__m_ObjectIDs[attrib.ID()] = None

        print( 'Append Node Snapshot...%s' % refObj.FullKey() )
        self.__m_Snapshots.append( refObj.GetSnapshot() )# append NENodeSnapshot



    def __CollectConnectArgs( self, refObjs, descendants ):

        # 選択オブジェクト群に従属する全てのノード/グループをリスト化する
        # リスト内で閉じたコネクションを全て抽出する
        obj_list = []

        for refObj in refObjs:
            self.__CollectChildrenForConnectArgs( refObj, obj_list, descendants )
        
        for obj in set(obj_list):# setしてlist内オブジェクトの重複をなくす
            for dest_attrib in obj.InputAttributes().values():
                for conn in dest_attrib.Connections().values():
                    if( conn.Source().Parent() in obj_list ):
                        self.__m_ObjectIDs[conn.ID()] = None
                        print( 'Append Connect Snapshot...%s' % conn.FullKey() )
                        self.__m_Snapshots.append( conn.GetSnapshot() )# append NEConnectionSnapshot


    
    def __CollectChildrenForConnectArgs( self, node, obj_list, descendants ):

        nodes_to_visit = [node]

        while( nodes_to_visit ):
            # pop currentnode from nodes_to_visit
            currentnode = nodes_to_visit.pop()

            # append children of cuddentnode to nodes_to_visit
            if( not descendants[ currentnode.ID() ] ):  # if no descendants specified(leaf group), append all children to nodes_to_visit
                for obj in currentnode.Children().values():
                    nodes_to_visit.append(obj)
            else:                                       # else append specified descendants to nodes_to_visit 
                for obj in currentnode.Children().values():
                    if( obj.ID() in descendants[ currentnode.ID() ] ):
                        nodes_to_visit.append(obj)
        
            if( isinstance(currentnode, NENodeObject) ):
                obj_list.append( currentnode )

            elif( isinstance(currentnode, NEGroupObject) ):
                for groupio in currentnode.GroupIOs():
                    obj_list += list( groupio.SymbolicLinks().values() )

        nodes_to_visit.clear()



    # Snapshot generation method for single NEGroupSnapshot. Does not deal with descendants.
    def __CollectCreateGroupArgs( self, refObj ):
        # Reserve ObjectID slot for NEGroupObject
        self.__m_ObjectIDs[refObj.ID()] = None

        # Append NEGroupSnapshot.
        print( 'Append Group Snapshot...%s' % refObj.Key() )
        self.__m_Snapshots.append( refObj.GetSnapshot() )# append NEGroupSnapshot

        # Append ObjectID slots for NEGroupIOObjects
        self.__m_ObjectIDs[ refObj.GroupInput().ID() ] = None# Input GroupIO
        self.__m_ObjectIDs[ refObj.GroupOutput().ID() ] = None# Output GroupIO
        print( 'Append GroupIn Snapshot...%s' % refObj.GroupInput().Key() )
        self.__m_Snapshots.append( refObj.GroupInput().GetSnapshot() )# append GroupIn's snapshot
        print( 'Append GroupOut Snapshot...%s' % refObj.GroupOutput().Key() )
        self.__m_Snapshots.append( refObj.GroupOutput().GetSnapshot() )# append GroupOut's snapshot

        # Append NESymbolicLinkSnapshot.
        for groupio in refObj.GroupIOs():
            for idx in range( groupio.NumSymbolicLinks() ):
                symboliclink = groupio.SymbolicLink(idx)
                id_set = symboliclink.IDSet()
                # Reserve ObjectID slots for symboliclink and input/output attributes.
                self.__m_ObjectIDs[id_set[0]] = None# symboliclink id
                self.__m_ObjectIDs[id_set[1]] = None# input attrib id
                self.__m_ObjectIDs[id_set[2]] = None# output attrib id
                print( 'Append SymbolicLink Snapshot...%s' % symboliclink.Key() )
                self.__m_Snapshots.append( symboliclink.GetSnapshot() )# snapshot_list.append( symboliclink.GetSnapshot() )# append NESymbolicLinkSnapshot



    def __CollectGroupArgsRecursive( self, refObj ):
        
        # Descend to child first
        for child in refObj.Children().values():
            self.__CollectGroupArgsRecursive( child )

        # Append snapshot after reaching leaf node.
        if( isinstance(refObj, NENodeObject) ):
            self.__CollectCreateNodeArgs( refObj )

        elif( isinstance(refObj, NEGroupObject) ):
            self.__CollectCreateGroupArgs( refObj )
            self.__CollectParentingSnapshots( refObj, refObj.ChildrenID() )



    def __CollectParentingSnapshots( self, refObj, descendant_ids ):
        children = [ child for child in refObj.Children().values() if child.ID() in descendant_ids ]
        print( 'Append Parent Snapshot...' )
        for child in children: print( '    %s' % child.FullKey() )
        self.__m_Snapshots.append( NEParentSnapshot( refObj.ID(), children ) )# append GroupOut's snapshot



    def ExportCommand( self, filepath ):

        #if( self.__m_Snapshots ):
        F = open( filepath, 'wb' )
        pickle.dump(self, F)

        F.close()
