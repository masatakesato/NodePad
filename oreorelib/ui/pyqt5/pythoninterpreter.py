from .stylesheet import *

import os
import re
import sys
import code
from rlcompleter import Completer

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



################################################################################################################################
#                                                                                                                              #
#                                                          Input Console                                                       #
#                                                                                                                              #
# -----------------------------------------------------------------------------------------------------------------------------#
#                                                           References                                                         #
#                                                                                                                              #
# http://stackoverflow.com/questions/12431555/enabling-code-completion-in-an-embedded-python-interpreter                       #
# http://stackoverflow.com/a/30861871/2052889                                                                                  #
# http://dumpz.org/523465/  print output in QTextEdit                                                                          #
# http://www.codeprogress.com/cpp/libraries/qt/showQtExample.php?key=QApplicationInstallEventFilter&index=188 eventfilter      #
#                                                                                                                              #
################################################################################################################################


class KeyEventFilter(QObject):

    def __init__( self, parent):
        super(KeyEventFilter, self).__init__(parent)


    def eventFilter( self, object, event ):
        
        if( event.type() == QEvent.KeyPress  ):

            if( (event.key()==Qt.Key_Z) and (event.modifiers() & Qt.ControlModifier) ): # ignore Ctrl+Z
                #sys.stdout.write( '^Z' )
                return True

            if( (event.key()==Qt.Key_Y) and (event.modifiers() & Qt.ControlModifier) ): # ignore Ctrl+Y
                #sys.stdout.write( '^Y' )
                return True

        return super(KeyEventFilter, self).eventFilter(object, event)




