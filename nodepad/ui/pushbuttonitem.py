from ..component.descriptors import *

from .graphicssettings import *
from .graphicsitembase import GraphicsNodeItem




# http://www.gulon.co.uk/2015/05/20/python-enums-as-flags/
class MouseState():
    # States
    OutsideReleased = 0b00
    OutsidePressed  = 0b01
    InsideReleased  = 0b10
    InsidePressed   = 0b11
    # State switch masks
    ButtonMask      = 0b01
    HoverMask       = 0b10


class PushButton(GraphicsNodeItem):

    def __init__( self, pixmap, callback, *args, **kwargs ):
        super(PushButton, self).__init__(*args, **kwargs)

        self.__m_ID = id(self)

        self.__m_DrawRect = QRectF(0,0,g_ButtonSize,g_ButtonSize)
        self.__m_BoundingRect = self.__m_DrawRect.adjusted( -g_ButtonFrameWidth, -g_ButtonFrameWidth, g_ButtonFrameWidth, g_ButtonFrameWidth )
        self.__m_Shape = QPainterPath()
        self.__m_Shape.addRect( self.__m_BoundingRect )
        self.__m_Pen = QPen( g_ButtonFrameColor[0], g_ButtonFrameWidth )
        
        self.__m_refPixmap = pixmap.scaledToWidth( g_ButtonSize, Qt.SmoothTransformation )
        self.__m_refCallback = callback# directly binding external callback function, because QGraphisItem cannot emit signals
        self.__m_MouseState = MouseState.OutsideReleased

        self.__m_Gradients = {
            MouseState.OutsideReleased: QLinearGradient(0,0,0,g_ButtonSize),
            MouseState.OutsidePressed: QLinearGradient(0,0,0,g_ButtonSize),
            MouseState.InsideReleased: QLinearGradient(0,0,0,g_ButtonSize),
            MouseState.InsidePressed: QLinearGradient(0,0,0,g_ButtonSize),
            }

        self.__m_Gradients[ MouseState.OutsideReleased ].setColorAt( 0, QColor(48,48,48) )
        self.__m_Gradients[ MouseState.OutsideReleased ].setColorAt( 0.49999, QColor(64,64,64) )

        self.__m_Gradients[ MouseState.OutsidePressed ].setColorAt( 0, QColor(48,48,48) )
        self.__m_Gradients[ MouseState.OutsidePressed ].setColorAt( 0.49999, QColor(64,64,64) )

        self.__m_Gradients[ MouseState.InsideReleased ].setColorAt( 0, QColor(64,64,64) )
        self.__m_Gradients[ MouseState.InsideReleased ].setColorAt( 0.49999, QColor(128,128,128) )

        self.__m_Gradients[ MouseState.InsidePressed ].setColorAt( 0, QColor(32,32,32) )
        self.__m_Gradients[ MouseState.InsidePressed ].setColorAt( 0.49999, QColor(64,64,64) )

        self.setAcceptHoverEvents( True )
        self.setAcceptTouchEvents( True )



    def ID( self ):
        return self.__m_ID


    def hoverEnterEvent( self, event ):
        super(PushButton, self).hoverMoveEvent(event)
        self.__m_MouseState ^= MouseState.HoverMask
        self.__m_Pen.setColor( g_ButtonFrameColor[1] )
        self.update()


    def hoverLeaveEvent( self, event ):
        super(PushButton, self).hoverLeaveEvent(event)
        self.__m_MouseState ^= MouseState.HoverMask
        self.__m_Pen.setColor( g_ButtonFrameColor[0] )


    def mousePressEvent( self, event ):
        self.setFlag( QGraphicsItem.ItemIsSelectable, True )# マウスボタンが押されている間だけ一時的に選択可能状態にする. mouseReleaseEventは選択可能状態でしか起動しないため.
        super(PushButton, self).mousePressEvent(event)
        self.__m_MouseState ^= MouseState.ButtonMask


    def mouseReleaseEvent( self, event ):
        if( self.sceneBoundingRect().contains( event.scenePos() ) ):
            self.__m_refCallback()
        self.setFlag( QGraphicsItem.ItemIsSelectable, False )# マウスボタンがリリースされたらすぐ選択不可状態に戻す. QGraphicsScene::selectedItemsに登録されるのを防ぐため.
        super(PushButton, self).mouseReleaseEvent(event)
        self.__m_MouseState ^= MouseState.ButtonMask


    def boundingRect(self):
        return self.__m_BoundingRect


    def shape( self ):
        if( self.scene().FocusViewID() != self._GraphicsNodeItem__m_RenderLayerID ):# QGraphicsViewごとにアイテムの表示/非表示を視切り替えて正しく動かすのに必要
            return QPainterPath()
        return self.__m_Shape


    def paint(self, painter, option, widget):
        #print('paint')
        if( self.scene().IsVisibleFromActiveView(self)==False ):
            return
        painter.setClipRect(option.exposedRect)
        painter.setBrush( self.__m_Gradients[ self.__m_MouseState ] )
        painter.setPen(self.__m_Pen)
        painter.drawRoundedRect( self.__m_DrawRect, g_ButtonRoundRadius, g_ButtonRoundRadius )

        if( option.levelOfDetailFromTransform(painter.worldTransform()) < 0.5):
            return
        painter.drawPixmap( self.__m_DrawRect, self.__m_refPixmap, self.__m_DrawRect )