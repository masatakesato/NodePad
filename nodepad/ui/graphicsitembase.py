from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtOpenGL import *
from PyQt5.QtCore import *


class GraphicsNodeItem(QGraphicsItem):

    def __init__(self):
        super(GraphicsNodeItem, self).__init__()

        self.__m_RenderLayerID = None


    def SetLayerID( self, layer_id ):
        self.__m_RenderLayerID = layer_id


    def LayerID( self ):
        return self.__m_RenderLayerID



class GraphicsPathItem(QGraphicsPathItem):

    def __init__(self):
        super(GraphicsPathItem, self).__init__()

        self.__m_RenderLayerID = None


    def SetLayerID( self, layer_id ):
        self.__m_RenderLayerID = layer_id


    def LayerID( self ):
        return self.__m_RenderLayerID



class GraphicsPortItem(QGraphicsItem):

    def __init__(self):
        super(GraphicsPortItem, self).__init__()

        self.__m_RenderLayerID = None

        #self.__m_FillColor = QColor()
        #self.__m_BorderColor = QColor()
        #self.__m_LabelColor = QColor()


    def SetLayerID( self, layer_id ):
        self.__m_RenderLayerID = layer_id


    def LayerID( self ):
        return self.__m_RenderLayerID

    
    #def SetFillColor( self, color ):
    #    self.__m_FillColor = color

   
    #def SetBorderColor( self, color ):
    #    self.__m_BorderColor = color


    #def SetLabelColor( self, color ):
    #    self.__m_LabelColor = color