class InputConsole(QPlainTextEdit):

    class Interpreter(code.InteractiveConsole):

        def __init__(self, locals):
            code.InteractiveConsole.__init__(self, locals)

        def runIt(self, command):
            try:
                code.InteractiveConsole.runsource(self, command)
            except SystemExit: # invalidate exit command
                pass


    def __init__(self, locals=locals(), parent=None ):
        super(InputConsole,  self).__init__(parent)

        self.editablePos = -1

        #sys.stdout = self # temporary disabled
        #sys.stderr = self # temporary disabled
        #sys.stdin = self
        self.refreshMarker = False  # to change back to >>> from ...
        self.multiLine = False  # code spans more than one line
        self.command = ''    # command to be ran
        self.PrintBanner()              # print sys info
        self.Marker()                   # make the >>> or ... marker
        self.history = []    # list of commands entered
        self.historyIndex = -1
        self.interpreterLocals = {}

        self.installEventFilter( KeyEventFilter(self) ) 
        self.setFont( QFont('MS Gothic', 9) )
        self.setStyleSheet( g_TextFieldStyleSheet + g_ScrollBarStyleSheet )

        
        self.setAcceptDrops(False) # forbid mouse drop

        # initilize interpreter with self locals
        self.InitInterpreter(locals)

        self.completer = Completer( self.interpreter.locals )
        self.tab = False
        self.repeat = 0

        delimiters = ' |\(|\)|\[|\]|\{|\}|\,|\:|\;|\@|\=|\->|\+=|\-=|\*=|\/=|\//=|\%=|\@=|\&=|\|=|\^=|\>>=|\<<=|\*\*='# \.|  # ドットは除外する。メンバ変数アクセスのワイルドカードとして必要
        operators = '\+|\-|\*|\*\*|\/|\//|\%|\@|\<<|\>>|\&|\||\^|\~|\<|\>|\<=|\>=|\==|\!='
        self.__m_Splitters = delimiters + '|' + operators



    def PrintBanner( self ):
        self.Write( sys.version )
        self.Write( ' on ' + sys.platform + '\n' )
        #self.Write( 'PyQt ' + PYQT_VERSION_STR + '\n' )
        #msg = 'Type !hist for a history view and !hist(n) history index recall'
        #self.Write( msg + '\n' )



    def Marker(self):
        if( self.multiLine ):
            self.insertPlainText( '... ' )
            self.editablePos = len( self.document().toPlainText() )
        else:
            self.insertPlainText( '>>> ' )
            self.editablePos = len( self.document().toPlainText() )



    def InitInterpreter( self, interpreterLocals=None ):
        if( interpreterLocals ):
            # when we pass in locals, we don't want it to be named "self"
            # so we rename it with the name of the class that did the passing
            # and reinsert the locals back into the interpreter dictionary
            if( 'self' in interpreterLocals ):
                selfName = interpreterLocals['self'].__class__.__name__
                interpreterLocalVars = interpreterLocals.pop('self')
                self.interpreterLocals[selfName] = interpreterLocalVars
        else:
            self.interpreterLocals = interpreterLocals
        self.interpreter = self.Interpreter( self.interpreterLocals )



    def UpdateInterpreterLocals( self, newLocals ):
        className = newLocals.__class__.__name__
        self.interpreterLocals[className] = newLocals



    def Write( self, line ):
        self.insertPlainText(line)
        self.ensureCursorVisible()



    def ExecuteCommand( self, line ):

        result = False

        std_backup = sys.stdin
        sys.stdin = None

        # set cursor to end of line to avoid line splitting
        textCursor = self.textCursor()
        position = len(self.document().toPlainText())
        textCursor.setPosition(position)
        self.setTextCursor(textCursor)
        
        #line = str(self.document().lastBlock().text())[4:]  # remove marker
        line.rstrip()
        self.historyIndex = -1

        if( self.CustomCommands(line) ):
            result = True
        else:
            try:
                line[-1]
                if( line == '    ' ):
                    self.haveLine = False
                else:
                    self.haveLine = True
                if( line[-1] == ':' ):
                    self.multiLine = True
                self.history.insert(0, line)
            except:
                self.haveLine = False

            if( self.haveLine and self.multiLine ):  # multi line command
                self.command += line + '\n'  # + command and line
                self.appendPlainText('')#self.append('')  # move down one line
                self.Marker()  # handle marker style
                result = True

            elif( self.haveLine and not self.multiLine ):  # one line command
                self.command = line  # line is the command
                self.appendPlainText('')#self.append('')  # move down one line
                self.interpreter.runIt(self.command)
                self.command = ''  # clear command
                self.Marker()  # handle marker style
                result = True

            elif( self.multiLine and not self.haveLine ):  # multi line done
                self.appendPlainText('')#self.append('')  # move down one line
                self.interpreter.runIt(self.command)
                self.command = ''  # clear command
                self.multiLine = False  # back to single line
                self.Marker()  # handle marker style
                result = True

            elif( not self.haveLine and not self.multiLine ):  # just enter
                self.appendPlainText('')#self.append('')
                self.Marker()
                result = True

        sys.stdin = std_backup

        return result



    def ClearCurrentBlock( self ):

        # block being current row
        length = len(self.document().lastBlock().text()[4:])

        # move cursor to end
        position = len(self.document().toPlainText())
        textCursor = self.textCursor()
        textCursor.setPosition(position)
        self.setTextCursor(textCursor)

        if( length == 0 ):
            return None
        else:
            # should have a better way of doing this but I can't find it
            #[self.textCursor().deletePreviousChar() for x in range(length)]
            
            for x in range(0, position-self.editablePos):
                self.textCursor().deletePreviousChar()

        return True



    def RecallHistory( self ):
        # used when using the arrow keys to scroll through history
        self.ClearCurrentBlock()
        if( self.historyIndex > -1 ):
            self.insertPlainText(self.history[self.historyIndex])
        return True



    def CustomCommands( self, command ):

        if( command == '!hist' ):  # display history
            self.appendPlainText('')#self.append('')  # move down one line
            # vars that are in the command are prefixed with ____CC and deleted
            # once the command is done so they don't show up in dir()
            backup = self.interpreterLocals.copy()
            history = self.history[:]
            history.reverse()
            for i, x in enumerate(history):
                iSize = len(str(i))
                delta = len(str(len(history))) - iSize
                line = line = ' ' * delta + '%i: %s' % (i, x) + '\n'
                sys.stdout.write( line )#self.Write( line )

                tex = self.textCursor().block().text()
                pass

            self.UpdateInterpreterLocals(backup)
            self.Marker()
            return True

        if( re.match('!hist\(\d+\)', command) ):  # recall command from history
            backup = self.interpreterLocals.copy()
            history = self.history[:]
            history.reverse()
            index = int(command[6:-1])
            self.ClearCurrentBlock()

            if( index < 0 or len(history) <= index ):
                sys.stdout.write( 'history index %d is out of range.\n' % index )
                return True

            command = history[ index ]

            if( command[-1] == ':' ):
                self.multiLine = True
            self.Write( command )
            self.UpdateInterpreterLocals( backup )
            return True

        return False



    def mousePressEvent( self,  event ):        
        super(InputConsole, self).mousePressEvent( event )

        if( self.editablePos <= self.textCursor().position() ):
            self.setReadOnly( False )
        else:
            self.setReadOnly( True )



    def mouseReleaseEvent( self,  event ):        
        super(InputConsole, self).mouseReleaseEvent( event )

        if( self.editablePos <= self.textCursor().selectionStart() ):
            self.setReadOnly( False )
        else:
            self.setReadOnly( True )




    def keyPressEvent(self, event):

        if( event.key() == Qt.Key_Tab ):            
            if( self.tab == False ):
                line_text = str(self.document().lastBlock().text())[4:]
                string_lsit = line_text.split()
                string_lsit = re.split( self.__m_Splitters, line_text )
                self.wildcard = string_lsit[-1] if string_lsit else ''
                self.tab = True
                self.prefix = line_text[:-len(self.wildcard)]

            try: 
                suggestion = self.completer.complete( self.wildcard, 0 )

                if( suggestion != '\t' and self.wildcard != '' and self.completer.matches ): #suggestion != '\t' and self.completer.matches ):
                    self.ClearCurrentBlock()
                    self.insertPlainText( self.prefix + self.completer.matches[self.repeat] )
                    #self.insertPlainText( self.completer.matches[self.repeat] )
                    self.repeat = ( self.repeat + 1 ) % len(self.completer.matches)
            except:
                self.tab = False
                self.repeat = 0

            return None

        elif( event.key() == Qt.Key_Down ):
            if( self.historyIndex == len(self.history) ):
                self.historyIndex -= 1
            try:
                if self.historyIndex > -1:
                    self.historyIndex -= 1
                    self.RecallHistory()
                else:
                    self.ClearCurrentBlock()
            except:
                pass

            return None

        elif( event.key() == Qt.Key_Up ):
            try:
                if( len(self.history) - 1 > self.historyIndex ):
                    self.historyIndex += 1
                    self.RecallHistory()
                else:
                    self.historyIndex = len(self.history)
            except:
                pass

            return None

        elif( event.key() == Qt.Key_Home ):
            # set cursor to first editable position.
            textCursor = self.textCursor()
            textCursor.setPosition( self.editablePos )
            self.setTextCursor( textCursor )

            return None

        elif( event.key() in [Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Left] ):

            # don't allow deletion of non-editable textfield
            textCursor = self.textCursor()
            start_pos = textCursor.selectionStart()
            end_pos = textCursor.selectionEnd()

            if( end_pos - start_pos > 0 ):
                if( start_pos <= self.editablePos and end_pos <= self.editablePos ):
                    #print( '1. start_pos < end_pos < editable_pos' )
                    self.setReadOnly(False)
                    textCursor.setPosition( self.editablePos, QTextCursor.MoveAnchor )
                    self.setTextCursor(textCursor)
                    return None

                elif( start_pos < self.editablePos and self.editablePos < end_pos ):
                    #print( '2. start_pos < editable_pos <= end_pos!!' )
                    self.setReadOnly(False)
                    textCursor.setPosition( self.editablePos )
                    textCursor.setPosition( end_pos, QTextCursor.KeepAnchor )
                    self.setTextCursor(textCursor)

                #elif( self.editablePos < start_pos and self.editablePos < end_pos ):
                #    #print( '3. editable_pos <= start_pos < end_pos' )
            
            # don't allow deletion of marker
            elif( (self.textCursor().position() <= self.editablePos) and (event.key() !=Qt.Key_Delete) ):
                return None

        elif( event.key() in [Qt.Key_Return, Qt.Key_Enter] ):

            line = str(self.document().lastBlock().text())[4:]  # remove marker
            if( self.ExecuteCommand( line ) == True ):
                return None


        self.tab = False
        self.repeat = 0

        # allow all other key events
        super(InputConsole, self).keyPressEvent(event)



    def insertFromMimeData( self, source ):
        
        lines = source.text().split('\n')
        if( len(lines)<=1 ):
            return super(InputConsole, self).insertFromMimeData(source)

        # execute commands( except last one)
        for i in range(0, len(lines)-1):
            self.Write( lines[i] )
            self.ExecuteCommand( lines[i] )

        # just put text(last command)
        self.Write( lines[ len(lines)-1 ] )






