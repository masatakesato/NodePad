from enum import IntEnum

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtOpenGL import *
from PyQt5.QtCore import *

import oreorelib.ui.pyqt5.stylesheet as UIStyle

from ..config.figure_params import *



############################### MainWidget #################################

g_DataChangedSymbol = { False: '', True: '*' }



############################### NodeEditor #################################

g_LabelFont = QFont('Aerial', 9.0)


g_LabelColor = QColor(255, 255, 255)
g_PortFrameColor = QColor(32, 32, 32)
g_PortColor = [ QColor(150, 200, 100), QColor(80, 90, 75) ] 
g_EdgeColor = [ QColor(164, 128, 100), QColor(255, 127, 39) ]

g_NodeFrameColor = [ QColor(32, 32, 32), QColor(255, 127, 39) ]
g_NodeShadowColor = QColor(32, 32, 32)

g_ArrowColor = QColor(120, 100, 64)
g_ArrowFrameColor = [ QColor(32, 32, 32), QColor(255, 127, 39) ]

g_ButtonFrameColor = [ QColor(48, 48, 48), QColor(32, 32, 32) ]

# Background Graphics Settings
g_GridStep = 50



############################# Attribute Editor #############################

g_ExpandWidgetFont = QFont('Aerial', 9.0, QFont.Bold)
g_AttribNameFont = QFont('Aerial', 9.0)

g_AttribLabelWidth = 50
g_AttribMarginLeft = 0
g_AttribMarginTop  = 0
g_AttribMarginRight = 0
g_AttribMarginBottom = 0

g_ImagePath_ArrowCollaped = ':/resource/images/arrow-right.png'
g_ImagePath_ArrowExpanded = ':/resource/images/arrow-down.png'






class MouseMode(IntEnum):

    DoNothing = -1

    # QGraphicsScene's item operation
    DrawEdge = 0
    MoveNode = 1
    MoveGroup = 2
    MoveGroupIO = 3
    MoveSymbolicLink = 4
    RemoveSymbolicLink = 5

    # QGraphicsView's operation    
    RubberBandSelection = 6
    MoveViewport = 7

    # Other operations
    ContextMenu = 8