import numbers
import traceback

from .vector import Vector


class Matrix:

    def __init__( self, numrows=2, numcols=2 ):
        self.__m_Elms = []
        self.__m_NumRows = numrows
        self.__m_NumCols = numcols

        for i in range(self.__m_NumRows):
            self.__m_Elms.append( Vector(numcols) )
                


    def Init( self, data ):
        try:
            if( not isinstance(data, list) ): raise ValueError( 'Not List.' )

            for i in range(self.__m_NumRows):
                for j in range(self.__m_NumCols):
                    if( not isinstance(data[i][j], numbers.Number) ): raise ValueError( 'Not numeric element.' )
                    self.__m_Elms[i][j] = data[i][j]
            return True

        except:
            traceback.print_exc()
            return False



    def Rows( self ):
        return self.__m_NumRows



    def Cols( self ):
        return self.__m_NumCols

     

    def __getitem__( self, row ):
        return self.__m_Elms[row]



    def __add__( self, other ):
        result = self.__class__( self.__m_NumRows, self.__m_NumCols )
        for i in range(self.__m_NumRows):
            for j in range(self.__m_NumCols):
                result.__m_Elms[i][j] = self.__m_Elms[i][j] + other.__m_Elms[i][j]
        return result



    def __sub__( self, other ):
        result = self.__class__( self.__m_NumRows, self.__m_NumCols )
        for i in range(self.__m_NumRows):
            for j in range(self.__m_NumCols):
                result.__m_Elms[i][j] = self.__m_Elms[i][j] - other.__m_Elms[i][j]
        return result



    def __mul__( self, other ):

        try:
            if( isinstance(other, Matrix) ):# mat by mat
                result = self.__class__( self.__m_NumRows, other.__m_NumCols )
                for i in range(self.__m_NumRows):
                    for j in range(other.__m_NumCols):
                        result[i][j] = 0.0
                        for k in range(self.__m_NumCols):
                            result[i][j] += self.__m_Elms[i][k] * other.__m_Elms[k][j]
                return result

            elif( isinstance(other, Vector) ):# mat by vector
                dim = min( other.Dim(), self.__m_NumRows )
                result = Vector( dim )
                for i in range( dim ):
                    result[i] = 0.0
                    for j in range( dim ):
                        result[i] += self.__m_Elms[i][j] * other[j]
                return result

            else:
                raise TypeError( 'Unsupported type.' )

        except:
            traceback.print_exc()
            return None



    def __rmul__( self, other ):
        result = self.__class__( self.__m_NumRows, self.__m_NumCols )
        for i in range(self.__m_NumRows):
            for j in range(self.__m_NumCols):
                result.__m_Elms[i][j] = other * self.__m_Elms[i][j]
        return result



    def __imul__( self, other ):
        try:
            if( isinstance(other, Matrix) ):# mat by mat
                result = []
                for i in range(self.__m_NumRows): result.append( Vector(other.__m_NumCols) )

                for i in range(self.__m_NumRows):
                    for j in range(other.__m_NumCols):
                        result[i][j] = 0.0
                        for k in range(self.__m_NumCols):
                            result[i][j] += self.__m_Elms[i][k] * other.__m_Elms[k][j]

                self.__m_Elms.clear()
                self.__m_Elms = result
                self.__m_NumCols = other.__m_NumCols
                return self

            elif( isinstance(other, Vector) ):# mat by vector
                result = []
                for i in range(self.__m_NumRows): result.append( Vector(1) )

                for i in range( self.__m_NumRows ):
                    result[i][0] = 0.0
                    for j in range( other.Dim() ):
                        result[i][0] += self.__m_Elms[i][j] * other[j]
                
                self.__m_Elms.clear()
                self.__m_Elms = result
                self.__m_NumCols = 1
                return self

            else:
                raise TypeError( 'Unsupported type.' )

        except:
            traceback.print_exc()
            return None



    def Print( self ):
        for elm in self.__m_Elms: elm.Print()