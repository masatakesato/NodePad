from oreorelib.math import util as mathutil



# Transform Class. Unused for now. 2020.07.07
class Transform2D:

    def __init__( self ):
        self.Local = mathutil.IdentityMat3()# Local transform matrix of THIS object
        self.Derived = mathutil.IdentityMat3()# Transform matrix accumulated from parent space.
        self.World = mathutil.IdentityMat3()# Local-to-world transform matrix.



    def SetTranslation( self, x, y ):
        pass



    def SetRotation( self, rotz ):
        pass



    def SetScaling( self, scale ):
        pass