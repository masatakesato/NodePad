from enum import IntEnum


################### Types #######################

class DataFlow(IntEnum):
    Unknown         = -1
    Input           = 0
    Output          = 1
    Internal        = 2 # internal.


class ConnectionMode(IntEnum):
    Disabled = 0
    Single = 1
    Multiple = 2


class SelectionMode(IntEnum):
    Add = 0
    Deselect = 1
    Clear = 2


############### Attribute Descriptor ###############

class AttribDesc:

    def __init__( self, attribtype, flow, datatype, allowmultconnect, editable, name, val, connectableTypes ):
        self.__m_AttribType = attribtype
        self.__m_DataFlow = flow
        self.__m_DataType = datatype
        self.__m_bEditable = editable
        self.__m_Enabled = True
        self.__m_AllowMultiConnect = allowmultconnect
        self.__m_Name = name
        self.__m_DefaultValue = val

        self.__m_ConnectableTypes = connectableTypes

        self.__m_ObjectID = None



    def SetAttributeType( self, attribtype ):
        self.__m_AttribType = attribtype



    def SetDataFlow( self, flow ):
        self.__m_DataFlow = flow



    def SetDataType( self, datatype ):
        self.__m_DataType = datatype



    def SetEditable( self, flag ):
        self.__m_bEditable = flag



    def SetEnable( self, flag ):
        self.__m_Enabled = flag



    def SetAllowMultiConnect( self, flag ):
        self.__m_AllowMultiConnect = flag



    def SetName( self, name ):
        self.__m_Name = name



    def SetDefaultValue( self, value ):
        self.__m_DefaultValue = value



    def ObjectID( self ):
        return self.__m_ObjectID



    def AttributeType( self ):
        return self.__m_AttribType



    def DataFlow( self ):
        return self.__m_DataFlow



    def IsInputFlow( self ):
        return self.__m_DataFlow==DataFlow.Input



    def IsOutputFlow( self ):
        return self.__m_DataFlow == DataFlow.Output



    def DataType( self ):
        return self.__m_DataType



    def ConnectableTypes( self ):
        return self.__m_ConnectableTypes



    def IsEditable( self ):
        return self.__m_bEditable



    def Enabled( self ):
        return self.__m_Enabled



    def MultipleConnectAllowed( self ):
        return self.__m_AllowMultiConnect



    def Name( self ):
        return self.__m_Name



    def DefaultValue( self ):
        return self.__m_DefaultValue



############### Node/Group/Symboliclink's Attribute Layout Descriptor ###############

class AttribLayoutDesc:

    def __init__( self ):
        self.__m_AttribDescs = { DataFlow.Input: list(), DataFlow.Output: [] }



    def Release( self ):
        self.__m_AttribDescs[ DataFlow.Input ].clear()
        self.__m_AttribDescs[ DataFlow.Output ].clear()



    def AddAttribDesc( self, desc, index=None ):
        if( index==None ):
            self.__m_AttribDescs[ desc.DataFlow() ].append( desc )
        else:
            self.__m_AttribDescs[ desc.DataFlow() ].insert( index, desc )



    def RemoveAttribDesc( self, desc ):
        self.__m_AttribDescs[ desc.DataFlow() ].remove( desc )



    def NumInputAttribDescs( self ):
        return len( self.__m_AttribDescs[ DataFlow.Input ] )



    def InputAttribDescs( self ):
        return self.__m_AttribDescs[ DataFlow.Input ]



    def NumOutputAttribDescs( self ):
        return len( self.__m_AttribDescs[ DataFlow.Output ] )



    def OutputAttribDescs( self ):
        return self.__m_AttribDescs[ DataFlow.Output ]



    def ChangeOrder( self, src_idx, dst_idx, dataflow ):
        self.__m_AttribDescs[ dataflow ].insert( dst_idx, self.__m_AttribDescs[ dataflow ].pop(src_idx) )



    #def Sort( self, order, dataflow ):
    #    self.__m_AttribDescs[ dataflow ] = [ x for _,x in sorted(zip(order, self.__m_AttribDescs[ dataflow ])) ]



############### Node/Group/Symboliclink's Descriptor ###############

class NodeDesc:

    def __init__( self, objectType, layoutdesc ):#, updater ):
        self.__m_ObjectType = objectType
        self.__m_AttribLayoutDesc = layoutdesc
        #self.__m_Updater = updater
        self.__m_Enabled = True
        self.__m_ObjectID = None



    def Release( self ):
        self.__m_AttribLayoutDesc.Release()



    def ObjectID( self ):
        return self.__m_ObjectID



    def ObjectType( self ):
        return self.__m_ObjectType



    def InputAttribDescs( self ):
        return self.__m_AttribLayoutDesc.InputAttribDescs()



    def OutputAttribDescs( self ):
        return self.__m_AttribLayoutDesc.OutputAttribDescs()



    def SetEnable( self, flag ):
        self.__m_Enabled = flag



    def Enabled( self ):
        return self.__m_Enabled



    #def Updater( self ):
    #    return self.__m_Updater