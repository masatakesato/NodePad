from ..component.descriptors import *

from .graphicssettings import *
from .graphicsitembase import GraphicsPathItem


# Edge
class Edge(GraphicsPathItem):

    def __init__( self, name, edge_id, src_pos, dest_pos ):
        super(Edge, self).__init__()

        #self.__m_ObjectType = type(self).__name__
        self.__m_ID = edge_id
        self.__m_Name = name

        self.__m_refSourcePort = None
        self.__m_refDestPort = None
        self.__m_SourcePos = src_pos # source position
        self.__m_DestPos = dest_pos   # destination position

        self.__m_BoundingRect = QRectF()
        self.__m_hw = g_EdgeWidth*0.5 
        self.__m_Pen = QPen( g_EdgeColor[0], g_EdgeWidth )
        
        self.setZValue(g_EdgeDepth)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.UpdatePath()


    def ConnectPort( self, sourceport, destport ):
        self.ConnectSourcePort( sourceport )
        self.ConnectDestPort( destport )

    def ConnectSourcePort( self, sourceport ):
        self.__m_refSourcePort = sourceport
        self.SetSourcePosition(self.__m_refSourcePort.scenePos())

    def ConnectDestPort( self, destport ):
        self.__m_refDestPort = destport
        self.SetDestPosition(self.__m_refDestPort.scenePos())


    def DisconnectPort( self ):
        self.__m_refSourcePort = None
        self.__m_refDestPort = None

    def DisconnectSourcePort(self):
        self.__m_refSourcePort = None

    def DisconnectDestPort(self):
        self.__m_refDestPort = None


    def SetSourcePosition(self, pos ):
        self.__m_SourcePos = pos


    def SetDestPosition(self, pos ):
        self.__m_DestPos = pos


    def UpdatePath(self):
        path = QPainterPath()
        dx = self.__m_DestPos.x() - self.__m_SourcePos.x()
        ctrl1 = QPointF(self.__m_SourcePos.x() + dx * 0.5, self.__m_SourcePos.y())# + dy * 0.1)
        ctrl2 = QPointF(self.__m_DestPos.x() - dx * 0.5, self.__m_DestPos.y())# + dy * 0.9)
   
        path.moveTo(self.__m_SourcePos)
        path.cubicTo(ctrl1, ctrl2, self.__m_DestPos)

        self.setPath(path)

        self.__m_BoundingRect = path.boundingRect().adjusted(-self.__m_hw, -self.__m_hw, self.__m_hw, self.__m_hw)


    def ObjectType( self ):
        return 'Connection'#self.__m_ObjectType


    def ID( self ):
        return self.__m_ID


    def Name( self ):
        return self.__m_Name


    def SetName( self, name ):
        self.__m_Name = name


    def SourcePort( self ):
        return self.__m_refSourcePort


    def DestinationPort( self ):
        return self.__m_refDestPort


    def SourceNodeID( self ):
        return self.__m_refSourcePort.ParentID()


    def DestinationNodeID( self ):
        return self.__m_refDestPort.ParentID()


    ####################### QGraphicsItem func override ################################

    def itemChange( self, change, value ):

        if( change == QGraphicsItem.ItemSelectedChange ):
            self.__m_Pen.setColor( g_EdgeColor[int(value)] )

        return super(Edge, self).itemChange(change, value)


    def boundingRect(self):
        return self.__m_BoundingRect


    def shape( self ):
        # マルチウィンドウでshape無効化する条件を調べる.サブウィンドウ開いた直後、エッジが表示されていない -> boundingRect実装すれば解決
        if( self.scene().FocusViewID() != self._GraphicsPathItem__m_RenderLayerID ):
            return QPainterPath()
        stroker = QPainterPathStroker()
        stroker.setWidth( g_EdgeCollisionWidth )
        return stroker.createStroke( self.path() )


    def paint( self, painter, option, widget ):
        if( self.scene().IsVisibleFromActiveView(self)==False ):
            return
        painter.setClipRect( option.exposedRect )
        painter.setPen( self.__m_Pen )
        painter.drawPath( self.path() )



# Temporary Edge
class TemporaryEdge(GraphicsPathItem):

    def __init__( self, pos ):
        super(TemporaryEdge, self).__init__()

        self.__m_SourcePos = pos # source position
        self.__m_DestPos = pos   # destination position

        self.__m_Pen = QPen(g_EdgeColor[0], g_EdgeWidth, Qt.DotLine)

        self.setZValue(g_EdgeDepth)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)

        self.UpdatePath()



    def SetSourcePosition( self, pos ):
        self.__m_SourcePos = pos


    def SetDestPosition( self, pos ):
        self.__m_DestPos = pos


    def UpdatePath(self):
        path = QPainterPath()
        dx = self.__m_DestPos.x() - self.__m_SourcePos.x()
        ctrl1 = QPointF(self.__m_SourcePos.x() + dx * 0.5, self.__m_SourcePos.y())# + dy * 0.1)
        ctrl2 = QPointF(self.__m_DestPos.x() - dx * 0.5, self.__m_DestPos.y())# + dy * 0.9)
   
        path.moveTo(self.__m_SourcePos)
        path.cubicTo(ctrl1, ctrl2, self.__m_DestPos)

        self.setPath(path)


    def ID( self ):
        return None



    ####################### QGraphicsItem func override ################################
    
    def paint(self, painter, option, widget):
        if( self.scene().IsVisibleFromActiveView(self)==False ):
            return
        painter.setClipRect(option.exposedRect)
        painter.setPen( self.__m_Pen )
        painter.drawPath( self.path() )

