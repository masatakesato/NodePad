from .frame import *
from .stylesheet import *



class MainWindow(Frame):

    def __init__( self, parent=None ):
        super(MainWindow, self).__init__(parent=parent)

        self.__m_MenuBar = QMenuBar( self )
        self.__m_MenuBar.setStyleSheet( g_MenuBarStyleSheet + g_MenuStyleSheet )
        self.__m_MenuBar.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )
        self.framelayout.insertWidget( 1, self.__m_MenuBar )

        self.__m_StatusBar = None



    def setMenuBar( self, menubar ):
        if( self.__m_MenuBar ):
            self.__m_MenuBar.hide()
            self.__m_MenuBar.deleteLater()

        self.__m_MenuBar = menubar
        self.__m_MenuBar.setStyleSheet( g_MenuBarStyleSheet + g_MenuStyleSheet )
        self.__m_MenuBar.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )
        self.framelayout.insertWidget( 1, self.__m_MenuBar )



    def menuBar( self ):
        return self.__m_MenuBar



    def centralWidget( self ):
        return self.m_content



    def setCentralWidget( self, widget ):
        if( self.m_content ):
            self.m_content.hide()
            self.m_content.deleteLater()
        self.m_content = widget
        self.m_content.setSizePolicy( QSizePolicy.Preferred, QSizePolicy.Preferred )
        self.framelayout.addWidget( self.m_content )#self.contentlayout.addWidget( self.m_content )



    def tekeCentralWidget( self ):
        widget = self.m_content
        widget.setParent(None)
        self.m_content = QWidget(self)
        
        return widget



    def statusBar( self ):
        return self.__m_StatusBar



    def setStatusBar( self, statusbar ):
        if( self.__m_StatusBar ):
            self.__m_StatusBar.hide()
            self.__m_StatusBar.deleteLater()
        self.__m_StatusBar = statusbar
        self.__m_StatusBar.setStyleSheet( g_StatusBarStyleSheet )
        self.__m_StatusBar.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )
        self.framelayout.insertWidget( 4, self.__m_StatusBar )



    def event( self, event ):
        if( event.type()==QEvent.StatusTip ):
            if( self.__m_StatusBar ): self.__m_StatusBar.showMessage( event.tip() )

        return super(Frame, self).event(event)
