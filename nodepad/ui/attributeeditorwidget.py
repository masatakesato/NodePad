import functools
import traceback

from ..component.descriptors import *

from .graphicssettings import *




class NodeInfo_Widget(QFrame):

    def __init__( self, object_id, label_str, parent, callback ):

        super(NodeInfo_Widget, self).__init__(parent)

        self.__m_refCallbackFunc = callback

        self.__m_ID = object_id

        # initialize label
        self.__m_Label = QLabel( label_str + ': ' )
        self.__m_Label.setStyleSheet( UIStyle.g_LabelStyleSheet )
        self.__m_Label.setFont( g_AttribNameFont )
        self.__m_Label.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        self.__m_Label.setAlignment( Qt.AlignRight | Qt.AlignVCenter )
        self.__m_Label.setMinimumWidth(100)

        # initialize lineEdit
        self.__m_LineEdit = QLineEdit()
        self.__m_LineEdit.setStyleSheet( UIStyle.g_LineEditStyleSheet )
        self.__m_LineEdit.setFixedWidth(150)
        self.__m_LineEdit.setAlignment( Qt.AlignLeft | Qt.AlignVCenter )
        self.__m_LineEdit.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )

        self.__m_CurrentValue = ''

        # connect signal and slot.
        self.__m_LineEdit.editingFinished.connect( self.__EditingFinishedSlot )

        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.__m_Label )
        layout.addWidget( self.__m_LineEdit )
        #layout.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        #layout.setAlignment( Qt.AlignVCenter | Qt.AlignHCenter )

        layout.addStretch()

        self.setLayout( layout )



    #def __del__( self ):
    #    self.__m_LineEdit.returnPressed.disconnect()
    #    self.__m_LineEdit.editingFinished.disconnect()



    def Release( self ):
        self.__m_LineEdit.editingFinished.disconnect()
        self.__m_refCallbackFunc = None



    def ID( self ):
        return self.__m_ID



    def SetValue( self, value ):
        try:
            self.__m_LineEdit.setText( value )
            self.__m_CurrentValue = value
        except:
            traceback.print_exc()



    def __EditingFinishedSlot( self ):
        print( 'NodeInfo_Widget::__EditingFinishedSlot()...' )
        self.__m_LineEdit.blockSignals(True)
        self.__m_LineEdit.clearFocus()
        self.__m_LineEdit.blockSignals(False)

        value = self.__m_LineEdit.text()
        if( value ):#and not value.isspace() ):
            self.__m_refCallbackFunc( self.__m_ID, self.__m_LineEdit.text() )
            self.__m_CurrentValue = value
        else:
            self.__m_LineEdit.setText( self.__m_CurrentValue )
            



class HorizontalLine(QFrame):

    def __init__( self, *args, **kwargs ):
        super(HorizontalLine, self).__init__(*args, **kwargs)

        self.setStyleSheet( UIStyle.g_SplitLineStyleSheet )
        self.setFrameShape( QFrame.HLine )
        
        self.setFrameShadow( QFrame.Sunken )



class VerticalLine(QFrame):

    def __init__( self, *args, **kwargs ):
        super(VerticalLine, self).__init__(*args, **kwargs)

        self.setStyleSheet( UIStyle.g_SplitLineStyleSheet )
        self.setFrameShape( QFrame.VLine )
        self.setFrameShadow( QFrame.Sunken )



