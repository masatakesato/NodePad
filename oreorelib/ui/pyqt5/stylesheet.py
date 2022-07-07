# reference http://www.yasinuludag.com/darkorange.stylesheet



g_MainWindowStyleSheet = """
QFrame
{
    background-color: rgb(24,24,24);
    
    margin: 5px 5px 5px 5px;
    border: 1px solid rgb(42,42,42);
    padding: 0px 0px 0px 0px;
}

QFrame:active
{
    background-color: rgb(32,32,32);
    border-color: rgb(125,50,0);/*rgb(60,60,60);*/
}

"""



g_TitleBarStyleSheet = """
QFrame
{
    color: rgb(235,235,235);
    background-color: rgb(42,42,42);
            
    font:12px bold;
    font-weight:bold;

    min-height: 30px;
    max-height: 30px;

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}

QLabel
{
    color: rgb(235,235,235);
    background-color: none;
    
    min-height: 18px;
    max-height: 18px;

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 6px 0px 6px;/* top, right, bottom, left */
}

"""



g_TitleButtonStyleSheet = """
QFrame
{
    background-color: none;

    min-width: 16px;
    max-width: 16px;
    min-height: 16px;
    max-height: 16px;

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}

QFrame:hover
{
    background-color: rgb(60,60,60);
}

QFrame[ pressed=true ]
{
    background-color: rgb(24,24,24);
}

QFrame[ icon = close ]
{
    padding: 6px 8px 6px 8px;
    image: url(:/resources/images/close.png);
}

QFrame[ icon = maximize ]
{
    padding: 6px 8px 6px 8px;
    image: url(:/resources/images/maximize.png);
}

QFrame[ icon = minimize ]
{
    padding: 6px 8px 6px 8px;
    image: url(:/resources/images/minimize.png);
}

QFrame[ icon = restore ]
{
    padding: 6px 8px 6px 8px;
    image: url(:/resources/images/restore.png) 0;
}

"""



g_MenuBarStyleSheet = """
QMenuBar
{
    color: rgb(235,235,235);
    background-color: rgb(42,42,42);
    spacing: 0px; /* spacing between menu bar items */

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}

QMenuBar::item
{
    background-color: transparent;
    
    min-height: 24px;
    max-height: 24px;

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 4px 14px 4px 14px; /* top, right, bottom, left */
}

QMenuBar::item:selected
{
    background-color: rgb(60,60,60);
}

"""



g_MenuStyleSheet = """
QMenu
{
    color: rgb(235,235,235);
    background-color: rgb(42,42,42);

    margin: 0px 0px 0px 0px;

    border: 1px solid rgb(60,60,60);
}

QMenu::item
{
    padding: 4px 8px;
}

QMenu::item:selected
{
    background-color: rgb(60,60,60);

    border: 0px none;
}

QMenu::separator
{
    background-color: rgb(60,60,60);

    height: 1px;

    margin: 2px 4px 2px 4px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}

"""



g_ResizeHandleStyleSheet = """
QFrame
{
    background-color: transparent;
           
    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}

"""



g_StatusBarStyleSheet = """
QStatusBar
{
    color: rgb(235,235,235);
    background-color: rgb(191,77,0);

    min-height: 22;
    max-height: 22;

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}

QSizeGrip
{
    background-color: none;

    margin: 1px 1px 1px 1px;
    border: 0px none;
    image: url(:/resources/images/sizegrip.png);
}

"""



g_ButtonStyleSheet = """
QPushButton
{
    color: rgb(235,235,235);
    background-color: rgb(60,60,60);

    margin: 1px 1px 1px 1px;

    border-left: 1px solid rgb(96,96,96);
    border-top: 1px solid rgb(72,72,72);
    border-right: 1px solid rgb(42,42,42);
    border-bottom: 1px solid rgb(32,32,32);

    padding: 5px 16px 5px 16px;
}

QPushButton:disabled
{
    color: rgb(118,118,118);
    background-color: none;

    border-left: 1px solid rgb(36,36,36);
    border-top: 1px solid rgb(36,36,36);
    border-right: 1px solid rgb(30,30,30);
    border-bottom: 1px solid rgb(30,30,30);
}

QPushButton:hover
{
    background-color: rgb(80,80,80);
}

QPushButton:pressed
{
    background-color: rgb(32,32,32);

    border-left: 1px solid rgb(42,42,42);
    border-top: 1px solid rgb(32,32,32); 
    border-right: 1px solid rgb(96,96,96);
    border-bottom: 1px solid rgb(72,72,72);
}
"""



