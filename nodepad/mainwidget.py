import sys
import functools
# TODO: Redirect stdout to QTextEdit.

from oreorelib.ui.pyqt5.mainwindow import MainWindow

from .ui.graphicssettings import *
from .ui.graphicsview import GraphicsView
from .ui.attributeeditorwidget import AttributeEditorWidget
from .ui.pythoninterpreter import PyInterp


#from .nescene import NEScene
from .nescene_ext import NESceneExt
from .nescene_manager import NESceneManager




class MainWidget(MainWindow):

    def __init__( self ):
        super(MainWidget, self).__init__()        
 
        #========== Initialize NEScene ===========#
        self.__m_NEScene = NESceneExt()#NEScene()

        #========== Initialize GraphicsViews ===========#
        self.__m_Views = {}

        # Setup default view
        rootView = GraphicsView( self.__m_NEScene.GetRootID(), g_GridStep ) 
        rootView.setScene( self.__m_NEScene.GraphicsScene() )
        rootView.FocusViewIdChanged.connect( self.__m_NEScene.GraphicsScene().SetFocusViewID )
        rootView.RenderViewIdChanged.connect( self.__m_NEScene.GraphicsScene().SetRenderViewID )

        self.__m_Views[ self.__m_NEScene.GetRootID() ] = rootView


        #============ Initialize Attribute Editor ============#
        qtab = QTabWidget()
        qtab.setLayout( QVBoxLayout() )
        qtab.setStyleSheet( UIStyle.g_TabWidgetStyleSheet )
        qtab.addTab( self.__m_NEScene.AttributeEditor(), 'Attribute Editor' )
        #qtab.addTab(QLabel('Label 2'), 'Tab2')
        
        attrEditFrame = QFrame()
        attrEditFrame.setFocusPolicy( Qt.StrongFocus )
        attrEditFrame.setStyleSheet( UIStyle.g_StaticFrameStyleSheet )
        attrEditFrame.setLayout( QVBoxLayout() )
        attrEditFrame.layout().setContentsMargins(0,0,0,0)
        attrEditFrame.layout().addWidget( qtab )

        #=============== Initialize Python Interpreter =============#
        self.__m_PythonConsole = PyInterp( locals(), self )
        self.__m_PythonConsole.setAcceptDrops(True)


        #============ Initialize SceneManager ===============#
        self.__m_SceneManager = NESceneManager()
        self.__m_SceneManager.BindNEScene( self.__m_NEScene, self.__m_Views, self.UpdateWindowTitle, self.CreateNodeEditView )

        vsplitter = QSplitter(Qt.Vertical)
        vsplitter.setContentsMargins(0, 0, 0, 0)
        vsplitter.addWidget( rootView )
        vsplitter.addWidget(self.__m_PythonConsole)

        hsplitter = QSplitter(Qt.Horizontal)
        hsplitter.setContentsMargins(0, 0, 0, 0)
        hsplitter.addWidget(vsplitter)
        hsplitter.addWidget( attrEditFrame )
        hsplitter.setStyleSheet(UIStyle.g_SplitterStyleSheet)
        #hsplitter.setSizes( [100, 100] )

        #Pal = QPalette()
        #Pal.setColor( QPalette.Background, QColor(80,80,80) )
        hsplitter.setAutoFillBackground(True)
        hsplitter.setStyleSheet(UIStyle.g_SplitterStyleSheet)
        #hsplitter.setPalette(Pal)
        
        #
        self.setCentralWidget(hsplitter)
        self.setGeometry( 300, 50, 1280, 768 )
        self.centralWidget().setContentsMargins(6,0,6,6)


        #=============== Initialize Actions ==============#
        self.__m_NewAction = QAction( '&New', self )
        self.__m_NewAction.setShortcut( 'Ctrl+N' )
        self.__m_NewAction.setStatusTip( 'Create new project' )
        self.__m_NewAction.triggered.connect( self.New )

        self.__m_OpenAction = QAction( '&Open', self )
        self.__m_OpenAction.setShortcut( 'Ctrl+O' )
        self.__m_OpenAction.setStatusTip( 'Open project' )
        self.__m_OpenAction.triggered.connect( self.Open )

        self.__m_SaveAction = QAction( '&Save', self )
        self.__m_SaveAction.setShortcut( 'Ctrl+S' )
        self.__m_SaveAction.setStatusTip( 'Save project' )
        self.__m_SaveAction.triggered.connect( self.Save )

        self.__m_SaveAsAction = QAction( '&Save As...', self )
        self.__m_SaveAsAction.setShortcut( 'Shift+Ctrl+S' )
        self.__m_SaveAsAction.setStatusTip( 'Save project as...' )
        self.__m_SaveAsAction.triggered.connect( self.SaveAs )

        self.__m_ImportAction = QAction( '&Import', self )
        self.__m_ImportAction.setStatusTip( 'Import' )
        self.__m_ImportAction.triggered.connect( self.Import )

        self.__m_ExportAction = QAction( '&Export', self )
        self.__m_ExportAction.setStatusTip( 'Export' )
        self.__m_ExportAction.triggered.connect( self.Export )

        self.__m_ExportSelectionAction = QAction( '&Export Selection', self )
        self.__m_ExportSelectionAction.setStatusTip( 'Exports selected objects...' )
        self.__m_ExportSelectionAction.triggered.connect( self.ExportSelection )

        self.__m_QuitAction = QAction( '&Quit', self )
        self.__m_QuitAction.setShortcut( 'Ctrl+Q' )
        self.__m_QuitAction.setStatusTip( 'Leave The App' )
        self.__m_QuitAction.triggered.connect( self.CloseApplication )     


        # Undo
        self.__m_UndoAction = QAction( '&Undo\tCtrl+Z', self )
        #self.__m_UndoAction.setShortcut( 'Ctrl+Z' )
        self.__m_UndoAction.setStatusTip( 'Undo' )
        self.__m_UndoAction.triggered.connect( self.__m_SceneManager.Undo )

        # Redo
        self.__m_RedoAction = QAction( '&Redo\tCtrl+Y', self )
        #self.__m_RedoAction.setShortcut( 'Ctrl+Y' )
        self.__m_RedoAction.setStatusTip( 'Redo' )
        self.__m_RedoAction.triggered.connect( self.__m_SceneManager.Redo )

        # Cut
        self.__m_CutAction = QAction( '&Cut\tCtrl+X', self )
        #self.__m_CutAction.setShortcut( 'Ctrl+X' )
        self.__m_CutAction.setStatusTip( 'Cut selected objects' )
        self.__m_CutAction.triggered.connect( self.__m_SceneManager.Cut )

        # Copy
        self.__m_CopyAction = QAction( '&Copy\tCtrl+C', self )
        #self.__m_CopyAction.setShortcut( 'Ctrl+C' )
        self.__m_CopyAction.setStatusTip( 'Copy selected objects' )
        self.__m_CopyAction.triggered.connect( self.__m_SceneManager.Copy )

        # Paste
        self.__m_PasteAction = QAction( '&Paste\tCtrl+V', self )
        #self.__m_PasteAction.setShortcut( 'Ctrl+V' )
        self.__m_PasteAction.setStatusTip( 'Paste objects' )
        self.__m_PasteAction.triggered.connect( self.__m_SceneManager.Paste )

        # Duplicate
        self.__m_DuplicateAction = QAction( '&Duplicate\tCtrl+D', self )
        #self.__m_DuplicateAction.setShortcut( 'Ctrl+D' )
        self.__m_DuplicateAction.setStatusTip( 'Duplicate selected objects' )
        self.__m_DuplicateAction.triggered.connect( self.__m_SceneManager.Duplicate )

        # Delete
        self.__m_DeleteAction = QAction( '&Delete\tDel', self )
        #self.__m_DeleteAction.setShortcut( 'Del' )
        self.__m_DeleteAction.setStatusTip( 'Delete selected objects' )
        self.__m_DeleteAction.triggered.connect( self.__m_SceneManager.Delete )

        # Group
        self.__m_GroupAction = QAction( '&Group\tCtrl+G', self )
        #self.__m_GroupAction.setShortcut( 'Ctrl+G' )
        self.__m_GroupAction.setStatusTip( 'Group selected objects' )
        self.__m_GroupAction.triggered.connect( self.__m_SceneManager.Group )

        # Ungroup
        self.__m_UngroupAction = QAction( '&Ungroup\tCtrl+U', self )
        #self.__m_UngroupAction.setShortcut( 'Ctrl+U' )
        self.__m_UngroupAction.setStatusTip( 'Ungroup selected objects' )
        self.__m_UngroupAction.triggered.connect( self.__m_SceneManager.Ungroup )

        # CheckGraph
        self.__m_CheckgraphAction = QAction( '&CheckGraph', self )
        self.__m_CheckgraphAction.setStatusTip( 'Check graph' )
        self.__m_CheckgraphAction.triggered.connect( self.__m_SceneManager.CheckGraph )


        # EvaluateSelectedNode.
        self.__m_EvaluateSelectedAction = QAction( '&Evaluate', self )
        self.__m_EvaluateSelectedAction.setStatusTip( 'Evaluate selected items' )
        self.__m_EvaluateSelectedAction.triggered.connect( self.__m_SceneManager.EvaluateSelected )



        #=============== Initialize Menubar ==================#
        # Main menu
        mainMenu = self.menuBar()
        #mainMenu.setFixedHeight(24)
        #mainMenu.setStyleSheet( UIStyle.g_MenuBarStyleSheet )

        # File menu
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.setStyleSheet( UIStyle.g_MenuStyleSheet )
        fileMenu.addAction(self.__m_NewAction)
        fileMenu.addAction(self.__m_OpenAction)
        fileMenu.addAction(self.__m_SaveAction)
        fileMenu.addAction(self.__m_SaveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.__m_ImportAction)
        fileMenu.addAction(self.__m_ExportAction)
        fileMenu.addAction(self.__m_ExportSelectionAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.__m_QuitAction)

        # Edit menu
        editMenu = mainMenu.addMenu('&Edit')
        editMenu.setStyleSheet( UIStyle.g_MenuStyleSheet )
        editMenu.addAction(self.__m_UndoAction)
        editMenu.addAction(self.__m_RedoAction)
        editMenu.addSeparator()
        editMenu.addAction(self.__m_CutAction)
        editMenu.addAction(self.__m_CopyAction)
        editMenu.addAction(self.__m_PasteAction)
        editMenu.addAction(self.__m_DuplicateAction)
        editMenu.addAction(self.__m_DeleteAction)
        editMenu.addSeparator()
        editMenu.addAction(self.__m_GroupAction)
        editMenu.addAction(self.__m_UngroupAction)

        # Build menu
        buildMenu = mainMenu.addMenu('&Build')
        buildMenu.setStyleSheet( UIStyle.g_MenuStyleSheet )
        buildMenu.addAction(self.__m_CheckgraphAction)
        buildMenu.addAction(self.__m_EvaluateSelectedAction )


        #============== Initialize StatusBar ===============#
        statusBar = QStatusBar()
        statusBar.setStyleSheet( UIStyle.g_StatusBarStyleSheet )
        self.setStatusBar( statusBar )


        #================= SetWindowTitle  =================#
        #self.setWindowTitle( 'NodePad' )
        self.UpdateWindowTitle()


    def Release( self ):
        self.__m_SceneManager.Release()
        self.__m_NEScene.Release()

        for view in self.__m_Views.values():
            view.Release()
        self.__m_Views.clear()



    def CloseChildViews( self ):
        root_id = self.__m_NEScene.GetRootID()
        view_ids = [ key for key in self.__m_Views.keys() if key!= root_id ]
        for view_id in view_ids:
            self.__m_Views[view_id].close()


    def SceneManager( self ):
        return self.__m_SceneManager



    def New( self ):

        if( self.__m_SceneManager.IsUpToDate()==False ):

            msgBox = QMessageBox()
            msgBox.setIcon( QMessageBox.Question )
            msgBox.setStyleSheet( UIStyle.g_MessageBoxStyleSheet + UIStyle.g_ButtonStyleSheet )
            msgBox.setText( 'The scene has been modified.\n Save changes?' )
            msgBox.setStandardButtons( QMessageBox.Question | QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel )
            msgBox.setDefaultButton( QMessageBox.Save )
        
            reply = msgBox.exec_()

            if( reply==QMessageBox.Save ):
                self.Save()

            elif( reply==QMessageBox.Cancel ):
                return
        
            #elif( reply==QMessageBox.Discard ):
            #    self.__m_SceneManager.Clear()

        self.CloseChildViews()
        self.__m_SceneManager.Clear()
        self.UpdateWindowTitle()



    def Open( self ):

        filepaths = []

        #========================== Display file open dialogue and get filepath =======================#
        dlg = QFileDialog()
        dlg.setAcceptMode( QFileDialog.AcceptOpen )
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setOption( QFileDialog.DontUseNativeDialog, True)
        dlg.setStyleSheet( UIStyle.g_DialogStyleSheet + UIStyle.g_ComboBoxStyleSheet + UIStyle.g_ListViewStyleSheet + UIStyle.g_TreeViewStyleSheet + UIStyle.g_LineEditStyleSheet + UIStyle.g_ButtonStyleSheet + UIStyle.g_ScrollBarStyleSheet )
        view = dlg.findChild(QTreeView)
        view.header().setStretchLastSection(False)
        view.header().setSectionResizeMode( view.header().count()-1, QHeaderView.Stretch )

        dlg.setNameFilters( [ 'Scenes (*.pkl)', 'All Files (*)' ] )
        
        if( dlg.exec_() ):
            filepaths = dlg.selectedFiles()
            dlg.deleteLater()

        if( not filepaths ):
            dlg.deleteLater()
            return

        #=================================== Deal with unsaved edit history ============================#
        if( self.__m_SceneManager.IsUpToDate()==False ):

            msgBox = QMessageBox()
            msgBox.setIcon( QMessageBox.Question )
            msgBox.setStyleSheet( UIStyle.g_MessageBoxStyleSheet + UIStyle.g_ButtonStyleSheet )
            msgBox.setText( 'The scene has been modified.\n Save changes?' )
            msgBox.setStandardButtons( QMessageBox.Question | QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel )
            msgBox.setDefaultButton( QMessageBox.Save )
        
            reply = msgBox.exec_()

            if( reply==QMessageBox.Save ):
                self.Save()

            elif( reply==QMessageBox.Cancel ):
                return

            #elif( reply==QMessageBox.Discard ):
            #    self.__m_SceneManager.Clear()

        #=================================== Initialize nodegraph data ============================#
        self.CloseChildViews()
        self.__m_SceneManager.Clear()
        self.__m_SceneManager.Open( filepaths[0] )            
        self.UpdateWindowTitle()



    def Save( self ):

        filepath = self.__m_SceneManager.GetFilePath()
        
        if( filepath=='Untitled' ):
            self.SaveAs()
        else:
            self.__m_SceneManager.Save( filepath )
            self.UpdateWindowTitle()

        #if( filepath ):
        #    self.__m_SceneManager.Save( filepath )
        #    self.UpdateWindowTitle()
        #else:
        #    self.SaveAs()



    def SaveAs( self ):

        filepath = []

        #========================== Display file save dialogue and get filepath =======================#
        dlg = QFileDialog()
        dlg.setLabelText( QFileDialog.Accept, 'Save As' )
        dlg.setAcceptMode( QFileDialog.AcceptSave )
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setOption( QFileDialog.DontUseNativeDialog, True)
        dlg.setStyleSheet( UIStyle.g_DialogStyleSheet + UIStyle.g_ComboBoxStyleSheet + UIStyle.g_ListViewStyleSheet + UIStyle.g_TreeViewStyleSheet + UIStyle.g_LineEditStyleSheet + UIStyle.g_ButtonStyleSheet + UIStyle.g_ScrollBarStyleSheet )
        view = dlg.findChild(QTreeView)
        view.header().setStretchLastSection(False)
        view.header().setSectionResizeMode( view.header().count()-1, QHeaderView.Stretch )

        dlg.setNameFilters( [ 'Scenes (*.pkl)', 'All Files (*)' ] )
        
        if( dlg.exec_() ):
            dlg.setDefaultSuffix( dlg.selectedNameFilter().replace(')','').rsplit('.',1)[-1] )
            filepath = dlg.selectedFiles()

        if( not filepath ):
            return

        #=================================== Save nodegraph data ============================#
        self.__m_SceneManager.Save( filepath[0] )
        self.UpdateWindowTitle()


    
    def Import( self ):

        filepaths = []

        #========================== Display file import dialogue and get filepath =======================#
        dlg = QFileDialog( caption='Import' )
        dlg.setLabelText( QFileDialog.Accept, 'Import' )
        dlg.setAcceptMode( QFileDialog.AcceptOpen )
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setOption( QFileDialog.DontUseNativeDialog, True)
        dlg.setStyleSheet( UIStyle.g_DialogStyleSheet + UIStyle.g_ComboBoxStyleSheet + UIStyle.g_ListViewStyleSheet + UIStyle.g_TreeViewStyleSheet + UIStyle.g_LineEditStyleSheet + UIStyle.g_ButtonStyleSheet + UIStyle.g_ScrollBarStyleSheet )
        view = dlg.findChild(QTreeView)
        view.header().setStretchLastSection(False)
        view.header().setSectionResizeMode( view.header().count()-1, QHeaderView.Stretch )

        dlg.setNameFilters( [ 'Scenes (*.pkl)', 'All Files (*)' ] )

        if( dlg.exec_() ):
            filepaths = dlg.selectedFiles()

        if( not filepaths ):
            return
        
        #=================================== Import nodegraph data ============================#
        self.__m_SceneManager.Import( filepaths[0] )            

    
    
    def Export( self ):

        filepath = []

        #========================== Display file export dialogue and get filepath =======================#
        dlg = QFileDialog( caption='Export' )
        dlg.setLabelText( QFileDialog.Accept, 'Export' )
        dlg.setAcceptMode( QFileDialog.AcceptSave )
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setOption( QFileDialog.DontUseNativeDialog, True)
        dlg.setStyleSheet( UIStyle.g_DialogStyleSheet + UIStyle.g_ComboBoxStyleSheet + UIStyle.g_ListViewStyleSheet + UIStyle.g_TreeViewStyleSheet + UIStyle.g_LineEditStyleSheet + UIStyle.g_ButtonStyleSheet + UIStyle.g_ScrollBarStyleSheet )
        view = dlg.findChild(QTreeView)
        view.header().setStretchLastSection(False)
        view.header().setSectionResizeMode( view.header().count()-1, QHeaderView.Stretch )

        dlg.setNameFilters( [ 'Scenes (*.pkl)', 'All Files (*)' ] )

        if( dlg.exec_() ):
            dlg.setDefaultSuffix( dlg.selectedNameFilter().replace(')','').rsplit('.',1)[-1] )
            filepath = dlg.selectedFiles()

        if( not filepath ):
            return

        #=================================== Export nodegraph data ============================#
        self.__m_SceneManager.Export( filepath[0] )

    
    def ExportSelection( self ):

        filepath = []

        #========================== Display file export dialogue and get filepath =======================#
        dlg = QFileDialog( caption='Export Selection' )
        dlg.setLabelText( QFileDialog.Accept, 'Export Selection' )
        dlg.setAcceptMode( QFileDialog.AcceptSave )
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setOption( QFileDialog.DontUseNativeDialog, True)
        dlg.setStyleSheet( UIStyle.g_DialogStyleSheet + UIStyle.g_ComboBoxStyleSheet + UIStyle.g_ListViewStyleSheet + UIStyle.g_TreeViewStyleSheet + UIStyle.g_LineEditStyleSheet + UIStyle.g_ButtonStyleSheet + UIStyle.g_ScrollBarStyleSheet )
        view = dlg.findChild(QTreeView)
        view.header().setStretchLastSection(False)
        view.header().setSectionResizeMode( view.header().count()-1, QHeaderView.Stretch )

        dlg.setNameFilters( [ 'Scenes (*.pkl)', 'All Files (*)' ] )

        if( dlg.exec_() ):
            dlg.setDefaultSuffix( dlg.selectedNameFilter().replace(')','').rsplit('.',1)[-1] )
            filepath = dlg.selectedFiles()

        if( not filepath ):
            return

        #=================================== Export nodegraph data ============================#
        self.__m_SceneManager.ExportSelection( filepath[0] )


    def CloseApplication( self ):

        if( self.__m_SceneManager.IsUpToDate()==False ):

            msgBox = QMessageBox()
            msgBox.setIcon( QMessageBox.Question )
            msgBox.setStyleSheet( UIStyle.g_MessageBoxStyleSheet + UIStyle.g_ButtonStyleSheet )
            msgBox.setText( 'The scene has been modified.\n Save changes?' )
            msgBox.setStandardButtons( QMessageBox.Question | QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel )
            msgBox.setDefaultButton( QMessageBox.Save )
        
            reply = msgBox.exec_()

            if( reply==QMessageBox.Save ):
                self.Save()
                self.Release()

            elif( reply==QMessageBox.Discard ):
                self.Release()

            elif( reply==QMessageBox.Cancel ):
                return

            sys.exit()

        else:
            sys.exit()


    # ウィンドウ閉じるボタン押した時のイベント
    def closeEvent( self, event ):
       
        if( self.__m_SceneManager.IsUpToDate()==False ):

            msgBox = QMessageBox()
            msgBox.setWindowTitle( 'NodePad' )
            msgBox.setIcon( QMessageBox.Question )
            msgBox.setStyleSheet( UIStyle.g_MessageBoxStyleSheet + UIStyle.g_ButtonStyleSheet )
            msgBox.setText( 'The scene has been modified.\n Do you really want to quit?' )
            msgBox.setStandardButtons( QMessageBox.Question | QMessageBox.Ok | QMessageBox.Cancel )
            msgBox.setDefaultButton( QMessageBox.Cancel )
        
            reply = msgBox.exec_()

            if( reply==QMessageBox.Ok ):
                self.Release()
                event.accept()
            else:
                event.ignore()

        else:
            self.Release()
            event.accept()


    def UpdateWindowTitle( self ):
        self.setWindowTitle( 'NodePad - ' + self.__m_SceneManager.GetFilePath() + g_DataChangedSymbol[ self.__m_SceneManager.IsModified() ] )


    def CreateNodeEditView( self, view_id, title ):

        print( 'MainWidget::CreateNodeEditView()...' )

        view = GraphicsView( view_id, g_GridStep )
        view.setScene( self.__m_NEScene.GraphicsScene() )

        view.setWindowTitle( title )
        view.FocusViewIdChanged.connect( self.__m_NEScene.GraphicsScene().SetFocusViewID )
        view.RenderViewIdChanged.connect( self.__m_NEScene.GraphicsScene().SetRenderViewID )
        view.WidgetClosed.connect( functools.partial(self.__RemoveEditorViewCallback, view_id ) )# 削除時のコールバック関数

        self.__m_Views[ view_id ] = view
        
        view.show()



    # GroupEditWindow削除時のコールバック関数
    def __RemoveEditorViewCallback( self, view_id ):
        try:
            self.__m_Views[ view_id ].Release()
            del self.__m_Views[ view_id ]
        except:
            traceback.print_exc()