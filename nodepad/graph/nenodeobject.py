from ..component.descriptors import *
from ..component.neobjectarray import *

from ..config.figure_params import *

from .neattributeobject import *


class NENodeObject(NEGraphObject):

    def __init__( self, name, nodeType, obj_id=None ):
        super(NENodeObject, self).__init__( name, nodeType, obj_id=obj_id )

        # clone NodeDesc object
        self.__m_LayoutDesc = AttribLayoutDesc()
        self.__m_Desc = NodeDesc( nodeType, self.__m_LayoutDesc )
        self.__m_Attributes = {}
        self.__m_refInputs = NEObjectArray()
        self.__m_refOutputs = NEObjectArray()

        self.__m_Desc._NodeDesc__m_ObjectID = self.ID()



    def Release( self ):
        self.ClearAttributes()
        super(NENodeObject, self).Release()



    def AddAttribute( self, attribDesc, attr_id ):
        attrib = NEAttributeObject( attribDesc, attr_id, self.ID() )
        attrib._NEGraphObject__m_Parent = self
        self.__m_Attributes[ attrib.ID() ] = attrib

        refIOs = self.__m_refInputs if attrib.IsInputFlow() else self.__m_refOutputs
        refIOs[ attrib.ID() ] = attrib
        self.__m_LayoutDesc.AddAttribDesc( attrib.GetDesc() )


    
    def RemoveAttribute( self, attr_id ):
        try:
            attrib = self.__m_Attributes[ attr_id ]
            attrib_key = attrib.Key()
            refIOs = self.__m_refInputs if attrib.IsInputFlow() else self.__m_refOutputs
            
            refIOs[attr_id] = None
            del refIOs[attr_id]

            attrib.Release()
            del self.__m_Attributes[ attr_id ]

        except:
            pass



    def ClearAttributes( self ):
        for attrib in self.__m_Attributes.values():
            if( attrib.HasChildren() ):  attrib.ClearChildren()

        #print( self.Key() + '.ClearAttributes()...' )
        self.__m_Attributes.clear()
        self.__m_refInputs.clear()
        self.__m_refOutputs.clear()

        self.__m_Desc = None


    
    def HasAttribute( self, attr_id ):
        return attr_id in self.__m_Attributes
        #return ( attr_id in self.__m_refInputs ) or ( attr_id in self.__m_refOutputs )



    def NumAttributes( self ):
        return len(self.__m_Attributes)



    def Attributes( self ):
        return self.__m_Attributes


    
    def AttributeByID( self, query ):
        try:
            return self.__m_Attributes[ query ]
        except:
            traceback.print_exc()
            return None



    def AttributeByName( self, query ):
        if( query in self.__m_refInputs ):
            return self.__m_refInputs[ query ]
        if(  query in self.__m_refOutputs ):
            return self.__m_refOutputs[ query ]
        return None



    def NumInputAttributes( self ):
        return len(self.__m_refInputs)



    def InputAttributes( self ):
        return self.__m_refInputs
    


    def InputAttribute( self, query ):
        try:
            return self.__m_refInputs[ query ]
        except:
            traceback.print_exc()
            return None



    def NumOutputAttributes( self ):
        return len(self.__m_refOutputs)



    def OutputAttributes( self ):
        return self.__m_refOutputs
    


    def OutputAttribute( self, query ):
        try:
            return self.__m_refOutputs[ query ]
        except:
            traceback.print_exc()
            return None



    def RenameAttribute( self, attr_id, newkey ):
        try:
            refAttrib = self.__m_Attributes[ attr_id ]
            ## Update KeyMap
            #self.__m_KeyMap[newkey] = self.__m_KeyMap.pop(refAttrib.Key())
            ## Update attribute's name
            #refAttrib.SetKey( newkey )
            #self.__m_Attributes.setname( refAttrib.Key(), newkey )

            if( attr_id in self.__m_refInputs ):
                self.__m_refInputs.setname( refAttrib.Key(), newkey )
            elif(  attr_id in self.__m_refOutputs ):
                self.__m_refOutputs.setname( refAttrib.Key(), newkey )

            refAttrib.GetDesc().SetName( newkey )
            refAttrib.SetKey( newkey )

            return True

        except:
            traceback.print_exc()
            return False



    def GetDesc( self ):
        return  self.__m_Desc



    def FullKey( self, suffix='' ):
        if( self._NEGraphObject__m_Parent ):
            return self._NEGraphObject__m_Parent.FullKey('|') + self._NEObject__m_Key + suffix
        else:
            return self._NEObject__m_Key + suffix



    def Info( self ):
        print( '//------------- Node: ' + self.FullKey() + ' -------------//' )
        if( self.Parent() ):
            print( 'Parent: %s' % self.Parent().Key() )

        for attrib in self.__m_Attributes.values():
            attrib.Info()



    def GetSnapshot( self ):
        return NENodeSnapshot( self )



