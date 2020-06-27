# https://stackoverflow.com/questions/46681266/qscrollarea-with-flowlayout-widgets-not-resizing-properly

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *




class ScrollBar( QScrollBar ):

    signal_maxlimit = pyqtSignal()
    signal_minlmit = pyqtSignal()


    def __init__( self, parent=None ):
        super( ScrollBar, self ).__init__( parent )


    def wheelEvent( self, event ):
        super(ScrollBar, self).wheelEvent(event)

        if( self.isEnabled() ):
            if( self.value() == self.maximum() and event.angleDelta().y() < -10 ):
                print( 'scrollbar at max limit' )
                self.signal_maxlimit.emit()

            elif( self.value() == self.minimum() and event.angleDelta().y() > +10 ):
                print( 'scrollbar at min limit' )
                self.signal_minlmit.emit()


    def mouseMoveEvent(self, QMouseEvent):
        super(ScrollBar, self).mouseMoveEvent(QMouseEvent)

        if( self.isEnabled() ):
            if( self.value() == self.maximum() ):
                print( 'scrollbar at max limit' )
                self.signal_maxlimit.emit()

            elif( self.value() == self.minimum() ):
                print( 'scrollbar at min limit' )
                self.signal_minlmit.emit()


    def mousePressEvent( self, QMouseEvent ):
        super(ScrollBar, self).mousePressEvent(QMouseEvent)

        if( self.isEnabled() ):
            if( self.value() == self.maximum() ):
                print( 'scrollbar at max limit' )
                self.signal_maxlimit.emit()

            elif( self.value() == self.minimum() ):
                print( 'scrollbar at min limit' )
                self.signal_minlmit.emit()




class ScrollArea( QScrollArea ):
    
    def __init__( self, parent=None ):
        super(ScrollArea, self).__init__(parent=parent)

        self.setVerticalScrollBar( ScrollBar(self) ) 
        self.setHorizontalScrollBar( ScrollBar(self) )
        self.signal_v = self.verticalScrollBar().signal_maxlimit
        self.signal_h = self.horizontalScrollBar().signal_maxlimit



class FlowLayout( QLayout ):

    heightChanged = pyqtSignal(int)

    def __init__( self, parent=None, mergin=0, spacing=-1 ):
        super(QLayout, self).__init__(parent)
        
        self.setSpacing( spacing )

        self.__m_ItemList = []


    def __del__( self ):
        while self.count():
            self.takeAt(0)


    def addItem( self, item ):
        self.__m_ItemList.append( item )

    
    def AddSpacing( self, size ):
        self.AddItem( QSpacerItem(size, 0, QSizePolicy.Fixed, QSizePolicy.Minimum) )

    
    def count( self ):
        return len( self.__m_ItemList )

    
    def itemAt( self, index ):
        try:
            return self.__m_ItemList[index]
        except:
            return None

    
    def takeAt( self, index ):
        try:
            return self.__m_ItemList.pop(index)
        except:
            return None


    def expandingDirections( self ):
        return Qt.Orientations( Qt.Orientation(0) )


    def hasHeightForWidth( self ):
        return True


    def heightForWidth( self, width ):
        height = self._do_layout( QRect(0, 0, width, 0), True )
        return height


    def setGeometry( self, rect ):
        super(FlowLayout, self).setGeometry(rect)
        self._do_layout( rect, False )


    def sizeHint(self):
        return self.minimumSize()


    def minimumSize( self ):
        size = QSize()

        for item in self.__m_ItemList:
            minsize = item.minimumSize()
            extent = item.geometry().bottomRight()
            size = size.expandedTo( QSize(minsize.width(), extent.y()) )

        margin = self.contentsMargins().left()
        size += QSize( 2*margin, 2*margin )
        return size


    def _do_layout( self, rect, test_only=False ):
        m = self.contentsMargins()
        effective_rect = rect.adjusted( +m.left(), +m.top(), -m.right(), -m.bottom() )
        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0

        for item in self.__m_ItemList:
            wid = item.widget()

            space_x = self.spacing()
            space_y = self.spacing()
            if( wid is not None ):
                space_x += wid.style().layoutSpacing( QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal )
                space_y += wid.style().layoutSpacing( QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical )
            
            next_x = x + item.sizeHint().width() + space_x
            if( next_x - space_x > effective_rect.right() and line_height > 0 ):
                x = effective_rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if( not test_only ):
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        new_height = y + line_height - rect.y()
        self.heightChanged.emit(new_height)
        
        return new_height