g_ScrollBarStyleSheet = """
QScrollBar::vertical
{
    background-color: rgb(48,48,48);
    width: 18px;

    margin: 18px 0px 18px 0px;
}

QScrollBar::handle:vertical
{
    background-color: rgb(72,72,72);
    min-height: 10px;

    border-left: 4px solid rgb(48,48,48);
    border-right: 4px solid rgb(48,48,48);
}

QScrollBar::handle:vertical:hover
{
    background-color: rgb(128,128,128);
}

QScrollBar::handle:vertical:pressed
{
    background-color: rgb(96,96,96);
}

QScrollBar::add-line:vertical
{
    background-color: rgb(48,48,48);
    width: 18px;
    height: 18px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover
{
    background-color: rgb(32,32,32);
}

QScrollBar::add-line:vertical:pressed
{
    background-color: rgb(18,18,18);
}

QScrollBar::sub-line:vertical
{
    background-color: rgb(48,48,48);
    width: 18px;
    height: 18px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover
{
    background-color: rgb(32,32,32);
}

QScrollBar::sub-line:vertical:pressed
{
    background-color: rgb(18,18,18);
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
    background-color: none;
}

QScrollBar::up-arrow:vertical
{
    width: 14px;
    height: 14px;
    image: url(:/resources/images/arrow-up.png);
}

QScrollBar::down-arrow:vertical
{
    width: 14px;
    height: 14px;
    image: url(:/resources/images/arrow-down.png);
}


QScrollBar::horizontal
{
    background-color: rgb(48,48,48);
    height: 18px;
    margin: 0px 18px 0px 18px;
}

QScrollBar::handle:horizontal
{
    background-color: rgb(72,72,72);
    min-height: 10px;
    border-top: 4px solid rgb(48,48,48);
    border-bottom: 4px solid rgb(48,48,48);
}

QScrollBar::handle:horizontal:hover
{
    background-color: rgb(128,128,128);
}

QScrollBar::handle:horizontal:pressed
{
    background-color: rgb(96,96,96);
}

QScrollBar::add-line:horizontal
{
    background-color: rgb(48,48,48);
    width: 18px;
    height: 18px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover
{
    background-color: rgb(32,32,32);
}

QScrollBar::add-line:horizontal:pressed
{
    background-color: rgb(18,18,18);
}

QScrollBar::sub-line:horizontal
{
    background-color: rgb(48,48,48);
    width: 18px;
    height: 18px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal:hover
{
    background-color: rgb(32,32,32);
}

QScrollBar::sub-line:horizontal:pressed
{
    background-color: rgb(18,18,18);
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
{
    background-color: none;
}

QScrollBar::left-arrow:horizontal
{
    width: 14px;
    height: 14px;
    image: url(:/resources/images/arrow-left.png);
}

QScrollBar::right-arrow:horizontal
{
    width: 14px;
    height: 14px;
    image: url(:/resources/images/arrow-right.png);
}
"""



g_DynamicFrameStyleSheet = """
QFrame
{
    color: rgb(255,127,39);
    background-color: rgb(42,42,42);

    margin: 0px 0px 0px 0px;
    border: 1px solid rgb(42,42,42);
    padding: 0px 0px 0px 0px;
}

QFrame:focus
{
    border: 1px solid rgb(96,96,96);
}

"""



g_StaticFrameStyleSheet = """
QFrame
{
    background-color: rgb(42,42,42);/*rgb(60,60,60);*/

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}

"""



g_TextFieldStyleSheet = """
QTextEdit, QPlainTextEdit
{
    color: rgb(255,127,39);
    background-color: rgb(24,24,24);
    selection-background-color: rgb(125,75,50);

    margin: 0px 0px 0px 0px;
    border: 1px solid rgb(60,60,60);
    padding: 0px 0px 0px 0px;
}

QTextEdit:focus, QPlainTextEdit:focus
{
    border: 1px solid rgb(96,96,96);
}

"""



# refactored. 2019.05.19
g_LabelStyleSheet = """
QLabel
{
    color: rgb(235,235,235);
    background-color: none;

    margin: 0px 0px 0px 0px;
    border: 0px none;/*0px solid rgb(0,0,0);*/
    padding: 1px 1px 1px 1px;
}

QLabel:disabled
{
    color: rgb(118,118,118);
    background-color: transparent;
}
"""