class AttributeEditor_ScalarDouble(QFrame):

    def __init__( self, object_id, label, minval, maxval, decimals, singlestep, parent, callback ):
        super(AttributeEditor_ScalarDouble, self).__init__(parent)
        
        self.__m_refCallbackFunc = callback

        self.__m_ID = object_id

        # range/precision settings
        self.__m_RangeMin = minval
        self.__m_RangeMax = maxval
        self.__m_Decimals = decimals
        self.__m_SingleStep = singlestep        

        # initialize label
        self.__m_Label = QLabel( label )
        self.__m_Label.setStyleSheet( UIStyle.g_LabelStyleSheet )
        self.__m_Label.setFont( g_AttribNameFont )
        self.__m_Label.setFixedWidth( g_AttribLabelWidth )
        self.__m_Label.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        self.__m_Label.setAlignment( Qt.AlignRight | Qt.AlignCenter )

        # initialize spinbox 
        self.__m_SpinBox = QDoubleSpinBox()
        self.__m_SpinBox.setStyleSheet( UIStyle.g_SpinBoxStyleSheet )
        self.__m_SpinBox.setDecimals( self.__m_Decimals )
        self.__m_SpinBox.setSingleStep( self.__m_SingleStep )
        self.__m_SpinBox.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        self.__m_SpinBox.setRange( self.__m_RangeMin, self.__m_RangeMax )

        # initialize slider
        self.__m_Slider = QSlider(Qt.Horizontal)
        self.__m_Slider.setStyleSheet( UIStyle.g_SliderStyleSheet )
        self.__m_Slider.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        self.__m_Slider.setRange(0,1e+6)
        self.__m_Slider.setSingleStep(1)
        self.__m_Slider.setPageStep(1e+5)

        #self.__m_Slider.setValue( 1 )
        self.__m_SpinBox.setValue( float('nan') ) # initialize using dummy value before signal/slot connection

        # connect signal and slot
        self.__m_SpinBox.valueChanged.connect( self.__ValueChangedSlot_Spin )
        self.__m_SpinBox.editingFinished.connect( self.__EditingFinishedSlot_Spin )
        self.__m_Slider.valueChanged.connect( self.__ValueChangedSlot_Slider )

        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.__m_Label )
        layout.addWidget( self.__m_SpinBox )
        layout.addWidget( self.__m_Slider )
        layout.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )

        self.setLayout( layout )

        # GUI http://puarts.com/?pid=922


    #def __del__( self ):
    #    self.__m_SpinBox.valueChanged.disconnect()
    #    self.__m_SpinBox.editingFinished.disconnect()
    #    self.__m_Slider.valueChanged.disconnect()

    def Release( self ):
        self.__m_SpinBox.valueChanged.disconnect()
        self.__m_SpinBox.editingFinished.disconnect()
        self.__m_Slider.valueChanged.disconnect()
        self.__m_refCallbackFunc = None


    def ID( self ):
        return self.__m_ID


    def SetLabel( self, label ):
        self.__m_Label.setText( label )


    def SetValue( self, value ):
        try:
            self.__m_SpinBox.setValue( value )
        except:
            traceback.print_exc()

    # slots 
    def __ValueChangedSlot_Spin( self, value ):
        #print( 'AttributeEditor_ScalarDouble::valueChanged_Spin()...' )
        val = (value - self.__m_SpinBox.minimum()) / (self.__m_SpinBox.maximum() - self.__m_SpinBox.minimum()) * self.__m_Slider.maximum()
        self.__m_Slider.setValue( int(val) )
        self.__m_refCallbackFunc( self.__m_ID, value )


    def __EditingFinishedSlot_Spin( self ):
        #print( 'AttributeEditor_ScalarDoubleeditingFinished_SpinBox()...')
        self.__m_SpinBox.clearFocus()


    def __ValueChangedSlot_Slider( self, value ):
        #print( 'AttributeEditor_ScalarDouble::valueChanged_Slider()...' )
        val = value / self.__m_Slider.maximum() * (self.__m_SpinBox.maximum() - self.__m_SpinBox.minimum()) + self.__m_SpinBox.minimum()
        self.__m_SpinBox.setValue( val )