######################### TODO: 試験実装. QGraphicsItemの外部で形状パラメータを保持したい ############################

    # Overriding NEGraphObject::SetSize
    def SetSize( self, size=None ):
        if( size ):
            super(NENodeObject, self).SetSize(size)
        else:
            numslots = max( 1, max( self.NumInputAttributes(), self.NumOutputAttributes() ) )
            width = g_NodeMinWidth + g_NodeFrameWidth * 2
            height = ( g_NodeMinHeight + numslots * g_AttribAreaHeight ) + g_NodeFrameWidth * 2
            super(NENodeObject, self).SetSize( [ width, height ] )
            

    #def __UpdateSize( self, numslots ):
        
    #    self.__m_Size[0] = g_NodeMinWidth
    #    self.__m_Size[1] = g_NodeMinHeight + max(1, numslots) * g_AttribAreaHeight 

    #    self.__m_Size[0] += g_NodeFrameWidth * 2
    #    self.__m_Size[1] += g_NodeFrameWidth * 2





class NENodeSnapshot():

    def __init__( self, refObj ):

        self.__m_NodeArgs = None
        self.__m_ActiveAttribIDs = [ [], [] ]# [0]:input attribute list, [1]: output attribute id list
        self.__m_AttribNames = []
        self.__m_AttribArgs = []

        self.__CollectNodeArgs( refObj )



    def ObjectType( self ):
        return self.__m_NodeArgs[0]



    def Translation( self ):
        return self.__m_NodeArgs[1]



    def Size( self ):
        return self.__m_NodeArgs[2]



    def ObjectID( self ):
        return self.__m_NodeArgs[3]



    def Key( self ):
        return self.__m_NodeArgs[4]



    def ParentID( self ):
        return self.__m_NodeArgs[5]



    def ActiveAttribIDs( self ):
        return self.__m_ActiveAttribIDs



    def AttribNames( self ):
        return self.__m_AttribNames



    def AttribArgs( self ):
        return self.__m_AttribArgs



    def __CollectNodeArgs( self, refObj ):

        object_id = refObj.ID()

        # Node Creation params( nodetype, position, object_id, node_name)
        self.__m_NodeArgs = [ refObj.ObjectType(), refObj.GetPosition(), refObj.GetSize(), object_id, refObj.Key(), refObj.ParentID() ]

        # Attribute name snapshots
        for attrib in refObj.Attributes().values():
            self.__m_AttribNames.append( ( object_id, attrib.ID(), attrib.Key(), attrib.LockState() ) )

        # Attribute settings
        for attrib in refObj.Attributes().values():
            self.__m_AttribArgs.append( ( object_id, attrib.ID(), attrib.Value(), attrib.LockState() ) )

        # Get Attribute IDs
        desc = refObj.GetDesc()
        for attribdesc in desc.InputAttribDescs():
            self.__m_ActiveAttribIDs[0].append( attribdesc.ObjectID()[1] )

        for attribdesc in desc.OutputAttribDescs():
            self.__m_ActiveAttribIDs[1].append( attribdesc.ObjectID()[1] )
