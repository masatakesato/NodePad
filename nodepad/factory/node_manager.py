import traceback

from ..component.descriptors import *



#TODO: プラグイン実装ではなく、関数記述だけからノード動的生成できないか.


class NodeTypeManager:

    def __init__( self ):
        self.__m_NodeDescs = {}
        self.__m_Index = []

        self.__m_ComputeFuncs = {}


    def Release( self ):
        for desc in self.__m_NodeDescs.values(): desc.Release()
        self.__m_NodeDescs.clear()
        self.__m_Index.clear()

        self.__m_ComputeFuncs.clear()


    def Register( self, objectType, layoutDesc, computeCallback ):
        if( objectType in self.__m_NodeDescs ):
            print( 'Warning: NodeType "' + objectType +'" already exists. Canceling registration.' )
            return False
        else:
            self.__m_NodeDescs[ objectType ] = NodeDesc( objectType, layoutDesc )
            self.__m_Index.append( objectType )

            self.__m_ComputeFuncs[ objectType ] = computeCallback

            #print( 'NodeTypeManager::Register()... Test computeCallback.' )
            #computeCallback(None)

            return True

    
    def Unregister( self, objectType ):
        if( objectType in self.__m_NodeDescs ):
            del self.__m_NodeDescs[ objectType ]
            self.__m_Index.remove(objectType)

            del self.__m_ComputeFuncs[ objectType ]

            return True
        else:
            print( 'Warning: NodeType "' + objectType +'" does not exists.' )
            return False


    def GetNodeDesc( self, objectType ):
        try:
            return self.__m_NodeDescs[ objectType ]
        except:
            traceback.print_exc()
            return None


    def GetNodeDescByIndex( self, idx ):
        try:
            return self.__m_NodeDescs[ self.__m_Index[idx] ]
        except:
            traceback.print_exc()
            return None


    def NumNodeDescs( self ):
        return len(self.__m_Index)



    def GetComputeFunc( self, objectType ):
        try:
            return self.__m_ComputeFuncs[ objectType ]
        except:
            traceback.print_exc()
            return None


    def GetComputeFuncByIndex( self, idx ):
        try:
            return self.__m_ComputeFuncs[ self.__m_Index[idx] ]
        except:
            traceback.print_exc()
            return None