class AttributeEditor_ScalarInt(QFrame):

    def __init__( self, object_id, label, minval, maxval, singlestep, pagestep, parent, callback ):

        super(AttributeEditor_ScalarInt, self).__init__(parent)
        
        self.__m_refCallbackFunc = callback

        self.__m_ID = object_id

        # range/step settings
        self.__m_RangeMin = minval
        self.__m_RangeMax = maxval
        self.__m_SingleStep = singlestep
        self.__m_PageStep = pagestep

        # initialize label
        self.__m_Label = QLabel( label )
        self.__m_Label.setStyleSheet( UIStyle.g_LabelStyleSheet )
        self.__m_Label.setFont( g_AttribNameFont )
        self.__m_Label.setFixedWidth( g_AttribLabelWidth )
        self.__m_Label.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        self.__m_Label.setAlignment( Qt.AlignRight | Qt.AlignCenter )

        # initialize spinbox 
        self.__m_SpinBox = QSpinBox()
        self.__m_SpinBox.setStyleSheet( UIStyle.g_SpinBoxStyleSheet )
        self.__m_SpinBox.setSingleStep( self.__m_SingleStep )
        self.__m_SpinBox.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        self.__m_SpinBox.setRange( self.__m_RangeMin, self.__m_RangeMax )

        # initialize slider
        self.__m_Slider = QSlider(Qt.Horizontal)
        self.__m_Slider.setStyleSheet( UIStyle.g_SliderStyleSheet )
        self.__m_Slider.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        self.__m_Slider.setRange( self.__m_RangeMin, self.__m_RangeMax )
        self.__m_Slider.setSingleStep( self.__m_SingleStep )
        self.__m_Slider.setPageStep( self.__m_PageStep )

        #self.__m_SpinBox.setValue( int(float('inf')) ) # initialize using dummy value before signal/slot connection

        # connect signal and slot
        self.__m_SpinBox.valueChanged.connect( self.__ValueChangedSlot_Spin )
        self.__m_SpinBox.editingFinished.connect( self.__EditingFinishedSlot_Spin )
        self.__m_Slider.valueChanged.connect( self.__m_SpinBox.setValue )

        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.__m_Label )
        layout.addWidget( self.__m_SpinBox )
        layout.addWidget( self.__m_Slider )
        layout.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )

        self.setLayout( layout )


    #def __del__( self ):
    #    self.__m_SpinBox.valueChanged.disconnect()
    #    self.__m_SpinBox.editingFinished.disconnect()
    #    self.__m_Slider.valueChanged.disconnect()


    def Release( self ):
        self.__m_SpinBox.valueChanged.disconnect()
        self.__m_SpinBox.editingFinished.disconnect()
        self.__m_Slider.valueChanged.disconnect()
        self.__m_refCallbackFunc = None


    def ID( self ):
        return self.__m_ID


    def SetLabel( self, label ):
        self.__m_Label.setText( label )


    def SetValue( self, value ):
        try:
            self.__m_SpinBox.setValue( value )
        except:
            traceback.print_exc()


    # slots 
    def __ValueChangedSlot_Spin( self, value ):
        self.__m_Slider.setValue( value )
        self.__m_refCallbackFunc( self.__m_ID, value )


    def __EditingFinishedSlot_Spin( self ):
        self.__m_SpinBox.clearFocus()



class AttributeEditor_String(QFrame):

    def __init__( self, object_id, label, parent, callback ):
        super(AttributeEditor_String, self).__init__(parent)

        self.__m_refCallbackFunc = callback

        self.__m_ID = object_id

        # initialize label
        self.__m_Label = QLabel( label )
        self.__m_Label.setStyleSheet( UIStyle.g_LabelStyleSheet )
        self.__m_Label.setFont( g_AttribNameFont )
        self.__m_Label.setFixedWidth( g_AttribLabelWidth )
        self.__m_Label.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        self.__m_Label.setAlignment( Qt.AlignRight | Qt.AlignCenter )

        # initialize lineEdit
        self.__m_LineEdit = QLineEdit()
        self.__m_LineEdit.setStyleSheet( UIStyle.g_LineEditStyleSheet )
        self.__m_LineEdit.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        
        # connect signal and slot
        self.__m_LineEdit.editingFinished.connect( self.__EditingFinishedSlot )

        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.__m_Label )
        layout.addWidget( self.__m_LineEdit )
        layout.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )

        self.setLayout( layout )


    #def __del__( self ):
    #    self.__m_LineEdit.returnPressed.disconnect()
    #    self.__m_LineEdit.editingFinished.disconnect()


    def Release( self ):
        self.__m_LineEdit.editingFinished.disconnect()
        self.__m_refCallbackFunc = None


    def ID( self ):
        return self.__m_ID


    def SetLabel( self, label ):
        self.__m_Label.setText( label )


    def SetValue( self, value ):
        try:
            self.__m_LineEdit.setText( value )
        except:
            traceback.print_exc()

    
    # slot
    def __EditingFinishedSlot( self ):
        #print( 'AttributeEditor_String::__EditingFinishedSlot()...' )
        self.__m_LineEdit.blockSignals(True)
        self.__m_LineEdit.clearFocus()
        self.__m_LineEdit.blockSignals(False)  
        self.__m_refCallbackFunc( self.__m_ID, self.__m_LineEdit.text() )