g_LineEditStyleSheet = """
QLineEdit
{
    color: rgb(235,235,235);
    background-color: rgb(24,24,24);/*rgb(42,42,42);*/
    selection-background-color: rgb(125,75,50);
    
    height: 18px;
    
    border-radius: 2px;
    border-left: 1px solid rgb(32,32,32);
    border-top: 1px solid rgb(32,32,32);
    border-right: 1px solid rgb(100,100,100);
    border-bottom: 1px solid rgb(100,100,100);

    padding: 0px 2px;
}

QLineEdit:disabled
{
    color: rgb(118,118,118);
    background-color: transparent;
}

QLineEdit:focus
{
    border: 1px solid darkgray;
}

QLineEdit:read-only
{
    color: rgb(100,100,100);
}

"""



g_SliderStyleSheet = """
QSlider
{
    background-color: none;
    margin: 0px 0px;
    border: 0px;
    padding: 0px;
}

QSlider::groove:horizontal
{
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(32,32,32), stop:1 rgb(100,100,100) );

    height: 6px;

    margin: 2px 3px;
    border-radius: 3px;
}

QSlider::handle:horizontal
{
    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgb(200,200,200), stop:1 rgb(32,32,32) );

    width: 16px;
    height: 18px;

    margin: -5px -3px;
    border-radius: 8px;
}

QSlider::handle:horizontal:disabled
{
    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgb(118,118,118), stop:1 rgb(32,32,32) );

    width: 16px;
    height: 18px;

    margin: -5px -3px;
    border-radius: 8px;
}

"""



g_SpinBoxStyleSheet = """
QSpinBox, QDoubleSpinBox
{
    color: rgb(235,235,235);
    background-color: rgb(24,24,24);
    selection-background-color: rgb(125,75,50);

    height: 18px;
    max-width: 64px;

    border-left: 1px solid rgb(32,32,32);
    border-top: 1px solid rgb(32,32,32);
    border-right: 1px solid rgb(100,100,100);
    border-bottom: 1px solid rgb(100,100,100);

    border-radius: 2px;
    padding: 0px 2px;
}

QSpinBox::up-button, QDoubleSpinBox:up-button
{
    background-color: rgb(42,42,42);
    image: url(:/resources/images/arrow-up.png);

    margin: 1px 0px 1px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}

QSpinBox::down-button, QDoubleSpinBox:down-button
{
    background-color: rgb(42,42,42);
    image: url(:/resources/images/arrow-down.png);

    margin: 1px 0px 1px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover, QDoubleSpinBox:up-button:hover, QDoubleSpinBox:down-button:hover
{
    background-color: rgb(128,128,128);
}

QSpinBox::up-button:pressed, QSpinBox::down-button:pressed, QDoubleSpinBox:up-button:pressed, QDoubleSpinBox:down-button:pressed
{
    background-color: rgb(32,32,32);
}






QSpinBox:disabled, QDoubleSpinBox:disabled
{
    color: rgb(118,118,118);
    background-color: transparent;
    selection-background-color: rgb(125,75,50);

    height: 18px;

    border-left: 1px solid rgb(32,32,32);
    border-top: 1px solid rgb(32,32,32);
    border-right: 1px solid rgb(100,100,100);
    border-bottom: 1px solid rgb(100,100,100);

    border-radius: 2px;
    padding: 0px 2px;
}

QSpinBox:focus, QDoubleSpinBox:focus
{
    border: 1px solid darkgray;
}

"""



g_CheckBoxStyleSheet = """

QCheckBox
{
    background-color: none;
}

QCheckBox:disabled
{
    /*color: #414141;
    background-color: rgb(42,42,42);*/
}

QCheckBox::indicator
{
    color: rgb(235,235,235);
    background-color: rgb(42,42,42);

    width: 12px;
    height: 12px;

    border-left: 1px solid rgb(32,32,32);
    border-top: 1px solid rgb(32,32,32);
    border-right: 1px solid rgb(100,100,100);
    border-bottom: 1px solid rgb(100,100,100);
}

QCheckBox::indicator:hover
{
    border: 1px solid darkgray;
}

QCheckBox::indicator:checked
{
    image: url(:/resources/images/checkbox.png);
}

QCheckBox::indicator:disabled
{
    border: 1px solid #444;
}

"""



