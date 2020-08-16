from .frame import *

from enum import Enum
import typing
import traceback




# Dockable's duration
class Duration(Enum):
    Persistent = 0x00 # Dockable remains even if no child tab exists.
    Volatile = 0x01   # Automatically deleted if no child tab exists.


# Tab anchor
class Anchor(Enum):
    Off = 0x00
    On = 0x01



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
        #print( 'Floater::Release()...' )

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
        #print( 'Floater::mousePressEvent()...' )
        if( self.handleSelected is None ):
            self.SelectSignal.emit( self.__m_ID )


    
    def mouseMoveEvent( self, event ):
        #print( 'Floater::mouseMoveEvent()...' )
        # Avoid docking at the end of widget resize operation
        if( self.handleSelected is None ):
            self.MoveSignal.emit( self.__m_ID, event.globalPos() )

        return super(Floater, self).mouseMoveEvent(event)



    def mouseReleaseEvent( self, event ):
        #print( 'Floater::mouseReleaseEvent()...' )
        # Avoid docking at the end of widget resize operation
        if( self.handleSelected is None ):
            self.ReleaseSignal.emit( event.globalPos() )

        return super(Floater, self).mouseReleaseEvent(event)
        


    def closeEvent( self, event ):
        #print( 'Floater::closeEvent()...' )
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


    __CLOSABLE_MASK__ = 0x01
    __DETACDHABLE_MASK__ = 0x02
    __PIVOT_MASK__ = 0x04

    @staticmethod
    def SetBit( value, bitmask, on=True ):
        return value | bitmask if on else value & ~bitmask

    @staticmethod
    def ClearBit( value, bitmask ):
        return value & ~bitmask

    @staticmethod
    def Bit( value, bitmask ):
        return bool( value & bitmask )




    def __init__( self, *args, **kwargs ):
        super(TabBar, self).__init__(*args, **kwargs)

        self.setTabsClosable( True )
        self.setMovable(False)# Disable default tab drag feature.
        self.setAttribute( Qt.WA_NoMousePropagation )# Avoid mouse event propagation to parent widget(TabWidget, OwnerFrame...)

        # Create Hooter tab. Used for mouse intersection.
        self.insertTab( 0, '        ' )
        self.setTabEnabled( 0, False )

        self.tabButton( 0, QTabBar.RightSide ).hide()
        self.SetTabClosable( 0, False )
        self.SetTabDetachable( 0, False )


        self.__m_FocusIndex = -1


        self.__m_DragMode = TabBar.__DRAG_NONE__
        self.__m_CurrIndex = -1
        self.__m_PivotRect = None
        self.__m_bInsidePivot  = False
        self.__m_bEnteredPivot = False



    def NumActiveTabs( self ) -> int:
        return self.count() - 1



    def SetFocusIndex( self, index ):
        if( self.__m_FocusIndex!=index ):
            #print( 'TabBar::SetFocusIndex()...%s: %d' % ( self.parentWidget().windowTitle(), index ) )
            self.__m_FocusIndex = index
            self.update()



    def SetTabClosable( self, index: int, on: bool ) -> None:
        #print( 'TabBar::SetTabClosable()...{}: {}'.format( index, on ) )
        self.tabButton( index, QTabBar.RightSide ).setEnabled(on)
        self.setTabData( index, self.SetBit( self.tabData(index), TabBar.__CLOSABLE_MASK__, on ) )



    def IsTabClosable( self, index: int ) -> bool:
        #return self.tabButton( index, QTabBar.RightSide ).size().isEmpty()==False
        return self.Bit( self.tabData(index), TabBar.__CLOSABLE_MASK__ )



    def SetTabDetachable( self, index: int, on: bool ) -> None:
        #print( 'TabBar::SetTabDetachable()...{}'.format( on ) )
        self.setTabData( index, self.SetBit( self.tabData(index), TabBar.__DETACDHABLE_MASK__, on ) )



    def IsTabDetachable( self, index: int ) -> bool:
        #print( 'TabBar::IsTabDetachable()...{}'.format( index ) )
        return self.Bit( self.tabData(index), TabBar.__DETACDHABLE_MASK__ )



    def tabInserted( self, index ):
        #print( 'TabBar::tabInserted(%d)' % index )
        self.setCurrentIndex(index)
        self.setTabData( index, TabBar.__CLOSABLE_MASK__ | TabBar.__DETACDHABLE_MASK__ )
        #return super(TabWidget, self).tabInserted(index)
        


    def tabRemoved( self, index ):
        #print( 'TabBar::tabRemoved(%d)' % index )
        self.setCurrentIndex( max(min(index, self.count()-2), 0) )# clamp current index range to [ 0, NumActiveTabs()-1 ]
        #return super(TabWidget, self).tabRemoved(index)



    def mousePressEvent( self, event ):
        #print( 'TabBar::mousePressEvent()...' )

        # Triggers tab drag operations ONLY WHEN LEFT MOUSE PRESSED.
        if( event.button()==Qt.LeftButton ):

            self.__m_CurrIndex = self.tabAt( event.pos() )

            if( self.__m_CurrIndex < self.NumActiveTabs() ):

                self.setCurrentIndex( self.__m_CurrIndex )
                self.__m_DragMode = TabBar.__DRAG_TAB__

                self.setTabData( self.__m_CurrIndex, self.SetBit( self.tabData(self.__m_CurrIndex), TabBar.__PIVOT_MASK__, True ) ) 
                self.__m_bInsidePivot  = True
                self.__m_bEnteredPivot = False
                self.__m_PivotRect = self.tabRect( self.__m_CurrIndex )

            else:
                event.ignore()

        return super(TabBar, self).mousePressEvent(event)



    def mouseMoveEvent( self, event ):
        #print( 'TabBar::mouseMoveEvent()...' )
        pos = event.pos()

        if( self.__m_DragMode==TabBar.__DRAG_WIDGET__ ):
            self.DragWidgetSignal.emit( event.globalPos() )
            event.ignore()

        elif( self.__m_DragMode==TabBar.__DRAG_TAB__ ):
            # Mouse is moving inside QTabBar area
            index = self.tabAt(pos)
            if( index !=-1 and index != self.NumActiveTabs() ):
                
                if( self.Bit( self.tabData(index), TabBar.__PIVOT_MASK__ ) != self.__m_bInsidePivot ):
                    #print('!!' )
                    self.__m_PivotRect = self.tabRect( self.__m_CurrIndex )
                    self.__m_bEnteredPivot = self.__m_PivotRect.contains(pos)
                    self.__m_bInsidePivot = not self.__m_bInsidePivot

                    self.moveTab( self.__m_CurrIndex, index )
                    self.__m_CurrIndex = index
                    
                elif( self.__m_PivotRect.contains(pos)==True and self.__m_bEnteredPivot==False ):
                    #print( 'Entered...' )
                    self.__m_bEnteredPivot = True
                    self.moveTab( self.__m_CurrIndex, index )
                    self.__m_CurrIndex = index

                #elif( self.__m_PivotRect.contains(pos)==False and self.__m_bEnteredPivot==True ):
                    #print( 'Left...' )

            # Mouse dragged detachable tab to outside TabBar area.
            elif( self.IsTabDetachable( self.__m_CurrIndex ) ):
                self.__m_DragMode = TabBar.__DRAG_WIDGET__
                self.DetachWidgetSignal.emit( self.__m_CurrIndex )


        #else:# TabBar.__DRAG_NONE__
        #    pass

        return super(TabBar, self).mouseMoveEvent(event)
        


    def mouseReleaseEvent( self, event ):
        #print( 'TabBar::mouseReleaseEvent()...' )

        # Detached widget has been released inside QTabBar area
        if( self.__m_DragMode==TabBar.__DRAG_WIDGET__ ):
            self.AttachWidgetSignal.emit( event.globalPos() )

        elif( self.__m_DragMode==TabBar.__DRAG_TAB__ ):
            self.setTabData( self.__m_CurrIndex, self.SetBit( self.tabData(self.__m_CurrIndex), TabBar.__PIVOT_MASK__, False ) )

        self.__m_CurrIndex = -1
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



    def Info( self, index ):
        print( '//============ Tab[{}] ==============//'.format( index ) )
        print( '  Name: {}\n  IsClosable: {}\n  IsDetachable: {}'.format( self.tabText(index), self.IsTabClosable(index), self.IsTabDetachable(index) )  )