# Curerntly unused.
class AttributeEditor_Double3(QFrame):

    def __init__( self, object_id, label, parent, callback ):
        super(AttributeEditor_Double3, self).__init__(parent)
        
        self.__m_refCallbackFunc = callback

        self.__m_ID = object_id

        # numeric settings
        self.__m_SingleStep = 0.01
        self.__m_Decimals = 2

        # initialize label
        self.__m_Label = QLabel( label )
        self.__m_Label.setStyleSheet( UIStyle.g_LabelStyleSheet )
        self.__m_Label.setFont( g_AttribNameFont )
        self.__m_Label.setFixedWidth( g_AttribLabelWidth )
        self.__m_Label.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        self.__m_Label.setAlignment( Qt.AlignRight | Qt.AlignCenter )

        # initialize spinbox 
        self.spinBox_X = QDoubleSpinBox()
        self.spinBox_X.setDecimals( self.__m_Decimals )
        self.spinBox_X.setSingleStep( self.__m_SingleStep )
        self.spinBox_X.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        
        self.spinBox_Y = QDoubleSpinBox()
        self.spinBox_Y.setDecimals( self.__m_Decimals )
        self.spinBox_Y.setSingleStep( self.__m_SingleStep )
        self.spinBox_Y.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )

        self.spinBox_Z = QDoubleSpinBox()
        self.spinBox_Z.setDecimals( self.__m_Decimals )
        self.spinBox_Z.setSingleStep( self.__m_SingleStep )
        self.spinBox_Z.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )

        # connect signal and slot
        self.spinBox_X.editingFinished.connect( self.__EditingFinishedSlot_SpinX )
        self.spinBox_Y.editingFinished.connect( self.__EditingFinishedSlot_SpinY )
        self.spinBox_Z.editingFinished.connect( self.__EditingFinishedSlot_SpinZ )

        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.__m_Label )
        layout.addWidget( self.spinBox_X )
        layout.addWidget( self.spinBox_Y )
        layout.addWidget( self.spinBox_Z )
        layout.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )

        self.setLayout( layout )


    #def __del__( self ):
    #    self.spinBox_X.editingFinished.disconnect()
    #    self.spinBox_Y.editingFinished.disconnect()
    #    self.spinBox_Z.editingFinished.disconnect()


    def Release( self ):
        self.spinBox_X.editingFinished.disconnect()
        self.spinBox_Y.editingFinished.disconnect()
        self.spinBox_Z.editingFinished.disconnect()
        self.__m_refCallbackFunc = None


    def ID( self ):
        return self.__m_ID


    def SetLabel( self, label ):
        self.__m_Label.setText( label )


    def SetValue( self, value ):
        try:
            self.spinBox_X.setValue( value[0] )
            self.spinBox_Y.setValue( value[1] )
            self.spinBox_Z.setValue( value[2] )
        except:
            traceback.print_exc()


    # slots
    def __EditingFinishedSlot_SpinX( self ):
        self.spinBox_X.clearFocus()

    def __EditingFinishedSlot_SpinY( self ):
        self.spinBox_Y.clearFocus()

    def __EditingFinishedSlot_SpinZ( self ):
        self.spinBox_Z.clearFocus()



class AttributeEditor_CheckBox(QFrame):

    def __init__( self, object_id, label, parent, callback ):
        super(AttributeEditor_CheckBox, self).__init__(parent)

        self.__m_refCallbackFunc = callback

        self.__m_ID = object_id

        # initialize label
        self.__m_Label = QLabel( label )
        self.__m_Label.setStyleSheet( UIStyle.g_LabelStyleSheet )
        self.__m_Label.setFont( g_AttribNameFont )
        self.__m_Label.setFixedWidth( g_AttribLabelWidth )
        self.__m_Label.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        self.__m_Label.setAlignment( Qt.AlignRight | Qt.AlignCenter )

        # initialize checkbox
        self.checkBox = QCheckBox()
        self.checkBox.setStyleSheet( UIStyle.g_CheckBoxStyleSheet )

        # connect signal and slot
        self.checkBox.toggled.connect( self.__ToggledSlot )

        
        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.__m_Label )
        layout.addWidget( self.checkBox )
        layout.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )

        self.setLayout( layout )


    def Release( self ):
        self.checkBox.toggled.disconnect()
        self.__m_refCallbackFunc = None


    def ID( self ):
        return self.__m_ID


    def SetLabel( self, label ):
        self.__m_Label.setText( label )


    def SetValue( self, value ):
        try:
            self.checkBox.setChecked( value )
        except:
            traceback.print_exc()


    def __ToggledSlot( self ):
        print( 'AttributeEditor_CheckBox::__ToggledSlot()...' )
        self.__m_refCallbackFunc( self.__m_ID, self.checkBox.isChecked() )



