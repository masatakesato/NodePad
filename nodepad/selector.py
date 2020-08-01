class Selector:

    def __init__( self, datatype ):
        self.__m_DataType = datatype
        self.__m_Objects = []
        self.__m_bChanged = False



    def Exec( self, *args, **kwargs ):

        obj_ids = [ arg for arg in args if isinstance(arg, self.__m_DataType) ]
 
        if( 'add' in kwargs ):# add
            if( kwargs['add']==True ):
                self.__Add( obj_ids )

        elif( 'delete' in kwargs ):# delete
            if( kwargs['delete']==True ):
                self.__Delete( obj_ids )

        elif( 'clear' in kwargs ):# clear
            if( kwargs['clear']==True ):
                self.__Clear( obj_ids )

        else:# no option specified
            self.__Add( obj_ids )



    def Iter( self ):
        return iter(self.__m_Objects)



    def Changed( self ):
        return self.__m_bChanged



    def Contains( self, query ):
        return query in self.__m_Objects



    def Info( self ):
        print( '//============ Selector Information ============//')
        print( 'Selected Objects:' )#, self.__m_Objects )
        for i, elm in enumerate(self.__m_Objects ):
            print( '  [{}]: {}'.format(i, elm) )
        print( 'Selection Changed: {}\n'.format( self.__m_bChanged ) )



    def __Add( self, objects ):

        len_before = len( self.__m_Objects )
        self.__m_Objects = list( dict.fromkeys( self.__m_Objects + objects ) )
        len_after = len( self.__m_Objects )

        self.__m_bChanged = len_before != len_after



    def __Delete( self, objects ):

        len_before = len( self.__m_Objects )
        self.__m_Objects = [ obj_id for obj_id in self.__m_Objects if not obj_id in objects ]
        len_after = len( self.__m_Objects )

        self.__m_bChanged = len_before != len_after



    def __Clear( self, objects ):

        if( not self.__m_Objects and not objects ):
            self.__m_bChanged = False

        else:
            self.__m_Objects.clear()
            self.__m_Objects = objects
            self.__m_bChanged = True
