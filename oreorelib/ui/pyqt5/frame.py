# https://stackoverflow.com/questions/9377914/how-to-customize-title-bar-and-window-of-desktop-application


from .resource import *
from .stylesheet import *

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






class TitleBar(QFrame):

    def __init__(self, parent=None):
        super(TitleBar, self).__init__(parent=parent)

        self.setStyleSheet( g_TitleBarStyleSheet )
        self.setMouseTracking( True )
        self.setAutoFillBackground( True )
        self.setBackgroundRole( QPalette.Highlight )
        #self.setStyleSheet( css_titlebar )

        self.__m_IconMinimize = QIcon( ':/resource/images/minimize.png' )
        self.__m_IconMaximize = QIcon( ':/resource/images/maximize.png' )
        self.__m_IconRestore = QIcon( ':/resource/images/restore.png' )
        self.__m_IconClose = QIcon( ':/resource/images/close.png' )


        self.__m_MinButton = QPushButton( self )
        #self.__m_MinButton.setStyleSheet( css_button )
        self.__m_MinButton.setIcon( self.__m_IconMinimize )

        self.__m_MaxButton = QPushButton( self )
        #self.__m_MaxButton.setStyleSheet( css_button )
        self.__m_MaxButton.setIcon( self.__m_IconMaximize )

        self.__m_CloseButton = QPushButton( self )
        #self.__m_CloseButton.setStyleSheet( css_button )
        self.__m_CloseButton.setIcon( self.__m_IconClose )

        self.__m_MinButton.setMinimumHeight( 10 )
        self.__m_CloseButton.setMinimumHeight( 10 )
        self.__m_MaxButton.setMinimumHeight( 10 )

        self.__m_Label = QLabel( self )
        #self.__m_Label.setStyleSheet( css_label )
        self.__m_Label.setText( 'Window Title' )
        hbox = QHBoxLayout( self )
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget( self.__m_Label )
        hbox.addWidget( self.__m_MinButton )
        hbox.addWidget( self.__m_MaxButton )
        hbox.addWidget( self.__m_CloseButton )
        hbox.insertStretch( 1, 500 )
        hbox.setSpacing( 4 )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )
        
        self.__m_CloseButton.clicked.connect( self.parent().close )
        self.__m_MinButton.clicked.connect( self.showSmall )
        self.__m_MaxButton.clicked.connect( self.showMaxRestore )

        self.maxNormal = False
        self.moving = False
        self.offset = QPoint()



    def setLabel( self, title ):
        self.__m_Label.setText( title )



    def showSmall(self):
        self.parent().showMinimized()



    def showMaxRestore(self):
        if(self.maxNormal):
            self.parent().showNormal()
            self.maxNormal = False
            self.__m_MaxButton.setIcon( self.__m_IconMaximize )
        else:
            self.parent().showMaximized()
            self.maxNormal = True
            self.__m_MaxButton.setIcon( self.__m_IconRestore )



    def mousePressEvent(self,event):
        if( event.button() == Qt.LeftButton ):
            self.moving = True
            self.offset = event.pos()
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
        self.setMouseTracking( True )
        self.m_titleBar = TitleBar( self )
        self.m_content = QFrame( self )
        self.m_content.setStyleSheet( g_StaticFrameStyleSheet )

        self.framelayout = QVBoxLayout()
        self.framelayout.setSpacing( 0 )
        self.framelayout.addWidget( self.m_titleBar )
        self.framelayout.setContentsMargins( 0, 0, 0, 0 )
     
        self.contentlayout = QVBoxLayout()
        self.contentlayout.setSpacing( 0 )
        self.contentlayout.addWidget( self.m_content )
        self.contentlayout.setContentsMargins( 0, 0, 0, 0 )
        
        self.framelayout.addLayout( self.contentlayout )
        super(Frame, self).setLayout( self.framelayout )#self.setLayout(framelayout)
       
        self.__m_Margin = 5

        self.__m_CurrentPos = QPoint()
        
        self.handleSelected = None
        self.__m_mousePressPos = None
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
        self.__m_mousePressPos = None
        self.__m_mousePressRect = None
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



    def setWindowTitle( self, title ):
        self.m_titleBar.setLabel(title)



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





    # Original __InteractiveResize method. Deprecated. 2019.06.05
    #def __InteractiveResize( self, mousePos ):

    #    if( self.handleSelected == self.TopLeft ):
    #        #diff_x = ( mousePos.x() - self.__m_mousePressPos.x() ) * ( mousePos.x()<=self.__m_mousePressPos.x() or self.width()>self.minimumWidth() ) * ( self.width()<self.maximumWidth() )
    #        diff_x = mousePos.x() - self.__m_mousePressPos.x()
    #        diff_x = min( self.__m_mousePressRect.width() - self.minimumWidth(), diff_x )# "pressrect.width - diff_x" must be greater equal "min width"
    #        diff_x = max( self.__m_mousePressRect.width() - self.maximumWidth(), diff_x )# "pressrect.width - diff_x" must be lesser equal "max width"
    #        #diff_y = ( mousePos.y() - self.__m_mousePressPos.y() ) * ( mousePos.y()<=self.__m_mousePressPos.y() or self.height()>self.minimumHeight() ) * ( self.height()<self.maximumHeight() )
    #        diff_y = mousePos.y() - self.__m_mousePressPos.y()
    #        diff_y = min( self.__m_mousePressRect.height() - self.minimumHeight(), diff_y )# "pressrect.height - diff_y" must be greater equal "min height"
    #        diff_y = max( self.__m_mousePressRect.height() - self.maximumHeight(), diff_y )# "pressrect.height - diff_y" must be lesser equal "max height"

    #        self.setGeometry( self.__m_mousePressRect.adjusted( diff_x, diff_y, 0, 0 ) )


    #    elif( self.handleSelected == self.Top ):
    #        #diff_y = ( mousePos.y() - self.__m_mousePressPos.y() ) * ( mousePos.y()<=self.__m_mousePressPos.y() or self.height()>self.minimumHeight() ) * ( self.height()<self.maximumHeight() )
    #        diff_y = mousePos.y() - self.__m_mousePressPos.y()
    #        diff_y = min( self.__m_mousePressRect.height() - self.minimumHeight(), diff_y )# "pressrect.height - diff_y" must be greater equal "min height"
    #        diff_y = max( self.__m_mousePressRect.height() - self.maximumHeight(), diff_y )# "pressrect.height - diff_y" must be lesser equal "max height"

    #        self.setGeometry( self.__m_mousePressRect.adjusted( 0, diff_y, 0, 0 ) )


    #    elif( self.handleSelected == self.TopRight ):
    #        diff_x = mousePos.x() - self.__m_mousePressPos.x()
    #        #diff_y = ( mousePos.y() - self.__m_mousePressPos.y() ) * ( mousePos.y()<=self.__m_mousePressPos.y() or self.height()>self.minimumHeight() ) * ( self.height()<self.maximumHeight() )
    #        diff_y = mousePos.y() - self.__m_mousePressPos.y()
    #        diff_y = min( self.__m_mousePressRect.height() - self.minimumHeight(), diff_y )# "pressrect.height - diff_y" must be greater equal "min height"
    #        diff_y = max( self.__m_mousePressRect.height() - self.maximumHeight(), diff_y )# "pressrect.height - diff_y" must be lesser equal "max height"

    #        self.setGeometry( self.__m_mousePressRect.adjusted( 0, diff_y, diff_x, 0 ) )


    #    elif( self.handleSelected == self.Left ):
    #        #diff = ( mousePos.x() - self.__m_mousePressPos.x() ) * ( mousePos.x()<=self.__m_mousePressPos.x() or self.width()>self.minimumWidth() ) * ( self.width()<self.maximumWidth() )
    #        diff_x = mousePos.x() - self.__m_mousePressPos.x()
    #        diff_x = min( self.__m_mousePressRect.width() - self.minimumWidth(), diff_x )# "pressrect.width - diff_x" must be greater equal "min width"
    #        diff_x = max( self.__m_mousePressRect.width() - self.maximumWidth(), diff_x )# "pressrect.width - diff_x" must be lesser equal "max width"

    #        self.setGeometry( self.__m_mousePressRect.adjusted( diff_x, 0, 0, 0 ) )


    #    elif( self.handleSelected == self.Right ):
    #        diff = mousePos.x() - self.__m_mousePressPos.x()

    #        self.setGeometry( self.__m_mousePressRect.adjusted( 0, 0, diff, 0 ) )


    #    elif( self.handleSelected == self.BottomLeft ):
    #        #diff_x = ( mousePos.x() - self.__m_mousePressPos.x() ) * ( mousePos.x()<=self.__m_mousePressPos.x() or self.width()>self.minimumWidth() ) * ( self.width()<self.maximumWidth() )
    #        diff_x = mousePos.x() - self.__m_mousePressPos.x()
    #        diff_x = min( self.__m_mousePressRect.width() - self.minimumWidth(), diff_x )# "pressrect.width - diff_x" must be greater equal "min width"
    #        diff_x = max( self.__m_mousePressRect.width() - self.maximumWidth(), diff_x )# "pressrect.width - diff_x" must be lesser equal "max width"
    #        diff_y = mousePos.y() - self.__m_mousePressPos.y()

    #        self.setGeometry( self.__m_mousePressRect.adjusted( diff_x, 0, 0, diff_y ) )


    #    elif( self.handleSelected == self.Bottom ):
    #        diff = mousePos.y() - self.__m_mousePressPos.y()

    #        self.setGeometry( self.__m_mousePressRect.adjusted( 0, 0, 0, diff ) )


    #    elif( self.handleSelected == self.BottomRight ):
    #        diff_x = mousePos.x() - self.__m_mousePressPos.x()
    #        diff_y = mousePos.y() - self.__m_mousePressPos.y()

    #        self.setGeometry( self.__m_mousePressRect.adjusted( 0, 0, diff_x, diff_y ) )


    #    #self.__UpdateHandlesPos()# resizeEventで呼び出すようにした. 2019.06.07
