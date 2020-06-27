from ..component.descriptors import *

from .graphicssettings import *
from .graphicsitembase import GraphicsPortItem



class Port(GraphicsPortItem):

    def __init__(self, name, object_id, portType):
        super(Port, self).__init__()

        # attributes
        self.__m_ID = object_id
        self.__m_Name = name
        self.__m_Flow = portType

        self.__m_Radius = g_PortRadius
        self.__m_Diam = self.__m_Radius * 2
        self.__m_PortRect = QRectF( -self.__m_Diam, -self.__m_Diam, self.__m_Diam*2, self.__m_Diam*2 )

        self.__m_Path = QPainterPath()
        self.__m_Path.addEllipse( self.__m_PortRect )

        self.__m_Pen = QPen(g_PortFrameColor, g_PortFrameWidth)
        self.setZValue(g_PortDepth)

        # create label graphics object
        self.__m_Font = g_LabelFont
        self.__m_LabelAlignment = Qt.AlignBottom | (Qt.AlignLeft if self.__m_Flow==DataFlow.Input else Qt.AlignRight)
        self.__m_LabelMargin = g_LabelMargin
        self.__m_LabelRect = QRectF()
        self.__m_BoundingRect = QRectF()

        self.setFlag( QGraphicsItem.ItemSendsScenePositionChanges )

        self.__UpdateBoundingRect()

        # connected edges
        self.__m_ConnectedEdges = {}


    def ConnectEdge( self, edge ):
        self.__m_ConnectedEdges[ edge.ID() ] = edge


    def DisconnectEdge( self, edge ):
        object_id = edge.ID()
        if( object_id in self.__m_ConnectedEdges ):
            self.__m_ConnectedEdges[ object_id ] = None
            del self.__m_ConnectedEdges[ object_id ]


    def SetName( self, name ):
        self.__m_Name = name
        self.__UpdateBoundingRect()


    def ConnectedEdges( self ):
        return self.__m_ConnectedEdges


    def Name( self ):
        return self.parentItem().Name() + '.' + self.__m_Name


    def ParentName( self ):
        return self.parentItem().Name()


    def LocalName( self ):
        return self.__m_Name


    def ParentID( self ):
        return self.__m_ID[0]


    def ID( self ):
        return self.__m_ID[1]


    def PortID( self ):
        return self.__m_ID
        

    def DataFlow( self ):
        return self.__m_Flow


    def IsInputFlow( self ):
        return self.__m_Flow==DataFlow.Input


    def IsOutputFlow( self ):
        return self.__m_Flow==DataFlow.Output


    def __UpdateBoundingRect( self ):

        fm = QFontMetricsF( self.__m_Font )
        label_dim = ( fm.width(self.__m_Name)+1.0, fm.height() )
        label_pos = ( self.__m_LabelMargin, -label_dim[1]*0.5 ) if self.__m_Flow==DataFlow.Input else ( -self.__m_LabelMargin - label_dim[0], -label_dim[1]*0.5 )
        self.__m_LabelRect = QRectF( label_pos[0], label_pos[1], label_dim[0], label_dim[1] )

        bb_min = ( min( self.__m_PortRect.left(), self.__m_LabelRect.left() ), min( self.__m_PortRect.top(), self.__m_LabelRect.top() ) )
        bb_max = ( max( self.__m_PortRect.right(), self.__m_LabelRect.right() ), max( self.__m_PortRect.bottom(), self.__m_LabelRect.bottom() ) )
        self.__m_BoundingRect = QRectF( bb_min[0], bb_min[1], bb_max[0]-bb_min[0], bb_max[1]-bb_min[1] )


    def __UpdateEdgePath( self ):

        if( self.__m_Flow==DataFlow.Input ):
            for edge in self.__m_ConnectedEdges.values():
                edge.SetDestPosition( self.scenePos() )
                edge.UpdatePath()
        else:
            for edge in self.__m_ConnectedEdges.values():
                edge.SetSourcePosition( self.scenePos() )
                edge.UpdatePath()



    ########################### QGraphicsItem func override ################################

    def itemChange( self, change, value ):

        if( change == QGraphicsItem.ItemScenePositionHasChanged ):
            self.__UpdateEdgePath()

        return super(Port, self).itemChange( change, value )


    def boundingRect(self):
        return self.__m_BoundingRect


    def shape(self):
        if( self.scene().FocusViewID() != self._GraphicsPortItem__m_RenderLayerID ):# QGraphicsViewごとにアイテムの表示/非表示を視切り替えて正しく動かすのに必要
            return QPainterPath()
        return self.__m_Path


    def paint(self, painter, option, widget):
        if( self.scene().IsVisibleFromActiveView(self)==False ):
            return
        painter.setClipRect(option.exposedRect)
        painter.setPen(self.__m_Pen)
        painter.setBrush(g_PortColor[self.__m_Flow])
        painter.drawRoundedRect( -self.__m_Radius, -self.__m_Radius, self.__m_Diam, self.__m_Diam, self.__m_Radius, self.__m_Radius )

        if( option.levelOfDetailFromTransform(painter.worldTransform()) < 0.5):
            return 
        painter.setFont( self.__m_Font )
        painter.setPen(g_LabelColor)
        painter.drawText( self.__m_LabelRect, self.__m_LabelAlignment, self.__m_Name )
