from oreorelib.ui.pyqt5.helper import *

from .graphicssettings import *



# https://wiki.qt.io/Smooth_Zoom_In_QGraphicsView/ja
class GraphicsView(QGraphicsView):

    #WidgetClosed = pyqtSignal()
    FocusViewIdChanged = pyqtSignal(object)
    RenderViewIdChanged = pyqtSignal(object)

    def __init__( self, key, gridstep ):
        super(GraphicsView, self).__init__()

        self.__m_Key = key
        self.__m_GridStep = gridstep
        self.__m_ZoomScale = 1.0
        self.__m_PrevPos = QPoint()
        
        self.__m_MouseMode = MouseMode.DoNothing
        self.__m_RubberBand = QRubberBand( QRubberBand.Rectangle, self )

        self.setStyleSheet( UIStyle.g_EditorStyleSheet )
        self.setRenderHints( QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing )
        pal = QPalette()
        pal.setBrush( QPalette.Highlight, QColor(170,115,26) )#QColor(255,127,39)
        self.__m_RubberBand.setPalette(pal)

        #self.setViewport(QOpenGLWidget())# これ使うと遅くない?
        self.setOptimizationFlags( QGraphicsView.DontSavePainterState )
        self.setViewportUpdateMode( QGraphicsView.SmartViewportUpdate )
        self.setCacheMode( QGraphicsView.CacheBackground )

        self.setResizeAnchor( QGraphicsView.AnchorViewCenter )

        self.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )

        self.setAcceptDrops(True)



    def __del__( self ):
        print( 'GraphicsView::__del__()...' )
        self.Release()



    def Release( self ):
        try:
            print( 'GraphicsView::Release()...' )

            self.setViewport(None)
            #self.FocusViewIdChanged.disconnect()
            #self.RenderViewIdChanged.disconnect()

            if( self.isSignalConnected( getSignal(self,"FocusViewIdChanged") ) ):
                print("  disconnecting signal FocusViewIdChanged")
                self.FocusViewIdChanged.disconnect()

            if( self.isSignalConnected( getSignal(self,"RenderViewIdChanged") ) ):
                print("  disconnecting signal RenderViewIdChanged")
                self.RenderViewIdChanged.disconnect()

        except:
            traceback.print_exc()



    def CenterOn( self, pos, zoom ):

        # reset scale transform
        self.setTransform( QTransform().scale( 1.0, 1.0 ) )

        # fit view
        w = self.viewport().width()
        h = self.viewport().height()

        wf = self.mapToScene( QPoint(w-1, 0) ).x() - self.mapToScene(QPoint(0,0)).x()
        hf = self.mapToScene( QPoint(0, h-1) ).y() - self.mapToScene(QPoint(0,0)).y()

        lf = -0.5 * w + pos.x()
        tf = -0.5 * h + pos.y()
        
        self.setSceneRect( lf, tf, wf, hf )
        self.fitInView( lf, tf, wf, hf )# using fitInView to avoid QGraphicsView::centerOn bug.

        # set scaling
        self.__m_ZoomScale = zoom
        self.setTransform( QTransform().scale( self.__m_ZoomScale, self.__m_ZoomScale ) )


    
    def __ChangeSelection( self, items, op ):

        change_func = {
            'true': lambda item : item.setSelected( True ),
            'false': lambda item : item.setSelected( False ),
            'invert': lambda item : item.setSelected( not item.isSelected() )
        }
        # Invert items selection inside rubberband at once.
        self.scene().blockSignals(True)
        for item in items: change_func[op](item)
        self.scene().blockSignals(False)

        # Emit selection changed signal.
        self.scene().selectionChanged.emit()



    ######################## QGraphicsView func override #########################

    # reference implementation of zoom in/out using mouse wheel:
    #  old: http://stackoverflow.com/questions/19113532/qgraphicsview-zooming-in-and-out-under-mouse-position-using-mouse-wheel
    #  current: http://blog.automaton2000.com/2014/04/mouse-centered-zooming-in-qgraphicsview.html
    def wheelEvent( self, event ):

        if( event.angleDelta().x() == 0 ):

            pos  = event.pos()
            posf = self.mapToScene(pos)

            by = 1.0
            angle = event.angleDelta().y()

            if( angle > 0 ):    by = 1 + ( angle / 360 * 0.2)
            elif( angle < 0 ):  by = 1 - (-angle / 360 * 0.2)
            else:               by = 1

            self.__m_ZoomScale *= by
            self.__m_ZoomScale = min(max(self.__m_ZoomScale,0.1), 5.0)
            #self.scale(by, by)
            self.setTransform( QTransform().scale( self.__m_ZoomScale, self.__m_ZoomScale ) )


            w = self.viewport().width()
            h = self.viewport().height()

            wf = self.mapToScene( QPoint(w-1, 0) ).x() - self.mapToScene(QPoint(0,0)).x()
            hf = self.mapToScene( QPoint(0, h-1) ).y() - self.mapToScene(QPoint(0,0)).y()

            lf = posf.x() - pos.x() * wf / w
            tf = posf.y() - pos.y() * hf / h

            # try to set viewport properly
            self.setSceneRect( lf, tf, wf, hf )
            #self.ensureVisible( lf, tf, wf, hf, 0, 0 )

            newPos = self.mapToScene(pos)
           
            # readjust according to the still remaining offset/drift. I don't know how to do this any other way
            self.setSceneRect( QRectF( QPointF(lf, tf) - newPos + posf, QSizeF(wf, hf)) )
            #self.ensureVisible( QRectF( QPointF(lf, tf) - newPos + posf, QSizeF(wf, hf)), 0, 0 )
            
            event.accept()



    def mousePressEvent(self, event):

        #print( 'GraphicsView::mousePressEvent()...' )

        self.__m_PrevPos = event.pos()

        if( event.modifiers() == Qt.AltModifier and event.button() == Qt.MiddleButton ):# View Translation
            self.__m_MouseMode = MouseMode.MoveViewport
            self.setCursor(Qt.SizeAllCursor)
            return

        # Walkaround for 'Ctrl+MouseLeft' item selection across multiple QGraphicsViews.
        elif( event.modifiers() == Qt.ControlModifier and event.button() == Qt.LeftButton ):# Switch Selection
            if( self.itemAt(event.pos()) ):
                #print( 'GraphicsView::mousePressEvent()... Detected Switch Selection.' )
                self.__m_MouseMode = MouseMode.SwitchSelection
                return
            else:
                self.__m_MouseMode = MouseMode.RubberBandSwitchSelection

        elif( event.button() == Qt.LeftButton and self.itemAt(event.pos())==None ):# Rubberband Selection
            self.__m_MouseMode = MouseMode.RubberBandSelection

        super(GraphicsView, self).mousePressEvent(event)



    def mouseMoveEvent(self, event):

        if( self.__m_MouseMode == MouseMode.MoveViewport ):
            delta = (self.mapToScene(event.pos()) - self.mapToScene(self.__m_PrevPos)) * -1.0
            center = QPoint( self.viewport().width()/2 + delta.x(), self.viewport().height()/2 + delta.y() )
            newCenter = self.mapToScene(center)
            
            self.__m_PrevPos = event.pos()
            self.centerOn(newCenter)

            rect = self.sceneRect()
            self.setSceneRect( rect.x() + delta.x(), rect.y() + delta.y(), rect.width(), rect.height() )
            #self.ensureVisible( rect.x() + delta.x(), rect.y() + delta.y(), rect.width(), rect.height(), 0, 0 )

        elif( self.__m_MouseMode == MouseMode.RubberBandSelection ):
            self.__m_RubberBand.setGeometry( QRect(self.__m_PrevPos, event.pos()).normalized() )
            self.__m_RubberBand.show()

        elif( self.__m_MouseMode == MouseMode.RubberBandSwitchSelection ):
            self.__m_RubberBand.setGeometry( QRect(self.__m_PrevPos, event.pos()).normalized() )
            self.__m_RubberBand.show()

        super(GraphicsView, self).mouseMoveEvent(event)
 


    def mouseReleaseEvent(self, event):

        #print( 'GraphicsView::mouseReleaseEvent()...' )

        if( self.__m_MouseMode == MouseMode.MoveViewport ):
            self.setCursor(Qt.ArrowCursor)

        elif( self.__m_MouseMode == MouseMode.RubberBandSelection ):
            if( self.__m_RubberBand.isVisible() ):
                self.__m_RubberBand.hide()
                self.__ChangeSelection( self.items( self.__m_RubberBand.geometry(), Qt.IntersectsItemShape ), 'true' )

        elif( self.__m_MouseMode == MouseMode.SwitchSelection ):# Walkaround for 'Ctrl+MouseLeft' item selection through multiple QGraphicsViews.
            topmost_item = ( self.itemAt( event.pos() ), )
            if( any( topmost_item ) ):
                self.__ChangeSelection( topmost_item, 'invert' )

        elif( self.__m_MouseMode == MouseMode.RubberBandSwitchSelection ):# Walkaround for 'Ctrl+MouseLeft' rubberband item selection through multiple QGraphicsViews.
            if( self.__m_RubberBand.isVisible() ):
                self.__m_RubberBand.hide()
                self.__ChangeSelection( self.items( self.__m_RubberBand.geometry(), Qt.IntersectsItemShape ), 'invert' )

        self.__m_MouseMode = MouseMode.DoNothing

        super(GraphicsView, self).mouseReleaseEvent(event)


       
    def drawBackground( self, painter, rect ):
        # draw horizontal grid
        painter.setPen( QPen( QColor(42, 42, 42), 1.0/self.__m_ZoomScale ) )
        
        start = int(rect.top()) + self.__m_GridStep / 2
        start -= start % self.__m_GridStep

        if(start > rect.top()):
            start -= self.__m_GridStep
        
        y = start - self.__m_GridStep
        while( y < rect.bottom() ):
            y += self.__m_GridStep
            painter.drawLine(rect.left(), y, rect.right(), y)

        # now draw vertical grid
        #start = rect.left() % self.__m_GridStep
        start = int(rect.left()) + self.__m_GridStep / 2
        start -= start % self.__m_GridStep

        if(start > rect.left()):
            start -= self.__m_GridStep
        
        x = start - self.__m_GridStep
        while( x < rect.right() ):
            x += self.__m_GridStep
            painter.drawLine(x, rect.top(), x, rect.bottom())



    def dragMoveEvent( self, event ):
        pass
        #return super(GraphicsView, self).dragMoveEvent(event)



    def dragLeaveEvent( self, event ):
        pass
        #return super(GraphicsView, self).dragLeaveEvent(event)



    def resizeEvent( self, event ):
        self.viewport().update()
        return super(GraphicsView, self).resizeEvent(event)



    def focusInEvent( self, event ):
        #print( 'GraphicsView::focusInEvent()...' )
        self.FocusViewIdChanged.emit( self.__m_Key )
        return super(GraphicsView, self).focusInEvent(event)



    def paintEvent( self, event ):
        self.RenderViewIdChanged.emit( self.__m_Key )
        super(GraphicsView, self).paintEvent(event)



    # View specific key event
    def keyPressEvent( self, event ):
        super(GraphicsView, self).keyPressEvent(event)

        if( event.key()==Qt.Key_F ):# center on
            if( not self.scene().items() ):
                self.CenterOn( QPointF(0.0,0.0), 1.0 )
                return

            itemsRect = QRectF()
            items = self.scene().selectedItems()
            if( items ):# unite selected items' boundengRects
                for item in self.scene().selectedItems():
                    itemsRect |= item.sceneBoundingRect()
            else:# use all items' rects if nothing selected.
                itemsRect = self.scene().itemsBoundingRect()

            zoom = 1.0 if itemsRect.isEmpty() else min( min( self.width() / itemsRect.width(), self.height() / itemsRect.height() ), 1.0 )
            self.CenterOn( itemsRect.center(), zoom )



    def closeEvent( self, event ):
        super(GraphicsView, self).closeEvent(event)
        #self.WidgetClosed.emit()