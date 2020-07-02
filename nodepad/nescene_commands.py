import pickle
import uuid

from .history.commandbase import CommandBase


from .graph.neconnectionobject import NEConnectionSnapshot
from .graph.nenodeobject import NENodeObject, NENodeSnapshot
from .graph.negroupobject import NEGroupObject, NEGroupSnapshot
from .graph.nesymboliclink import NESymbolicLinkSnapshot
from .graph.negroupioobject import NEGroupIOSnapshot

#from .nescene import NEScene
from .nescene_ext import NESceneExt


#========================== Commands ===================================#



########################### TODO: カスタムコードノードの操作コマンド試験実装. #####################################

# TODO: Register CustomNode creation procedure at GraphicsScene::contextMenuEvent.
# TODO: Implement NESceneManager::CreateCustomNode_Exec.
# TODO: Implement NESceneManager::RemoveCustomNodeByID_Exec.
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
        self.__m_refNEScene.CreateCustomNode_Operation( self.__m_Snapshot.ObjectType(), self.__m_Snapshot.Translation(), self.__m_Snapshot.Key(), self.__m_Snapshot.ObjectID(), self.__m_Snapshot.ParentID(), self.__m_Snapshot.ActiveAttribIDs() )
        for attribName in self.__m_Snapshot.AttribNames():
            self.__m_refNEScene.RenameAttribute_Operation( (attribName[0], attribName[1]), attribName[2] )
        for attribArg in self.__m_Snapshot.AttribArgs():
            self.__m_refNEScene.SetAttribute_Operation( (attribArg[0], attribArg[1]), attribArg[2] )

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
        self.__m_refNEScene.CreateNode_Operation( self.__m_Snapshot.ObjectType(), self.__m_Snapshot.Translation(), self.__m_Snapshot.Size(), self.__m_Snapshot.Key(), self.__m_Snapshot.ObjectID(), self.__m_Snapshot.ParentID(), self.__m_Snapshot.ActiveAttribIDs() )
        for attribName in self.__m_Snapshot.AttribNames():
            self.__m_refNEScene.RenameAttribute_Operation( (attribName[0], attribName[1]), attribName[2] )
        for attribArg in self.__m_Snapshot.AttribArgs():
            self.__m_refNEScene.SetAttribute_Operation( (attribArg[0], attribArg[1]), attribArg[2] )

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



