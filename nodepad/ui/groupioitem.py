import sip
import traceback
import uuid

from ..component.descriptors import *

from .graphicssettings import *
from .graphicsitembase import GraphicsNodeItem
from .symboliclinkitem import SymbolicLink




def clamp( val, min_val, max_val ):
    return min( max(val,min_val), max_val )



class GroupIO(GraphicsNodeItem):

    __color = { DataFlow.Input: QColor(186,179,137), DataFlow.Output: QColor(180,158,143) }

    def __init__( self, name, dataflow, group_id, object_id ):
        super(GroupIO, self).__init__()

        self.__m_ObjectType = 'GroupIO'

        self.__m_ID = object_id
        self.__m_GroupID = group_id
        self.__m_Flow = dataflow

        self.__m_PortSlots = []
        self.__m_BlankIndex = -1
        self.__m_LastSlotIndex = 0

        self.__m_BoundingRect = QRectF()
        self.__m_DrawRect = QRectF()
        self.__m_Shape = QPainterPath()
        self.__m_Brush = QBrush( self.__color[dataflow] )
        self.__m_Pen = QPen( g_NodeFrameColor[0], g_GroupIOFrameWidth )

        self.setFlags( QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable )
        self.setFlag( QGraphicsItem.ItemSendsScenePositionChanges )
        
        self.__UpdateBoundingRect( len(self.__m_PortSlots) )

        self.__m_Width = self.__m_BoundingRect.width()
        self.__m_SlotAlignX = self.__m_Width if self.__m_Flow==DataFlow.Input else 0.0

        # GroupIO's Label
        self.__m_Label = name
        self.__m_Font = g_LabelFont
        fm = QFontMetricsF( self.__m_Font )
        label_dim = ( fm.width(self.__m_Label), fm.height() )
        label_pos = ( (self.__m_Width - label_dim[0]) / 2, g_TitlebarHeight / 2 - label_dim[1] / 2 )
        self.__m_LabelRect = QRectF( label_pos[0], label_pos[1], label_dim[0], label_dim[1] )


    def SetColor( self, color ):
        self.__m_Brush.setColor(color)


    # Add Item
    def AddItem( self, item, idx=-1 ):

        if( item in self.__m_PortSlots ):
            return
        
        slot_idx = None
        snap_pos = None        

        if( self.__m_BlankIndex != -1 ):# ブランクがある場合はitemに置き換える
            slot_idx = self.__m_BlankIndex
            snap_pos = self.__CalcSlotPosition( self.__m_BlankIndex )
            #print('GroupIO::AddItem...replace blank', slot_idx, self.__m_BlankIndex)
            self.__m_PortSlots[slot_idx] = item
            self.__m_BlankIndex = -1

        else:
            if( idx != -1 ):
                slot_idx = clamp( idx, 0, len(self.__m_PortSlots) )
                snap_pos = self.__CalcSlotPosition( slot_idx )
            else:
                slot_idx, snap_pos = self.__GetSnapPoint( self.mapFromScene(item.scenePos()) )
            self.__m_PortSlots.insert(slot_idx, item)
            #print('GroupIO::AddItem...insert new element', slot_idx, self.__m_BlankIndex)

        item.setParentItem( self )
        item.setPos( snap_pos )
        item.SetSlotIndex( slot_idx )

        self.__UpdateBoundingRect( len(self.__m_PortSlots) )

        for i in range(slot_idx+1, len(self.__m_PortSlots)):
            self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
            self.__m_PortSlots[i].SetSlotIndex(i)


    # AppendItem
    def AppendItem( self, item ):

        if( item in self.__m_PortSlots ):
            return

        item.setParentItem( self )
        self.__m_PortSlots.append(item)

        slot_idx = len(self.__m_PortSlots) - 1
        item.setPos( self.__CalcSlotPosition( slot_idx ) )
        item.SetSlotIndex(slot_idx)

        self.__UpdateBoundingRect( len(self.__m_PortSlots) )


    def RemoveItem( self, item ):
        try:
            #print('GroupIO::RemoveItem...')
            idx = self.__m_PortSlots.index(item)
            self.__m_PortSlots.remove(item)
            item.setParentItem( self.parentItem() )
            
            itempos = self.mapToParent( item.pos() )
            item.setPos( itempos)

            self.__UpdateBoundingRect( len(self.__m_PortSlots) )

            for i in range(idx, len(self.__m_PortSlots)):
                self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
                self.__m_PortSlots[i].SetSlotIndex(i)

        except:
            traceback.print_exc()


    def RemoveItemByIndex( self, idx ):
        try:
            item = self.__m_PortSlots.pop(idx)
            item.setParentItem( self.parentItem() )

            self.__UpdateBoundingRect( len(self.__m_PortSlots) )

            for i in range(idx, len(self.__m_PortSlots)):
                self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
                self.__m_PortSlots[i].SetSlotIndex(i)

            return item

        except:
            traceback.print_exc()
            return None


    def MoveItem( self, item ):
        
        pos = item.pos()
        if( self.sceneBoundingRect().intersects(item.sceneBoundingRect())==False ):
            return False

        src_idx = item.SlotIndex()#self.__m_PortSlots.index(item)
        dest_idx, snap_pos = self.__GetSnapPoint(pos)
        
        if( src_idx != dest_idx ):
            #print('changing self.__m_PortSlots element order',  src_idx, dest_idx)
            self.__m_PortSlots.insert(dest_idx, self.__m_PortSlots.pop(src_idx))
            item.SetSlotIndex( dest_idx )
        
        # 他の要素の位置を更新する
        idx_min, idx_max = (src_idx, dest_idx) if src_idx<=dest_idx else (dest_idx+1, src_idx+1)
        #print( src_idx, dest_idx )

        for idx in range(idx_min, idx_max):
            #print( 'updating pos at', idx )
            self.__m_PortSlots[idx].setPos( self.__CalcSlotPosition(idx) )
            self.__m_PortSlots[idx].SetSlotIndex( idx )

        return True


    def SnapItem( self, item ):#, pos ):
        dest_idx, snap_pos = self.__GetSnapPoint( item.pos() )#pos)
        item.setPos( snap_pos )


    def AddBlank( self, scenePos ):

        src_idx = self.__m_BlankIndex
        dest_idx = self.__CalcSlotIndex( self.mapFromScene( scenePos ), 0, len(self.__m_PortSlots) )

        if( src_idx==dest_idx ):
            return

        #print('GroupIO::AddBlank', dest_idx)
        if( self.__m_BlankIndex !=-1 ):  del self.__m_PortSlots[self.__m_BlankIndex]
        self.__m_PortSlots.insert( dest_idx, None )
        self.__m_BlankIndex = dest_idx


        # 他の要素の位置を更新する
        idx_min, idx_max = 0, 0

        if( src_idx ==-1 ):
            idx_min, idx_max = dest_idx+1, len(self.__m_PortSlots)
            self.__UpdateBoundingRect( len(self.__m_PortSlots) )
        else:
            idx_min, idx_max = (src_idx, dest_idx) if src_idx<=dest_idx else (dest_idx+1, src_idx+1)
        #print( src_idx, dest_idx )

        for idx in range(idx_min, idx_max):
            #print( 'updating pos at', idx )
            self.__m_PortSlots[idx].setPos( self.__CalcSlotPosition(idx) )
            self.__m_PortSlots[idx].SetSlotIndex( idx )


    def MoveBlank( self, scenePos ):

        if( self.__m_BlankIndex==-1 ):
            return

        src_idx = self.__m_BlankIndex
        dest_idx = self.__CalcSlotIndex( self.mapFromScene( scenePos ), 0, self.__m_LastSlotIndex )#len(self.__m_PortSlots)-1 )

        if( src_idx==dest_idx ):
            return

        #print('GroupIO::MoveBlank', dest_idx)
        self.__m_PortSlots.insert( dest_idx, self.__m_PortSlots.pop(src_idx) )
        self.__m_BlankIndex = dest_idx

        # 他の要素の位置を更新する
        idx_min, idx_max = (src_idx, dest_idx) if src_idx<=dest_idx else (dest_idx+1, src_idx+1)
        #print( src_idx, dest_idx )

        for idx in range(idx_min, idx_max):
            #print( 'updating pos at', idx )
            self.__m_PortSlots[idx].setPos( self.__CalcSlotPosition(idx) )
            self.__m_PortSlots[idx].SetSlotIndex( idx )


    def RemoveBlank( self ):
        try:
            if( self.__m_BlankIndex == -1):
                return

            #print('GroupIO::RemoveBlank...', self.__m_BlankIndex )
            del self.__m_PortSlots[ self.__m_BlankIndex ]
            
            self.__UpdateBoundingRect( len(self.__m_PortSlots) )

            for i in range(self.__m_BlankIndex, len(self.__m_PortSlots)):
                self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
                self.__m_PortSlots[i].SetSlotIndex(i)

            self.__m_BlankIndex = -1

        except:
            traceback.print_exc()


    def SetIndex( self, src_idx, dst_idx ):

        self.__m_PortSlots.insert( dst_idx, self.__m_PortSlots.pop(src_idx) )

        start = min( src_idx, dst_idx )
        count = max( src_idx, dst_idx ) + 1

        for i in range( start, count ):
            self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
            self.__m_PortSlots[i].SetSlotIndex(i)


    def ObjectType( self ):
        return self.__m_ObjectType


    def ID( self ):
        return self.__m_ID


    def Name( self ):
        return ''


    def SetName( self, name ):
        print( 'GroupIO::SetName forbidden...' )


    def ParentID( self ):
        return self.__m_GroupID


    def DataFlow( self ):
        return self.__m_Flow


    def IsInputFlow( self ):
        return self.__m_Flow==DataFlow.Input


    def IsOutputFlow( self ):
        return self.__m_Flow==DataFlow.Output


    def BlankIndex( self ):
        return self.__m_BlankIndex


    def NumSymbolicLinks( self ):
        return len(self.__m_PortSlots)


    def SymbolicLinks( self ):
        return self.__m_PortSlots


    def SymbolicLink( self, idx ):
        try:
            return self.__m_PortSlots[ idx ]
        except:
            traceback.print_exc()


    def IsRegistrableSymbolicLink( self, item ):
        try:
            if( item in self.childItems() ):
                return False
            if( item.DataFlow() != self.__m_Flow ): 
                return False
            return True
        except:
            traceback.print_exc()
            return False


    def __CalcSlotPosition( self, idx ):
        return QPointF( self.__m_SlotAlignX, g_SlotHeight*0.5 +       g_SlotHeight * float(idx) +       g_TitlebarHeight )


    def __CalcSlotIndex( self, pos, min_val, max_val ):
        return clamp( round((pos.y()-g_TitlebarHeight-g_SlotHeight*0.5)/g_SlotHeight), min_val, max_val )


    def __GetSnapPoint( self, pos ):
        slot_idx = clamp( round((pos.y()-g_TitlebarHeight-g_SlotHeight*0.5)/g_SlotHeight), 0, self.__m_LastSlotIndex )
        return int(slot_idx), QPointF( self.__m_SlotAlignX, g_SlotHeight*0.5 +       slot_idx * g_SlotHeight +       g_TitlebarHeight )


    def __UpdateBoundingRect( self, numslots ):
        self.prepareGeometryChange()
        self.__m_DrawRect.setRect( 0, 0, g_GroupIOWidth, g_SlotHeight * max(1, numslots) + g_TitlebarHeight + g_HeightMargin )
        self.__m_BoundingRect = self.__m_DrawRect.adjusted( -g_GroupIOFrameWidth, -g_GroupIOFrameWidth, g_GroupIOFrameWidth, g_GroupIOFrameWidth )
        self.__m_Shape = QPainterPath()
        self.__m_Shape.addRect( self.__m_BoundingRect )
        self.__m_LastSlotIndex = max( numslots-1, 0 )






    ######################### QGraphicsItem func override ################################

    def itemChange( self, change, value ):

        ## workaround for pyqt bug:
        ## http://www.riverbankcomputing.com/pipermail/pyqt/2012-August/031818.html
        if( change==QGraphicsItem.ItemParentChange ):
            return sip.cast(value, QGraphicsItem)

        if( change == QGraphicsItem.ItemSelectedChange ):
            if( value == True ):
                #self.setZValue( self.zValue() + 1 )
                self.__m_Pen.setColor(g_NodeFrameColor[1])
            else:
                #self.setZValue( self.zValue() - 1 )
                self.__m_Pen.setColor(g_NodeFrameColor[0])
        
        return super(GroupIO, self).itemChange( change, value )


    def boundingRect(self):
        return self.__m_BoundingRect


    def shape( self ):
        if( self.scene().FocusViewID() != self._GraphicsNodeItem__m_RenderLayerID ):# QGraphicsViewごとにアイテムの表示/非表示を視切り替えて正しく動かすのに必要
            return QPainterPath()
        return self.__m_Shape



    def paint( self, painter, option, widget=None ):
        if( self.scene().IsVisibleFromActiveView(self)==False ):
            return
        painter.setClipRect(option.exposedRect)
        painter.setBrush( self.__m_Brush )
        painter.setPen(self.__m_Pen)
        painter.drawRoundedRect( self.__m_DrawRect, g_BoxRoundRadius, g_BoxRoundRadius )

        if( option.levelOfDetailFromTransform(painter.worldTransform()) < 0.5):
            return 
        painter.setFont( self.__m_Font )
        painter.setPen(g_LabelColor)
        painter.drawText( self.__m_LabelRect, Qt.AlignCenter, self.__m_Label )
