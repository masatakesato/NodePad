# Undo/Redo implementation using Command pattern
# reference: http://gernotklingler.com/blog/implementing-undoredo-with-the-command-pattern/

import traceback

from .commandbase import CommandBase



#----- Terminal Command  -----
class TerminalCommand( CommandBase ):

    def __init__( self, callback=None ):
        super(TerminalCommand, self).__init__()
        self.__m_refCallback = callback


    def __del__( self ):
        self.Release()


    def Release( self ):
        self.__m_refCallback = None
    

    def execute( self ):
        print( '--------------- TerminalCommand::execute() ---------------' )
        if( self.__m_refCallback ): self.__m_refCallback()


    def undo( self ):
        print( '--------------- TerminalCommand::undo() ---------------' )
        if( self.__m_refCallback ): self.__m_refCallback()


    def redo( self ):
        print( '--------------- TerminalCommand::redo() ---------------' )
        if( self.__m_refCallback ): self.__m_refCallback()



# ----- Undo/Redo Controller -----
 
class CommandManager:

    def __init__( self ):
        self.__m_UndoStack = []
        self.__m_RedoStack = []
        self.__m_Readout = None


    def __del__( self ):
        self.Clear()


    def Release( self ):
        self.Clear()


    def Clear( self ):
        self.__m_UndoStack.clear()
        self.__m_RedoStack.clear()
        self.__m_Readout = None


    def SetReadout( self ):
        try:
            self.__m_Readout = id(self.__m_UndoStack[-1])

        except:
            traceback.print_exc()
 

    def executeCmd( self, command ):

        self.__m_RedoStack.clear()

        command.execute()
        self.__m_UndoStack.append( command )
 
        return command


    def undo( self ):

        #print( '########################### CommandManager::undo()... ###########################' )

        if( len(self.__m_UndoStack) <= 0 ):
            return

        # pop terminal command and append to self.__m_RedoStack. execute later...
        topcommand = None
        if( isinstance( self.__m_UndoStack[-1], TerminalCommand ) ):
            topcommand = self.__m_UndoStack.pop() # remove top entry from undo stack
            self.__m_RedoStack.append( topcommand ) # add undone command to undo stack

        while( self.__m_UndoStack ):
            if( isinstance( self.__m_UndoStack[-1], TerminalCommand ) ):
                break
            command = self.__m_UndoStack.pop() # remove top entry from undo stack
            self.__m_RedoStack.append( command ) # add undone command to undo stack
            command.undo()                  # undo most recently executed command

        # Execute terminal command
        if( topcommand ):
            topcommand.undo()


    def redo( self ):

        #print( '########################### CommandManager::redo()... ###########################' )

        if( len(self.__m_RedoStack) <= 0 ):
            return
        
        while( self.__m_RedoStack ):
            command = self.__m_RedoStack.pop() # remove top entry from redo stack
            self.__m_UndoStack.append( command ) # add undone command to redo stack
            command.redo()                  # redo most recently executed command

            if( isinstance( command, TerminalCommand ) ):
                break


    def IsUpToDate( self ):
        if( not self.__m_UndoStack ):
            if( not self.__m_RedoStack ):
                return True
        elif( id(self.__m_UndoStack[-1])==self.__m_Readout ):
            return True

        return False


    def IsModified( self ):
        if( self.__m_UndoStack ):
            if( id(self.__m_UndoStack[-1])==self.__m_Readout ):
                return False
            else:
                return True
        else:
            if( self.__m_Readout ):
                return True
            else:
                return False
