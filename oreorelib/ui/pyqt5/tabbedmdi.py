from .frame import *

from enum import Enum
import typing
import traceback




# Dockable's duration
class Duration(Enum):
    Persistent = 0x00 # Dockable remains even if no child tab exists.
    Volatile = 0x01   # Automatically deleted if no child tab exists.




class Floater(Frame):

    # Signals
    SelectSignal = pyqtSignal(object)
    MoveSignal = pyqtSignal(object, QPoint)
    ReleaseSignal = pyqtSignal(QPoint)
    CloseSignal = pyqtSignal(object)



    def __init__( self, *args, **kwargs ):
        super(Floater, self).__init__(*args, **kwargs)

        self.setLayout( QVBoxLayout() )
        self.__m_Attribs = {}
        self.__m_ID = id(self)



    def Release( self ):
        if( self.receivers(self.SelectSignal) ):
            self.SelectSignal.disconnect()

        if( self.receivers(self.MoveSignal) ):
            self.MoveSignal.disconnect()

        if( self.receivers(self.ReleaseSignal) ):
            self.ReleaseSignal.disconnect()



    def ID( self ):
        return self.__m_ID



    def SetAttribs( self, attribs: dict ) -> None:
        self.__m_Attribs = attribs



    def GetAttribs( self ) -> dict:
        return self.__m_Attribs



    def mousePressEvent( self, event ):
        super(Floater, self).mousePressEvent(event)
        print( 'Floater::mousePressEvent()...' )
        if( self.handleSelected is None ):
            self.SelectSignal.emit( self.__m_ID )


    
    def mouseMoveEvent( self, event ):
        print( 'Floater::mouseMoveEvent()...' )
        # Avoid docking at the end of widget resize operation
        if( self.handleSelected is None ):
            self.MoveSignal.emit( self.__m_ID, event.globalPos() )

        return super(Floater, self).mouseMoveEvent(event)



    def mouseReleaseEvent( self, event ):
        print( 'Floater::mouseReleaseEvent()...' )
        # Avoid docking at the end of widget resize operation
        if( self.handleSelected is None ):
            self.ReleaseSignal.emit( event.globalPos() )

        return super(Floater, self).mouseReleaseEvent(event)
        


    def closeEvent( self, event ):
        self.Release()
        super(Floater, self).closeEvent(event)
        self.CloseSignal.emit( self.__m_ID )




