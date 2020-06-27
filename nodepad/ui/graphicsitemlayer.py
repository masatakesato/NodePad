import sys
import traceback

from .graphicsitembase import *
from .nodeitem import Node
from .groupitem import Group



class GraphicsItemLayer():

    def __init__( self, layer_id ):
        self.__m_ID = layer_id
        self.__m_refItems = {}# key: object's id(uuid), value:


    def Release( self ):
        self.Clear()


    def Clear( self ):
        for key in self.__m_refItems.keys():
            self.__m_refItems[key] = None
        self.__m_refItems.clear()


    def AddItem( self, item ):
        self.__m_refItems[ item.ID() ] = item
        item.SetLayerID( self.__m_ID )

        for childitem in item.childItems():
            self.__m_refItems[ childitem.ID() ] = childitem
            childitem.SetLayerID( self.__m_ID )


    def RemoveItem( self, item_id ):
        try:
            item = self.__m_refItems[ item_id ]
            item.SetLayerID( None )

            for childitem in item.childItems():
                childitem.SetLayerID( None )
                self.__m_refItems[ childitem.ID()  ] = None
                del self.__m_refItems[ childitem.ID()  ]

            self.__m_refItems[ item_id ] = None
            del self.__m_refItems[ item_id ]

        except:
            traceback.print_exc()


    def NumItems( self ):
        return len(self.__m_refItems)


    def HasItem( self, item_id ):
        return item_id in self.__m_refItems


    def BoundingRect( self ):
        left = sys.float_info.max
        right = -sys.float_info.max
        bottom = -sys.float_info.max
        top = sys.float_info.max
        
        for item in self.__m_refItems.values():
            if( isinstance( item, Group ) or isinstance(item, Node ) ):
                left = min( left, item.sceneBoundingRect().left() )
                right = max( right, item.sceneBoundingRect().right() )
                bottom = max( bottom, item.sceneBoundingRect().bottom() )
                top = min( top, item.sceneBoundingRect().top() )

        return QRectF( left, top, right-left, bottom-top )