class SelectionList:

    def __init__( self, datatype ):
        self.__m_Selection_list = []
        self.__m_Changed = False
        self.__m_DataType = datatype


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
        return iter(self.__m_Selection_list)


    def Changed( self ):
        return self.__m_Changed


    def Print( self ):
        print( 'SelectionList:', self.__m_Selection_list )
        print( 'Changed:', self.__m_Changed )


    def __Add( self, object_ids ):
        len_before = len( self.__m_Selection_list )
        self.__m_Selection_list = list( dict.fromkeys( self.__m_Selection_list + object_ids ) )
        len_after = len( self.__m_Selection_list )
        self.__m_Changed = len_before != len_after


    def __Delete( self, object_ids ):
        len_before = len( self.__m_Selection_list )
        self.__m_Selection_list = [ obj_id for obj_id in self.__m_Selection_list if not obj_id in object_ids ]
        len_after = len( self.__m_Selection_list )
        self.__m_Changed = len_before != len_after


    def __Clear( self, object_ids ):
        if( not self.__m_Selection_list and not object_ids ):
            self.__m_Changed = False
        else:
            self.__m_Selection_list.clear()
            self.__m_Selection_list = object_ids
            self.__m_Changed = True