class TabBar(QTabBar):

    # Signals
    DetachWidgetSignal = pyqtSignal(int)
    AttachWidgetSignal = pyqtSignal(QPoint)
    DragWidgetSignal = pyqtSignal(QPoint)

    # Drag mode
    __DRAG_NONE__ = -1
    __DRAG_TAB__ = 0
    __DRAG_WIDGET__ = 1

    # State change patterns...
    # __DRAG_NONE__ -> __DRAG_NONE__
    # __DRAG_NONE__ -> __DRAG_TAB__ -> __DRAG_NONE__
    # __DRAG_NONE__ -> __DRAG_TAB__ -> __DRAG_WIDGET__ -> __DRAG_NONE__



    def __init__( self, *args, **kwargs ):
        super(TabBar, self).__init__(*args, **kwargs)

        self.setTabsClosable( True )
        self.setMovable(False)# Disable default tab drag feature.
        self.setAttribute( Qt.WA_NoMousePropagation )# Avoid mouse event propagation to parent widget(TabWidget, OwnerFrame...)

        # Create Hooter tab. Used for mouse intersection.
        self.insertTab( 0, '        ' )
        self.setTabEnabled( 0, False )
        self.__m_CloseButtonSize = ( self.tabButton(0, QTabBar.RightSide).width(), self.tabButton(0, QTabBar.RightSide).height() )
        self.tabButton( 0, QTabBar.RightSide ).resize( 0, 0 )# set tabbutton size to zero(unclickable).

        self.__m_CurrentIndex = -1
        self.__m_DragMode = TabBar.__DRAG_NONE__
        self.__m_FocusIndex = -1
        


    def NumActiveTabs( self ) -> int:
        return self.count() - 1



    def SetFocusIndex( self, index ):
        if( self.__m_FocusIndex!=index ):
            print( 'TabBar::SetFocusIndex()...%s: %d' % ( self.parentWidget().windowTitle(), index ) )
            self.__m_FocusIndex = index
            self.update()



    def SetTabClosable( self, index: int, on: bool ) -> None:
        self.tabButton( index, QTabBar.RightSide ).resize( self.__m_CloseButtonSize[0]*int(on), self.__m_CloseButtonSize[1]*int(on) )



    def IsTabClosable( self, index: int ) -> bool:
        return self.tabButton( index, QTabBar.RightSide ).size().isEmpty()==False



    def tabInserted( self, index ):
        print( 'TabBar::tabInserted(%d)' % index )
        self.setCurrentIndex(index)
        #return super(TabWidget, self).tabInserted(index)
        


    def tabRemoved( self, index ):
        print( 'TabBar::tabRemoved(%d)' % index )
        self.setCurrentIndex( max(min(index, self.count()-2), 0) )# clamp current index range to [ 0, NumActiveTabs()-1 ]
        #return super(TabWidget, self).tabRemoved(index)



    def mousePressEvent( self, event ):
        print( 'TabBar::mousePressEvent()...' )

        self.__m_CurrentIndex = self.tabAt( event.pos() )

        # Triggers tab drag operations ONLY WHEN LEFT MOUSE PRESSED.
        if( event.button()==Qt.LeftButton ):# and self.__m_CurrentIndex != self.NumActiveTabs() ):
            if( self.__m_CurrentIndex == self.NumActiveTabs() ):
                event.ignore()
            else:
                self.setCurrentIndex( self.__m_CurrentIndex )
                self.__m_DragMode = TabBar.__DRAG_TAB__

        return super(TabBar, self).mousePressEvent(event)



    def mouseMoveEvent( self, event ):
        #print( 'TabBar::mouseMoveEvent()...' )
        pos = event.pos()

        if( self.__m_DragMode==TabBar.__DRAG_WIDGET__ ):
            self.DragWidgetSignal.emit( event.globalPos() )
            event.ignore()

        elif( self.__m_DragMode==TabBar.__DRAG_TAB__ ):
            # Mouse is moving inside QTabBar area
            if( self.rect().contains(pos) ):
                index = self.tabAt(pos)
                if( index != self.__m_CurrentIndex and index != self.NumActiveTabs() ):
                    self.moveTab( self.__m_CurrentIndex, index )
                    self.__m_CurrentIndex = index
            # Mouse has just moved outside QTabBar area
            else:
                self.__m_DragMode = TabBar.__DRAG_WIDGET__
                self.DetachWidgetSignal.emit( self.__m_CurrentIndex )

        #else:# TabBar.__DRAG_NONE__
        #    pass

        return super(TabBar, self).mouseMoveEvent(event)
        


    def mouseReleaseEvent( self, event ):
        print( 'TabBar::mouseReleaseEvent()...' )
        
        # Detached widget has been released inside QTabBar area
        if( self.__m_DragMode==TabBar.__DRAG_WIDGET__ ):
            self.AttachWidgetSignal.emit( event.globalPos() )

        self.__m_CurrentIndex = -1
        self.__m_DragMode = TabBar.__DRAG_NONE__

        return super(TabBar, self).mouseReleaseEvent(event)



# https://stackoverflow.com/questions/58250870/pyqt5-adding-add-and-remove-widget-buttons-beside-every-tab
# https://forum.qt.io/topic/92923/qtabbar-paintevent-issue/4
# https://stackoverflow.com/questions/49464153/giving-a-color-to-single-tab-consumes-too-much-processing-power
    def paintEvent( self, event ):
        super(TabBar, self).paintEvent(event)

        if( self.__m_FocusIndex!=-1 ):
            painter = QPainter(self)
            option = QStyleOptionTab()
            self.initStyleOption( option, self.__m_FocusIndex )

            palette = self.palette()
            palette.setColor( palette.Button, QColor(36,36,36) )
            #palette.setColor( palette.Window, QColor(232,232,232) )
            #palette.setColor( palette.Background, QColor(42,42,42,0) )
            option.palette = palette

            self.style().drawControl( QStyle.CE_TabBarTabShape, option, painter )