# Curerntly unused.
class AttributEditor_CombobBox(QFrame):

    def __init__( self, object_id, label, items, parent ):

        super(AttributEditor_CombobBox, self).__init__(parent)

        self.__m_ID = object_id

        # initialize label
        self.__m_Label = QLabel( label )
        self.__m_Label.setStyleSheet( UIStyle.g_LabelStyleSheet )
        self.__m_Label.setFont( g_AttribNameFont )
        self.__m_Label.setFixedWidth( g_AttribLabelWidth )
        self.__m_Label.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        self.__m_Label.setAlignment( Qt.AlignRight | Qt.AlignCenter )

        # initialize ComboBox
        self.__m_ComboBox = QComboBox()
        self.__m_ComboBox.addItems( items )
        self.__m_ComboBox.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        
        # connect signal and slot
        
        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.__m_Label )
        layout.addWidget( self.__m_ComboBox )
        layout.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )

        self.setLayout( layout )


    def ID( self ):
        return self.__m_ID


    def SetLabel( self, label ):
        self.__m_Label.setText( label )


    def SetValue( self, value ):
        try:
            self.__m_ComboBox.setCurrentIndex( value )
        except:
            traceback.print_exc()



class ExpandWidgetHeader(QLabel):

    headerClicked = pyqtSignal()# bool )

    def __init__( self, pixmap_collapse_path, pixmap_expand_path, caption='', parent=None ):
        super(ExpandWidgetHeader, self).__init__(parent=parent)

        self.setText( caption )
        self.setStyleSheet( UIStyle.g_ExpandWidgetHeaderStyleSheet )
        self.setFixedHeight(20)

        self.setFont( g_ExpandWidgetFont )

        self.__m_Pixmap = { True:QPixmap(pixmap_collapse_path).scaledToHeight( self.height(), Qt.SmoothTransformation ),
                           False:QPixmap(pixmap_expand_path).scaledToHeight( self.height(), Qt.SmoothTransformation ) }

        self.__m_Hidden = False


    def setPixmap( self, hidden ):
        self.__m_Hidden = hidden


    def sizeHint( self ):
        parentHint = super(ExpandWidgetHeader, self).sizeHint()
        # add margins here if needed
        return QSize( parentHint.width() + self.__m_Pixmap[self.__m_Hidden].width(),
                     max(parentHint.height(), self.__m_Pixmap[self.__m_Hidden].height()) )


    def paintEvent( self, event ):
        super(ExpandWidgetHeader, self).paintEvent(event)

        #if( self.__m_Pixmap.isNull()==False ):
        y = ( self.height() - self.__m_Pixmap[self.__m_Hidden].height() ) / 2 # add margin if needed
        painter = QPainter(self)
        painter.drawPixmap(5, y, self.__m_Pixmap[self.__m_Hidden]) # hardcoded horizontal margin


    def mouseReleaseEvent( self, event ):
        self.headerClicked.emit()



class ExpandWidgetBody(QFrame):

    def __init__(self, parent=None):
        super(ExpandWidgetBody, self).__init__(parent=parent)

        self.setStyleSheet( UIStyle.g_ExpandWidgetBodyStyleSheet + UIStyle.g_ScrollBarStyleSheet )
        self.__m_Layout = QVBoxLayout()
        self.setLayout( self.__m_Layout )


    def AddWidget( self, widget ):
        try:
            self.__m_Layout.addWidget( widget )
        except:
            traceback.print_exc()


    def RemoveWidget( self, widget ):
        try:
            self.__m_Layout.removeWidget( widget )
        except:
            traceback.print_exc()



class ExpandWidget(QFrame):

    expandChanged = pyqtSignal()

    def __init__( self, caption='', hidden=False, parent=None ):
        super(ExpandWidget, self).__init__(parent=parent)

        self.setStyleSheet( UIStyle.g_ExpandWidgetStyleSheet )
        self.__m_Header = ExpandWidgetHeader( g_ImagePath_ArrowCollaped, g_ImagePath_ArrowExpanded, caption )
        self.__m_Body = ExpandWidgetBody()
        self.__m_Hidden = hidden
        
        layout = QVBoxLayout()
        layout.setContentsMargins( 3, 3, 3, 6 )
        self.setLayout( layout )

        layout.setSpacing(2)
        layout.addWidget( self.__m_Header )
        layout.addWidget( self.__m_Body )

        self.__m_Header.headerClicked.connect( self.__HeaderClickedSlot )
        

    def Body( self ):
        return self.__m_Body


    def SetExpand( self, flag ):
        self.__m_Hidden = not flag
        self.__m_Header.setPixmap( self.__m_Hidden )
        if( self.__m_Hidden==True ):
            self.__m_Body.hide()
        else:
            self.__m_Body.show()


    # Slot. switches body expand/collapse mode.
    def __HeaderClickedSlot( self ):
        self.__m_Hidden = not self.__m_Hidden
        self.__m_Header.setPixmap( self.__m_Hidden )
        if( self.__m_Hidden==True ):
            self.__m_Body.hide()
        else:
            self.__m_Body.show()
        

    def AddWidget( self, widget ):
        self.__m_Body.AddWidget( widget )


    def RemoveWidget( self, widget ):
        self.__m_Body.RemoveWidget( widget )