g_TabWidgetStyleSheet = """ 

QFrame
{
    background-color: transparent;

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}

/*====================== TabWidget settings ==========================*/
QTabWidget
{
    background-color: rgb(42,42,42);
}

QTabWidget::pane
{
    /*background-color: transparent;*/ /* valid inside padding area */
    margin: 0px 0px 0px 0px;
    
    border-top: 2px solid rgb(72,72,72);
    border-right: 1px solid rgb(72,72,72);
    border-bottom: 1px solid rgb(72,72,72);
    border-left: 1px solid rgb(72,72,72);

    padding: 0px 0px 0px 0px;
}

QTabWidget::pane:focus
{
    border-top: 2px solid rgb(191,77,0);
}

QTabWidget::pane[ TabWidgetFocus = true ]
{
    border-top: 2px solid rgb(191,77,0);
}


/*======================== TabBar settings ==========================*/
QTabBar::tab
{
    color: rgb(235,235,235);
    background-color: rgb(42,42,42);

    min-height: 17px;
    max-height: 17px;

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 2px 24px 2px 12px; /*top, right, bottom, left*/
}

QTabBar::tab:hover
{
    background-color: rgb(60,60,60);
}

QTabBar::tab:selected
{
    background-color: rgb(72,72,72);
}

QTabBar::tab:selected:focus
{
    background-color: rgb(191,77,0);
}

QTabBar::tab:selected[ TabWidgetFocus = true ]
{
    background-color: rgb(191,77,0);
}


/*============== TabBar close button Settings ======================*/
QTabBar::close-button
{
    background-color: transparent;

    min-width: 16px;
    max-width: 16px;
    min-height: 16px;
    max-height: 16px;
    
    padding: 2px 2px 2px 2px;

    image: url(:/resources/images/close.png);
}

QTabBar::close-button:disabled
{
    image: url(:/resources/images/close-disabled.png);
}

/* Disabled. Unable to handle mousehover propergation to neighbor tab (after tab insertion). */
/*
QTabBar::close-button:hover
{
    background-color: rgb(96,96,96);
}
*/
QTabBar::close-button:pressed
{
    background-color: rgb(32,32,32);
}

QTabBar::close-button:selected:hover
{
    background-color: rgb(128,128,128);
}


QTabBar::close-button:selected:pressed
{
    background-color: rgb(48,48,48);
}

QTabBar::close-button:selected:hover:focus
{
    background-color: rgb(255,127,39);
}

QTabBar::close-button:selected:hover[ TabWidgetFocus = true ]
{
    background-color: rgb(255,127,39);
}

QTabBar::close-button:selected:pressed:focus
{
    background-color: rgb(125,50,0);
}

QTabBar::close-button:selected:pressed[ TabWidgetFocus = true ]
{
    background-color: rgb(125,50,0);
}


/*===================== Left/Right arrow icons Settings ======================*/
QTabBar QToolButton
{
    min-width: 16px;
    max-width: 16px;

    background-color: rgb(42,42,42);

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}


QTabBar QToolButton::left-arrow
{
    background-color: rgb(60,60,60);

    padding: 1px 1px 1px 1px;

    image: url(:/resources/images/arrow-left.png);
}

QTabBar QToolButton::left-arrow:hover
{
    background-color: rgb(72,72,72);
}

QTabBar QToolButton::left-arrow:pressed
{
    background-color: rgb(32,32,32);
}


QTabBar QToolButton::right-arrow
{
    background-color: rgb(60,60,60);

    padding: 1px 1px 1px 1px;

    image: url(:/resources/images/arrow-right.png);
}

QTabBar QToolButton::right-arrow:hover
{
    background-color: rgb(72,72,72);
}

QTabBar QToolButton::right-arrow:pressed
{
    background-color: rgb(32,32,32);
}

"""



g_SplitLineStyleSheet = """
QFrame
{
    /*border: 3px solid green;*/
    background-color: rgb(42,42,42);/*rgb(60,60,60);*/

    margin: -0.5px 0px 0.5px 0px;
    padding: 0px -8px 0px -8px;

    border-top: 1px solid rgb(32,32,32);
    border-right: 1px solid rgb(16,16,16);
    border-bottom: 1px solid rgb(80,80,80);
}
"""



g_ExpandWidgetHeaderStyleSheet = """
QLabel
{
    color: rgb(235,235,235);
    background-color: rgb(80,80,80);

    margin: 0px 0px 0px 0px;
    border: 1px solid rgb(80,80,80);
    padding: 0px 0px 0px 0px;

    border-radius: 2px;

    qproperty-alignment: AlignCenter;
}
"""



g_ExpandWidgetBodyStyleSheet = """
QFrame
{
    background-color: rgb(64,64,64);

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}
"""



g_ExpandWidgetStyleSheet = """
QFrame
{
    color: rgb(235,235,235);
    background-color: rgb(60,60,60);/*rgb(0,0,255);*/

    margin: 0px 0px 0px 0px;/*margin: -5px -8px -5px -8px;*/
    border: 0px none;
    padding: 0px 0px 0px 0px;
}
"""



g_ScrollAreaWidgetStyleSheet = """
QWidget
{
    background-color: rgb(60,60,60);/*rgb(255,0,255);*/

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}
"""



