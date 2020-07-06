from oreorelib.math import util as mathutil


class Transform:

    def __init__( self ):
        self.__m_LocalTransform = mathutil.IdentityMat3() # Local transformation matrix of THIS object
        self.__m_DerivedTransform = mathutil.IdentityMat3() # Transform matrix accumulated from parent space.
        self.__m_DirtyFlag = True # True: Transform matrices are out of date(needs update), False: Transform matrices are up to date.



    def SetTranslation( self, pos ):
        mathutil.SetTranslateMat3( self.__m_LocalTransform, pos[0], pos[1] )



    def Update( self ):
        self.__m_DirtyFlag = False# Set transform matrices status to 'up to date'



    def SetDirty( self ):
        self.__m_DirtyFlag = True



    def SetClean( self ):
        self.__m_DirtyFlag = False



    def IsDirty( self ):
        return self.__m_DirtyFlag