class ScrollAreaWidget(QScrollArea):

    def __init__( self, *args, **kwargs ):
        super(ScrollAreaWidget, self).__init__(*args, **kwargs)

        self.setStyleSheet( UIStyle.g_ScrollBarStyleSheet )

        self.setWidgetResizable( True )
        self.setVerticalScrollBarPolicy( Qt.ScrollBarAsNeeded )
        self.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )

        self.__m_InnerLayout = QVBoxLayout()
        self.__m_InnerLayout.setContentsMargins( g_AttribMarginLeft, g_AttribMarginTop, g_AttribMarginRight, g_AttribMarginBottom )
        self.__m_InnerLayout.setSpacing(0)
        self.__m_InnerLayout.addStretch()
        
        self.__m_InnerWidget = QFrame()
        self.__m_InnerWidget.setStyleSheet( UIStyle.g_ScrollAreaWidgetStyleSheet)
        self.__m_InnerWidget.setLayout( self.__m_InnerLayout )
        self.setWidget( self.__m_InnerWidget )


    def AddWidget( self, widget ):
        try:
            self.__m_InnerLayout.insertWidget( self.__m_InnerLayout.count()-1, widget )
        except:
            traceback.print_exc()


    def RemoveWidget( self, widget ):
        try:
            self.__m_InnerLayout.removeWidget( widget )
        except:
            traceback.print_exc()




