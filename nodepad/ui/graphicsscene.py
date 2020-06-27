import functools
import traceback

from ..component.descriptors import *

from .graphicssettings import *
from .graphicsitemlayer import GraphicsItemLayer
from .edgeitem import Edge, TemporaryEdge
from .portitem import Port
from .nodeitem import Node
from .symboliclinkitem import SymbolicLink
from .groupitem import Group
from .groupioitem import GroupIO
from .pushbuttonitem import PushButton


class GraphicsScene(QGraphicsScene):

    def __init__(self, root_id, nodetypemanager, parent=None):
        super(GraphicsScene, self).__init__(parent)
        
        self.setSceneRect(-400, -400, 800, 800)
        self.setItemIndexMethod( QGraphicsScene.NoIndex )

        self.selectionChanged.connect( self.__SelectionChangedSlot )


        self.__m_MouseStartPos = QPointF()
        self.__m_GraphicsItems = {} # key: uuid, val: Node/Group/Edge/SymbolicLink, etc...
        
        self.__m_RootLayerID = root_id
        self.__m_FocusViewID = root_id
        self.__m_RenderViewLayerID = root_id# 

        self.__m_GraphicsViewLayers = {}# key: QGraphicsView's id, value: GraphicsItemLayer object
        self.__m_GraphicsViewLayers[ root_id ] = GraphicsItemLayer( root_id )
        
        self.__m_TempEdge = None
        self.__m_refGroupIO = None
        self.__m_refStartPort = None        

        self.__m_refCallbackFunc = None
        self.__m_refNodeTypeManager = nodetypemanager

        self.__m_TranslateProhibitedTypes = [ Edge, SymbolicLink ]


        self.__m_MouseDragMode = MouseMode.DoNothing




    def Init( self, root_id ):
        print( 'GraphicsScene::Init()...' )

        self.clearSelection()
        self.clear()
        self.__m_GraphicsItems.clear()
        self.__m_GraphicsViewLayers.clear()
        self.__m_FocusViewID = root_id
        self.__m_RenderViewLayerID = root_id
        self.__m_GraphicsViewLayers[ root_id ] = GraphicsItemLayer( root_id )


    def Release( self ): 
        print( 'GraphicsScene::Release()...' )

        self.selectionChanged.disconnect( self.__SelectionChangedSlot )

        self.clearSelection()
        self.clear()
        self.__m_GraphicsItems.clear()
        self.__m_GraphicsViewLayers.clear()
        self.__m_FocusViewID = None
        self.__m_RenderViewLayerID = None

        self.__m_refCallbackFunc = None
        self.__m_refNodeTypeManager = None


    def IsVisibleFromActiveView( self, item ):
        try:
            return self.__m_GraphicsViewLayers[ self.__m_RenderViewLayerID ].HasItem( item.ID() )
        except:
            return False



    #====================== Setup ==========================#

    def BindCallbackFunc( self, func ):
        self.__m_refCallbackFunc = func


    def UnbindCallbackFunc( self ):
        self.__m_refCallbackFunc = None


    def SetFocusViewID( self, view_id ):
        self.__m_FocusViewID = view_id


    def FocusViewID( self ):
        return self.__m_FocusViewID


    def SetRenderViewID( self, view_id ):
        self.__m_RenderViewLayerID = view_id


    def RemoveGraphicsViewLayer( self, layer_id ):
        try:
            del self.__m_GraphicsViewLayers[ layer_id ]# layer_idはルートオブジェクトのID
        except:
            return


    #=============== Command functions ================#
    def ExecCommand_( self, *args, **kwargs ):
        self.__m_refCallbackFunc( *args, **kwargs )


    def CreateNode_Exec( self, node_name, node_id, nodeDesc, pos, parent_id ):
        try:
            node = Node( node_name, node_id, nodeDesc )
            self.addItem(node)
            self.__m_GraphicsItems[ node_id ] = node


            # Create Input Port GraphicsItems and add to node
            for desc in nodeDesc.InputAttribDescs():
                port = Port( desc.Name(), desc.ObjectID(), desc.DataFlow() )
                node.AddPort( port )

            # Create Output Port GraphicsItems and add to node
            for desc in nodeDesc.OutputAttribDescs():
                port = Port( desc.Name(), desc.ObjectID(), desc.DataFlow() )
                node.AddPort( port )

            # Add to EditableLayer
            self.__m_GraphicsViewLayers[ parent_id ].AddItem( node )
            node.setPos( pos[0], pos[1] )

        except:
            traceback.print_exc()


    def RemoveNode_Exec( self, node_id ):
        try:
            node = self.__m_GraphicsItems[ node_id ]

            # Remove from EditableLayer
            self.__m_GraphicsViewLayers[ node.LayerID() ].RemoveItem( node_id )

            # Remove from GraphicsScene
            self.removeItem( self.__m_GraphicsItems[ node_id ] )
            del self.__m_GraphicsItems[ node_id ]

        except:
            traceback.print_exc()


    def Connect_Exec( self, conn_name, conn_id, source_id, dest_id, parent_id ):
        try:
            source_port = self.__m_GraphicsItems[ source_id[0] ].OutputPort( source_id[1] )
            dest_port = self.__m_GraphicsItems[ dest_id[0] ].InputPort( dest_id[1] )

            # create edge object
            edge = Edge( conn_name, conn_id, source_port.scenePos(), dest_port.scenePos() )
            self.__m_GraphicsItems[ conn_id ] = edge

            self.addItem( edge )

            # establish edge-to-port link
            edge.ConnectSourcePort(source_port)
            edge.ConnectDestPort(dest_port)
            edge.UpdatePath()

            # establish port-to-edge link
            source_port.ConnectEdge( edge )
            dest_port.ConnectEdge( edge )

            # Add Edge to EditableLayer
            self.__m_GraphicsViewLayers[ parent_id ].AddItem( edge )

        except:
            traceback.print_exc()
            #print( 'GraphicsScene::Connect_Exec()... Aborting connect operation. could not find attribute.' )


    def Disconnect_Exec( self, edge_id ):
        try:
            edge = self.__m_GraphicsItems[ edge_id ]
            
            # remove edge reference from ports
            if( edge.SourcePort() ):
                edge.SourcePort().DisconnectEdge(edge)

            if( edge.DestinationPort() ):
                edge.DestinationPort().DisconnectEdge(edge)

            # remove port reference from edge
            edge.DisconnectPort()

            # Remove Edge from EditableLayer
            self.__m_GraphicsViewLayers[ edge.LayerID() ].RemoveItem( edge_id )

            # remove from GraphicssScene
            self.removeItem( edge )
            del self.__m_GraphicsItems[ edge.ID() ]

            return True

        except:
            traceback.print_exc()
            return False


    def Reconnect_Exec( self, conn_id, source_id, dest_id, parent_id ):
        try:

            edge = self.__m_GraphicsItems[ conn_id ]
            
            # remove edge reference from ports
            if( edge.SourcePort() ):
                edge.SourcePort().DisconnectEdge(edge)

            if( edge.DestinationPort() ):
                edge.DestinationPort().DisconnectEdge(edge)


            source_port = self.__m_GraphicsItems[ source_id[0] ].OutputPort( source_id[1] )
            dest_port = self.__m_GraphicsItems[ dest_id[0] ].InputPort( dest_id[1] )

            # establish edge-to-port link
            edge.ConnectSourcePort(source_port)
            edge.ConnectDestPort(dest_port)
            edge.UpdatePath()

            # establish port-to-edge link
            source_port.ConnectEdge( edge )
            dest_port.ConnectEdge( edge )

            # Change Layer
            self.__m_GraphicsViewLayers[ edge.LayerID() ].RemoveItem( edge.ID() )# Remove from curent parent layer
            self.__m_GraphicsViewLayers[ parent_id ].AddItem( edge )# Add to new parent layer

            return True

        except:
            traceback.print_exc()
            return False


    def Rename_Exec( self, obj_id, newname ):
        try:
            obj = self.__m_GraphicsItems[ obj_id ]
            obj.SetName( newname )
            self.update()
            return True
        except:
            traceback.print_exc()
            return False


    def RenameAttribute_Exec( self, attrib_id, newname ):
        try:
            self.__m_GraphicsItems[attrib_id[0]].RenamePort( attrib_id[1], newname )
            self.update()
            return True
        except:
            traceback.print_exc()
            return False


    def CreateGroup_Exec( self, group_name, group_id, pos, parent_id ):
        print( 'GraphicsScene::CreateGroup_Exec' )

        # Create Group
        group = Group( group_name, group_id, functools.partial( self.__m_refCallbackFunc, 'EditGroupByID', group_id, group_name ) )
        self.__m_GraphicsItems[ group_id ] = group
        self.addItem( group )

        # Create new EditableLayer for group children
        self.__m_GraphicsViewLayers[ group_id ] = GraphicsItemLayer( group_id )

        # Add group to EditableLayer
        self.__m_GraphicsViewLayers[ parent_id ].AddItem( group )
        group.setPos( pos[0], pos[1] )

        return True


    def RemoveGroup_Exec( self, group_id ):
        try:
            group = self.__m_GraphicsItems[ group_id ]

            # Remove from EditableLayer
            self.__m_GraphicsViewLayers[ group.LayerID() ].RemoveItem( group_id )

            # Remove from GraphicsScene
            self.removeItem( group )
            del self.__m_GraphicsItems[ group_id ]

        except:
            traceback.print_exc()


    def Translate_Exec( self, object_id, translate, relative ):

        if( object_id in self.__m_GraphicsItems ):
            curr_pos = self.__m_GraphicsItems[ object_id ].scenePos()
            newpos = ( float(relative) * curr_pos.x() + translate[0], float(relative) * curr_pos.y() + translate[1] ) 
            self.__m_GraphicsItems[ object_id ].setPos( newpos[0], newpos[1] )
            return True

        return False
                

    def SetVisible_Exec( self, object_id, flag ):

        if( object_id in self.__m_GraphicsItems ):
            self.__m_GraphicsItems[ object_id ].setVisible(flag)
            return True

        return False


    def Parent_Exec( self, object_id, parent_id ):

        # Remove from current layer
        curr_parent_id = self.__m_GraphicsItems[ object_id ].LayerID()
        self.__m_GraphicsViewLayers[ curr_parent_id ].RemoveItem( object_id )

        # Add to new layer
        self.__m_GraphicsViewLayers[ parent_id ].AddItem( self.__m_GraphicsItems[ object_id ] )
 
        # update scene
        self.update()


    def ActivateSymbolicLink_Exec( self, group_id, name, symboliclinkdesc, slot_index=-1 ):
        try:
            # Create symbolic link
            symboliclink = SymbolicLink( name, symboliclinkdesc, group_id )

            # Add to GraphicsScene
            self.addItem( symboliclink )
            self.__m_GraphicsItems[ symboliclink.ID() ] = symboliclink

            # Add symboliclink to GroupIO
            group = self.__m_GraphicsItems[group_id]
            group_io = group.GroupIO( symboliclink.DataFlow() )
            reserved_slotidx = group_io.NumSymbolicLinks() if slot_index==-1 else slot_index
            group_io.AddItem( symboliclink, reserved_slotidx )

            # Add Symboliclink's exposed attributes to Groupitem and update position
            group.AddSymbolicLink( symboliclink, reserved_slotidx )

            # Add SymbolicLink to EditableLayer
            self.__m_GraphicsViewLayers[ group_id ].AddItem( symboliclink )

            # Add Exposed Port to EditableLayer( specify group's visible layer)
            self.__m_GraphicsViewLayers[ group.LayerID() ].AddItem( symboliclink.ExposedPort() )

            return True

        except:
            traceback.print_exc()
            return False


    def DeactivateSymbolicLink_Exec( self, symboliclink_id ):
        try:
            symboliclink = self.__m_GraphicsItems[ symboliclink_id ]
            group = self.__m_GraphicsItems[ symboliclink.GroupID() ]
            group_io = group.GroupIO( symboliclink.DataFlow() )
            
            # Detach SymbolicLink from GroupIO
            symboliclink.parentItem().RemoveItem( symboliclink )

            # Detach SymbolicLink from Group
            group.RemoveSymbolicLink( symboliclink.ExposedPort().ID() )# symboliclink_id )
                        
            # Remove Exposed Port from EditableLayer
            self.__m_GraphicsViewLayers[ symboliclink.ExposedPort().LayerID() ].RemoveItem( symboliclink.ExposedPort().ID() )    

            # Remove SymbolicLink from EditableLayer
            self.__m_GraphicsViewLayers[ symboliclink.LayerID() ].RemoveItem( symboliclink_id )

            # Remove SymbolicLink from GraphicsScene
            self.removeItem( symboliclink.ExposedPort() )
            self.removeItem( self.__m_GraphicsItems[ symboliclink_id ] )
            del self.__m_GraphicsItems[ symboliclink_id ]

        except:
            traceback.print_exc()


    def SetSymbolicLinkSlotIndex_Exec( self, symboliclink_id, slot_index ):
        try:
            symboliclink = self.__m_GraphicsItems[ symboliclink_id ]
            group = self.__m_GraphicsItems[ symboliclink.GroupID() ]
            groupio = group.GroupIO( symboliclink.DataFlow() )

            groupio.SetIndex( symboliclink.SlotIndex(), slot_index )

            if( symboliclink.IsInputFlow() ):   group.UpdateInputPortPositions()
            elif( symboliclink.IsOutputFlow() ):    group.UpdateOutputPortPositions()

        except:
            traceback.print_exc()


    def CreateGroupIO_Exec( self, name, dataflow, pos, group_id, object_id ):
        try:
            # Create GroupIO
            groupio = GroupIO( name, dataflow, group_id, object_id )
            groupio.setPos( pos[0], pos[1] )
            self.addItem( groupio )
            self.__m_GraphicsItems[ groupio.ID() ] = groupio

            # Add GroupIO to EditableLayer
            self.__m_GraphicsViewLayers[ group_id ].AddItem( groupio )

            # Assing GroupIO to Group
            group = self.__m_GraphicsItems[ group_id ]
            group.BindGroupIO( groupio )

            return True

        except:
            traceback.print_exc()
            return False


    def RemoveGroupIO_Exec( self, object_id ):
        try:
            groupio = self.__m_GraphicsItems[ object_id ]
            group = self.__m_GraphicsItems[ groupio.ParentID() ]

            # Remove from GroupIO from Group
            group.UnbindGroupIO( groupio.DataFlow() )

            # Remove from EditableLayer
            self.__m_GraphicsViewLayers[ groupio.LayerID() ].RemoveItem( object_id )

            # Remove from GraphicsScene
            self.removeItem( self.__m_GraphicsItems[ object_id ] )
            del self.__m_GraphicsItems[ object_id ]

        except:
            traceback.print_exc()


    #================ Scene Edit Functions =================#
    def Group( self ):
        item_id_list = [ item.ID() for item in self.selectedItems() ]
        self.__m_refCallbackFunc( 'GroupByID', item_id_list, parent_id=self.__m_FocusViewID )


    def Ungroup( self ):
        for item in self.selectedItems():
            self.__m_refCallbackFunc( 'UngroupByID', item.ID() )


    def Undo( self ):
        self.__m_refCallbackFunc( 'Undo' )


    def Redo( self ):
        self.__m_refCallbackFunc( 'Redo' )


    def Cut( self ):
        item_id_list = [ item.ID() for item in self.selectedItems() ]
        self.clearSelection()
        self.__m_refCallbackFunc( 'CutByID', item_id_list, parent_id=self.__m_FocusViewID )


    def Copy( self ):
        item_id_list = [ item.ID() for item in self.selectedItems() ]
        self.__m_refCallbackFunc( 'CopyByID', item_id_list, parent_id=None )#, parent_id=self.__m_FocusViewID )
        #TODO: 親空間跨いでのノード複製に対応したいのでparent_id指定を無効化できるか検証中. 2020.01.21

    def Paste( self ):
        self.__m_refCallbackFunc( 'PasteByID', parent_id=self.__m_FocusViewID )


    def Duplicate( self ):
        item_id_list = [ item.ID() for item in self.selectedItems() ]
        self.__m_refCallbackFunc( 'DuplicateByID', item_id_list, parent_id=self.__m_FocusViewID )


    def RemoveSelectedObjects( self ):
        item_id_list = [ item.ID() for item in self.selectedItems() ]
        self.clearSelection()
        self.__m_refCallbackFunc( 'DeleteByID', item_id_list )


    def CheckConnectivity( self, port1_id, port2_id ):
        return self.__m_refCallbackFunc( 'CheckConnectivityByID', port1_id, port2_id )


    def CheckLocked( self, port_id ):
        return self.__m_refCallbackFunc( 'CheckLockedByID', port_id )


    def IsSelected( self, object_id ):
        try:
            return self.__m_GraphicsItems[ object_id ] in self.selectedItems()
        except:
            traceback.print_exc()
            return False



    #def CheckSymbolize( self, port_id ):
    #    return self.__m_refCallbackFunc( 'CheckSymbolizeByID', port_id )

    def CheckSymbolize( self, port, dataflow ):
        if( port.DataFlow() == dataflow ):
            return self.__m_refCallbackFunc( 'CheckSymbolizeByID', port.PortID() )
        return False


    def Import( self, filepath, pos ):
        return self.__m_refCallbackFunc( 'Import', filepath, (pos.x(), pos.y()) )


    def Translate( self ):
        for item in self.selectedItems():
            if( type(item) in self.__m_TranslateProhibitedTypes ): continue
            itemPos = item.scenePos()
            self.__m_refCallbackFunc( 'TranslateByID', item.ID(), (itemPos.x(), itemPos.y()) )


    def GetSelectedObjectIDs( self ):
        return [ item.ID() for item in self.selectedItems() ]


