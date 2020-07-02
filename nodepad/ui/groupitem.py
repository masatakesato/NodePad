from ..component.descriptors import *

from .graphicssettings import *
from .graphicsitembase import GraphicsNodeItem
from .symboliclinkitem import *
from .pushbuttonitem import PushButton



class Group(GraphicsNodeItem):

    def __init__( self, name, group_id, group_edit_callback ):
        super(Group, self).__init__()
        
        self.__m_ID = group_id
        self.__m_Name = name
        self.__m_refCallback = group_edit_callback

        # Inputs/Outpus
        self.__m_refInputPorts = {}
        self.__m_refOutputPorts = {}

        self.__m_refSymbolicLinks = {}# key: exposed port id, val: SymbolicLink item

        # GroupIO reference
        self.__m_refGroupIO = {}


        self.__m_BoundingRect = QRectF()
        self.__m_DrawRect = QRectF()
        self.__m_Shape = QPainterPath()
        self.__m_Pen = QPen( g_NodeFrameColor[0], g_GroupFrameWidth )

        self.__UpdateBoundingRect( 0 )

        self.__m_Gradient = QLinearGradient(0, 0, 0, g_TitlebarHeight)
        self.__m_Gradient.setColorAt(0, QColor(142,130,112))
        self.__m_Gradient.setColorAt(0.49999, QColor(80,60,40))
        self.__m_Gradient.setColorAt(0.5, QColor(44,32,26))
        self.__m_Gradient.setColorAt(0.99999, QColor(54,50,40))
        self.__m_Gradient.setColorAt(1.0, QColor(72,64,56))

        self.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
        self.setFlag( QGraphicsItem.ItemIsMovable )
        self.setFlag( QGraphicsItem.ItemIsSelectable )

        # Group's Label
        self.__m_Label = self.__m_Name#'Group: ' + self.__m_Name
        self.__m_Font = g_LabelFont
        fm = QFontMetricsF( self.__m_Font )
        label_dim = ( min( self.__m_DrawRect.width() - g_ButtonSize, fm.width(self.__m_Label) ), fm.height() )
        label_pos = ( g_LabelMargin, g_TitlebarHeight / 2 - label_dim[1] / 2 )
        self.__m_LabelRect = QRectF( label_pos[0], label_pos[1], label_dim[0], label_dim[1] )
        
        # GroupEdit Pushbutton
        self.__m_EditButton = PushButton( QPixmap( ':/resource/images/edit-group.png'), self.__EditGroupButtonPushed )# group_edit_callback
        self.__m_EditButton.setParentItem( self )
        self.__m_EditButton.setPos( self.__m_BoundingRect.width() - g_TitlebarHeight, 0.5 * (g_TitlebarHeight-g_ButtonSize) )



    def AddSymbolicLink( self, symboliclink, slot_index=-1 ):

        self.__m_refSymbolicLinks[ symboliclink.ExposedPort().ID() ] = symboliclink

        if( symboliclink.ObjectType()=='InputSymbolicLink' ):
            symboliclink.ExposedPort().setParentItem( self )
            self.__m_refInputPorts[ symboliclink.ExposedPort().ID() ] = symboliclink.ExposedPort()
            self.UpdateInputPortPositions()

        elif( symboliclink.ObjectType()=='OutputSymbolicLink' ):
            symboliclink.ExposedPort().setParentItem( self )
            self.__m_refOutputPorts[ symboliclink.ExposedPort().ID() ] = symboliclink.ExposedPort()
            self.UpdateOutputPortPositions()

        self.__UpdateBoundingRect( max( len(self.__m_refInputPorts), len(self.__m_refOutputPorts) ) )


    def RemoveSymbolicLink( self, port_id ):

        symboliclink = self.__m_refSymbolicLinks[ port_id ]

        # Remove input port entry
        if( symboliclink.ObjectType()=='InputSymbolicLink' ):
            symboliclink.ExposedPort().setParentItem( None )
            input_port_id = symboliclink.ExposedPort().ID()
            self.__m_refInputPorts[ input_port_id ] = None
            del self.__m_refInputPorts[ input_port_id ]

            self.UpdateInputPortPositions()

        # Remove output port entry
        elif( symboliclink.ObjectType()=='OutputSymbolicLink' ):
            symboliclink.ExposedPort().setParentItem( None )
            output_port_id = symboliclink.ExposedPort().ID()
            self.__m_refOutputPorts[ output_port_id ] = None
            del self.__m_refOutputPorts[ output_port_id ]

            self.UpdateOutputPortPositions()

        # Unbind symboliclink
        self.__m_refSymbolicLinks[ port_id ] = None
        del self.__m_refSymbolicLinks[ port_id ]

        self.__UpdateBoundingRect( max( len(self.__m_refInputPorts), len(self.__m_refOutputPorts) ) )


    def UpdateInputPortPositions( self ):
        for port_id, port_item in self.__m_refInputPorts.items():
            self.__m_refInputPorts[ port_id ].setPos( 0, g_TitlebarHeight + g_AttribAreaHeight * (self.__m_refSymbolicLinks[ port_id ].SlotIndex() + 0.5) )


    def UpdateOutputPortPositions( self ):
        for port_id, port_item in self.__m_refOutputPorts.items():
            self.__m_refOutputPorts[ port_id ].setPos( self.__m_DrawRect.width(), g_TitlebarHeight + g_AttribAreaHeight * (self.__m_refSymbolicLinks[ port_id ].SlotIndex() + 0.5) )


    def ClearSymbolicLinks( self ):
        
        port_ids = [ v.ExposedPort().ID() for v in self.__m_refSymbolicLinks.values() ]
        for port_id  in port_ids:
            self.RemoveSymbolicLink( port_id )

        #synboliclink_ids = list(self.__m_refSymbolicLinks.keys())

        #for symboliclink_id in synboliclink_ids:
        #    self.RemoveSymbolicLink( symboliclink_id )

        return synboliclink_ids


    def RenamePort( self, port_id, newkey ):
        symboliclink = self.__m_refSymbolicLinks[ port_id ]
        symboliclink.SetName( newkey )


    def ObjectType( self ):
        return 'Group'


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
        self.__m_Label = name#'Group: ' + name

        fm = QFontMetricsF( self.__m_Font )
        self.__m_LabelRect.setWidth( min( self.__m_DrawRect.width() - g_ButtonSize, fm.width(self.__m_Label) ) )


    def Name( self ):
        return self.__m_Name


    def BindGroupIO( self, groupio ):
        self.__m_refGroupIO[ groupio.DataFlow() ] = groupio


    def UnbindGroupIO( self, dataflow ):
        try:
            return self.__m_refGroupIO.pop(dataflow)
        except:
            traceback.print_exc()
            return None


    def GroupIO( self, dataflow ):
        return self.__m_refGroupIO[ dataflow ]


    def __UpdateBoundingRect( self, numslots ):
        self.prepareGeometryChange()
        self.__m_DrawRect.setRect( 0, 0, g_GroupMinWidth, g_GroupMinHeight + max(1, numslots)*g_AttribAreaHeight )
        self.__m_BoundingRect = self.__m_DrawRect.adjusted( -g_GroupFrameWidth, -g_GroupFrameWidth, g_GroupFrameWidth, g_GroupFrameWidth )
        self.__m_Shape = QPainterPath()
        self.__m_Shape.addRect( self.__m_BoundingRect )



    def __EditGroupButtonPushed( self ):
        print( 'Group::__EditGroupButtonPushed()...' )
        self.__m_refCallback( title=self.__m_Label )



    ######################### QGraphicsItem func override ################################

    def itemChange( self, change, value ):

        if( change == QGraphicsItem.ItemSelectedChange ):
            if( value == True ):
                self.setZValue( self.zValue() + 1 )
                self.__m_Pen.setColor(g_NodeFrameColor[1])
            else:
                self.setZValue( self.zValue() - 1 )
                self.__m_Pen.setColor(g_NodeFrameColor[0])

        return super(Group, self).itemChange( change, value )


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
        painter.drawRoundedRect( self.__m_DrawRect, g_BoxRoundRadius, g_BoxRoundRadius )

        if( option.levelOfDetailFromTransform(painter.worldTransform()) < 0.5):
            return 
        painter.setFont( self.__m_Font )
        painter.setPen(g_LabelColor)
        painter.drawText( self.__m_LabelRect, Qt.AlignLeft, self.__m_Label )