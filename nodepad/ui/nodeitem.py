from ..component.descriptors import *

from .graphicssettings import *
from .graphicsitembase import GraphicsNodeItem
from .portitem import Port
from .pushbuttonitem import PushButton



class Node(GraphicsNodeItem):

    def __init__( self, name, node_id, nodeDesc ):#, node_edit_callback ):
        super(Node, self).__init__()
        
        self.__m_ObjectType = nodeDesc.ObjectType()

        self.__m_ID = node_id
        self.__m_Name = name


        self.__m_BoundingRect = QRectF()
        self.__m_DrawRect = QRectF()
        self.__m_Shape = QPainterPath()
        self.__m_Pen = QPen( g_NodeFrameColor[0], g_NodeFrameWidth )

        self.__UpdateBoundingRect( 0 )

        self.__m_Gradient = QLinearGradient(0, 0, 0,g_TitlebarHeight)
        self.__m_Gradient.setColorAt(0, QColor(128,128,128))
        self.__m_Gradient.setColorAt(0.49999, QColor(60,60,60))
        self.__m_Gradient.setColorAt(0.5, QColor(32,32,32))
        self.__m_Gradient.setColorAt(0.99999, QColor(48,48,48))
        self.__m_Gradient.setColorAt(1.0, QColor(64,64,64))


        self.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
        self.setFlag( QGraphicsItem.ItemIsMovable )
        self.setFlag( QGraphicsItem.ItemIsSelectable )

        # Node's Label
        self.__m_Label = nodeDesc.ObjectType()
        self.__m_Font = g_LabelFont
        fm = QFontMetricsF( self.__m_Font )
        label_dim = ( min( self.__m_DrawRect.width() - g_ButtonSize, fm.width(self.__m_Label) ), fm.height() )
        label_pos = ( g_LabelMargin, g_TitlebarHeight / 2 - label_dim[1] / 2 )
        self.__m_LabelRect = QRectF( label_pos[0], label_pos[1], label_dim[0], label_dim[1] )

        # Port UIs (key: object id, value: Port
        self.__m_refInputPorts = {}
        self.__m_refOutputPorts = {}

        # NodeEdit Pushbutton
        #if( node_edit_callback ):
        #    self.__m_EditButton = PushButton( QPixmap( ':/resource/images/edit-group.png'), node_edit_callback )# TODO: attach code_edit_callback for custom scripting.
        #    self.__m_EditButton.setParentItem( self )
        #    self.__m_EditButton.setPos( self.__m_BoundingRect.width() - g_TitlebarHeight, 0.5 * (g_TitlebarHeight-g_ButtonSize) )


        # DropShadow Effect...... Disabled. Decreases performance. Causes access violation.
        #effect = QGraphicsDropShadowEffect()
        #effect.setBlurRadius(5)
        #effect.setOffset(5,5)
        #effect.setColor( g_NodeShadowColor )
        #self.setGraphicsEffect(effect)


    def AddPort( self, port ):

        port.setParentItem(self)

        # create port object
        if( port.DataFlow()==DataFlow.Input ):
            idx = len( self.__m_refInputPorts )
            posy = g_TitlebarHeight + g_AttribAreaHeight * (idx + 0.5)
            port.setPos( 0, posy )
            self.__m_refInputPorts[ port.ID() ] = port

        elif( port.DataFlow()==DataFlow.Output ):
            idx = len( self.__m_refOutputPorts )
            posy = g_TitlebarHeight + g_AttribAreaHeight * (idx + 0.5)
            port.setPos( self.__m_DrawRect.width(), posy )#self.__m_Width, posy )
            self.__m_refOutputPorts[ port.ID() ] = port

        self.__UpdateBoundingRect( max( len(self.__m_refInputPorts), len(self.__m_refOutputPorts) ) )


    def RemovePort( self, port_id ):

        if( port_id in self.__m_refInputPorts ):
            self.__m_refInputPorts[ port_id ].setParentItem( self.parentItem() )
            self.__m_refInputPorts[ port_id ] = None
            del self.__m_refInputPorts[ port_id ]

        elif( port_id in self.__m_refOutputPorts ):
            self.__m_refOutputPorts[ port_id ].setParentItem( self.parentItem() )
            self.__m_refOutputPorts[ port_id ] = None
            del self.__m_refOutputPorts[ port_id ]

        self.__UpdateBoundingRect( max( len(self.__m_refInputPorts), len(self.__m_refOutputPorts) ) )


    def RenamePort( self, port_id, newkey ):

        if( port_id in self.__m_refInputPorts ):
            self.__m_refInputPorts[ port_id ].SetName(newkey)

        elif( port_id in self.__m_refOutputPorts ):
            self.__m_refOutputPorts[ port_id ].SetName(newkey)
  

    def ObjectType( self ):
        return self.__m_ObjectType


    def InputPorts( self ):
        return self.__m_refInputPorts


    def OutputPorts( self ):
        return self.__m_refOutputPorts


    def InputPort( self, object_id ):
        try:
            return self.__m_refInputPorts[ object_id ]
        except:
            traceback.print_exc()
            return None


    def OutputPort( self, object_id ):
        try:
            return  self.__m_refOutputPorts[ object_id ]
        except:
            traceback.print_exc()
            return None


    def Port( self, object_id ):
        if( object_id in self.__m_refInputPorts ):
            return self.__m_refInputPorts[ object_id ]
        elif( object_id in self.__m_refOutputPorts ):
            return self.__m_refOutputPorts[ object_id ]
        return None


    def ID( self ):
        return self.__m_ID


    def SetName( self, name ):
        self.__m_Name = name


    def Name( self ):
        return self.__m_Name


    def __UpdateBoundingRect( self, numslots ):
        self.prepareGeometryChange()
        self.__m_DrawRect.setRect( 0, 0, g_NodeMinWidth, g_NodeMinHeight + max(1, numslots)*g_AttribAreaHeight )
        self.__m_BoundingRect = self.__m_DrawRect.adjusted( -g_NodeFrameWidth, -g_NodeFrameWidth, g_NodeFrameWidth, g_NodeFrameWidth )
        self.__m_Shape = QPainterPath()
        self.__m_Shape.addRect( self.__m_BoundingRect )



    ######################### QGraphicsItem func override ################################

    def itemChange( self, change, value ):
        
        if( change == QGraphicsItem.ItemSelectedChange ):
            if( value == True ):
                self.setZValue( self.zValue() + 1 )
                self.__m_Pen.setColor(g_NodeFrameColor[1])
            else:
                self.setZValue( self.zValue() - 1 )
                self.__m_Pen.setColor(g_NodeFrameColor[0])

        return super(Node, self).itemChange( change, value )


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
        painter.setBrush(self.__m_Gradient)
        painter.setPen(self.__m_Pen)
        painter.drawRoundedRect( self.__m_DrawRect, g_BoxRoundRadius, g_BoxRoundRadius )#painter.drawRoundedRect(0, 0, self.__m_Width, self.__m_Height, g_BoxRoundRadius, g_BoxRoundRadius)

        if( option.levelOfDetailFromTransform(painter.worldTransform()) < 0.5):
            return 
        painter.setFont( self.__m_Font )
        painter.setPen(g_LabelColor)
        painter.drawText( self.__m_LabelRect, Qt.AlignLeft, self.__m_Label )