# TabWidget
class TabWidget(QTabWidget):
    
    # Signals
    RaiseSignal = pyqtSignal(object)
    MoveSignal = pyqtSignal(object, QPoint)
    ReleaseSignal = pyqtSignal(object, QPoint)
    CloseSignal = pyqtSignal(object)

    # TabWidget Lock modes
    __ACTIVE__ = 0  
    __LOCKED__ = 1  # Drag and Drop feature is disabled
    __TRASHED__ = 2 # TabWidget will be deleted at TabbedMDIManager::__Cleanup()


    
    def __init__( self, *args, **kwargs ):
        super(TabWidget, self).__init__(*args, **kwargs)
        
        # Setup custom QTabBar
        self.__m_TabBar = TabBar(self)
        self.setTabBar( self.__m_TabBar )

        self.setWindowTitle( '        ' )
        self.setStyleSheet( g_TabWidgetStyleSheet )
        self.setAttribute( Qt.WA_NoMousePropagation )# Avoid mouse event propagation to parent widget(OwnerFrame...)
        self.setFocusPolicy( Qt.StrongFocus )

        self.tabCloseRequested.connect( self.__CloseTab )

        self.__m_Status = TabWidget.__ACTIVE__

        self.__m_Duration = Duration.Volatile
        # True: TabWidget will be destroyed automatically if no active tab exists.
        # False: TabWidget is persistent regardless of active tab existence.

        self.__m_ID = id(self)#kwargs['widget_id'] if 'widget_id' in kwargs else id(self)



    def Release( self ):
        if( self.receivers(self.RaiseSignal) ):
            self.RaiseSignal.disconnect()

        if( self.receivers(self.MoveSignal) ):
            self.MoveSignal.disconnect()

        if( self.receivers(self.ReleaseSignal) ):
            self.ReleaseSignal.disconnect()



    def ID( self ):
        return self.__m_ID



    def SetDuration( self, duration: Duration ) -> None:
        #print( 'TabWidget::SetDuration( {} )...'.format( duration ) )
        self.__m_Duration = duration



    def IsPersistent( self ) -> bool:
        return self.__m_Duration == Duration.Persistent



    def IsVolatile( self ) -> bool:
        return self.__m_Duration == Duration.Volatile



    def SetLock( self, on: bool ) -> None:
        #print( 'TabWidget::SetLock( %r )...' % on )
        self.__m_Status = int(on) and TabWidget.__LOCKED__



    def IsLocked( self ) -> bool:
        return self.__m_Status == TabWidget.__LOCKED__



    def SetTrash( self, on: bool ) -> None:
        #print( 'TabWidget::SetTrash( %r )...' % on )
        self.__m_Status = int(on) and TabWidget.__TRASHED__
        self.setWindowOpacity( float(not on) )



    def IsTrashed( self ) -> bool:
        return self.__m_Status == TabWidget.__TRASHED__



    def IsActive( self ) -> bool:
        return self.__m_Status == TabWidget.__ACTIVE__



    def NumActiveTabs( self ) -> int:
        return self.count() - 1# equivalent to self.__m_TabBar.NumActiveTabs()



    def SetTabClosable( self, index: int, on: bool ) -> None:
        self.__m_TabBar.SetTabClosable( index, on )



    def IsTabClosable( self, index: int ) -> bool:
        return self.__m_TabBar.IsTabClosable( index )



    #def mousePressEvent( self, event ):
    #    #print( 'TabWidget::mousePressEvent()...' )
    #    return super(TabWidget, self).mousePressEvent(event)



    def mouseMoveEvent( self, event ):
        #print( 'TabWidget::mouseMoveEvent()...' )
        self.MoveSignal.emit( self.__m_ID, event.globalPos() )
        return super(TabWidget, self).mouseMoveEvent(event)



    def mouseReleaseEvent( self, event ):
        #print( 'TabWidget::mouseReleaseEvent()...' )
        self.ReleaseSignal.emit( self.__m_ID, event.globalPos() )
        return super(TabWidget, self).mouseReleaseEvent(event)



    def changeEvent( self, event ):
        #print( 'TabWidget::changeEvent()...' )
        if( event.type()==QEvent.ActivationChange and self.isActiveWindow() ):
            self.RaiseSignal.emit( self.__m_ID )
        return super(TabWidget, self).changeEvent(event)



    def closeEvent( self, event ):
        #print( 'TabWidget::closeEvent()...' )
        super(TabWidget, self).closeEvent(event)
        self.CloseSignal.emit( self.__m_ID )



    def __CloseTab( self, index: int ):
        print( 'TabWidget::__CloseTab()...%d' % index )
        self.widget(index).setParent(None)
        if( self.NumActiveTabs() < 1 and self.__m_Duration==Duration.Volatile ):# if tab widget is dynamic and no active tab remains, mark as trash.
            self.__m_Status = TabWidget.__TRASHED__



    def raise_( self ):
        print( 'TabWidget::raise_()...%s' % self.windowTitle() )
        self.RaiseSignal.emit( self.__m_ID )
        return super(TabWidget, self).raise_()




