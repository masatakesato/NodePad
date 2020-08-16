# https://stackoverflow.com/questions/9377914/how-to-customize-title-bar-and-window-of-desktop-application


from .resource import *
from .stylesheet import *

import typing
from enum import IntEnum

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class Region(IntEnum):
    Below   = -1
    Inside  = 0
    Above   = 1



class ResizeHandle(QFrame):
    
    region_info = {
        'TopLeft':    ((-1,-1), Qt.SizeFDiagCursor), 'Top':    ((0,-1), Qt.SizeVerCursor), 'TopRight':    ((1,-1), Qt.SizeBDiagCursor),
        'Left':       ((-1, 0), Qt.SizeHorCursor),   'Center': ((0, 0), Qt.ArrowCursor),   'Right':       ((1, 0), Qt.SizeHorCursor),
        'BottomLeft': ((-1, 1), Qt.SizeBDiagCursor), 'Bottom': ((0, 1), Qt.SizeVerCursor), 'BottomRight': ((1, 1), Qt.SizeFDiagCursor)
    }

    def __init__(self, region='Center', parent=None):
        super(ResizeHandle, self).__init__(parent=parent)
        
        self.setStyleSheet( g_ResizeHandleStyleSheet )
        self.__m_Region = self.region_info[region][0]
        self.__m_Cursor = self.region_info[region][1]


    def Region( self ):
        return self.__m_Region


    def enterEvent( self, event ):
        self.setCursor( self.__m_Cursor )
        return super(ResizeHandle, self).enterEvent(event)


    def leaveEvent( self, event ):
        self.setCursor( Qt.ArrowCursor )
        return super(ResizeHandle, self).leaveEvent(event)




class TitleButton(QFrame):

    clicked = pyqtSignal()

    def __init__( self, *args, **kwargs ):
        super(TitleButton, self).__init__(*args, **kwargs)

        self.setAttribute( Qt.WA_NoMousePropagation )
        self.setFocusPolicy( Qt.NoFocus )
        
        self.setStyleSheet( g_TitleButtonStyleSheet )

        self.__m_Inside = False



    def SetStyleProperty( self, name: str, value: typing.Any ):
        self.setProperty( name, value )
        self.setStyle( self.style() )



    def __UpdateInsideProperty( self, on: bool ):
        self.__m_Inside = on
        self.setProperty('pressed', on )
        self.setStyle( self.style() )



    def mousePressEvent( self, event ):
        #print( 'TitleButton::mousePressEvent()...' )
        self.__UpdateInsideProperty( True )
        return super(TitleButton, self).mousePressEvent(event)



    def mouseMoveEvent( self, event ):
        #print( 'TitleButton::mouseMoveEvent()...' )
        isInside = self.rect().contains( event.pos() ) 
        if( self.__m_Inside != isInside ):
            #print( 'In/Out Changed {}'.format( self.rect().contains( event.pos() ) ) )
            self.__UpdateInsideProperty( isInside )
        return super(TitleButton, self).mouseMoveEvent(event)



    def mouseReleaseEvent( self, event ):
        #print( 'TitleButton::mouseMoveEvent()...' )
        if( self.rect().contains( event.pos() ) ):
            self.clicked.emit()
        self.__UpdateInsideProperty( False )
        return super(TitleButton, self).mouseReleaseEvent(event)




class TitleBar(QFrame):

    def __init__( self, ownerWidget: QWidget ):
        super(TitleBar, self).__init__()

        self.setStyleSheet( g_TitleBarStyleSheet )
        self.setAutoFillBackground( True )
        self.setBackgroundRole( QPalette.Highlight )

        self.__m_MinButton = TitleButton()
        self.__m_MinButton.setProperty( 'icon', 'minimize' )
        self.__m_MinButton.setStyle( self.__m_MinButton.style() )

        self.__m_MaxButton = TitleButton()
        self.__m_MaxButton.setProperty( 'icon', 'maximize' )
        self.__m_MaxButton.setStyle( self.__m_MaxButton.style() )

        self.__m_CloseButton = TitleButton()
        self.__m_CloseButton.setProperty( 'icon', 'close' )
        self.__m_CloseButton.setStyle( self.__m_CloseButton.style() )

        self.__m_Label = QLabel()
        self.__m_Label.setText( 'Window Title' )
        
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.addWidget( self.__m_Label )
        self.hbox.addWidget( self.__m_MinButton )
        self.hbox.addWidget( self.__m_MaxButton )
        self.hbox.addWidget( self.__m_CloseButton )
        self.hbox.insertStretch( 1, 500 )
        self.hbox.setSpacing( 4 )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )
        
        self.setLayout( self.hbox )

        self.__m_CloseButton.clicked.connect( ownerWidget.close )
        self.__m_MinButton.clicked.connect( self.showSmall )
        self.__m_MaxButton.clicked.connect( self.showMaxRestore )

        self.maxNormal = False
        self.moving = False
        self.offset = QPoint()



    def setLabel( self, title ):
        self.__m_Label.setText( title )



    def label( self ) -> str:
        return self.__m_Label.text()



    def showSmall(self):
        self.parent().showMinimized()



    def showMaxRestore(self):
        if(self.maxNormal):
            self.parent().showNormal()
            self.maxNormal = False
            self.__m_MaxButton.SetStyleProperty( 'icon', 'maximize' )
        else:
            self.parent().showMaximized()
            self.maxNormal = True
            self.__m_MaxButton.SetStyleProperty( 'icon', 'restore' )



    def mousePressEvent(self,event):
        if( event.button() == Qt.LeftButton ):
            self.moving = True
            self.offset = self.mapToParent( event.pos() )
        return super(TitleBar, self).mousePressEvent(event)



    def mouseMoveEvent( self, event ):
        self.setCursor(Qt.ArrowCursor)
        if( self.moving and self.maxNormal==False ):
            self.parent().move( event.globalPos() - self.offset )
        return super(TitleBar, self).mouseMoveEvent(event)



    def mouseReleaseEvent( self, event ):
        self.moving = False
        return super(TitleBar, self).mouseReleaseEvent(event)