g_EditorStyleSheet = """
QGraphicsView
{
    background-color: rgb(24,24,24);
    selection-background-color: rgb(125,75,50);

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}
"""



g_TransparentEditorStyleSheet = """
QGraphicsView
{
    background-color: transparent;
    selection-background-color: rgb(125,75,50);

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}
"""



g_SplitterStyleSheet = """
QSplitter
{
    background-color: rgb(42,42,42);
    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}

QSplitter::handle
{
    background-color: rgb(42,42,42);
}

QSplitter::handle:horizontal
{
    width: 6px;
}

QSplitter::handle:vertical
{
    height: 6px;
}

"""



# TODO: File open dialogue uses this stylesheet. 
g_ListViewStyleSheet = """
QListView
{
    color: rgb(235,235,235);
    background-color: rgb(24,24,24);/*rgb(42,42,42);*/

    margin: 0px 0px 0px 0px;
    border: 1px solid rgb(60,60,60);
    padding: 0px 0px 0px 0px;
}

QListView::item
{
    color: rgb(235,235,235);
}

QListView::item:hover
{
    background-color: rgb(60,60,60);/*rgb(100,100,100);*/
}
/*
QListView::item:selected
{
    border: 1px solid #567dbc;
}
*/
QListView::item:selected:active
{
    background-color: rgb(255,127,39);
}

QListView::item:selected:!active
{
    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);*/
}

"""



# TODO: File open dialogue uses this stylesheet. 
g_TreeViewStyleSheet = """

/* http://stackoverflow.com/questions/26162387/qtableview-qtablewidget-grid-stylesheet-grid-line-width */
QHeaderView
{
    color: rgb(235,235,235);
    background-color: rgb(24,24,24);/*rgb(42,42,42);*/
    show-decoration-selected: 1;
}

QHeaderView::section
{
    color: rgb(235,235,235);
    background-color: rgb(42,42,42);/*rgb(80,80,80);*/
}

QTreeView
{
    background-color: rgb(24,24,24);/*rgb(42,42,42);*/

    margin: 0px 0px 0px 0px;
    border: 1px solid rgb(60,60,60);
    padding: 0px 0px 0px 0px;
}

QTreeView::item
{
    color: rgb(235,235,235);
}

QTreeView::item:hover
{
    background-color: rgb(60,60,60);/*rgb(100,100,100);*/
}

QTreeView::item:selected:active
{
    background-color: rgb(255,127,39);
}

QTreeView::item:selected:!active
{
    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);*/
}
"""



# TODO: File open dialogue uses this stylesheet. 
g_ComboBoxStyleSheet = """
QComboBox
{
    color: rgb(235,235,235);
    background-color: rgb(42,42,42);

    min-width: 6em;

    border: 1px solid rgb(80,80,80);
    border-radius: 3px;
    
    padding: 1px 18px 1px 3px;
}
/*
QComboBox:editable
{
    background-color: white;
}
*/
QComboBox:!editable, QComboBox::drop-down:editable
{
    background-color: rgb(42,42,42);
}

/* QComboBox gets the "on" state when the popup is open */
QComboBox:!editable:on, QComboBox::drop-down:editable:on
{
    background-color: rgb(255,127,39);
}

QComboBox:on /* shift the text when the popup opens */
{
    padding-top: 3px;
    padding-left: 4px;
}

QComboBox::drop-down
{
    border: 0px;
}

QComboBox::down-arrow
{
    width: 14px;
    height: 14px;
    image: url(:/resources/images/arrow-down.png);
}

QComboBox::down-arrow:on /* shift the arrow when popup is open */
{
    top: 1px;
    left: 1px;
}

QComboBox QAbstractItemView
{
    selection-background-color: rgb(60,60,60);
}

"""



# TODO: File open dialogue uses this stylesheet. 
g_DialogStyleSheet = """
QWidget
{
    color: rgb(235,235,235);
    background-color: rgb(42,42,42);
}

/* Left part: ListView*/

/* Right part: TreeView */

QDialog, QFileDialog
{
    color: rgb(100,100,100);
}

"""

# file open dialogue stylesheets
# g_DialogStyleSheet + g_ComboBoxStyleSheet + g_ListViewStyleSheet + g_TreeViewStyleSheet + g_LineEditStyleSheet + g_ButtonStyleSheet + g_ScrollBarStyleSheet



g_MessageBoxStyleSheet = """
QWidget
{
    color: rgb(235,235,235);
    background-color: rgb(42,42,42);
}
"""

#TODO: refactor. 2019.05.20
#g_MessageBoxStyleSheet = basewstyle + buttonstyle