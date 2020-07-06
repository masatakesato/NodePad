import numbers
import traceback


class Vector:

    def __init__( self, dim ):
        self.__m_Elms = [0.0] * dim
        self.__m_Dim = dim



    def Dim( self ):
        return self.__m_Dim



    def __getitem__( self, i ):
        return self.__m_Elms[i]



    def __setitem__( self, i, v ):
        self.__m_Elms[i] = v



    def Print( self ):
        print( self.__m_Elms )
