import uuid


class NEObject:

    def __init__( self, key, objtype, obj_id=None ):
        self.__m_ID = obj_id if obj_id else uuid.uuid1()
        self.__m_Key = key
        self.__m_ObjectType = objtype



    def Key( self ):
        return self.__m_Key



    def SetKey( self, key ):
        #print( 'NEObject::SetKey()... %s' % key )
        self.__m_Key = key
        return True



    def ObjectType( self ):
        return self.__m_ObjectType



    def IsObjectType( self, objtype ):
        return self.__m_ObjectType == objtype



    def SetObjectType( self, objtype ):
        self.__m_ObjectType = objtype



    def ID( self ):
        return self.__m_ID