class ReconnectCommand(CommandBase):

    def __init__( self, neScene, object_id, attrib_ids ):
        super(ReconnectCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = neScene.GetSnapshot( object_id )# keep before-reconnection state for undo

        self.__m_NewAttribIDs = attrib_ids


    def execute( self ):
        self.__m_refNEScene.Reconnect_Operation( self.__m_Snapshot.ObjectID(), self.__m_NewAttribIDs[0], self.__m_NewAttribIDs[1] )

    def undo( self ):
        print( 'ReconnectCommand::undo()...' )
        self.__m_refNEScene.Reconnect_Operation( self.__m_Snapshot.ObjectID(), self.__m_Snapshot.SourceAttribID(), self.__m_Snapshot.DestinationAttribID() )

    def redo( self ):
        print( 'ReconnectCommand::redo()...' )
        self.__m_refNEScene.Reconnect_Operation( self.__m_Snapshot.ObjectID(), self.__m_NewAttribIDs[0], self.__m_NewAttribIDs[1] )




# TODO: グループノード作成と、ノードの親グループ変更を別コマンドに分離できるか検討する.
class GroupCommand(CommandBase):

    def __init__( self, neScene, obj_id_list, pos, size, name, parent_id, object_id ):
        super(GroupCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = None
        self.__m_Position = pos
        self.__m_Size = size
        self.__m_Name = name
        self.__m_ParentID = parent_id
        self.__m_ObjectID = object_id
        self.__m_GroupMembers = obj_id_list


    def execute( self ):
        self.__m_Snapshot = self.__m_refNEScene.Group_Operation( self.__m_GroupMembers, self.__m_Position, self.__m_Size, self.__m_Name, self.__m_ObjectID, self.__m_ParentID ).GetSnapshot()

    def undo( self ):
        print( 'GroupCommand::undo()...' )
        self.__m_refNEScene.Ungroup_Operation( self.__m_Snapshot.ObjectID() )

    def redo( self ):
        print( 'GroupCommand::redo()...' )
        self.__m_refNEScene.Group_Operation( self.__m_Snapshot.MemberIDs(), self.__m_Snapshot.Translation(), self.__m_Snapshot.Size(), self.__m_Snapshot.Key(), self.__m_Snapshot.ObjectID(), self.__m_Snapshot.ParentID() )



class UngroupCommand(CommandBase):

    def __init__( self, neScene, object_id ):
        super(UngroupCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_Snapshot = neScene.GetSnapshot( object_id )


    def execute( self ):
        self.__m_refNEScene.Ungroup_Operation( self.__m_Snapshot.ObjectID() )

    def undo( self ):
        print( 'UngroupCommand::undo()...' )
        self.__m_refNEScene.Group_Operation( self.__m_Snapshot.MemberIDs(), self.__m_Snapshot.Translation(), self.__m_Snapshot.Size(), self.__m_Snapshot.Key(), self.__m_Snapshot.ObjectID(), self.__m_Snapshot.ParentID() )

    def redo( self ):
        print( 'UngroupCommand::redo()...' )
        self.__m_refNEScene.Ungroup_Operation( self.__m_Snapshot.ObjectID() )



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

    def __init__( self, neScene, attrib_id, state ):
        super(LockAttributeCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_ObjectID = attrib_id
        self.__m_NewState = state
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
        self.__m_NewName, self.__m_PrevName = self.__m_refNEScene.Rename_Operation( self.__m_ObjectID, self.__m_NewName )

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

    def __init__( self, neScene, object_id, flag ):
        super(SetVisibleCommand, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_ObjectID = object_id
        self.__m_NewState = flag
        self.__m_PrevState = None


    def execute( self ):
        self.__m_PrevState = self.__m_refNEScene.SetVisible_Operation( self.__m_ObjectID, self.__m_NewState )

    def undo( self ):
        print( 'SetVisibleCommand::undo()...' )
        self.__m_refNEScene.SetVisible_Operation( self.__m_ObjectID, self.__m_PrevState )

    def redo( self ):
        print( 'SetVisibleCommand::redo()...' )
        self.__m_refNEScene.SetVisible_Operation( self.__m_ObjectID, self.__m_NewState )


# TODO: ParentByID_Exec(現在未使用)と併せて設計実装予定.
#class ParentCommand(CommandBase):

#    def __init__( self, neScene, object_id, parent_id ):
#        super(ParentCommand, self).__init__()

#        self.__m_refNEScene = neScene
#        self.__m_ObjectID = object_id
#        self.__m_NewParentID = parent_id
#        self.__m_PrevParentID = neScene.GetObjectByID(object_id).ParentID()# keep current parentid before parant change


#    def execute( self ):
#        self.__m_PrevParentID = self.__m_refNEScene.Parent_Operation( self.__m_ObjectID, self.__m_NewParentID )

#    def undo( self ):
#        print( 'ParentCommand::undo()...' )
#        self.__m_refNEScene.Parent_Operation( self.__m_ObjectID, self.__m_PrevParentID )

#    def redo( self ):
#        print( 'ParentCommand::redo()...' )
#        self.__m_refNEScene.Parent_Operation( self.__m_ObjectID, self.__m_NewParentID )



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
        self.__m_refNEScene.CreateSymbolicLink_Operation( self.__m_Snapshot.GroupID(), self.__m_Snapshot.AttribDesc(), self.__m_Snapshot.Value(), self.__m_Snapshot.Key(), self.__m_Snapshot.ObjectIDSet(), self.__m_Snapshot.SlotIntex() )
        for attribArg in self.__m_Snapshot.AttribArgs():
            self.__m_refNEScene.SetAttribute_Operation( (attribArg[0], attribArg[1]), attribArg[2] )
 
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



# TODO: 複数オブジェクトの一括選択機能にした方がいいか検討する.
#class SelectCommand():

#    def __init__( self, neScene, object_id ):
#        super(SelectCommand, self).__init__()

#        self.__m_refNEScene = neScene
#        self.__m_ObjectID = object_id


#    def execute( self ):
#        self.__m_refNEScene.Select_Operation( self.__m_ObjectID )
    
#    def undo( self ):
#        print( 'SelectCommand::undo()...' )
#        self.__m_refNEScene.Select_Operation( None )

#    def redo( self ):
#        print( 'SelectCommand::redo()...' )
#        self.__m_refNEScene.Select_Operation( self.__m_ObjectID )




class SelectCommand_Multi():

    def __init__( self, neScene, object_ids, option ):
        super(SelectCommand_Multi, self).__init__()

        self.__m_refNEScene = neScene
        self.__m_ObjectIDs = object_ids
        self.__m_Option = option


    def execute( self ):
        self.__m_refNEScene.Select_Operation_Multi( self.__m_ObjectIDs, self.__m_Option )
    
    def undo( self ):
        print( 'SelectCommand_Multi::undo()...' )
        self.__m_refNEScene.Select_Operation_Multi( [], {'clear':True} )

    def redo( self ):
        print( 'SelectCommand_Multi::redo()...' )
        self.__m_refNEScene.Select_Operation_Multi( self.__m_ObjectIDs, self.__m_Option )




# TODO: 複数グループを跨いで選択したノード群をどうやってスナップショット化するか考える.

class SnapshotCommand():

    def __init__( self ):
        self.__m_ObjectIDs = {}
        self.__m_Snapshots = []
        self.__m_SelectedObjectIDs = set()



    def Init( self, neScene, obj_id_list ):
        self.Clear()
        
        print('//===================== Initializing Snapshots ===================//' )
# TODO: 同一オブジェクトの重複選択を消す必要あるかも.( 例えばコネクション: 直接選択 + ノード接続からの自動検出 )
        refObj_list = [ neScene.GetObjectByID( obj_id ) for obj_id in obj_id_list ]
        #print( 'Duplicate', [ obj.FullKey() for obj in refObj_list ] )

        for refObj in refObj_list:
            if( isinstance(refObj, NENodeObject) ):
                self.__CollectCreateNodeArgs(refObj)
            elif( isinstance(refObj, NEGroupObject) ):
                self.__CollectGroupArgs(refObj)
            self.__m_SelectedObjectIDs.add( refObj.ID() )

        self.__CollectConnectArgs( refObj_list )


        for ss in self.__m_Snapshots:
            print( ss )


################################################################################################################
# TODO: 複数親空間を跨ぐノード群選択時のスナップショット収集コード. 2020.01.30

        print('//===================== Initializing Snapshots(new version) ===================//' )
        snapshot_gen_list, descendants = neScene.NodeGraph().PrepareSnapshot( obj_id_list )
        
        for obj_id in snapshot_gen_list:
            
            refObj = neScene.GetObjectByID( obj_id )

            if( isinstance(refObj, NENodeObject) ):
                print( 'CreateNodeByID_Exec()...%s' % refObj.Key() )
                #self.__CollectCreateNodeArgs(refObj)
            elif( isinstance(refObj, NEGroupObject) ):
                print( 'CreateGroupByID_Exec()...%s' % refObj.Key() )
                #self.__CollectGroupArgs(refObj)
                for child_id in descendants[ obj_id ]:
                    refChild = neScene.GetObjectByID( child_id )
                    print( '        ParentByID_Exec()...%s' % refChild.Key() )

            #self.__m_SelectedObjectIDs.add( obj_id )


        #self.__CollectConnectArgs( refObj_list )

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

        print( 'CreateNodeByID_Exec()...%s' % refObj.Key() )
        self.__m_Snapshots.append( refObj.GetSnapshot() )# append NENodeSnapshot



    def __CollectConnectArgs( self, refObjs ):

        # 選択オブジェクト群に従属する全てのノード/グループをリスト化する
        # リスト内で閉じたコネクションを全て抽出する
        obj_list = []

        for refObj in refObjs:
            self.__CollectChildrenForConnectArgs( refObj, obj_list )
        
        for obj in set(obj_list):# setしてlist内オブジェクトの重複をなくす
            for dest_attrib in obj.InputAttributes().values():
                for conn in dest_attrib.Connections().values():
                    if( conn.Source().Parent() in obj_list ):
                        self.__m_ObjectIDs[conn.ID()] = None
                        print( 'ConnecteateByID_Exec()...%s' % conn.Key() )
                        self.__m_Snapshots.append( conn.GetSnapshot() )# append NEConnectionSnapshot


    
    def __CollectChildrenForConnectArgs( self, node, obj_list ):

        nodes_to_visit = [node]

        while( nodes_to_visit ):
            currentnode = nodes_to_visit.pop()
            for obj in currentnode.Children().values():
                nodes_to_visit.append(obj)
        
            if( isinstance(currentnode, NENodeObject) ):
                obj_list.append( currentnode )
            elif( isinstance(currentnode, NEGroupObject) ):
                for groupio in currentnode.GroupIOs():
                    obj_list += list( groupio.SymbolicLinks().values() )

        nodes_to_visit.clear()



    def __CollectGroupArgs( self, refObj ):
        
        snapshot_list = []
        self.__ConstructSnapshotTree( refObj, snapshot_list )
        self.__m_Snapshots += snapshot_list



    def __ConstructSnapshotTree( self, obj, snapshot_list ):
        
        for child in obj.Children().values():
            self.__ConstructSnapshotTree( child, snapshot_list )

        # Reserve ObjectID slots
        self.__m_ObjectIDs[obj.ID()] = None

        if( isinstance(obj, NENodeObject) ):
# TODO: __CollectCreateNodeArgsに置き換える.

            # Reserve ObjectID space for attributes
            for attrib in obj.Attributes().values():
                self.__m_ObjectIDs[attrib.ID()] = None
            # Append snapshot
            print( 'CreateNodeByID_Exec()...%s' % obj.Key() )
            snapshot_list.append( obj.GetSnapshot() )# append NENodeSnapshot

        elif( isinstance(obj, NEGroupObject) ):
# TODO: __CollectCreateGroupArgs関数を定義してまとめる.

            # Append NEGroupSnapshot first.
            print( 'CreateCroupByID_Exec()...%s' % obj.Key() )
            snapshot_list.append( obj.GetSnapshot() )# append NEGroupSnapshot

            # Append NEGroupIOSnapshot for reoroducing GroupIO's position.
            self.__m_ObjectIDs[ obj.GroupInput().ID() ] = None# symboliclink id
            self.__m_ObjectIDs[ obj.GroupOutput().ID() ] = None# input attrib id
            print( 'CreateGroupIOByID_Exec()...%s' % obj.GroupInput().Key() )
            snapshot_list.append( obj.GroupInput().GetSnapshot() )# append NEGroupIOSnapshot
            print( 'CreateGroupIOByID_Exec()...%s' % obj.GroupOutput().Key() )
            snapshot_list.append( obj.GroupOutput().GetSnapshot() )# append NEGroupIOSnapshot

            # Reserve ObjectID slots for symbolic links, and append NESymbolicLinkSnapshot.
            for groupio in obj.GroupIOs():
                for idx in range( groupio.NumSymbolicLinks() ):
                    symboliclink = groupio.SymbolicLink(idx)
                    id_set = symboliclink.IDSet()
                    self.__m_ObjectIDs[id_set[0]] = None# symboliclink id
                    self.__m_ObjectIDs[id_set[1]] = None# input attrib id
                    self.__m_ObjectIDs[id_set[2]] = None# output attrib id
                    print( 'CreateSymbolicLinkByID_Exec()...%s' % symboliclink.Key() )
                    snapshot_list.append( symboliclink.GetSnapshot() )# append NESymbolicLinkSnapshot

                

    def ExportCommand( self, filepath ):

        #if( self.__m_Snapshots ):
        F = open( filepath, 'wb' )
        pickle.dump(self, F)

        F.close()