# Independent Dockable Frame. Behaves like TabWidget
class DockableFrame(Frame):

    # Signals
    RaiseSignal = pyqtSignal(object)
    MoveSignal = pyqtSignal(object, QPoint)
    ReleaseSignal = pyqtSignal(object, QPoint)
    CloseSignal = pyqtSignal(object)


    def __init__( self, *args, **kwargs ):
        super(DockableFrame, self).__init__(*args, **kwargs)

        self.setWindowTitle( '        ' )
        self.resize( 512, 512 )
        self.setLayout( QVBoxLayout() )
        self.layout().setContentsMargins(4,4,4,4)

        self.__m_TabWidget = TabWidget()
        self.layout().addWidget( self.__m_TabWidget )

        self.__m_TabWidget.currentChanged.connect( self.__SetWindowTitle )

        self.tabCloseRequested = self.__m_TabWidget.tabCloseRequested


        self.__m_ID = id(self)#kwargs['widget_id'] if 'widget_id' in kwargs else id(self)



    def Release( self ):
        self.__m_TabWidget.Release()

        if( self.receivers(self.RaiseSignal) ):
            self.RaiseSignal.disconnect()

        if( self.receivers(self.MoveSignal) ):
            self.MoveSignal.disconnect()

        if( self.receivers(self.ReleaseSignal) ):
            self.ReleaseSignal.disconnect()



    def ID( self ):
        return self.__m_ID



    def SetDuration( self, duration: Duration ) -> None:
        self.__m_TabWidget.SetDuration(duration)



    def IsPersistent( self ) -> bool:
        return self.__m_TabWidget.IsPersistent()



    def IsVolatile( self ) -> bool:
        return self.__m_TabWidget.IsVolatile()



    def TabWidget( self ) -> TabWidget:
        return self.__m_TabWidget



    def SetLock( self, on: bool ) -> None:
        #print( 'DockableFrame::SetLock()...%r' % on )
        self.__m_TabWidget.SetLock(on)



    def IsLocked( self ) -> bool:
        return self.__m_TabWidget.IsLocked()



    def SetTrash( self, on: bool ) -> None:
        self.__m_TabWidget.SetTrash( on )
        self.setWindowOpacity( float(not on) )



    def IsTrashed( self ) -> bool:
        return self.__m_TabWidget.IsTrashed()



    def IsActive( self ) -> bool:
        return self.__m_TabWidget.IsActive()



    def NumActiveTabs( self ) -> int:
        return self.__m_TabWidget.NumActiveTabs()



    def SetTabClosable( self, index: int, on: bool ) -> None:
        self.__m_TabWidget.SetTabClosable( index, on )



    def IsTabClosable( self, index: int ) -> bool:
        return self.__m_TabWidget.IsTabClosable( index )



    def __SetWindowTitle( self, index: int ) -> None:
        self.setWindowTitle( self.__m_TabWidget.tabText(index) )



    def currentIndex( self ):
        return self.__m_TabWidget.currentIndex()



    def setCurrentIndex( self, index: int ) -> None:
        return self.__m_TabWidget.setCurrentIndex(index)



    def count( self ) -> int:
        return self.__m_TabWidget.count()



    def widget( self, index: int ) -> QWidget:
        return self.__m_TabWidget.widget( index )



    def tabBar( self ) -> QTabBar:
        return self.__m_TabWidget.tabBar()



    def addTab( self, widget: QWidget, label: str ) -> int:
        return self.__m_TabWidget.addTab( widget, label )



    def insertTab( self, index: int, widget: QWidget, label: str ) -> int:
        return self.__m_TabWidget.insertTab( index, widget, label )



    #def removeTab( self, index: int ) -> None:
    #    return self.__m_TabWidget.removeTab( index )



    def mousePressEvent( self, event ):
        super(DockableFrame, self).mousePressEvent(event)
        #print( 'DockableFrame::mousePressEvent()...' )
        if( self.handleSelected is None and self.IsVolatile() ):
            self.__m_TabWidget.SetLock(True) 



    def mouseMoveEvent( self, event ):
        #print( 'DockableFrame::mouseMoveEvent()...%s' % self.windowTitle() )
        if( self.handleSelected is None and self.IsVolatile() ):# Avoid docking check while resizing widget.
            self.MoveSignal.emit( self.__m_ID, event.globalPos() )
        return super(DockableFrame, self).mouseMoveEvent(event)



    def mouseReleaseEvent( self, event ):
        #print( 'DockableFrame::mouseReleaseEvent()...' )
        if( self.handleSelected is None and self.IsVolatile() ):# Avoid docking check while resizing widget.
            self.ReleaseSignal.emit( self.__m_ID, event.globalPos() )
            self.__m_TabWidget.SetLock(False)
        return super(DockableFrame, self).mouseReleaseEvent(event)



    def changeEvent( self, event ):
        #print( 'DockableFrame::changeEvent()...' )
        if( event.type()==QEvent.ActivationChange and self.isActiveWindow() ):
            self.RaiseSignal.emit( self.__m_ID )
        return super(DockableFrame, self).changeEvent(event)



    def closeEvent( self, event ):
        #print( 'DockableFrame::closeEvent()...' )
        super(DockableFrame, self).closeEvent(event)
        self.CloseSignal.emit( self.__m_ID )



    def raise_( self ):
        #print( 'DockableFrame::raise_()...%s' % self.windowTitle() )
        self.RaiseSignal.emit( self.__m_ID )
        return super(DockableFrame, self).raise_()




