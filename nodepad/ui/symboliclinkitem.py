import sip
import traceback

from ..component.descriptors import *

from .graphicssettings import *
from .graphicsitembase import GraphicsNodeItem
from .portitem import Port


class SymbolicLink(GraphicsNodeItem):

    __flow = { 'InputSymbolicLink':DataFlow.Input, 'OutputSymbolicLink':DataFlow.Output }

    def __init__( self, name, nodeDesc, group_id ):
        super(SymbolicLink, self).__init__()
        
        # SymbolicLink params
        self.__m_ObjectType = nodeDesc.ObjectType()
        self.__m_ID = nodeDesc.ObjectID()
        self.__m_Name = name
        self.__m_Flow = self.__flow[ nodeDesc.ObjectType() ]
        self.__m_GroupID = group_id
        self.__m_SlotIndex = -1
        self.__m_Ports = {}

        # Ports
        in_desc = nodeDesc.InputAttribDescs()[0]
        out_desc = nodeDesc.OutputAttribDescs()[0]

        self.__m_ExposedID = in_desc.ObjectID()[1] if self.__m_ObjectType=='InputSymbolicLink' else out_desc.ObjectID()[1]
        self.__m_ProtectedID = out_desc.ObjectID()[1] if self.__m_ObjectType=='InputSymbolicLink' else in_desc.ObjectID()[1]

        self.__m_Ports[ in_desc.ObjectID()[1] ] = Port( '', in_desc.ObjectID(), in_desc.DataFlow() )
        self.__m_Ports[ out_desc.ObjectID()[1] ] = Port( '', out_desc.ObjectID(), out_desc.DataFlow() )

        self.__m_Ports[ self.__m_ProtectedID ].setParentItem(self)
        self.__m_Ports[ self.__m_ExposedID ].SetName( name )
        
        self.__m_Font = g_LabelFont
        self.__m_LabelAlignment = Qt.AlignBottom | (Qt.AlignLeft if self.__m_ObjectType=='OutputSymbolicLink' else Qt.AlignRight)
        self.__m_LabelMargin = float(g_LabelMargin)
        self.__m_LabelRect = None
        self.__m_PolygonShape = None
        self.__m_BoundingRect = None
        self.__m_Shape = None#QPainterPath()
        self.__m_Pen = QPen(g_ArrowFrameColor[0], g_ArrowFrameWidth)
        
        self.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
        self.setFlag( QGraphicsItem.ItemIsMovable )
        self.setFlag( QGraphicsItem.ItemIsSelectable )

        self.__UpdateBoundingRect()


    def __UpdateBoundingRect( self ):

        fm = QFontMetricsF( self.__m_Font )
        label_dim = ( fm.width(self.__m_Name)+1.0, fm.height() )
        label_pos = ( self.__m_LabelMargin, -label_dim[1]*0.5 ) if self.__m_ObjectType=='OutputSymbolicLink' else ( -self.__m_LabelMargin - label_dim[0], -label_dim[1]*0.5 ) #( label_dim[0]*0.0, -label_dim[1]*0.5 )
        self.__m_LabelRect = QRectF( label_pos[0], label_pos[1], label_dim[0], label_dim[1] )

        left = -label_dim[0]-self.__m_LabelMargin*1.5 if self.__m_ObjectType=='InputSymbolicLink' else -g_PortRadius*1.5
        right = g_PortRadius*1.5 if self.__m_ObjectType=='InputSymbolicLink' else label_dim[0]+self.__m_LabelMargin

        arrowCoords = [ QPointF(left, -g_ArrowHeight*0.5-g_ArrowFrameWidth),
                       QPointF(left, g_ArrowHeight*0.5+g_ArrowFrameWidth),
                       QPointF(right, g_ArrowHeight*0.5+g_ArrowFrameWidth),
                       QPointF(right+g_ArrowLength, 0.0),
                       QPointF(right, -g_ArrowHeight*0.5-g_ArrowFrameWidth) ]

        self.__m_PolygonShape = QPolygonF( arrowCoords )
        self.__m_BoundingRect = self.__m_PolygonShape.boundingRect().adjusted( -g_ArrowFrameWidth, -g_ArrowFrameWidth, g_ArrowFrameWidth, g_ArrowFrameWidth )
        self.__m_Shape = QPainterPath()
        self.__m_Shape.addPolygon( self.__m_PolygonShape )


    def ObjectType( self ):
        return self.__m_ObjectType


    def InputPort( self, object_id ):
        try:
            return self.__m_Ports[ object_id ]
        except:
            traceback.print_exc()
            return None


    def OutputPort( self, object_id ):
        try:
            return  self.__m_Ports[ object_id ]
        except:
            traceback.print_exc()
            return None


    def Port( self, object_id ):
        try:
            return  self.__m_Ports[ object_id ]
        except:
            traceback.print_exc()
            return None


    def ExposedPort( self ):
        return self.__m_Ports[ self.__m_ExposedID ]


    def ProtectedPort( self ):
        return self.__m_Ports[ self.__m_ProtectedID ]


    def ID( self ):
        return self.__m_ID


    def GroupID( self ):
        return self.__m_GroupID


    def DataFlow( self ):
        return self.__m_Flow


    def IsInputFlow( self ):
        return self.__m_Flow==DataFlow.Input


    def IsOutputFlow( self ):
        return self.__m_Flow==DataFlow.Output


    def SetName( self, name ):
        self.__m_Name = name
        self.__m_Ports[ self.__m_ExposedID ].SetName(name)
        self.__UpdateBoundingRect()


    def Name( self ):
        return self.__m_Name


    def SetSlotIndex( self, idx ):
        self.__m_SlotIndex = idx


    def SlotIndex( self ):
        return self.__m_SlotIndex



    ######################### QGraphicsItem func override ################################

    def itemChange( self, change, value ):

        # workaround for pyqt bug: http://www.riverbankcomputing.com/pipermail/pyqt/2012-August/031818.html
        if( change==QGraphicsItem.ItemParentChange and isinstance(value, QGraphicsItem) ):
            return sip.cast(value, QGraphicsItem)

        if( change == QGraphicsItem.ItemSelectedChange ):

            if( value == True ):
                self.setZValue( self.zValue() + 1 )
                self.__m_Pen.setColor(g_ArrowFrameColor[1])
            else:
                self.setZValue( self.zValue() - 1 )
                self.__m_Pen.setColor(g_ArrowFrameColor[0])

        return super(SymbolicLink, self).itemChange( change, value )


    def boundingRect(self):
        return self.__m_BoundingRect


    def shape( self ):
        if( self.scene().FocusViewID() != self._GraphicsNodeItem__m_RenderLayerID ):# QGraphicsViewごとにアイテムの表示/非表示を視切り替えて正しく動かすのに必要
            return QPainterPath()
        return self.__m_Shape


    def paint(self, painter, option, widget):
        if( self.scene().IsVisibleFromActiveView(self)==False ):
            return
        painter.setClipRect(option.exposedRect)
        painter.setPen(self.__m_Pen)
        painter.setBrush( g_ArrowColor)
        painter.drawPolygon( self.__m_PolygonShape )

        if( option.levelOfDetailFromTransform(painter.worldTransform()) < 0.5 ):
            return 
        painter.setFont( self.__m_Font )
        painter.setPen(g_LabelColor)
        painter.drawText( self.__m_LabelRect, self.__m_LabelAlignment, self.__m_Name )