class AttributeEditorWidget(QFrame):

    def __init__( self ):
        super(AttributeEditorWidget, self).__init__()
        
        self.__m_refObjectID = None
        self.__m_AttributeEditWidget = None
        self.__m_WidgetDict = {} # widget dictionary

        self.setLayout( QVBoxLayout() )
        self.layout().setContentsMargins( 3, 3, 3, 3 )
        self.setMinimumWidth(350)
        self.setStyleSheet( UIStyle.g_StaticFrameStyleSheet )

        self.__m_bTriggered = False # True if this instance triggered NodeGraph update.

        self.__m_refCallbackFunc = None

        # expand/collapse states
        self.__m_bWidgetExpanded = { 'Input': True, 'Output': True, 'GroupInput': True, 'GroupOutput': True }



    def InitializeWidget( self, obj_id, nodeDesc, name ):

        self.__m_refObjectID = obj_id

        # Create widget
        if( nodeDesc.ObjectType()=='GroupIO' ):
            self.__CreateWidget_GroupIO( nodeDesc, self.__m_refCallbackFunc )
        else:
            self.__CreateWidget( nodeDesc, name, self.__m_refCallbackFunc )

            

    def DeinitializeWidget( self ):
        
        if( self.layout() is not None ):

            while( self.layout().count() ):

                item = self.layout().takeAt(0)
                widget = item.widget()

                if( widget is not None ):
                    widget.deleteLater()
                else:
                    del item

        self.__m_refObjectID = None

        self.__m_WidgetDict.clear()



    def BindCallbackFunc( self, callbackfunc ):
        self.__m_refCallbackFunc = callbackfunc



    def UnbindCallbackFunc( self ):
        self.__m_refCallbackFunc = None



    def ActiveObjectID( self ):
        return self.__m_refObjectID



    def Rename_Exec( self, node_id, name ):
        print( 'AttributeEditorWidget::Rename_Exec()...' )
        if( node_id in self.__m_WidgetDict ):
            self.__m_WidgetDict[ node_id ].SetValue( name )



    def RenameAttribute_Exec( self, attrib_id, name ):
        print( 'AttributeEditorWidget::RenameAttribute_Exec()...' )
        if( attrib_id in self.__m_WidgetDict ):
            self.__m_WidgetDict[ attrib_id ].SetLabel( name )



    def SetValue_Exec( self, attrib_id, value ):
        print( 'AttributeEditorWidget::SetValue_Exec()...' )
        if( attrib_id in self.__m_WidgetDict ):
            self.__m_WidgetDict[ attrib_id ].SetValue( value )



    def SetEnabled_Exec( self, attrib_id, state ):
        print( 'AttributeEditorWidget::SetEnabled_Exec()...' )
        if( attrib_id in self.__m_WidgetDict ):
            self.__m_WidgetDict[ attrib_id ].setEnabled( state )



    def HasTrigerred( self ):
        return self.__m_bTriggered



    def __CallbackFunc( self, *args, **kwargs ):
        self.__m_bTriggered = True
        self.__m_refCallbackFunc( *args, **kwargs )
        self.__m_bTriggered = False



    def __SwitchExpand( self, key ):
        #print( 'AttributeEditorWidget::Switching Attribute Editor Expand/Collapse:', key )
        self.__m_bWidgetExpanded[key] = not self.__m_bWidgetExpanded[key]



    def __CreateWidget( self, nodeDesc, name, callbackfunc ):

        #====================== Initialize Node Title =======================#
        nodeInfoWidget = NodeInfo_Widget( self.__m_refObjectID, nodeDesc.ObjectType(), self, functools.partial( self.__CallbackFunc, 'RenameByID' ) )
        nodeInfoWidget.SetValue( name )
        self.__m_WidgetDict[ self.__m_refObjectID ] = nodeInfoWidget
        self.layout().addWidget( nodeInfoWidget )

        # Insert horizontal line between node title and input attribute fields
        self.layout().addWidget( HorizontalLine() )


        #=================== Initialize Attribute Edit Widget ================#
        self.__m_AttributeEditWidget = ScrollAreaWidget()
        self.layout().addWidget( self.__m_AttributeEditWidget )
        
        # Create input attribute UI components
        collapsibleWidget_In = ExpandWidget( 'Input Attributes' )
        collapsibleWidget_In._ExpandWidget__m_Header.headerClicked.connect( functools.partial( self.__SwitchExpand, key='Input' ) )
        if( not 'Input' in self.__m_bWidgetExpanded ):  self.__m_bWidgetExpanded[ 'Input' ] = True
        hasAttrib = False

        for desc in nodeDesc.InputAttribDescs():

            if( desc.IsEditable()==False ):
                continue
            
            # Create AttributeWidget and assign as collapsible widget's child
            newWidget = self.__CreateAttributeWidget( desc, self.__CallbackFunc )

            # Assign Widget
            if( newWidget ):
                self.__m_WidgetDict[ newWidget.ID() ] = newWidget
                collapsibleWidget_In.AddWidget( newWidget )
                hasAttrib = True
            
        if( hasAttrib ):
            self.__m_AttributeEditWidget.AddWidget( collapsibleWidget_In )
            collapsibleWidget_In.SetExpand( self.__m_bWidgetExpanded['Input'] )
        else:
            del collapsibleWidget_In

        # Create output attribute UI components
        collapsibleWidget_Out = ExpandWidget( 'Output Attributes' )
        collapsibleWidget_Out._ExpandWidget__m_Header.headerClicked.connect( functools.partial( self.__SwitchExpand, key='Output' ) )
        if( not 'Output' in self.__m_bWidgetExpanded ):  self.__m_bWidgetExpanded[ 'Output' ] = True
        hasAttrib = False

        for desc in nodeDesc.OutputAttribDescs():
            
            if( desc.IsEditable()==False ):
                continue
            
            # Create AttributeWidget and assign as collapsible widget's child
            newWidget = self.__CreateAttributeWidget( desc, self.__CallbackFunc )

            # Assign Widget
            if( newWidget ):
                self.__m_WidgetDict[ newWidget.ID() ] = newWidget
                collapsibleWidget_Out.AddWidget( newWidget )
                hasAttrib = True

        if( hasAttrib ):
            self.__m_AttributeEditWidget.AddWidget( collapsibleWidget_Out )
            collapsibleWidget_Out.SetExpand( self.__m_bWidgetExpanded['Output'] )
        else:
            del collapsibleWidget_Out



    def __CreateAttributeWidget( self, desc, callbackfunc, *, name=None ):

        label = desc.Name() if name==None else name

        if( desc.DataType() is float ):
            return AttributeEditor_ScalarDouble( desc.ObjectID(), label, -1000.0, 1000.0, 2, 0.01, self, functools.partial( self.__CallbackFunc, 'SetAttributeByID' ) )

        elif( desc.DataType() is int ):
            return AttributeEditor_ScalarInt( desc.ObjectID(), label, -100, 100, 1, 10, self, functools.partial( self.__CallbackFunc, 'SetAttributeByID' ) )

        elif( desc.DataType() is str ):
            return AttributeEditor_String( desc.ObjectID(), label, self, functools.partial( self.__CallbackFunc, 'SetAttributeByID' ) )

        elif( desc.DataType() is bool ):
            return AttributeEditor_CheckBox( desc.ObjectID(), label, self, functools.partial( self.__CallbackFunc, 'SetAttributeByID' ) )

        else:
            return None



    def __CreateWidget_GroupIO( self, nodeDesc, callbackfunc ):

        #=================== Initialize Attribute Edit Widget ================#
        self.__m_AttributeEditWidget = ScrollAreaWidget()
        self.layout().addWidget( self.__m_AttributeEditWidget )
        
        # Create input attribute UI components
        if( len(nodeDesc.InputAttribDescs()) > 0 ):

            collapsibleWidget_In = ExpandWidget( 'Group Inputs' )
            collapsibleWidget_In._ExpandWidget__m_Header.headerClicked.connect( functools.partial( self.__SwitchExpand, key='GroupInput' ) )
            if( not 'GroupInput' in self.__m_bWidgetExpanded ):  self.__m_bWidgetExpanded[ 'GroupInput' ] = True
            hasAttrib = True

            for desc in nodeDesc.InputAttribDescs():
                # Create AttributeNameWidget and assign as collapsible widget's child 
                nameWidget = NodeInfo_Widget( desc.ObjectID()[0], 'Attribute Name', self, functools.partial( self.__CallbackFunc, 'RenameByID' ) )
                nameWidget.SetValue( desc.Name() )
                self.__m_WidgetDict[ nameWidget.ID() ] = nameWidget
                collapsibleWidget_In.AddWidget( nameWidget)

                # Create AttributeWidget and assign as collapsible widget's child
                if( desc.IsEditable()==True ):
                    attribWidget = self.__CreateAttributeWidget( desc, self.__CallbackFunc, name='Value' )
                    if( attribWidget ):
                        self.__m_WidgetDict[ attribWidget.ID() ] = attribWidget
                        collapsibleWidget_In.AddWidget( attribWidget )

                # Add Horizontal Line
                collapsibleWidget_In.AddWidget( HorizontalLine() )
            
            self.__m_AttributeEditWidget.AddWidget( collapsibleWidget_In )
            collapsibleWidget_In.SetExpand( self.__m_bWidgetExpanded['GroupInput'] )


        # Create output attribute UI components
        if( len(nodeDesc.OutputAttribDescs()) > 0 ):
        
            collapsibleWidget_Out = ExpandWidget( 'Group Outputs' )
            collapsibleWidget_Out._ExpandWidget__m_Header.headerClicked.connect( functools.partial( self.__SwitchExpand, key='GroupOutput' ) )
            if( not 'GroupOutput' in self.__m_bWidgetExpanded ):  self.__m_bWidgetExpanded[ 'GroupOutput' ] = True

            for desc in nodeDesc.OutputAttribDescs():
                # Create AttributeNameWidget and assign as collapsible widget's child 
                nameWidget = NodeInfo_Widget( desc.ObjectID()[0], 'Attribute Name', self, functools.partial( self.__CallbackFunc, 'RenameByID' ) )
                nameWidget.SetValue( desc.Name() )
                self.__m_WidgetDict[ nameWidget.ID() ] = nameWidget
                collapsibleWidget_Out.AddWidget( nameWidget)

                # Create AttributeWidget and assign as collapsible widget's child
                if( desc.IsEditable()==True ):
                    attribWidget = self.__CreateAttributeWidget( desc, self.__CallbackFunc, name='Value' )
                    if( attribWidget ):
                        self.__m_WidgetDict[ attribWidget.ID() ] = attribWidget
                        collapsibleWidget_Out.AddWidget( attribWidget )

                # Add Horizontal Line
                collapsibleWidget_Out.AddWidget( HorizontalLine() )
        
            self.__m_AttributeEditWidget.AddWidget( collapsibleWidget_Out )
            collapsibleWidget_Out.SetExpand( self.__m_bWidgetExpanded['GroupOutput'] )



    def mousePressEvent( self, event ):
        # なにもない場所でマウスクリックした際に、UIからフォーカスを外す
        focuswidget = self.focusWidget()
        if( focuswidget ):
            if( isinstance(focuswidget, QLineEdit) ):
                focuswidget.editingFinished.emit()# 編集途中の文字列をQLineEditに保持させる
            focuswidget.clearFocus()

        return super(AttributeEditorWidget, self).mousePressEvent(event)