import math

from .vector import Vector
from .matrix import Matrix




################# Vector #####################

def Vec2( x, y ):
    vec = Vector(2)
    vec[0] = x
    vec[1] = y
    return vec



def Vec3( x, y, z ):
    vec = Vector(3)
    vec[0] = x
    vec[1] = y
    vec[2] = z
    return vec



def Vec4( x, y, z, w ):
    vec = Vector(4)
    vec[0] = x
    vec[1] = y
    vec[2] = z
    vec[3] = w
    return vec



def SetVec2( vec, x, y ):
    vec[0] = x
    vec[1] = y



def SetVec3( vec, x, y, z ):
    vec[0] = x
    vec[1] = y
    vec[2] = z



def SetVec4( vec, x, y, z, w ):
    vec[0] = x
    vec[1] = y
    vec[2] = z
    vec[3] = w




################## 3x3 Matrix #################


def IdentityMat3():
    m = Matrix( 3, 3 )
    m[0][0] = m[1][1] = m[2][2] = 1.0
    return m



def SetIdentityMat3( m ):
    for i in range(m.Rows()):
        for j in range(m.Cols()):
            m[i][j] = 1.0 if i==j else 0.0



def TranslateMat3( x, y ):
    m = IdentityMat3()
    m[0][2] = x
    m[1][2] = y
    return m



def SetTranslateMat3( m, x, y ):
    SetIdentityMat3( m )
    m[0][2] = x
    m[1][2] = y



def InverseMat3( m ):

    m_inv = 1.0 / ( m[0][0]*m[1][1]*m[2][2] + m[0][1]*m[1][2]*m[2][0] + m[0][2]*m[1][0]*m[2][1] - m[0][2]*m[1][1]*m[2][0] - m[0][1]*m[1][0]*m[2][2] - m[0][0]*m[1][2]*m[2][1] )
    
    cofactor = Matrix(3, 3)

    cofactor[0][0] = m[1][1] * m[2][2] - m[1][2] * m[2][1]
    cofactor[0][1] = -( m[0][1] * m[2][2] - m[0][2] * m[2][1] )
    cofactor[0][2] = m[0][1] * m[1][2] - m[0][2] * m[1][1]

    cofactor[1][0] = -( m[1][0] * m[2][2] - m[1][2] * m[2][0] )
    cofactor[1][1] = m[0][0] * m[2][2] - m[0][2] * m[2][0]
    cofactor[1][2] = -( m[0][0] * m[1][2] - m[0][2] * m[1][0] )

    cofactor[2][0] = m[1][0] * m[2][1] - m[1][1] * m[2][0]
    cofactor[2][1] = -( m[0][0] * m[2][1] - m[0][1] * m[2][0] )
    cofactor[2][2] = m[0][0] * m[1][1] - m[0][1] * m[1][0]

    return m_inv * cofactor