import math

from .vector import Vector
from .matrix import Matrix




################# Vector #####################

def vector2( x, y ):
    vec = Vector(2)
    vec[0] = x
    vec[1] = y
    return vec



def vector3( x, y, z ):
    vec = Vector(3)
    vec[0] = x
    vec[1] = y
    vec[2] = z
    return vec




################## 3x3 Matrix #################


def identity_3x3():
    m = Matrix( 3, 3 )
    m[0][0] = m[1][1] = m[2][2] = 1.0
    return m



def translate_3x3( x, y ):
    m = identity_3x3()
    m[0][2] = x
    m[1][2] = y
    m[2][2] = 1.0
    return m



def inverse_3x3( m ):

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