class TabbedMDIManager:

    # Opacity settings. Overlapped on other dockable: 0.5, No overlap: 1.0.
    __c_Opacity = (1.0, 0.5)

    # Position offset of detaced floater.
    __c_FloaterOffset = QPoint(-10, -10)



    def __init__( self ):

        self.__m_Dockables = {}# key: widget_id, value: widget
        self.__m_Order = []# Topmost order information of self.__m_Dockables
        self.__m_Floaters = {}# key: floater widget id, value: floater object
        self.__m_ContentWidgets = {}# key: widget_id, value: content widget



    def __del__( self ):
        print( 'TabbedMDIManager::__del__()...' )
        self.Release()



    def Release( self ):
        print( 'TabbedMDIManager::Release()...' )

        for widget_id in list( self.__m_ContentWidgets.keys() ):
            self.__DeleteContentWidget( widget_id )

        for widget_id in list( self.__m_Dockables.keys() ):
            self.__DeleteDockable( widget_id )

        for widget_id in list( self.__m_Floaters.keys() ):
            self.__DeleteFloater( widget_id )




    def AddDockable( self, widget_type: type, duration=Duration.Volatile ) -> typing.Any:
        try:
            newWidget = widget_type()
            newWidget.SetDuration( duration )

            # connect dockable signals
            newWidget.RaiseSignal.connect( self.__UpdateTopMost )
            newWidget.MoveSignal.connect( self.__CheckDockableIntersection )
            newWidget.ReleaseSignal.connect( self.__AttachDockable )
            newWidget.CloseSignal.connect( self.__DeleteDockable )
            newWidget.tabCloseRequested.connect( self.__Cleanup )

            # connect tabbar signals
            newWidget.tabBar().DetachWidgetSignal.connect( lambda index: self.__DetachFloater( newWidget.ID(), index ) )
            newWidget.tabBar().AttachWidgetSignal.connect( self.__AttachFloater )
            newWidget.tabBar().DragWidgetSignal.connect( self.__DragFloater )

            self.__m_Dockables[ newWidget.ID() ] = newWidget
            self.__m_Order.append( newWidget.ID() )

            newWidget.show()

            return newWidget.ID()

        except:
            traceback.print_exc()
            return None



    def DeleteDockable( self, dockable_id ):
        try:
            if( not dockable_id in self.__m_Dockables ):
                return False
            
            self.__DeleteDockable( dockable_id )
            return True

        except:
            traceback.print_exc()
            return False



    def SetDuration( self, dockable_id: typing.Any, duration: Duration ) -> bool:
        try:
            self.__m_Dockables[ dockable_id ].SetDuration( duration )
            return True
        except:
            traceback.print_exc()
            return False



    def GetDockable( self, dockable_id ):
        try:
            return self.__m_Dockables[ dockable_id ]

        except:
            traceback.print_exc()
            return None



    def FindParentDockable( self, widget_id: typing.Any ) -> (typing.Any, int):
        try:
            contentWidget = self.__m_ContentWidgets[ widget_id ]

            #parentDockable = None
            #parentTabWidget = None
            dockableID = None
            index = -1

            widget = contentWidget.parentWidget()
            while( widget ):
                if( type(widget) is DockableFrame ):
                    dockableID = widget.ID()
                    break
                elif( type(widget) is TabWidget ):
                    dockableID = widget.ID()
                    index = widget.indexOf( contentWidget )

                widget = widget.parentWidget()

            return dockableID, index

        except:
            traceback.print_exc()
            return None, -1



    def AddTab( self, dockable_id: typing.Any, widget: QWidget, label: str, widget_id: typing.Any) -> bool:
        try:
            if( not dockable_id in self.__m_Dockables ):
                return False

            self.__m_ContentWidgets[ widget_id ] = widget
            self.__m_Dockables[ dockable_id ].addTab( widget, label )

            return True

        except:
            traceback.print_exc()
            return False



    def InsertTab( self, dockable_id: typing.Any, index: int, widget: QWidget, label: str, widget_id: typing.Any) -> bool:
        try:
            if( not dockable_id in self.__m_Dockables ):
                return False

            self.__m_ContentWidgets[ widget_id ] = widget
            self.__m_Dockables[ dockable_id ].insertTab( index, widget, label )

            return True

        except:
            traceback.print_exc()
            return False



    def DeleteTab( self, widget_id ) -> bool:
        try:
            self.__DeleteContentWidget( widget_id )
            return True

        except:
            traceback.print_exc()
            return False



    def SetTabClosable( self, dockable_id: typing.Any, index: int, on: bool ) -> None:
        try:
            self.__m_Dockables[ dockable_id ].SetTabClosable( index, on )
        except:
            traceback.print_exc()




    #===================== private methods ==========================#

    def __Cleanup( self ):
        print( 'TabbedMDIManager::__Cleanup()...' )

        emptyOwnerIDs = [ owner_id for owner_id, widget in self.__m_Dockables.items() if widget.IsTrashed() ]

        # Transfer floater's content widget to dockable.
        for floater in self.__m_Floaters.values():
            ownerWidget = self.__m_Dockables[ emptyOwnerIDs.pop() ] if bool(emptyOwnerIDs) else self.__m_Dockables[ self.AddDockable(DockableFrame, Duration.Volatile) ]
            
            if( floater.layout().count() > 0 ):

                contentWidget = floater.layout().itemAt(0).widget()
                ownerWidget.addTab( contentWidget, contentWidget.windowTitle() )
                ownerWidget.SetTabClosable( 0, floater.GetAttribs()[ 'TabClosable' ] )
                ownerWidget.activateWindow()
                ownerWidget.show()

                ownerWidget.move( floater.pos() )
                
                ownerWidget.SetTrash( False )
      
        # Delete unused dockables
        for owner_id in emptyOwnerIDs:
            self.__DeleteDockable( owner_id )

        # Delete unused floaters
        for float_id in list( self.__m_Floaters.keys() ):
            self.__DeleteFloater( float_id )

        # Delete unparented content widgets
        for widget_id in list( self.__m_ContentWidgets.keys() ):
            if( self.__m_ContentWidgets[ widget_id ].parentWidget() is None ):
                self.__DeleteContentWidget( widget_id )



    # Sort Dockables in top-most order
    def __UpdateTopMost( self, widget_id ):

        depth = self.__m_Order.index(widget_id)
        # Reorder OwnerFrames
        for d in reversed( range(1, depth+1) ):
            self.__m_Order[d] = self.__m_Order[d-1]
        self.__m_Order[0] = widget_id

        # Clear TabBar's Focus Index
        for d in reversed( range(1, len(self.__m_Order) ) ):
            self.__m_Dockables[self.__m_Order[d]].tabBar().SetFocusIndex(-1)

        print( 'TabbedMDIManager::__UpdateTopMost()...%s' % self.__m_Dockables[ self.__m_Order[0] ].windowTitle() )

        # Debug print dockable order
        #for i, widget_id in enumerate(self.__m_Order):
        #    print( '%d: %s' % ( i, self.__m_Dockables[widget_id].windowTitle() ) )



    # Detach content widget from TabWidget
    def __DetachFloater( self, owner_id, index ):

        print( 'TabbedMDIManager::__DetachFloater()...%d' % index )

        ownerWidget = self.__m_Dockables[ owner_id ]

        floater = Floater()

        # connect signals
        floater.SelectSignal.connect( self.__SetCurrenFloaterID )
        floater.MoveSignal.connect( self.__CheckFloaterIntersection )
        floater.ReleaseSignal.connect( self.__AttachFloater )
        floater.CloseSignal.connect( self.__DeleteFloater )

        # transfer content widget to floater
        contentWidget = ownerWidget.widget( index )
        floater.SetAttribs( { 'TabClosable': ownerWidget.IsTabClosable(index) } )
        floater.setWindowTitle( contentWidget.windowTitle() )
        floater.resize( contentWidget.width(), contentWidget.height() )
        floater.layout().addWidget( contentWidget )
        contentWidget.setVisible(True)# MUST SET VISIBLE. Widgets detached from QTabWidget are INVISIBLE.

        floater.show()

        self.__m_Floaters[ floater.ID() ] = floater
        self.__m_CurrFloaterID = floater.ID()
        
        # Update onweframe display
        if( ownerWidget.NumActiveTabs() < 1 and ownerWidget.IsVolatile() ):# if dockable is dynamic and no active tab remains, mark as trash.
            ownerWidget.SetTrash(True) 



    def __SetCurrenFloaterID( self, curr_id ):
        self.__m_CurrFloaterID = curr_id



    def __DeleteContentWidget( self, widget_id ):
        print( 'TabbedMDIManager::__DeleteContentWidget()...' )
        try:
            self.__m_ContentWidgets[ widget_id ].setParent(None)
            #self.__m_ContentWidgets[ widget_id ].Release()
            self.__m_ContentWidgets[ widget_id ].deleteLater()
            del self.__m_ContentWidgets[ widget_id ]
        except:
            traceback.print_exc()



    def __DeleteFloater( self, widget_id ):
        print( 'TabbedMDIManager::__DeleteFloater()...' )
        try:
            self.__m_Floaters[ widget_id ].Release()
            self.__m_Floaters[ widget_id ].deleteLater()
            del self.__m_Floaters[ widget_id ]
        except:
            traceback.print_exc()



    def __DeleteDockable( self, widget_id ):
        print( 'TabbedMDIManager::__DeleteDockable()...' )
        try:
            self.__m_Dockables[ widget_id ].Release()
            self.__m_Dockables[ widget_id ].deleteLater()
            del self.__m_Dockables[ widget_id ]
            self.__m_Order.remove( widget_id )
        except:
            traceback.print_exc()



    def __DragFloater( self, globalPos: QPoint ):
        print( 'TabbedMDIManager::__DragFloater()...' )
        self.__CheckFloaterIntersection( self.__m_CurrFloaterID, globalPos )
        self.__m_Floaters[ self.__m_CurrFloaterID ].move( globalPos + TabbedMDIManager.__c_FloaterOffset )



    def __CheckFloaterIntersection( self, widget_id, globalPos ):
        #print( 'TabbedMDIManager::__CheckFloaterIntersection()...' )
        
        floatingWidgetOpacity = TabbedMDIManager.__c_Opacity[0]
        raiseOwnerIndex = 0
        tabBarIndex = -1

        # Check intersection against 'active' dockable
        for i, owner_id in enumerate( self.__m_Order ):            
            ownerWidget = self.__m_Dockables[ owner_id ]
            if( not ownerWidget.IsActive() ): continue
            
            pos =ownerWidget.mapFromGlobal(globalPos) 
            if( ownerWidget.rect().contains(pos) ):
                # Update raiseOwnerIndex
                raiseOwnerIndex = i
                # Update floater's opacity
                tabBar = ownerWidget.tabBar()
                pos = tabBar.mapFromGlobal(globalPos)
                floatingWidgetOpacity = TabbedMDIManager.__c_Opacity[ int( tabBar.rect().contains(pos) ) ]
                if( tabBar.rect().contains(pos) ):
                    tabBarIndex = tabBar.tabAt(pos)
                tabBar.SetFocusIndex( tabBarIndex )
                break

        if( raiseOwnerIndex > 0 ):
            self.__m_Dockables[ self.__m_Order[ raiseOwnerIndex ] ].raise_()
            self.__m_Floaters[ widget_id ].raise_()

        if( floatingWidgetOpacity != self.__m_Floaters[ widget_id ].windowOpacity() ):
            self.__m_Floaters[ widget_id ].setWindowOpacity( floatingWidgetOpacity )



    def __CheckDockableIntersection( self, widget_id, globalPos ):
        #print( 'TabbedMDIManager::__CheckDockableIntersection()...' )
        
        floatingWidgetOpacity = TabbedMDIManager.__c_Opacity[0]
        raiseOwnerIndex = 0
        tabBarIndex = -1

        for i, owner_id in enumerate( self.__m_Order ):

            ownerWidget = self.__m_Dockables[ owner_id ]
            if( not ownerWidget.IsActive() ): continue

            pos =ownerWidget.mapFromGlobal(globalPos)
            if( ownerWidget.rect().contains(pos) ):
                # Update raiseOwnerIndex
                raiseOwnerIndex = i
                # Update floater's opacity
                tabBar = ownerWidget.tabBar()
                pos = tabBar.mapFromGlobal(globalPos)
                floatingWidgetOpacity = TabbedMDIManager.__c_Opacity[ int( tabBar.rect().contains(pos) ) ]
                if( tabBar.rect().contains(pos) ):
                    tabBarIndex = tabBar.tabAt(pos)
                tabBar.SetFocusIndex( tabBarIndex )
                break

        if( raiseOwnerIndex > 1 ):
            self.__m_Dockables[ self.__m_Order[ raiseOwnerIndex ] ].raise_()
            self.__m_Dockables[ widget_id ].raise_()

        if( floatingWidgetOpacity != self.__m_Dockables[ widget_id ].windowOpacity() ):
            self.__m_Dockables[ widget_id ].setWindowOpacity( floatingWidgetOpacity )



    # Dock floater to dockable
    def __AttachFloater( self, globalPos ):
        print( 'TabbedMDIManager::__AttachFloater()...' )

        floater = self.__m_Floaters[ self.__m_CurrFloaterID ]
        attribs = floater.GetAttribs()

        for owner_id in self.__m_Order:

            ownerWidget = self.__m_Dockables[ owner_id ]
            if( not ownerWidget.IsActive() ): continue

            tabBar = ownerWidget.tabBar()
            index = tabBar.tabAt( tabBar.mapFromGlobal( globalPos ) )
            
            if( index != -1 ):
                
                if( floater.layout().count() > 0 ):
                    contentWidget = floater.layout().itemAt(0).widget()
                    ownerWidget.insertTab( index, contentWidget, contentWidget.windowTitle() )
                    ownerWidget.SetTabClosable( index, attribs[ 'TabClosable' ] )
                    ownerWidget.activateWindow()
                    ownerWidget.setWindowOpacity(1.0)

                tabBar.SetFocusIndex(-1)

                # Delete floater
                self.__DeleteFloater( self.__m_CurrFloaterID )
                self.__m_CurrFloaterID = None

                break

        self.__Cleanup()



    def __AttachDockable( self, widget_id, globalPos ):
        print( 'TabbedMDIManager::__AttachDockable()...' )

        srcOwner = self.__m_Dockables[ widget_id ]
        numActiveSrcTabs = srcOwner.NumActiveTabs()
        srcCurrentIndex = srcOwner.currentIndex()

        for owner_id in self.__m_Order:

            destOwner = self.__m_Dockables[ owner_id ]
            if( not destOwner.IsActive() ): continue

            tabBar = destOwner.tabBar()
            index = tabBar.tabAt( tabBar.mapFromGlobal( globalPos ) )

            if( index != -1 ):
                for i in range( numActiveSrcTabs ):
                    # get widget from top
                    contentWidget = srcOwner.widget(0)
                    # insert into tab position[index + i]
                    destOwner.insertTab( index+i, contentWidget, contentWidget.windowTitle() )
                    contentWidget.setVisible(True)

                destOwner.setCurrentIndex( index + srcCurrentIndex )# Restore srcOwner's current tab selected.
                destOwner.activateWindow()
        
                tabBar.SetFocusIndex(-1)

                # Delete dockable
                self.__DeleteDockable( widget_id )

                break








#def onTabFocusChanged( old: QWidget, new: QWidget, propertyName: str ) -> None:
#    #print( '{} -> {}'.format( old, new ) )

#    #print( '/---------------- old -----------------------/')
#    while( old ):# isinstance(old, QWidget)
#        #print( old )
#        if( isinstance( old, QTabWidget ) ):
#            old.setProperty( propertyName, False )
#            old.setStyle( old.style() )
#            tabBar = old.tabBar()
#            tabBar.setProperty( propertyName, False )
#            tabBar.setStyle( tabBar.style() )
#            break
#        old = old.parentWidget()

#    #print( '/---------------- new -----------------------/')
#    while( new ):# isinstance(new, QWidget)
#        #print( new )
#        if( isinstance( new, QTabWidget ) ):
#            new.setProperty( propertyName, True )
#            new.setStyle( new.style() )
#            tabBar = new.tabBar()
#            tabBar.setProperty( propertyName, True )
#            tabBar.setStyle( tabBar.style() )
#            break
#        new = new.parentWidget()       
#    #print( '\n')