class Frame(QFrame):

    TopLeft = 1
    Top = 2
    TopRight = 3
    Left = 4
    Right = 5
    BottomLeft = 6
    Bottom = 7
    BottomRight = 8


    def __init__(self, parent=None):
        super(Frame, self).__init__(parent=parent)
        
        self.setFrameShape( QFrame.StyledPanel )
        self.setStyleSheet( g_MainWindowStyleSheet )
        self.setWindowFlags( Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint )
        self.m_titleBar = TitleBar( self )
        self.m_content = QFrame()
        self.m_content.setStyleSheet( g_StaticFrameStyleSheet )

        self.framelayout = QVBoxLayout()
        self.framelayout.setSpacing( 0 )
        self.framelayout.addWidget( self.m_titleBar )
        self.framelayout.addWidget( self.m_content )
        self.framelayout.setContentsMargins( 0, 0, 0, 0 )
     
        #self.contentlayout = QVBoxLayout()
        #self.contentlayout.setSpacing( 0 )
        #self.contentlayout.addWidget( self.m_content )
        #self.contentlayout.setContentsMargins( 0, 0, 0, 0 )
        
        #self.framelayout.addLayout( self.contentlayout )
        super(Frame, self).setLayout( self.framelayout )#self.setLayout(framelayout)
       
        self.__m_Margin = 5

        self.handleSelected = None
        self.__m_mousePressPos = QPoint()
        self.__m_mousePressRect = None

        self.handles = {}
        self.handles[self.Top] = ResizeHandle( 'Top', self )
        self.handles[self.Bottom] = ResizeHandle( 'Bottom', self )
        self.handles[self.Left] = ResizeHandle( 'Left', self )
        self.handles[self.Right] = ResizeHandle( 'Right', self )
        self.handles[self.TopRight] = ResizeHandle( 'TopRight', self )
        self.handles[self.BottomRight] = ResizeHandle( 'BottomRight', self )
        self.handles[self.BottomLeft] = ResizeHandle( 'BottomLeft', self )
        self.handles[self.TopLeft] = ResizeHandle( 'TopLeft', self )


        minimizeAction = QAction( 'Minimize', self )
        minimizeAction.triggered.connect( self.showMinimized )
        restoreAction = QAction( 'Restore', self )
        restoreAction.triggered.connect( self.showNormal )

        trayIconMenu = QMenu( self)
        trayIconMenu.addAction( minimizeAction )
        trayIconMenu.addAction( restoreAction )

        self.__m_TrayIconMenu = QSystemTrayIcon( self )
        self.__m_TrayIconMenu.setContextMenu( trayIconMenu )



    def contentWidget(self):
        return self.m_content



    def titleBar( self ):
        return self.m_titleBar



    def handleAt( self, point ):        
        for k, v, in self.handles.items():
            if( v.geometry().contains(point) ):
                return v.Region()#k#
        return None



    def mousePressEvent( self, event ):
        self.handleSelected = self.handleAt( event.pos() )
        if( self.handleSelected ):
            self.__m_mousePressPos = event.globalPos()
            self.__m_mousePressRect = self.geometry()

        return super(Frame, self).mousePressEvent(event)



    def mouseMoveEvent( self, event ):
        if( self.handleSelected ):
            self.__InteractiveResize( event.globalPos() )
            return
        return super(Frame, self).mouseMoveEvent(event)



    def mouseReleaseEvent( self, event ):
        self.handleSelected = None
        #self.__m_mousePressPos = None
        #self.__m_mousePressRect = None
        return super(Frame, self).mouseReleaseEvent(event)



    def resizeEvent( self, QResizeEvent ):
        self.__UpdateHandlesPos()
        return super(Frame, self).resizeEvent(QResizeEvent)
        


    def showMaximized( self ):
        for handle in self.handles.values():
            handle.hide()
        return super(Frame, self).showMaximized()



    def showNormal( self ):
        for handle in self.handles.values():
            handle.show()
        return super(Frame, self).showNormal()



    def setWindowTitle( self, title: str ) -> None:
        self.m_titleBar.setLabel(title)



    def windowTitle( self ) -> str:
        return self.m_titleBar.label()



    def layout( self ):
        return self.m_content.layout()



    def setLayout( self, layout ):
        return self.m_content.setLayout(layout)



    def __InteractiveResize( self, mousePos ):

        region = self.handleSelected
        dx = mousePos.x() - self.__m_mousePressPos.x()
        dy = mousePos.y() - self.__m_mousePressPos.y()
        offset = [0,0,0,0]

        if( region[0] == Region.Below ):
            # "mousePressRect.width - dx" must be in range [ minimumWidth, maximumWidth ].
            offset[0] = min( max( self.__m_mousePressRect.width()-self.maximumWidth(), dx ), self.__m_mousePressRect.width()-self.minimumWidth() )
        elif( region[0] == Region.Above ):
            offset[2] = dx

        if( region[1] == Region.Below ):
            # "mousePressRect.height - dy" must be in range [ minimumHeight, maximumHeight ].
            offset[1] = min( max( self.__m_mousePressRect.height()-self.maximumHeight(), dy ), self.__m_mousePressRect.height() - self.minimumHeight() )

        elif( region[1] == Region.Above ):
            offset[3] = dy

        self.setGeometry( self.__m_mousePressRect.adjusted( offset[0], offset[1], offset[2], offset[3] ) )



    def __UpdateHandlesPos( self ):

        self.handles[self.Top].setGeometry( self.__m_Margin, 0, self.width()-self.__m_Margin*2, self.__m_Margin )
        self.handles[self.Bottom].setGeometry(self.__m_Margin, self.height()-self.__m_Margin, self.width()-self.__m_Margin*2, self.__m_Margin )
        self.handles[self.Left].setGeometry( 0, self.__m_Margin, self.__m_Margin, self.height()-self.__m_Margin*2 )
        self.handles[self.Right].setGeometry( self.width()-self.__m_Margin, self.__m_Margin, self.__m_Margin, self.height()-self.__m_Margin*2 )
 
        self.handles[self.TopRight].setGeometry( self.width()-self.__m_Margin, 0, self.__m_Margin, self.__m_Margin )
        self.handles[self.BottomRight].setGeometry( self.width()-self.__m_Margin, self.height()-self.__m_Margin, self.__m_Margin, self.__m_Margin )
        self.handles[self.BottomLeft].setGeometry( 0, self.height()-self.__m_Margin, self.__m_Margin, self.__m_Margin )
        self.handles[self.TopLeft].setGeometry( 0, 0, self.__m_Margin, self.__m_Margin )



    #============== Size edit method wrapper for borderless window ===============#
    def Width( self ) -> int: ...
    def Height( self ) -> int: ...
    def Size( self ) -> QSize: ...

    def MaximumWidth( self ) -> int: ...
    def MaximumHeight( self ) -> int: ...
    def MaximumSize( self ) -> QSize: ...

    def MinimumWidth( self ) -> int: ...
    def MinimumHeight( self ) -> int: ...
    def MinimumSize( self ) -> QSize: ...


    def Resize( self, w: int, h: int ) -> None:# ...
        margins = self.contentsMargins()
        self.resize( w + margins.left() + margins.right(), h + margins.top() + margins.bottom() + self.m_titleBar.height() )


    def Resize_( self, s: QSize ) -> None:# ...
        margins = self.contentsMargins()
        s.setWidth( s.width() + margins.left() + margins.right() )
        s.setHeight( s.height() + margins.top() + margins.bottom() + self.m_titleBar.height() )
        self.resize( s )


    def SetFixedHeight( self, h: int ) -> None: ...
    def SetFixedWidth( self, w: int ) -> None: ...
    def SetFixedSize( self, w: int, h: int ) -> None: ...
    def SetFixedSize_( self, s: QSize ) -> None: ...

    def SetGeometry( self, x: int, y: int, w: int, h: int ) -> None: ...
    def SetGeometry_( self, r: QRect ) -> None: ...

    def SetMaximumWidth( self, maxw: int ) -> None: ...
    def SetMaximumHeight( self, maxh: int ) -> None: ...
    def SetMaximumSize( self, maxw: int, maxh: int ) -> None: ...
    def SetMaximumSize_( self, s: QSize ) -> None: ...

    def SetMinimumWidth( self, minw: int ) -> None: ...
    def SetMinimumHeight( self, minh: int ) -> None: ...
    def SetMinimumSize( self, minw: int, minh: int ) -> None: ...
    def SetMinimumSize_( self, s: QSize ) -> None: ...