# TabWidget
class TabWidget(QTabWidget):
    
    # Signals
    RaiseSignal = pyqtSignal(object)
    CleanupSignal = pyqtSignal(bool)

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
        self.setStyleSheet(  g_TabWidgetStyleSheet )
        self.setAttribute( Qt.WA_NoMousePropagation )# Avoid mouse event propagation to parent widget(OwnerFrame...)
        self.setFocusPolicy( Qt.StrongFocus )

        self.tabCloseRequested.connect( self.DeleteTab )

        self.__m_Status = TabWidget.__ACTIVE__

        self.__m_Duration = Duration.Volatile
        # True: TabWidget will be destroyed automatically if no active tab exists.
        # False: TabWidget is persistent regardless of active tab existence.

        self.__m_ID = id(self)#kwargs['widget_id'] if 'widget_id' in kwargs else id(self)



    #def __del__( self ):
    #    print( 'TabWidget::__del__()...' )
    #    while( self.NumActiveTabs() ):
    #        self.DeleteTab(0)



    def Clear( self ):
        #print( 'TabWidget::Clear()...' )
        if( self.__m_Duration==Duration.Persistent ):
            while( self.NumActiveTabs() ):
                self.widget(0).setParent(None)            
        else:
            self.Release()



    def Release( self ):
        #print( 'TabWidget::Release()...' )

        if( self.receivers(self.RaiseSignal) ):
            self.RaiseSignal.disconnect()

        while( self.NumActiveTabs() ):
            self.widget(0).setParent(None)

        self.__m_Duration=Duration.Volatile
        self.__m_Status = TabWidget.__TRASHED__



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



    def SetTabDetachable( self, index: int, on: bool ) -> None:
        self.__m_TabBar.SetTabDetachable( index, on )



    def IsTabDetachable( self, index: int ) -> bool:
        return self.__m_TabBar.IsTabDetachable( index )



    def DeleteTab( self, index: int ) -> None:
        #print( 'TabWidget::DeleteTab()...%d' % index )
        self.widget(index).setParent(None)
        if( self.NumActiveTabs() < 1 and self.__m_Duration==Duration.Volatile ):# if tab widget is dynamic and no active tab remains, mark as trash.
            self.__m_Status = TabWidget.__TRASHED__
        self.CleanupSignal.emit( True )



    def DetachTab( self, index: int ) -> QWidget:
        contentWidget = self.widget(index)
        contentWidget.setParent(None)
        if( self.NumActiveTabs() < 1 and self.__m_Duration==Duration.Volatile ):# if tab widget is dynamic and no active tab remains, mark as trash.
            self.__m_Status = TabWidget.__TRASHED__
        self.CleanupSignal.emit( False )
        return contentWidget



    def changeEvent( self, event ):
        #print( 'TabWidget::changeEvent()...' )
        if( event.type()==QEvent.ActivationChange and self.isActiveWindow() ):
            self.RaiseSignal.emit( self.__m_ID )
        return super(TabWidget, self).changeEvent(event)



    def closeEvent( self, event ):
        #print( 'TabWidget::closeEvent()...' )
        self.__m_Status = TabWidget.__TRASHED__
        super(TabWidget, self).closeEvent(event)
        self.CleanupSignal.emit( True )



    def raise_( self ):
        #print( 'TabWidget::raise_()...%s' % self.windowTitle() )
        self.RaiseSignal.emit( self.__m_ID )
        return super(TabWidget, self).raise_()





