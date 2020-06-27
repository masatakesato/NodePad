from .neobject import *


import collections
import traceback


# NEObject array. Supports both "object_id" and "string key" suffixes.
class NEObjectArray( collections.MutableMapping ):

    class Elem():
        def __init__( self, data, objId, name ):
            self.data = data
            self.objId = objId
            self.name = name


    def __init__( self ):

        self.__m_DataArray = {}# key: name, value: Elem
        self.__m_IndexMap = [] # value: reference to DataArray Element
        self.__m_ObjIdMap = {} # key: uuid, value: reference to DataArray Element

        self.__m_GetItemCallbacks = { uuid.UUID: self.__callback__getitem_objId, int: self.__callback__getitem_index, str: self.__callback__getitem_name }
        self.__m_SetItemCallbacks = { uuid.UUID: self.__callback__setitem_objId, int: self.__callback__setitem_index, str: self.__callback__setitem_name }
        self.__m_DelItemCallbacks = { uuid.UUID: self.__callback__delitem_objId, int: self.__callback__delitem_index, str: self.__callback__delitem_name }
        self.__m_ContainsCallbacks = { uuid.UUID: self.__callback__contains_objId, int: self.__callback__contains_index, str: self.__callback__contains_name }



    ############# override ################
    def __getitem__( self, key ):
        try:
            return self.__m_GetItemCallbacks[type(key)]( key )
        except:
            traceback.print_exc()
            return None   


    def __setitem__( self, key, value ):
        try:
            self.__m_SetItemCallbacks[type(key)]( key, value )
        except:
            traceback.print_exc()


    def __delitem__( self, key ):
        try:
            self.__m_DelItemCallbacks[type(key)]( key )  
        except:
            traceback.print_exc()


    def __len__( self ):
        return len(self.__m_DataArray)


    def __iter__( self ):
        return iter(self.__m_DataArray)


    def __keytransform__(self, key):
        return key


    def __contains__( self, key ):
        return self.__m_ContainsCallbacks[type(key)](key)


    def append( self, value, name ):
        try:
            if( not isinstance(value, NEObject) ):#if( not isinstance(value, NEGraphObject) ):
                return
            data = self.Elem( value, value.ID(), name )
            self.__m_DataArray.__setitem__( name, data )
            self.__m_ObjIdMap.__setitem__( data.objId, data )
            self.__m_IndexMap.append( data )
        except:
            traceback.print_exc()


    def insert( self, index, name, value ):
        try:
            if( not isinstance(value, NEObject) ):#if( not isinstance(value, NEGraphObject) ):
                return
            if( self.__m_DataArray.__contains__(name) ):
                self.__callback__delitem_name(name)

            newdata = self.Elem( value, value.ID(), name )
            self.__m_DataArray.__setitem__( name, newdata )
            self.__m_ObjIdMap.__setitem__( newdata.objId, newdata )
            self.__m_IndexMap.insert( index, newdata )

        except:
            traceback.print_exc()


    def setname( self, name, newname ):

        if( newname in self.__m_DataArray ):
            print( newname + ' is already in use. aborting setname()...' )
            return

        self.__m_DataArray[ newname ] = self.__m_DataArray.pop( name )
        self.__m_DataArray[ newname ].name = newname


    def setid( self, objId, newid ):

        if( newid in self.__m_ObjIdMap ):
            print( str(newid) + ' is already in use. aborting setname()...' )
            return

        self.__m_ObjIdMap[ newid ] = self.__m_ObjIdMap.pop( objId ) # replace uuid key
        self.__m_ObjIdMap[ newid ].objId = newid


    def setindex( self, srcidx, dstidx ):

        if( srcidx==dstidx ):
            return

        if( srcidx >= len(self.__m_IndexMap) ):
            #print( 'srcidx(' + str(srcidx) + ') is out of range. aborting setindex()...' )
            return
           
        if( dstidx >= len(self.__m_IndexMap) ):
            #print( 'dstidx(' + str(dstidx) + ') is out of range. aborting setindex()...' )
            return

        self.__m_IndexMap.insert( dstidx, self.__m_IndexMap.pop( srcidx ) )


    def name_at_index( self, index ):
        return self.__m_IndexMap.__getitem__(index).name


    def name_at_objid( self, objId ):
        return self.__m_ObjIdMap.__getitem__(objId).name



    ############# private callback funcs #############

    def __callback__getitem_objId( self, objId ):
        return self.__m_ObjIdMap.__getitem__(objId).data

    def __callback__getitem_index( self, index ):
        return self.__m_IndexMap.__getitem__(index).data

    def __callback__getitem_name( self, name ):
        return self.__m_DataArray.__getitem__(name).data


    def __callback__setitem_objId( self, objId, value ):
        name = value.Key()
        newdata = self.Elem( value, objId, name )
        self.__callback_setitem( objId, name, value )


    # キー/uuidが重複する場合はどうする？
    def __callback__setitem_index( self, index, value ):

        print( 'setitem using index not allowed. use name or objid instead.' )
        #if( index >= self.__len__() ):
        #    print( '__callback__setitem_index: Index out of range. aborting...' )
        #    return

        #data = self.__m_IndexMap.__getitem__(index)
        #newdata = self.Elem( value, data.objId, data.name )

        #self.__m_ObjIdMap.__delitem__( data.objId )
        #self.__m_IndexMap.__setitem__( index, None )
        #self.__m_DataArray.__delitem__( data.name )

        #self.__m_DataArray.__setitem__( newdata.name, newdata )
        #self.__m_ObjIdMap.__setitem__( newdata.objId, newdata )
        #self.__m_IndexMap.__setitem__( index, newdata )


    def __callback__setitem_name( self, name, value ):#
        objId = value.ID()
        newdata = self.Elem( value, objId, name )
        self.__callback_setitem( objId, name, value )


    # 配列要素の順序を保持したままアイテム追加する
    def __callback_setitem( self, objId, name, value ):

        newdata = self.Elem( value, objId, name )

        if( objId in self.__m_ObjIdMap ):# objIdが既存の検索キーと衝突する場合
            data = self.__m_ObjIdMap.__getitem__(objId)
            index = self.__m_IndexMap.index(data)

            self.__m_ObjIdMap.__delitem__( data.objId )
            self.__m_IndexMap.__setitem__( index, None )
            self.__m_DataArray.__delitem__( data.name )

            self.__m_IndexMap.__setitem__( index, newdata )

        elif( name in self.__m_DataArray ):# value.Key()が既存の検索キーと衝突する場合
            data = self.__m_DataArray.__getitem__( name )
            index = self.__m_IndexMap.index(data)

            self.__m_ObjIdMap.__delitem__( data.objId )
            self.__m_IndexMap.__setitem__( index, None )
            self.__m_DataArray.__delitem__( data.name )

            self.__m_IndexMap.__setitem__( index, newdata )

        else:# 新規登録の場合
            self.__m_IndexMap.append( newdata )

        self.__m_DataArray.__setitem__( newdata.name, newdata )
        self.__m_ObjIdMap.__setitem__( newdata.objId, newdata )


    def __callback__delitem_objId( self, objId ):
        self.__callback__delitem( self.__m_ObjIdMap.__getitem__(objId) )


    def __callback__delitem_index( self, index ):
        self.__callback__delitem( self.__m_IndexMap.__getitem__(index) )


    def __callback__delitem_name( self, name ):
        self.__callback__delitem( self.__m_DataArray.__getitem__(name) )


    def __callback__delitem( self, data ):
        self.__m_ObjIdMap.__delitem__( data.objId )
        self.__m_IndexMap.__delitem__( self.__m_IndexMap.index(data) )
        self.__m_DataArray.__delitem__( data.name )



    def __callback__contains_objId( self, objId ):
        return objId in self.__m_ObjIdMap

    def __callback__contains_index( self, index ):
        return index>=0 and index<len(self.__m_IndexMap)

    def __callback__contains_name( self, name ):
        return name in self.__m_DataArray


    def Info( self ):
        print('=============== Array elements ===============')
        for i in range(0, len(self)):
            print( i, ': (', self.__m_IndexMap[i].name, ',', self.__m_IndexMap[i].objId, '):', self.__m_IndexMap[i].data.Key() )