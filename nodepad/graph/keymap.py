from collections import defaultdict

from .negraphobject import NEGraphObject


g_NodeKeySplitter = '|'



class KeyMap:

    def __init__( self, root=None ):

        self.__m_LookupTable = defaultdict(dict)

        if( root ):
            self.__m_LookupTable[ root.Key() ][ root.ID() ] = root


    def __del__( self ):
        self.Release()


    def Release( self ):
        self.__m_LookupTable.clear()


    # query_key must be fullkey
    def IsAlreadyUsed( self, query_key, exclude_ids=() ):
        
        partialKeys = tuple( reversed(query_key.split(g_NodeKeySplitter)) )

        if( not(partialKeys[0] in self.__m_LookupTable) ):
            return False
        
        # Try to find completely matched element from multiple elements
        filtered = [ v for v in self.__m_LookupTable[partialKeys[0]].values() if( query_key==v.FullKey() and not v.ID() in exclude_ids ) ]
        if( len(filtered) > 0 ): # found unique element
            return True
    
        return False


    def GetCompletelyMatched( self, query_key ):

        partialKeys = tuple( reversed(query_key.split(g_NodeKeySplitter)) )

        if( not(partialKeys[0] in self.__m_LookupTable) ):
            print( 'No localKey entry found... ')
            return None

        localList = list(self.__m_LookupTable[ partialKeys[0] ].values())

        # Check if single element completely matches with query_key
        if( len(localList)==1 and query_key==localList[0].FullKey() ):
            return localList[0]

        return None


    def GetObject( self, query_key ):

        partialKeys = tuple( reversed(query_key.split(g_NodeKeySplitter)) )

        if( not(partialKeys[0] in self.__m_LookupTable) ):
            print( 'No localKey entry found... ')
            return None

        #print( 'LocalKey entry found... ')
        localList = list(self.__m_LookupTable[ partialKeys[0] ].values())

        # Check if single element completely matches with query_key
        if( len(localList)==1 and query_key==localList[0].FullKey() ):
            print( 'Found unique result: ', localList[0].FullKey() )
            return localList[0]
        
        # Try to find completely matched element from multiple elements
        filtered = [ v for v in localList if(query_key==v.FullKey()) ]
        if( len(filtered)==1 ): # found unique element
            print( 'Filtered completely matched result: ', filtered[0].FullKey() )
            return filtered[0]

        # Try to find partially matched element from localList
        filtered = [ v for v in localList if(query_key in v.FullKey()) ]
        if( len(filtered)==1 ): # found unique element
            print( 'Found partially matched result: ', filtered[0].FullKey() )
            return filtered[0]
        
        # multiple candicates
        print( 'Multiple partially matched candicates. Which one?' )
        for obj in filtered: print( '  ', obj.FullKey(), '(', obj.ID(), ')' )

        return None


    def Add( self, obj ):
        self.__m_LookupTable[ obj.Key() ][ obj.ID() ] = obj


    def Remove( self, obj ):

        # disable obj references
        del self.__m_LookupTable[ obj.Key() ][ obj.ID() ]
    
        # cleanup. remove empty local key entry
        if( not self.__m_LookupTable[ obj.Key() ] ):
            #print( 'Removing empty keyMap entry: ', obj.Key() )
            del self.__m_LookupTable[ obj.Key() ]


    def Rename( self, obj_id, old_key, new_key ):

        try:
            self.__m_LookupTable[new_key][obj_id] = self.__m_LookupTable[old_key].pop(obj_id)
            if( not self.__m_LookupTable[old_key] ):   del self.__m_LookupTable[old_key]
            return True
        except:
            return False