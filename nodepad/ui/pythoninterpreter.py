# http://stackoverflow.com/questions/12431555/enabling-code-completion-in-an-embedded-python-interpreter
# http://stackoverflow.com/a/30861871/2052889
# http://dumpz.org/523465/  print output in QTextEdit
# http://www.codeprogress.com/cpp/libraries/qt/showQtExample.php?key=QApplicationInstallEventFilter&index=188 eventfilter

import os
import re
import sys
import code
from rlcompleter import Completer

from .graphicssettings import *



class MyEventFilter(QObject):

    def __init__( self, parent):
        super(MyEventFilter, self).__init__(parent)


    def eventFilter( self, object, event ):
        
        if( event.type() == QEvent.KeyPress  ):

            if( (event.key()==Qt.Key_Z) and (event.modifiers() & Qt.ControlModifier) ): # ignore Ctrl+Z
                print('^Z')
                return True

            if( (event.key()==Qt.Key_Y) and (event.modifiers() & Qt.ControlModifier) ): # ignore Ctrl+Y
                print('^Y')
                return True

        return super(MyEventFilter, self).eventFilter(object, event)



class PyInterp(QPlainTextEdit):

    class Interpreter(code.InteractiveConsole):

        def __init__(self, locals):
            code.InteractiveConsole.__init__(self, locals)

        def runIt(self, command):
            try:
                code.InteractiveConsole.runsource(self, command)
            except SystemExit: # invalidate exit command
                pass


    def __init__(self, locals, parent=None ):
        super(PyInterp,  self).__init__(parent)

        self.editablePos = -1


        #sys.stdout = self # temporary disabled
        #sys.stderr = self # temporary disabled
        #sys.stdin = self
        self.refreshMarker = False  # to change back to >>> from ...
        self.multiLine = False  # code spans more than one line
        self.command = ''    # command to be ran
        self.printBanner()              # print sys info
        self.marker()                   # make the >>> or ... marker
        self.history = []    # list of commands entered
        self.historyIndex = -1
        self.interpreterLocals = {}

        self.installEventFilter( MyEventFilter(self) ) 
        self.setFont( QFont('MS Gothic', 9) )
        self.setStyleSheet( UIStyle.g_TextFieldStyleSheet + UIStyle.g_ScrollBarStyleSheet )

        
        self.setAcceptDrops(False) # forbid mouse drop

        # initilize interpreter with self locals
        self.initInterpreter(locals)

        self.completer = Completer( self.interpreter.locals )
        self.tab = False
        self.repeat = 0

        delimiters = ' |\(|\)|\[|\]|\{|\}|\,|\:|\;|\@|\=|\->|\+=|\-=|\*=|\/=|\//=|\%=|\@=|\&=|\|=|\^=|\>>=|\<<=|\*\*='# \.|  # ドットは除外する。メンバ変数アクセスのワイルドカードとして必要
        operators = '\+|\-|\*|\*\*|\/|\//|\%|\@|\<<|\>>|\&|\||\^|\~|\<|\>|\<=|\>=|\==|\!='
        self.__m_Splitters = delimiters + '|' + operators


    def printBanner(self):
        self.write(sys.version)
        self.write(' on ' + sys.platform + '\n')
        self.write('PyQt ' + PYQT_VERSION_STR + '\n')
        # msg = 'Type !hist for a history view and !hist(n) history index recall'
        # self.write(msg + '\n')


    def marker(self):
        if self.multiLine:
            self.insertPlainText('... ')
            self.editablePos = len( self.document().toPlainText() )
        else:
            self.insertPlainText('>>> ')
            self.editablePos = len( self.document().toPlainText() )



    def initInterpreter(self, interpreterLocals=None):
        if interpreterLocals:
            # when we pass in locals, we don't want it to be named "self"
            # so we rename it with the name of the class that did the passing
            # and reinsert the locals back into the interpreter dictionary
            selfName = interpreterLocals['self'].__class__.__name__
            interpreterLocalVars = interpreterLocals.pop('self')
            self.interpreterLocals[selfName] = interpreterLocalVars
        else:
            self.interpreterLocals = interpreterLocals
        self.interpreter = self.Interpreter( self.interpreterLocals )


    def updateInterpreterLocals(self, newLocals):
        className = newLocals.__class__.__name__
        self.interpreterLocals[className] = newLocals


    def write(self, line):
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

        if( self.customCommands(line) ):
            result = True#return True
        else:
            try:
                line[-1]
                if line == '    ':
                    self.haveLine = False
                else:
                    self.haveLine = True
                if line[-1] == ':':
                    self.multiLine = True
                self.history.insert(0, line)
            except:
                self.haveLine = False

            if( self.haveLine and self.multiLine ):  # multi line command
                self.command += line + '\n'  # + command and line
                self.appendPlainText('')#self.append('')  # move down one line
                self.marker()  # handle marker style
                result = True#return True

            elif( self.haveLine and not self.multiLine ):  # one line command
                self.command = line  # line is the command
                self.appendPlainText('')#self.append('')  # move down one line
                self.interpreter.runIt(self.command)
                self.command = ''  # clear command
                self.marker()  # handle marker style
                result = True#return True

            elif( self.multiLine and not self.haveLine ):  # multi line done
                self.appendPlainText('')#self.append('')  # move down one line
                self.interpreter.runIt(self.command)
                self.command = ''  # clear command
                self.multiLine = False  # back to single line
                self.marker()  # handle marker style
                result = True#return True

            elif( not self.haveLine and not self.multiLine ):  # just enter
                self.appendPlainText('')#self.append('')
                self.marker()
                result = True#return True

        sys.stdin = std_backup

        return result
        #return False




    def clearCurrentBlock(self):

        # block being current row
        length = len(self.document().lastBlock().text()[4:])

        # move cursor to end
        position = len(self.document().toPlainText())
        textCursor = self.textCursor()
        textCursor.setPosition(position)
        self.setTextCursor(textCursor)

        if length == 0:
            return None
        else:
            # should have a better way of doing this but I can't find it
            #[self.textCursor().deletePreviousChar() for x in range(length)]
            
            for x in range(0, position-self.editablePos):
                self.textCursor().deletePreviousChar()

        return True

    def recallHistory(self):
        # used when using the arrow keys to scroll through history
        self.clearCurrentBlock()
        if self.historyIndex > -1:
            self.insertPlainText(self.history[self.historyIndex])
        return True

    def customCommands(self, command):

        if command == '!hist':  # display history
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
                self.write(line)

                tex = self.textCursor().block().text()
                pass

            self.updateInterpreterLocals(backup)
            self.marker()
            return True

        if re.match('!hist\(\d+\)', command):  # recall command from history
            backup = self.interpreterLocals.copy()
            history = self.history[:]
            history.reverse()
            index = int(command[6:-1])
            self.clearCurrentBlock()
            command = history[index]
            if command[-1] == ':':
                self.multiLine = True
            self.write(command)
            self.updateInterpreterLocals(backup)
            return True

        return False

    def mousePressEvent( self,  event ):
        
        super(PyInterp, self).mousePressEvent( event )

        if( self.editablePos <= self.textCursor().position() ):
            self.setReadOnly(False)
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
                    self.clearCurrentBlock()
                    self.insertPlainText( self.prefix + self.completer.matches[self.repeat] )
                    #self.insertPlainText( self.completer.matches[self.repeat] )
                    self.repeat = ( self.repeat + 1 ) % len(self.completer.matches)
            except:
                self.tab = False
                self.repeat = 0

            return
        
        self.tab = False
        self.repeat = 0

        
        #if( event.key() == Qt.Key_Escape ):
        #    # proper exit
        #    self.interpreter.runIt('exit()')

        if( event.key() == Qt.Key_Down ):
            if self.historyIndex == len(self.history):
                self.historyIndex -= 1
            try:
                if self.historyIndex > -1:
                    self.historyIndex -= 1
                    self.recallHistory()
                else:
                    self.clearCurrentBlock()
            except:
                pass
            return None

        if( event.key() == Qt.Key_Up ):
            try:
                if len(self.history) - 1 > self.historyIndex:
                    self.historyIndex += 1
                    self.recallHistory()
                else:
                    self.historyIndex = len(self.history)
            except:
                pass
            return None

        if( event.key() == Qt.Key_Home ):
            # set cursor to position 4 in current block. 4 because that's where
            # the marker stops
            #blockLength = len(self.document().lastBlock().text()[4:])
            #lineLength = len(self.document().toPlainText())
            #position = lineLength - blockLength
            textCursor = self.textCursor()
            textCursor.setPosition(self.editablePos)
            self.setTextCursor(textCursor)

            return None

        #if event.key() in [Qt.Key_Left, Qt.Key_Backspace]:
        #    # don't allow deletion of marker
        #    # if qt version < 4.7, have to use position() - block().position()
        #    if self.textCursor().positionInBlock() == 4:
        #        return None

        if( event.key() in [Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Left] ):

            # don't allow deletion of non-editable textfield
            start_pos = self.textCursor().selectionStart()
            end_pos = self.textCursor().selectionEnd()

            if( end_pos - start_pos > 0 ):
                if( start_pos < self.editablePos ):
                    return None
            
                elif( end_pos < self.editablePos ):
                    return None
            
            # don't allow deletion of marker
            #elif( (self.textCursor().positionInBlock() == 4) and (event.key() !=Qt.Key_Delete) ):
            #    return None
            elif( (self.textCursor().position() <= self.editablePos) and (event.key() !=Qt.Key_Delete) ):
                return None


        if( event.key() in [Qt.Key_Return, Qt.Key_Enter] ):

            line = str(self.document().lastBlock().text())[4:]  # remove marker
            if( self.ExecuteCommand( line ) == True ):
                return None

        line = self.document().toPlainText()

        # allow all other key events
        super(PyInterp, self).keyPressEvent(event)


    def insertFromMimeData( self, source ):
        
        lines = source.text().split('\n')
        if( len(lines)<=1 ):
            return super(PyInterp, self).insertFromMimeData(source)

        # execute commands( except last one)
        for i in range(0, len(lines)-1):
            self.write( lines[i] )
            self.ExecuteCommand( lines[i] )

        # just put text(last command)
        self.write( lines[ len(lines)-1 ] )