################################################################################################################################
#                                                                                                                              #
#                                                         Output Console                                                       #
#                                                                                                                              #
# -----------------------------------------------------------------------------------------------------------------------------#
#                                                           References                                                         #
#                                                https://4uwingnet.tistory.com/9                                               #
#                                                                                                                              #
################################################################################################################################



class StdoutRedirect(QObject):

    printSignal = pyqtSignal( str, bool )
 

    def __init__( self, *args ):
        QObject.__init__(self, None)
        self.daemon = True
        self.sysstdout = sys.stdout.write
        self.sysstderr = sys.stderr.write



    def Start(self):
        sys.stdout.write = lambda msg: self.__Write( msg, False )
        sys.stderr.write = lambda msg: self.__Write( msg, True )


 
    def Stop(self):
        sys.stdout.write = self.sysstdout
        sys.stderr.write = self.sysstderr


 
    def __Write( self, s, isError ):
        sys.stdout.flush()
        self.printSignal.emit( s, isError )




class OutputConsole(QTextEdit):

    COLOR = { False: QColor(255, 127, 39), True: QColor(255, 0, 0) }# hard-coded text color from g_TextFieldStyleSheet.


    def __init__(self, parent=None):
        super(OutputConsole, self).__init__(parent=parent)
        
        self.setFont( QFont('MS Gothic', 9) )
        self.setStyleSheet( g_TextFieldStyleSheet + g_ScrollBarStyleSheet )

        # member variable     
        self._stdout = StdoutRedirect()
        self._stdout.Start()
        self._stdout.printSignal.connect( self.__AppendText )
 
        self.setReadOnly( True )



    def Lock( self ):
        self._stdout.Stop()



    def Unlock( self ):
        self._stdout.Start()



    def closeEvent( self, event ):
        self._stdout.Stop()
        return super(OutputConsole, self).closeEvent(event)



    def __AppendText( self, msg, isError ):
        self.moveCursor( QTextCursor.End )
        self.setTextColor( OutputConsole.COLOR[isError] )
        self.insertPlainText(msg)
        # refresh textedit show, refer) https://doc.qt.io/qt-5/qeventloop.html#ProcessEventsFlag-enum
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)


        