# Independent Dockable Frame. Behaves like TabWidget
class DockableFrame(Frame):

    # Signals
    RaiseSignal = pyqtSignal(object)
    MoveSignal = pyqtSignal(object, QPoint)
    ReleaseSignal = pyqtSignal(object, QPoint)


    def __init__( self, *args, **kwargs ):
        super(DockableFrame, self).__init__(*args, **kwargs)

        self.setWindowTitle( '        ' )
        self.Resize( 512, 512 )
        self.setLayout( QVBoxLayout() )
        self.layout().setContentsMargins( 4, 4, 4, 4 )

        self.__m_TabWidget = TabWidget()
        self.layout().addWidget( self.__m_TabWidget )

        self.__m_TabWidget.currentChanged.connect( self.__SetWindowTitle )

        self.CleanupSignal = self.__m_TabWidget.CleanupSignal
        self.tabCloseRequested = self.__m_TabWidget.tabCloseRequested

        self.__m_ID = id(self)



    def Clear( self ):
        #print( 'DockableFrame::Clear()...' )

        if( self.IsPersistent() ):
            self.__m_TabWidget.Clear()

        else:
            self.Release()



    def Release( self ):
        #print( 'DockableFrame::Release()...' )

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



    def SetTabDetachable( self, index: int, on: bool ) -> None:
        self.__m_TabWidget.SetTabDetachable( index, on )



    def IsTabDetachable( self, index: int ) -> bool:
        return self.__m_TabWidget.IsTabDetachable( index )



    def DeleteTab( self, index: int ) -> None:
        self.__m_TabWidget.DeleteTab( index )



    def DetachTab( self, index: int ) -> QWidget:
        return self.__m_TabWidget.DetachTab( index )



    def __SetWindowTitle( self, index: int ) -> None:
        self.setWindowTitle( self.__m_TabWidget.tabText(index) )



    def currentIndex( self ):
        return self.__m_TabWidget.currentIndex()



    def setCurrentIndex( self, index: int ) -> None:
        #print( 'DockableFrame::setCurrentIndex()... %d' % index )
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
        self.__m_TabWidget.SetTrash( True )
        super(DockableFrame, self).closeEvent(event)
        self.CleanupSignal.emit( True )



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

        self.__m_CurrFloaterID = None



    def __del__( self ):
        #print( 'TabbedMDIManager::__del__()...' )
        self.Release()



    def Clear( self ):
        #print( 'TabbedMDIManager::Clear()...' )

        # Clear all dockers
        for dockable in self.__m_Dockables.values():
            dockable.Clear()

        # Do cleanup
        self.__Cleanup()



    def Release( self ):
        #print( 'TabbedMDIManager::Release()...' )

        # Delete all dockables
        for widget_id in list( self.__m_Dockables.keys() ):
            self.__DeleteDockable( widget_id )

        # Delete all content widgets
        for widget_id, widget in list( self.__m_ContentWidgets.items() ):
            self.__DeleteContentWidget( widget_id, destroy=True )

        # Delete all floaters
        for widget_id in list( self.__m_Floaters.keys() ):
            self.__DeleteFloater( widget_id )

        # Debug print
        #self.Info()



    def AddDockable( self, widget_type: type, duration=Duration.Volatile ) -> typing.Any:
        try:
            newWidget = widget_type()
            newWidget.SetDuration( duration )

            # connect dockable signals
            newWidget.RaiseSignal.connect( self.__UpdateTopMost )
            newWidget.CleanupSignal.connect( self.__Cleanup )
            if( widget_type is DockableFrame ):
                newWidget.MoveSignal.connect( self.__CheckDockableIntersection )
                newWidget.ReleaseSignal.connect( self.__AttachDockable )

            # connect tabbar signals
            newWidget.tabBar().DetachWidgetSignal.connect( lambda index: self.__DetachFloater( newWidget.ID(), index ) )
            newWidget.tabBar().AttachWidgetSignal.connect( self.__AttachFloater )
            newWidget.tabBar().DragWidgetSignal.connect( self.__DragFloater )

            self.__m_Dockables[ newWidget.ID() ] = newWidget
            self.__m_Order.append( newWidget.ID() )

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
            dockableID = None
            index = -1

            if( widget_id in self.__m_ContentWidgets ):

                contentWidget = self.__m_ContentWidgets[ widget_id ]

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
            dockable_id, index = self.FindParentDockable( widget_id )
            self.__m_Dockables[ dockable_id ].DeleteTab( index )
            return True

        except:
            traceback.print_exc()
            return False



    def DetachTab( self, widget_id ) -> QWidget:
        try:
            dockable_id, index = self.FindParentDockable( widget_id )
            contentWidget = self.__m_Dockables[ dockable_id ].DetachTab( index )
            return contentWidget

        except:
            traceback.print_exc()
            return None



    def SetTabClosable( self, dockable_id: typing.Any, index: int, on: bool ) -> None:
        try:
            self.__m_Dockables[ dockable_id ].SetTabClosable( index, on )
        except:
            traceback.print_exc()



    def SetTabDetachable( self, dockable_id: typing.Any, index: int, on: bool ) -> None:
        try:
            self.__m_Dockables[ dockable_id ].SetTabDetachable( index, on )
        except:
            traceback.print_exc()



    def SetTabTitle( self, content_id, title ):
        try:
            contentWidget = self.__m_ContentWidgets[ content_id ]
            contentWidget.setWindowTitle( title )

            widget = contentWidget.parentWidget()
            bUpdateTitle = False

            while( widget ):

                if( type(widget) is DockableFrame ):
                    break

                elif( type(widget) is TabWidget ):
                    contentIndex = widget.indexOf( contentWidget )
                    widget.setTabText( contentIndex, title )

                    if( widget.currentIndex()==contentIndex ):
                        bUpdateTitle = True

                widget = widget.parentWidget()

            if( bUpdateTitle ):
                widget.setWindowTitle( title )
                print( 'TabbedMDIManager::SetTabTitle()... {}'.format( title ) )

        except:
            traceback.print_exc()



    def Show( self ) -> None:
        for dockable_id in reversed(self.__m_Order):
            self.__m_Dockables[ dockable_id ].show()



    def Hide( self ) -> None:
        for dockable in self.__m_Dockables.values():
            dockable.hide()



    def Activate( self, dockable_id, index=-1 ):
        try:
            #print( 'TabbedMDIManager::Activate()... {}, {}'.format( self.__m_Dockables[ dockable_id ].windowTitle(), index ) )
            self.__UpdateTopMost( dockable_id )
            self.__m_Dockables[ dockable_id ].setCurrentIndex( index )        
            self.__m_Dockables[ dockable_id ].activateWindow()

        except:
            traceback.print_exc()



    #===================== private methods ==========================#

    # Sort Dockables in top-most order
    def __UpdateTopMost( self, widget_id ):
        #print( 'TabbedMDIManager::__UpdateTopMost()...' )

        depth = self.__m_Order.index(widget_id)
        # Reorder OwnerFrames
        for d in reversed( range(1, depth+1) ):
            self.__m_Order[d] = self.__m_Order[d-1]
        self.__m_Order[0] = widget_id

        # Clear TabBar's Focus Index
        for d in reversed( range(1, len(self.__m_Order) ) ):
            self.__m_Dockables[self.__m_Order[d]].tabBar().SetFocusIndex(-1)

        #print( 'TabbedMDIManager::__UpdateTopMost()...%s' % self.__m_Dockables[ self.__m_Order[0] ].windowTitle() )

        # Debug print dockable order
        #for i, widget_id in enumerate(self.__m_Order):
        #    print( '%d: %s' % ( i, self.__m_Dockables[widget_id].windowTitle() ) )



    # Detach content widget from TabWidget
    def __DetachFloater( self, owner_id, index ):

        #print( 'TabbedMDIManager::__DetachFloater()...%d' % index )

        ownerWidget = self.__m_Dockables[ owner_id ]

        floater = Floater()

        # connect signals
        floater.SelectSignal.connect( self.__SetCurrenFloaterID )
        floater.MoveSignal.connect( self.__CheckFloaterIntersection )
        floater.ReleaseSignal.connect( self.__AttachFloater )
        floater.CloseSignal.connect( self.__DeleteFloater )

        # transfer content widget to floater
        contentWidget = ownerWidget.widget( index )
        floater.SetAttribs( { 'TabClosable': ownerWidget.IsTabClosable(index), 'Size': ownerWidget.size() } )
        floater.setWindowTitle( contentWidget.windowTitle() )
        floater.resize( contentWidget.size() )
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



    def __Cleanup( self, destroyContentWidgets=True ):
        #print( 'TabbedMDIManager::__Cleanup()...' )

        # Delete unused dockables
        for widget_id, widget in list( self.__m_Dockables.items() ):
            if( widget.IsTrashed() ):
                self.__DeleteDockable( widget_id )

        # Delete unparented content widgets
        for widget_id, widget in list( self.__m_ContentWidgets.items() ):
            if( widget.parentWidget() is None ):
                self.__DeleteContentWidget( widget_id, destroyContentWidgets )

        # Delete floaters
        for float_id in list( self.__m_Floaters.keys() ):
            self.__DeleteFloater( float_id )


        # Debug print dockables/contentWidgets status
        #self.Info()



    def __DeleteDockable( self, widget_id ):
        #print( 'TabbedMDIManager::__DeleteDockable()...' )
        try:
            # Delete dockable
            self.__m_Dockables[ widget_id ].Release()
            self.__m_Dockables[ widget_id ].deleteLater()
            del self.__m_Dockables[ widget_id ]
            self.__m_Order.remove( widget_id )

        except:
            traceback.print_exc()



    def __DeleteContentWidget( self, widget_id, destroy: bool ) -> None:
        #print( 'TabbedMDIManager::__DeleteContentWidget()...', widget_id )
        try:
            self.__m_ContentWidgets[ widget_id ].setParent(None)
            if( destroy ): self.__m_ContentWidgets[ widget_id ].deleteLater()
            del self.__m_ContentWidgets[ widget_id ]

        except:
            traceback.print_exc()



    def __DeleteFloater( self, widget_id ):
        #print( 'TabbedMDIManager::__DeleteFloater()...' )
        try:
            self.__m_Floaters[ widget_id ].Release()
            self.__m_Floaters[ widget_id ].deleteLater()
            del self.__m_Floaters[ widget_id ]

        except:
            traceback.print_exc()



    def __MergeDockables( self ):
        #print( 'TabbedMDIManager::__MergeDockables()...' )

        emptyOwnerIDs = [ owner_id for owner_id, widget in self.__m_Dockables.items() if widget.IsTrashed() ]

        # Transfer floater's content widget to dockable.
        for floater in self.__m_Floaters.values():
            ownerWidget = self.__m_Dockables[ emptyOwnerIDs.pop() ] if bool(emptyOwnerIDs) else self.__m_Dockables[ self.AddDockable(DockableFrame, Duration.Volatile) ]
            
            if( floater.layout().count() > 0 ):

                contentWidget = floater.layout().itemAt(0).widget()


                ownerWidget.addTab( contentWidget, contentWidget.windowTitle() )
                ownerWidget.SetTabClosable( 0, floater.GetAttribs()[ 'TabClosable' ] )
                ownerWidget.resize( floater.GetAttribs()[ 'Size' ] )
                ownerWidget.activateWindow()
                ownerWidget.show()

                ownerWidget.move( floater.pos() )
                
                ownerWidget.SetTrash( False )

        self.__Cleanup()



    def __DragFloater( self, globalPos: QPoint ):
        #print( 'TabbedMDIManager::__DragFloater()...' )
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
        #print( 'TabbedMDIManager::__AttachFloater()...' )

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

        self.__MergeDockables()



    def __AttachDockable( self, widget_id, globalPos ):
        #print( 'TabbedMDIManager::__AttachDockable()...' )

        srcDockable = self.__m_Dockables[ widget_id ]
        numActiveSrcTabs = srcDockable.NumActiveTabs()
        srcCurrentIndex = srcDockable.currentIndex()

        for owner_id in self.__m_Order:

            destDockable = self.__m_Dockables[ owner_id ]
            if( not destDockable.IsActive() ): continue

            tabBar = destDockable.tabBar()
            index = tabBar.tabAt( tabBar.mapFromGlobal( globalPos ) )

            if( index != -1 ):
                for i in range( numActiveSrcTabs ):
                    # get widget from top
                    contentWidget = srcDockable.widget(0)
                    tabClosable = srcDockable.IsTabClosable(0)

                    # insert into tab position[index + i]
                    destDockable.insertTab( index+i, contentWidget, contentWidget.windowTitle() )
                    destDockable.SetTabClosable( index+i, tabClosable )
                    contentWidget.setVisible(True)

                destDockable.setCurrentIndex( index + srcCurrentIndex )# Restore srcDockable's current tab selected.
                destDockable.activateWindow()
        
                tabBar.SetFocusIndex(-1)

                # Delete dockable
                self.__DeleteDockable( widget_id )

                # Debug print
                #self.Info()

                break



    # Debug print dockables/contentWidgets status
    def Info( self ):
        print( '//==================== TabbedMDIManager::Info()... ====================//' )
        print( '  Dockables:', len(self.__m_Dockables) )
        for dockable in self.__m_Dockables.values():
            print( '    name: \'{}\', type: {}'.format( dockable.windowTitle(), dockable.__class__.__name__ ) )
        print()
        print( '  ContentWidgets:', len(self.__m_ContentWidgets) )
        for content in self.__m_ContentWidgets.values():
            print( '    name: \'{}\', hasParent: {}, type: {}'.format( content.windowTitle(), bool(content.parentWidget()), content.__class__.__name__ ) )

        print()





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
#    #print( '' )