# TODO: 処理をGraphicsSceneの外でやるべきか検討する. 2020.06.17
    def CalcGroupIOOffsets( self, group_id ):
        try:
            grouplayer = self.__m_GraphicsViewLayers[ group_id ]
            rect_group = grouplayer.BoundingRect()
            
            #print( grouplayer.NumItems(), rect_group.width(), rect_group.height() )
            return ( ( rect_group.left() - g_GroupIOWidth*1.5, 0.0 ), ( rect_group.right() + g_GroupIOWidth*0.5, 0.0 ) )

        except:
            traceback.print_exc()
            return ()


# TODO: 指定GraphicsItemだけを選択状態にする. シグナルemitはブロックする.
    def UpdateSelection( self, obj_id_list ):
        try:
            self.blockSignals( True )

            self.clearSelection()

            for obj_id in obj_id_list:
                self.__m_GraphicsItems[ obj_id ].setSelected(True)

            self.blockSignals( False )

        except:
            traceback.print_exc()


    def __SelectionChangedSlot( self ):

        print( 'GraphicScene::__SelectionChangedSlot()...' )
        inclusiveTypes = [ Node, Group, GroupIO ]# SymbolicLinkは外してある. 2020.06.18

        # 何も選択されていない場合はitem_idをNoneにしてコールバック
        if( not self.selectedItems() ):
            #self.__m_refCallbackFunc( 'SelectByID', None )
            self.__m_refCallbackFunc( 'SelectByID_Multi', [], {'clear':True} )
            return

        # 先頭オブジェクトだけを選択処理する
        #self.__m_refCallbackFunc( 'SelectByID', item.ID() )
        self.__m_refCallbackFunc( 'SelectByID_Multi', [ item.ID() for item in self.selectedItems() if type(item) in inclusiveTypes ], {'clear':True} )# [ item.ID() for item in self.selectedItems() ]



    # 正しくアサインされたらTrueを、アサインできなかった場合はFalseを返す
    def __AssignSynbolicLinkToGroupIO( self, item, groupio ):

        # データフローが異なる場合も、登録処理を中止
        if( item.DataFlow() != groupio.DataFlow() ):
            return False

        # 既にgroupioがitemを保持している場合は、登録処理を中止
        if( item.parentItem()==groupio ):
            item.parentItem().SnapItem(item )
            self.__m_refCallbackFunc( 'SetSymbolicLinkSlotIndexByID', item.ID(), item.SlotIndex() )
            return True

        if( item.parentItem() ):
            item.parentItem().RemoveItem(item)
        
        groupio.AddItem( item )

        return True


    def contextMenuEvent( self, event ):

        # functool.partial + connect + *argcの組み合わせ専用の関数。argsの最後に挿入されるboolを除いてコールバックする特殊関数
        def callback( *args, **kwargs ):
            return self.__m_refCallbackFunc( *args[:-1], **kwargs )

        if( self.__m_refNodeTypeManager == None ):
            return

        pos = event.scenePos()

        menu = QMenu()
        menu.setStyleSheet( UIStyle.g_MenuStyleSheet )
        # http://stackoverflow.com/questions/8824311/how-to-pass-arguments-to-callback-functions-in-pyqt

        for i in range( self.__m_refNodeTypeManager.NumNodeDescs() ): # refNodeTypeManager.NumNodeDescs() ):

            key = self.__m_refNodeTypeManager.GetNodeDescByIndex(i).ObjectType()# refNodeTypeManager.GetNodeDescByIndex(i).ObjectType()
            action = QAction( key, self )
            #action.triggered.connect( functools.partial(self.CreateNode, nodetype=key, pos=event.scenePos()) ) # OK
            #action.triggered.connect( lambda nodetype=key : self.CreateNode( nodetype, event.scenePos() ) ) # NG
            #menu.addAction( action )
            
            #menu.addAction( key, lambda nodetype=key : self.CreateNode( nodetype, event.scenePos() ) )# OK
            #menu.addAction( key, functools.partial(self.CreateNode, nodetype=key, pos=event.scenePos()) )

            action.triggered.connect( functools.partial( callback, 'CreateNode', key, pos=(pos.x(), pos.y()), size=None, parent_id=self.__m_FocusViewID ) )

            menu.addAction( action )

        #menu.addAction( 'TestNode2', lambda: self.CreateNode( val.Name(), event.scenePos() ) )
        #menu.addAction( 'TestNode', lambda: self.CreateNode( 'TestNode', event.scenePos() ) )
        # http://stackoverflow.com/questions/18428095/qt4-qmenu-addaction-connect-function-with-arguments
        # use "lambda:" for parametrized functions


        menu.exec(event.screenPos())


    def mousePressEvent( self, event ):

        if( event.button() == Qt.RightButton ):
            event.accept()
            return

        item = self.itemAt( event.scenePos(), QTransform() )
        if( isinstance(item, Port) ):
            if( self.CheckLocked( item.PortID() )==False ): # コネクション生成許可されているポートの場合は、破線エッジを描画する
                self.__m_refStartPort = item
                self.__m_TempEdge = TemporaryEdge( item.scenePos() )
                self.addItem(self.__m_TempEdge)
                self.__m_GraphicsViewLayers[ self.__m_FocusViewID ].AddItem( self.__m_TempEdge )
                self.__m_MouseDragMode = MouseMode.DrawEdge
                return

        elif( isinstance(item, SymbolicLink) ):
            self.__m_MouseDragMode = MouseMode.MoveSymbolicLink
            self.__m_refGroupIO = item.parentItem()


        self.__m_MouseStartPos = event.screenPos()

        super(GraphicsScene, self).mousePressEvent( event )


    def mouseMoveEvent( self, event ):
        
        groupio = next( (item for item in self.items(event.scenePos()) if isinstance(item, GroupIO) ), None )

        if( self.__m_MouseDragMode==MouseMode.DrawEdge ):
            scenepos = event.scenePos()
            currPort = self.itemAt( scenepos, QTransform())          

            # Snap TempEdge's endpoint to Port
            if( isinstance(currPort, Port) and currPort != self.__m_refStartPort ):
                if( self.CheckConnectivity( self.__m_refStartPort.PortID(), currPort.PortID() ) == True ):
                    scenepos = currPort.scenePos()

            self.__m_TempEdge.SetDestPosition(scenepos)
            self.__m_TempEdge.UpdatePath()
                        
            # Update GroupIO's blank position
            sourceitem = self.__m_refStartPort.parentItem()
            if( groupio==None and self.__m_refGroupIO==None ):# アトリビュートからエッジを引き出しているが、GroupIOが関与しない場合
                pass
                #print('nothing...')

            elif( self.__m_refGroupIO and groupio==None ):# GroupIOの外部へSynbolicLinkをドラッグしている場合
                #print( 'mouseDownLeaved', self.__m_refGroupIO )
                self.__m_refGroupIO.RemoveBlank()
                
            elif( groupio and self.__m_refGroupIO==None ):# アトリビュートからGroupIOへドラッグしている場合
                #print( 'mouseDownEntered', groupio )
                if( self.CheckSymbolize(self.__m_refStartPort, groupio.DataFlow()) ):
                    groupio.AddBlank( event.scenePos() )

            elif( groupio == self.__m_refGroupIO ):# マウスボタン押した位置と同じGroupIOの場合
                #print( 'mouseDownHover', groupio )
                if( self.CheckSymbolize(self.__m_refStartPort, groupio.DataFlow()) ):
                    groupio.MoveBlank( event.scenePos() )

        elif( self.__m_MouseDragMode==MouseMode.MoveSymbolicLink ):# SymbolicLinkをマウスドラッグする処理だけ抽出

            grabitem = self.mouseGrabberItem()

            if( groupio==None and self.__m_refGroupIO==None ):
                pass
                #print('nothing...')

            elif( self.__m_refGroupIO and groupio==None ):
                #print( 'mouseDownLeaved', self.__m_refGroupIO )
                self.__m_refGroupIO.RemoveBlank()

            elif( groupio and self.__m_refGroupIO==None ):
                #print( 'mouseDownEntered', groupio )
                if( groupio.IsRegistrableSymbolicLink(grabitem) ):
                    groupio.AddBlank( event.scenePos() )

            elif( groupio == self.__m_refGroupIO ):
                #print( 'mouseDownHover', self.__m_refGroupIO )
                if( grabitem in groupio.childItems() ):
                    groupio.MoveItem( grabitem )
                else:
                    if( groupio.IsRegistrableSymbolicLink(grabitem) ):
                        groupio.MoveBlank( grabitem.scenePos() )

        self.__m_refGroupIO = groupio


        super(GraphicsScene, self).mouseMoveEvent(event)


    def mouseReleaseEvent( self, event ):

        item = self.itemAt(event.scenePos(),QTransform())
        grabberitem = self.mouseGrabberItem()

        # アイテム選択状態でマウスドラッグ終了する場合
        mouseMovement = event.screenPos() - self.__m_MouseStartPos
        if( self.selectedItems() and ( mouseMovement.x() or mouseMovement.y() ) ):
            self.Translate()

        if( self.__m_MouseDragMode == MouseMode.DrawEdge ):
            if( isinstance(item, Port) ):# Portの上でマウスボタンリリースした -> Port間にコネクション作成
                self.__m_refCallbackFunc( 'ConnectByID', self.__m_refStartPort.PortID(), item.PortID(), check=True )
            elif( isinstance(item, GroupIO) ):# GroupIO上でリリース -> シンボリックリンク作成
                if( self.CheckSymbolize(self.__m_refStartPort, item.DataFlow()) ):
                    self.__m_refCallbackFunc( 'CreateSymbolicLinkByID', self.__m_refStartPort.PortID(), slot_index=item.BlankIndex() )

            # __m_TempEdgeを削除する
            self.__m_GraphicsViewLayers[ self.__m_FocusViewID ].RemoveItem( self.__m_TempEdge.ID() )
            self.removeItem(self.__m_TempEdge)
            del self.__m_TempEdge
            self.__m_TempEdge = None
            self.__m_refStartPort=None
            
        elif( self.__m_MouseDragMode == MouseMode.MoveSymbolicLink ):
            if( self.__m_refGroupIO ):# 掴んでいたSymbolicLinkを__m_refGroupIOの上で離した場合
                if( self.__AssignSynbolicLinkToGroupIO( grabberitem, self.__m_refGroupIO )==False ):
                    self.__m_MouseDragMode = MouseMode.RemoveSymbolicLink
            else:
                self.__m_MouseDragMode = MouseMode.RemoveSymbolicLink
        

        self.__m_refGroupIO = None
        
        
        super(GraphicsScene, self).mouseReleaseEvent( event )

        # QGraphicsItem削除は、mouseReleaseEventの後で実施する
        if( self.__m_MouseDragMode == MouseMode.RemoveSymbolicLink ):
            self.__m_refCallbackFunc( 'DeleteByID', [ grabberitem.ID() ] )

        self.__m_MouseDragMode = MouseMode.DoNothing



    def keyPressEvent( self, event ):
        
        if( (event.key()==Qt.Key_Z) and (event.modifiers() & Qt.ControlModifier) ):# Undo(Ctrl+Z)
            self.Undo()

        elif( (event.key()==Qt.Key_Y) and (event.modifiers() & Qt.ControlModifier) ):# Undo(Ctrl+Y)
            self.Redo()

        elif( (event.key()==Qt.Key_X) and (event.modifiers() & Qt.ControlModifier) ):# Cut(Ctrl+X)
            self.Cut()

        elif( (event.key()==Qt.Key_C) and (event.modifiers() & Qt.ControlModifier) ):# Copy(Ctrl+C)
            self.Copy()

        elif( (event.key()==Qt.Key_V) and (event.modifiers() & Qt.ControlModifier) ):# Paste(Ctrl+V)
            self.Paste()

        elif( (event.key()==Qt.Key_D) and (event.modifiers() & Qt.ControlModifier) ):# Duplicate(Ctrl+D)
            self.Duplicate()

        if( event.key()==Qt.Key_Delete ):
            self.RemoveSelectedObjects()

        elif( (event.key()==Qt.Key_G) and (event.modifiers() & Qt.ControlModifier) ):# Group(Ctrl+G)
            self.Group()

        elif( (event.key()==Qt.Key_U) and (event.modifiers() & Qt.ControlModifier) ):# Ungroup(Ctrl+U)
            self.Ungroup()

        return super(GraphicsScene, self).keyPressEvent(event)



    def dragEnterEvent( self, event ):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
        return super(GraphicsScene, self).dragEnterEvent(event) 



    def dropEvent( self, event ):
        try:
            pos = event.scenePos()
            for url in event.mimeData().urls():
                filepath = str(url.toLocalFile())
                self.Import( filepath, pos )
        except:
            traceback.print_exc()

        return super(GraphicsScene, self).dropEvent(event)