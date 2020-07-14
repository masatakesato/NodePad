from collections import defaultdict, deque
import traceback


from ..component.descriptors import *
from ..component.nedata import NEData
from ..component.nedatabuffer import NEDataBuffer

from ..factory.pipeline import Pipeline

from .negraphobject import NEGraphObject
from .nerootobject import NERootObject
from .neattributeobject import NEAttributeObject
from .neconnectionobject import NEConnectionObject
from .nenodeobject import NENodeObject
from .negroupobject import NEGroupObject
from .nesymboliclink import NESymbolicLink
from .negroupioobject import NEGroupIOObject

from .keymap import KeyMap





#================== Node Traversal ====================#

# Depth First Scan without recursion
def DepthFirstScan( node, group_id_list, node_id_list ):

    nodes_to_visit = [node]

    while( nodes_to_visit ):
        currentnode = nodes_to_visit.pop()
        for obj in currentnode.Children().values():
            nodes_to_visit.append(obj)
        
        #do something
        if( isinstance(currentnode, NENodeObject) ):
            node_id_list.append( currentnode.ID() )
        elif( isinstance(currentnode,NEGroupObject) ):
            group_id_list.append( currentnode.ID() )

    nodes_to_visit.clear()



# Depth First Scan with recursion
#def DepthFirstScan_rec( node, group_id_list, node_id_list ):
    
#    if( isinstance(node,NENodeObject) ):
#        node_id_list.append( node.ID() )
#    elif( isinstance(node,NEGroupObject) ):
#        group_id_list.append( node.ID() )
#    else:
#        return

#    #if( len(node.Children()) < 1 ):
#    #    return

#    for child in node.Children().values():
#        DepthFirstScan_rec( child, group_id_list, node_id_list )


#def BreadsFirstScan( root ):

#    q = queue.Queue()

#    q.put( root )

#    while not q.empty():

#        data = q.get()
#        if( isinstance( data, Node) ):
#            data.Info()

#        for child in data.Children().values():
#            q.put( child )





c_IDMapSupportTypes = (
    NERootObject,
    NENodeObject,
    NEConnectionObject,
    NEGroupObject,
    NEGroupIOObject,
    NESymbolicLink, )



c_KeyMapSupportTypes = (
    NENodeObject,
    NEGroupObject,
    NEGroupIOObject,
    NESymbolicLink, )



c_RenamableTypes = (    
    NENodeObject,
    NEGroupObject,
    NESymbolicLink, )



c_EditableTypes = (
    NENodeObject,
    NEGroupObject,
    NEGroupIOObject, )





class NENodeGraph():

    def __init__( self ):

        self.__m_Root = NERootObject( 'Root' )
        self.__m_KeyMap = KeyMap( self.__m_Root )
        self.__m_IDMap = { self.__m_Root.ID(): self.__m_Root }

        self.__m_Pipeline = Pipeline()



    def __del__( self ):
        print( 'NENodeGraph::__del__()...' )
        self.Release()



    def Init( self ):
        self.__m_KeyMap.Release()
        self.__m_IDMap.clear()
        self.__m_Root.Release()

        self.__m_KeyMap.Add(self.__m_Root)
        self.__m_IDMap[ self.__m_Root.ID() ] = self.__m_Root

        self.__m_Pipeline.Clear()



    def Release( self ):
        self.__m_KeyMap.Release()
        self.__m_IDMap.clear()

        self.__m_Root.Release()

        self.__m_Pipeline.Release()



    def GetRoot( self ):
        return self.__m_Root



    def GetRootID( self ):
        return self.__m_Root.ID()



    #########################################################################
    #               Object Create/Delete Operation(public func)             #
    #########################################################################

    def AddNode( self, nodeDesc, computeFunc, pos, size, name, object_id, attrib_ids, parent_id ):
        try:
            newNode = self.__AddNodeToScene( nodeDesc, pos, size, name, object_id, attrib_ids, parent_id )

            # Allocate DataBlock
            dataBuffer = self.__m_Pipeline.AllocateDataBlock( newNode.GetDesc() )
        
            for attrib in newNode.InputAttributes().values():
                data = dataBuffer.Inputs()[ attrib.ID() ]
                attrib.BindData(data)

            for attrib in newNode.OutputAttributes().values():
                data = dataBuffer.Outputs()[ attrib.ID() ]
                attrib.BindData(data)

            # Register Compute Func
            self.__m_Pipeline.RegisterComputeFunc( newNode.ID(), computeFunc )

            return newNode

        except:
            traceback.print_exc()
            return None


    
    def RenameByID( self, obj_id, newname_temp ):
        try:
            obj = self.__m_IDMap[ obj_id ]
            if( not type(obj) in c_RenamableTypes ):
                return newname_temp, None 

            new_name_candidate = newname_temp.replace('.', '_') # convert irregal character'.' to '_'
            prev_name = obj.Key()
            
            # Check if rename is required or not
            if( prev_name==new_name_candidate ):
                print( 'name unchanged. exiting.' )
                return prev_name, prev_name

            # Generate new unique name
            parentfullkey = self.__m_IDMap[obj_id].Parent().FullKey('|')
            new_name = self.__ResolveKeyConflict( parentfullkey + new_name_candidate ).replace( parentfullkey, '' )
            #new_name = self.__ResolveKeyConflict( new_name_candidate )# and publish available name

            # Rename Object
            if( isinstance(obj, NESymbolicLink) ):
                obj.Parent().RenameAttribute( obj.ExposedAttribute().ID(), new_name )
            else:
                obj.SetKey( new_name )

            # Update Keymap
            self.__m_KeyMap.Rename( obj_id, prev_name, new_name )
            
            return new_name, prev_name

        except:
            traceback.print_exc()
            return newname_temp, None



    def RenameAttributeByID( self, attrib_id, newname_temp ):
        try:
            new_name = newname_temp.replace('.', '_') # convert irregal character'.' to '_'

            #========= Check if renamable =================#
            parent = self.__m_IDMap[ attrib_id[0] ]
            attrib = parent.AttributeByID( attrib_id[1] )
            prev_name = attrib.ParentKey() if isinstance(parent,NEGroupObject) else attrib.Key()

            if( prev_name==new_name ):
                print( 'name unchanged. exiting.' )
                return prev_name, prev_name

            # Rename Attribute
            parent.RenameAttribute( attrib_id[1], new_name )
            
            # Update Keymap if symboliclink
            if( isinstance(parent,NEGroupObject) ):
                self.__m_KeyMap.Rename( attrib.Parent().ID(), prev_name, new_name )

            return new_name, prev_name

        except:
            traceback.print_exc()
            return newname_temp, None



    def AddConnectionByID( self, attrib1_id, attrib2_id, object_id=None ):
        try:
            # Get Attribute
            attrib1 = self.GetAttributeByID( attrib1_id )
            attrib2 = self.GetAttributeByID( attrib2_id )

            source_attrib, dest_attrib = (attrib1, attrib2) if attrib1.IsOutputFlow() else (attrib2, attrib1)

            print( 'AddConnectionByID:', source_attrib.FullKey() + ' <---> ' + dest_attrib.FullKey() )

            # Create Connection Object
            newConn = self.__AddConnectionToScene( source_attrib, dest_attrib, object_id )

            # Connect NEData Reference
            source_data = source_attrib.Data()
            dest_data = dest_attrib.Data()
            source_data.BindReference( dest_data )
            dest_data.BindReference( source_data )

            # Propagate Dirty Flag to Destination Attribute(s).
            self.__m_Pipeline.PropagateDirty( dest_attrib.ParentID() )

            # Lock Destination Attribute
            dest_attrib.SetEnable( False )

            return newConn

        except:
            traceback.print_exc()
            return None



    def SetAttributeByID( self, attrib_id, value ):

        attrib = self.GetAttributeByID( attrib_id )
        if( attrib==None ):
            return None

        prev_val = attrib.Value()
        attrib.SetValue( value )

        # Execute Dirty Propagation.
        self.__m_Pipeline.PropagateDirty( attrib_id[0] )

        return prev_val
    


    def LockAttributeByID( self, attrib_id, state ):

        attrib = self.GetAttributeByID( attrib_id )
        if( attrib==None ):
            return None

        prev_state = attrib.Enabled()
        attrib.SetEnable( state )

        return prev_state



    def RemoveConnectionByID( self, conn_id ):

        if( not conn_id in self.__m_IDMap ):
            print( 'Connection object(' + str(conn_id) + ') does not exist on NodeGraph' )
            return None
        
        conn = self.__m_IDMap[ conn_id ]

        print( 'NENodeGraph::RemoveConnectionByID()...', conn.Source().FullKey(), ' <---> ', conn.Destination().FullKey() )

        source_attrib = conn.Source()
        dest_attrib = conn.Destination()

        # Remove connection from scene
        self.__RemoveConnectionFromScene( conn )
        
        # Disconnect NEData Reference
        source_data = source_attrib.Data()
        dest_data = dest_attrib.Data()
        source_data.UnbindReference( dest_data )
        dest_data.UnbindReference( source_data )
        
        # Propagate Dirty Flag to Destination Attribute(s).
        self.__m_Pipeline.PropagateDirty( dest_attrib.ParentID() )

        if( dest_attrib.HasConnections()==False ):
            dest_attrib.SetEnable(True)
            return dest_attrib.AttributeID()

        else:
            return None



    def ReconnectByID( self, conn_id, attrib1_id, attrib2_id ):
        try:
            conn = self.__m_IDMap[ conn_id ]
            prev_src_attrib_id = conn.Source().AttributeID()
            prev_dest_attrib_id = conn.Destination().AttributeID()
            prev_parent_id = conn.ParentID()

            ###################### Disconnect ########################
            # *---conn---*
            curr_source_attrib = conn.Source()
            curr_dest_attrib = conn.Destination()

            # Break source's attrib-connection link  x---conn---*
            curr_source_attrib.UnbindConnection( conn )
            conn.UnbindSource()

            # Break destination's attrib-connection link x---conn---x
            curr_dest_attrib.UnbindConnection( conn )
            conn.UnbindDestination()
            
            # Disconnect NEData Reference
            curr_source_data = curr_source_attrib.Data()
            curr_dest_data = curr_dest_attrib.Data()
            curr_source_data.UnbindReference( curr_dest_data )
            curr_dest_data.UnbindReference( curr_source_data )

            # Propagate Dirty Flag to Destination Attribute(s).
            self.__m_Pipeline.PropagateDirty( curr_dest_attrib.ParentID() )


            ##################### Reconnect ##########################
            # Get New Attribute
            attrib1 = self.GetAttributeByID( attrib1_id )
            attrib2 = self.GetAttributeByID( attrib2_id )
            new_source_attrib, new_dest_attrib = (attrib1, attrib2) if attrib1.IsOutputFlow() else (attrib2, attrib1)

            # Establish source's attrib-connection link
            new_source_attrib.BindConnection( conn )
            conn.BindSource( new_source_attrib )

            # Establish dest's attrib-connection link
            new_dest_attrib.BindConnection( conn )
            conn.BindDestination( new_dest_attrib )

            # Set parent space
            new_source_attrib.ParentSpace().AddMember( conn )

            # Connect NEData
            new_source_data = new_source_attrib.Data()
            new_dest_data = new_dest_attrib.Data()
            new_source_data.BindReference( new_dest_data )
            new_dest_data.BindReference( new_source_data )

            # Propagate Dirty Flag to Destination Attribute(s).
            self.__m_Pipeline.PropagateDirty( new_dest_attrib.ParentID() )

            # Update connected ObjectTypes if needed.
            if( new_source_attrib.Parent().ObjectType()=='InputSymbolicLink' ):
                conn.SetObjectType( 'InputSymbolicLinkConnection' )
            elif( new_dest_attrib.Parent().ObjectType()=='OutputSymbolicLink' ):
                conn.SetObjectType( 'OutputSymbolicLinkConnection' )
            else:
                conn.SetObjectType( 'Connection' )

            return conn

        except:
            traceback.print_exc()
            return None



    def RemoveNodeByID( self, node_id ):
        # Remove
        self.__RemoveNodeFromScene( self.__m_IDMap[ node_id ] )

        # Remove Datablock
        self.__m_Pipeline.ReleaseDataBlock( node_id )
        self.__m_Pipeline.ReleaseComputeFunc( node_id )



    def GetConnectionIDByAttribute( self, attribkey1, attribkey2 ):
        try:
            attrib1 = self.GetAttribute( attribkey1 )
            attrib2 = self.GetAttribute( attribkey2 )
            conns = list( set(attrib1.Connections().values()) & set(attrib2.Connections().values()) )

            return conns[0].ID()

        except:
            traceback.print_exc()
            return None



    def GetAttribute( self, name ):

        # Extract nodename and attrname
        name_components = name.split( '.', 1 )
        if( len(name_components)<=1 ):
            print( 'NENodeGraph::GetAttribute()...Cannot get attribute: Invalid name. ')
            return None

        nodename = name_components[0]
        attrname = name_components[1]

        # retrieve node
        node = self.__m_KeyMap.GetObject( nodename )
        if( node == None ):
            print( 'NENodeGraph::GetAttribute()...Cannot get attribute: Node ' + nodename + ' does not exist.' )
            return None
        
        # return node attribute
        return node.AttributeByName( attrname )



    def GetAttributeID( self, name ):

        # Extract nodename and attrname
        name_components = name.split( '.', 1 )
        if( len(name_components)<=1 ):
            print( 'NENodeGraph::GetAttributeID()...Cannot get attribute: Invalid name. ')
            return None

        nodename = name_components[0]
        attrname = name_components[1]

        # retrieve node
        node = self.__m_KeyMap.GetObject( nodename )
        if( node == None ):
            print( 'NENodeGraph::GetAttributeID()...Cannot get attribute: Node ' + nodename + ' does not exist.' )
            return None
        
        # retrieve attribute
        attrib = node.AttributeByName( attrname )
        if( attrib == None ):
            print( 'NENodeGraph::GetAttributeID()...Cannot get attribute: Attribute ' + attrname + ' does not exist.' )
            return None

        # return node attribute
        return attrib.GetDesc().ObjectID()



    def GetAttributeByID( self, attrib_id ):# attrib_id must be touple. [0]: node/group's object_id, [1]: attribute's object_id
        try:
            return self.__m_IDMap[ attrib_id[0] ].AttributeByID( attrib_id[1] )
        except:
            traceback.print_exc()
            #print( 'NENodeGraph::GetAttributeByID()...Cannot get attribute: ', attrib_id, ' does not exist.' )
            return None



    def GetSymbolocLinkInitialParams( self, attrib_id ):
        try:
            attrib = self.GetAttributeByID( attrib_id )
            if( attrib==None ):
                return None

            return attrib.ParentNode().ParentID(), attrib.GetDesc(), attrib.Value(), attrib.Key()

        except:
            traceback.print_exc()
            return None



    def ExistsByID( self, object_id, object_types=( NENodeObject, NEGroupObject, NEGroupIOObject, NESymbolicLink, NEConnectionObject ) ):

        if( not object_id in self.__m_IDMap ): # Object does not exist -> False
            return False

        if( type(self.__m_IDMap[object_id]) in object_types ):# Matched object matches to specified types -> True
            return True

        return False # Object found. but type mismatch -> False



    def GetSymbolicLinkByAttributeID( self, attrib_id ):
        try:
            attrib_list = self.__m_IDMap[ attrib_id[0] ].AttributeByID( attrib_id[1] ).GetConnectedAttributes()
            attrib = next( (attr for attr in attrib_list if isinstance( attr.Parent(), NESymbolicLink ) ), None )
            return attrib.Parent()
        except:
            traceback.print_exc()
            return None



    def ExtractSymbolicLinkConnections( self, object_id ):
        try:
            obj = self.__m_IDMap[object_id]
            return obj.ExtractConnections() if isinstance(obj, NESymbolicLink) else None

        except:
            traceback.print_exc()
            return None



    def GetGroupIOIDs( self, group_id ):
        try:
            return self.__m_IDMap[ group_id ].GroupIOIDs()

        except:
            traceback.print_exc()
            return []



    def GetObjectByID( self, obj_id, typefilter ):
        try:
            obj = self.__m_IDMap[ obj_id ]
            return obj if type(obj) in typefilter else None
        except:
            traceback.print_exc()
            return None



    def GetObjectByName( self, name, typefilter ):
        try:
            obj = self.__m_KeyMap.GetObject(name)
            return obj if type(obj) in typefilter else None
        except:
            traceback.print_exc()
            return None



    def GetObjectID( self, name, typefilter ):
        try:
            obj = self.__m_KeyMap.GetObject(name)
            return obj.ID() if type(obj) in typefilter else None
        except:
            traceback.print_exc()
            return None



    def GetObjectTypeByID( self, obj_id ):
        return type(self.__m_IDMap[ obj_id ]) if obj_id in self.__m_IDMap else None



    def GetParentID( self, object_id ):
        try:
            return self.__m_IDMap[ object_id ].ParentID()

        except:
            traceback.print_exc()
            return None




    def AddGroup( self, pos, size, name, object_id, parent_id ):
        newGroup = self.__AddGroupToScene( pos, size, name, object_id, parent_id )
        return newGroup



    def RemoveGroupByID( self, node_id ):
        # Get node
        if( not node_id in self.__m_IDMap ):
            print( 'NENodeGraph::RemoveGroupByID()...Node does not exist' )
            return False
        # Remove
        self.__RemoveGroupFromScene( self.__m_IDMap[ node_id ] )

        return True



    def TranslateByID( self, object_id, translate, relative ):

        if( not object_id in self.__m_IDMap ):
            return None

        prev_pos = self.__m_IDMap[ object_id ].GetPosition()
        new_pos = ( translate[0] + prev_pos[0] * float(relative), translate[1] + prev_pos[1] * float(relative) )
        self.__m_IDMap[ object_id ].SetTranslation( new_pos )

        return ( new_pos[0]-prev_pos[0], new_pos[1]-prev_pos[1] )



    def SetVisibleByID( self, object_id, flag ):

        if( not object_id in self.__m_IDMap ):
            return None

        prev_flag = self.__m_IDMap[ object_id ].Visibility()
        self.__m_IDMap[ object_id ].SetVisible( flag )

        return prev_flag



    def ParentByID( self, object_id, parent_id ):
        
        try:
            print('NENodeGraph::ParentByID()...Parenting %s to %s' % (self.__m_IDMap[object_id].Key(), self.__m_IDMap[parent_id].Key()) )

            # Remove from current parent.
            prev_parent_id = self.__m_IDMap[object_id].ParentID()
            self.__UpdateTransform( prev_parent_id )# Update relevant transform matrices
            self.__m_IDMap[prev_parent_id].RemoveMember( object_id )

            # Add to new parent
            self.__UpdateTransform( parent_id )# Update relevant transform matrices
            self.__m_IDMap[parent_id].AddMember( self.__m_IDMap[object_id] )
            
            #return prev_parent_id, self.__m_IDMap[object_id].GetPosition()# RemoveMemberの影響で位置座標がワールド空間に戻っている
            return self.__m_IDMap[object_id]

        except:
            traceback.print_exc()
            return None, (0, 0)



    def ActivateSymbolicLinkByID( self, group_id, attribdesc, value, name, symboliclink_idset, slot_index=-1 ):

        try:
            #print( 'NENodeGraph::ActivateSymbolicLinkByID()...' )

            # Create SymbolicLink
            parent = self.__m_IDMap[ group_id ]
            symboliclink = self.__AddSymbolicLinkToScene( parent, attribdesc, value, name, symboliclink_idset )
            parent.BindSymbolicLink( symboliclink, slot_index )
            
            # Allocate DataBlock
            dataBuffer = self.__m_Pipeline.AllocateDataBlock( symboliclink.GetDesc() )
        
            for attrib in symboliclink.InputAttributes().values():
                data = dataBuffer.Inputs()[ attrib.ID() ]
                attrib.BindData(data)

            for attrib in symboliclink.OutputAttributes().values():
                data = dataBuffer.Outputs()[ attrib.ID() ]
                attrib.BindData(data)
           
            # Register Compute Func
            self.__m_Pipeline.RegisterComputeFunc( symboliclink.ID(), None )

            return symboliclink

        except:
            traceback.print_exc()
            return None



    def DeactivateSymbolicLinkByID( self, symboliclink_id ):
        try:
            symboliclink = self.GetObjectByID( symboliclink_id, (NESymbolicLink,) )
            parent = symboliclink.Parent()

            # Unparent Symboliclink
            if( isinstance(parent, NEGroupObject) ):
                parent.UnbindSymbolicLink( symboliclink )
        
            # Remove SymbolicLink from Scene
            self.__RemoveSymbolicLinkFromScene( symboliclink )

            # Remove Datablock
            self.__m_Pipeline.ReleaseDataBlock( symboliclink_id )
            self.__m_Pipeline.ReleaseComputeFunc( symboliclink_id )

        except:
            traceback.print_exc()


        
    def SetSymbolicLinkSlotIndexByID( self, symboliclink_id, index ):
        try:
            symboliclink = self.GetObjectByID( symboliclink_id, (NESymbolicLink,) )
            parent = symboliclink.Parent()
            
            prev_index = symboliclink.SlotIndex()
            parent.SetSymbolicLinkSlotIndex( symboliclink, index )

            return prev_index

        except:
            traceback.print_exc()
            return None



    def CreateGroupIO( self, dataflow, pos, group_id, object_id ):
        try:
            groupIO = self.__AddGroupIOToScene( dataflow, pos, group_id, object_id )
            return groupIO
        except:
            traceback.print_exc()
            return None



    def RemoveGroupIOByID( self, object_id ):
        # Get GroupIO
        if( not object_id in self.__m_IDMap ):
            print( 'NENodeGraph::RemoveGroupIOByID()...GroupIO does not exist' )
            return False
        # Remove
        self.__RemoveGroupIOFromScene( self.__m_IDMap[ object_id ] )

        return True



    def GetConnectionIDs( self, node_id ):
        try:
            conn_id_list = []

            node = self.GetObjectByID( node_id, ( NENodeObject, NEGroupObject, NESymbolicLink, NEGroupIOObject, ) )
            if( node==None ):
                return conn_list

            for attrib in node.Attributes().values():
                conn_id_list += attrib.ConnectionIDs()#list(attrib.Connections().values())#[ v.ID() for v in attrib.Connections().values() ]

            return set(conn_id_list)

        except:
            return []



    def GetAttribConnectionIDs( self, attrib_id ):
        try:
            attrib = self.__m_IDMap[ attrib_id[0] ].AttributeByID( attrib_id[1] )
            return attrib.ConnectionIDs()

        except:
            traceback.print_exc()
            return []


    def IsConnectedByID( self, attrib_id1, attrib_id2 ):

        attrib1 = self.GetAttributeByID( attrib_id1 )
        attrib2 = self.GetAttributeByID( attrib_id2 )

        if( attrib1==None or attrib2==None ):
            return False

        return attrib2.IsConnected( attrib1 )



    def IsConnectableByID( self, attrib_id1, attrib_id2, checkloop=False ):

        attrib1 = self.GetAttributeByID( attrib_id1 )
        attrib2 = self.GetAttributeByID( attrib_id2 )

        if( attrib1==None or attrib2==None ):
            return False

        attrib_source, attrib_dest = (attrib1, attrib2) if attrib1.IsOutputFlow() else (attrib2, attrib1)

        # Check Connectivity
        if( attrib_source.IsConnectable( attrib_dest )==False ):
            return False

        # Check existing connection
        if( attrib_source.IsConnectedTo( attrib_dest )==True ):
            return False

        if( checkloop ):
            return self.__m_Pipeline.CheckLoop( { attrib_source.ParentID():attrib_dest.ParentID() } )

        return True



    def IsLockedByID( self, attrib_id ):# Check if attribute connection is frozen(connection change forbidden)
        try:
            return self.GetAttributeByID( attrib_id ).IsLocked()
        except:
            traceback.print_exc()
            return False



    def CanBeSymbolized( self, attrib_id ):
        print( 'NENodeGraph::CanBeSymbolized()...' )
        attrib = self.GetAttributeByID( attrib_id )
        if( attrib==None ):
            return False

        parent = attrib.ParentSpace()
        if( not isinstance(parent,NEGroupObject) ):
            print( '    Unable to symbolize. Parent space must be Group...' )
            return False

        return parent.CanSymbolize( attrib )



    def PositionChanged( self, object_id, translate, relative ):

        if( not object_id in self.__m_IDMap ):
            return False

        prev_pos = self.__m_IDMap[ object_id ].GetPosition()
        new_pos = ( translate[0] + prev_pos[0] * float(relative), translate[1] + prev_pos[1] * float(relative) )
        
        if( new_pos==prev_pos ):
            return False

        return True



    def CollectAllDescendantIDsByID( self, node_id ):

        root_node = self.GetObjectByID( node_id, c_IDMapSupportTypes )

        if( root_node==None ):
            return None, None

        group_id_list = []
        node_id_list = []

        DepthFirstScan( root_node, group_id_list, node_id_list )

        return group_id_list, node_id_list



    def CollectOverlappedConnectionsByID( self, attrib_ids ):

        overlapped_conn_ids = []

        for attrib_id in attrib_ids:
            attrib = self.GetAttributeByID( attrib_id )

            if( attrib==None ): continue
            if( attrib.MultipleConnectAllowed()==True ): continue
            
            overlapped_conn_ids += attrib.ConnectionIDs()

        return overlapped_conn_ids



    def CollectConnections( self, obj_id_list, parent_id ):
        try:
            typefilter = (NENodeObject, NEGroupObject,)
            obj_list = [ self.__m_IDMap[object_id] for object_id in obj_id_list if type(self.__m_IDMap[object_id]) in typefilter ]
            grand_parent_id = self.__m_IDMap[parent_id].ParentID()# シンボリックリンク生成可能な親空間 

            # Gather all connections relevant to obj_id_list
            conn_dict = {}
            for obj in obj_list:
                for attrib in obj.Attributes().values():
                    conn_dict.update( attrib.Connections() )

            # Divide to open/closed category
            closed_conn_ids = []# connections between obj_id_list nodes
            open_attrib_info = defaultdict(list)# connection from external. attrib_in_ids[ attrib_id to symbolize ] = [ (conn_id, internal_attrib_id), ... ]
            removal_conn_info = []# connection to be removed while paranting operation.

            for conn_id, conn in conn_dict.items():
                src_is_internal = conn.Source().ParentNode().ID() in obj_id_list
                dst_is_internal = conn.Destination().ParentNode().ID() in obj_id_list
                
                if( src_is_internal and dst_is_internal ):# both attributes exist in obj_id_list
                    closed_conn_ids.append( conn_id )

                elif( conn.ParentID()==grand_parent_id ):
                    if( dst_is_internal ):# only dest attribute exists in obj_id_list -> input connection from external space
                        open_attrib_info[ conn.DestinationAttribID() ].append( (conn_id, conn.SourceAttribID()) )
                        removal_conn_info.append( conn_id )
                    else:# only dest attribute exists in obj_id_list -> input connection from external space
                        open_attrib_info[ conn.SourceAttribID() ].append( (conn_id, conn.DestinationAttribID()) )
                        removal_conn_info.append( conn_id )

                else:
                    removal_conn_info.append( conn_id )

            return closed_conn_ids, open_attrib_info, removal_conn_info

        except:
            traceback.print_exc()
            return {}, {}, []



    def GetGroupMemberIDs( self, group_id ):
        try:
            return self.__m_IDMap[ group_id ].GetMemberIDs()

        except:
            traceback.print_exc()
            return [], []
        


    def GetSymboliclinkIDs( self, group_id ):       
        symboliclink_id_list = []
        for groupio in self.__m_IDMap[ group_id ].GroupIOs():
            symboliclink_id_list += [ v.ID() for v in groupio.SymbolicLinks().values() ]

        return symboliclink_id_list



    def FilterObjects( self, obj_id_list, *, typefilter, parent_id ):
        try:
            # Filter by type only if typefilters is specified
            obj_ids_filtered = [ obj_id for obj_id in obj_id_list if type(self.__m_IDMap[obj_id]) in typefilter ] if typefilter else obj_id_list
        
            # Filter by parent space if parent_id is specified
            if( parent_id==None ):
                return obj_ids_filtered

            return [ obj_id for obj_id in obj_ids_filtered if self.__m_IDMap[obj_id].ParentID()==parent_id ]

        except:
            traceback.print_exc()
            return []



    def FilterDescendants( self, obj_id_list, parent_id ):
        try:
            direct_children = self.__m_IDMap[ parent_id ].Children()

            return [ obj_id for obj_id in obj_id_list if
                    ( type(self.__m_IDMap[obj_id]) in (NENodeObject, NEGroupObject) ) and    # include nodegraph and group only
                    ( self.IsAncestorOf(obj_id, parent_id) == False ) and                   # exclude parent_id's ancestors
                    ( obj_id != parent_id ) and                                              # exclude parent_id self
                    ( not obj_id in direct_children ) ]                                      # exclude parent_id's children

        except:
            traceback.print_exc()
            return []



    def GetCentroid( self, obj_id_list ):

        centroid = [0, 0]
        numobj = float(len(obj_id_list))

        for obj_id in obj_id_list:
            obj_pos = self.__m_IDMap[obj_id].GetPosition()
            centroid[0] += obj_pos[0]
            centroid[1] += obj_pos[1]

        num_inv = 1.0 / numobj if numobj else 0.0
        centroid[0] *= num_inv
        centroid[1] *= num_inv

        return centroid



    def IsValidNewName( self, object_id, name ):
        try:
            return  ( self.__m_IDMap[ object_id ].Key() != name ) and ( name )# and ( not name.isspace() )
        except:
            traceback.print_exc()
            return False



    def __ResolveNameConflict( self, obj_id ):
        obj_key = self.__m_IDMap[ obj_id ].FullKey()
        if( self.__m_KeyMap.IsAlreadyUsed( obj_key, [obj_id] ) ):
            parentfullkey = self.__m_IDMap[obj_id].Parent().FullKey('|')
            resolved_key = self.__ResolveKeyConflict( obj_key )
            return resolved_key.replace( parentfullkey, '' )

        return None



    def ResolveNameConflicts( self, obj_id_list ):
        rename_dict = {}
        for obj_id in obj_id_list:
            resolved_name = self.__ResolveNameConflict( obj_id )
            if( resolved_name ): rename_dict[ obj_id ] = resolved_name

        return rename_dict



    def __ResolveParentNameConflict( self, obj_id, parent_id ):
        parentfullkey = self.__m_IDMap[parent_id].FullKey('|')
        parentedkey = parentfullkey + self.__m_IDMap[ obj_id ].Key()
        if( self.__m_KeyMap.IsAlreadyUsed( parentedkey, [obj_id] ) ):
            producedkey = self.__ResolveKeyConflict( parentedkey )
            return producedkey.replace( parentfullkey, '' )

        return None



    def ResolveParentNameConflicts( self, obj_id_list, parent_id ):
        rename_dict = {}
        parent = self.__m_IDMap[parent_id]
        for obj_id in obj_id_list:
            resolved_name = self.__ResolveParentNameConflict( obj_id, parent_id )
            if( resolved_name ): rename_dict[ obj_id ] = resolved_name

        return rename_dict



    def __ResolveUnparentNameConflict( self, obj_id ):
        obj = self.__m_IDMap[ obj_id ]
        if( not type(obj) in c_RenamableTypes ):
            return None

        parentfullkey = obj.Parent().Parent().FullKey('|')
        unparentedkey = parentfullkey + obj.Key()
        if( self.__m_KeyMap.IsAlreadyUsed( unparentedkey, [obj_id] ) ):
            producedkey = self.__ResolveKeyConflict( unparentedkey )
            return producedkey.replace( parentfullkey, '' )

        return None



    def ResolveUnparentNameConflicts( self, group_id ):
        
        rename_dict = {}

        group = self.GetObjectByID( group_id, (NEGroupObject,) )
        if( group is None ):
            return rename_dict

        obj_id_list = group.ChildrenID()
        for obj_id in obj_id_list:
            resolved_name = self.__ResolveUnparentNameConflict( obj_id )
            if( resolved_name ): rename_dict[ obj_id ] = resolved_name

        return rename_dict



    def ValidateVisibilityUpdate( self, object_id, visibility ):
        try:
            obj = self.__m_IDMap[ object_id ]
            if( isinstance(obj, NEGraphObject)==False ):
                return False
            if( obj.Visibility()==visibility ):
                return False

            return True

        except:
            traceback.print_exc()
            return False



    def ValidateAttributeUpdate( self, attrib_id, new_value ):
        try:
            attrib = self.GetAttributeByID( attrib_id )

            if( attrib==None ):# check if attribute exisits
                return False

            old_value = attrib.Value()
            if( old_value==new_value ):# check if value needs to be updated
                return False

            return True

        except:
            traceback.print_exc()
            return False



    def ValidateSymboliclinkUpdate( self, object_id, new_slot ):
        try:
            obj = self.GetObjectByID( object_id, (NESymbolicLink,) )            
            return new_slot!=obj.SlotIndex() if obj else None

        except:
            traceback.print_exc()
            return False



    def CheckGraph( self ):
        return self.__m_Pipeline.CheckLoop()



    def Evaluate( self, object_id ):
        self.__m_IDMap[ object_id].Info()

        return self.__m_Pipeline.Evaluate( object_id )



    def GetSnapshot( self, object_id ):
        try:
            return self.__m_IDMap[ object_id ].GetSnapshot()
        except:
            traceback.print_exc()
            return None



    # check if ancestor_id is ancestor of object_id
    def IsAncestorOf( self, ancestor_id, object_id ):
        try:
            #print( 'NENodeGraph::IsAncestorOf()...' )
            root_id = self.__m_Root.ID()
            curr_id = self.__m_IDMap[ object_id ].ParentID()

            while( curr_id != root_id ):
                if( curr_id == ancestor_id ):
                    return True
                curr_id = self.__m_IDMap[ curr_id ].ParentID()

            return False

        except:
            traceback.print_exc()
            return False



    # check if object_id is descendant of descendant_id
    def IsDescendantOf( self, object_id, descendant_id ):
        return self.IsAncestorOf( descendant_id, object_id )




    #########################################################################
    #               Object Create/Delete Operation(private func)            #
    #########################################################################


    def __AddConnectionToScene( self, source_attrib, dest_attrib, object_id=None ):
        
        connectionType = 'Connection'
        if( source_attrib.ObjectType()=='ProtectedSymbolicLink' ):
            connectionType ='InputSymbolicLinkConnection'
        elif( dest_attrib.ObjectType()=='ProtectedSymbolicLink' ):
            connectionType = 'OutputSymbolicLinkConnection'

        # Create connection object and assing uuid-based unique name
        conn = NEConnectionObject( connectionType, object_id )
        #conn.SetKey( 'connector_' + str(conn.ID()) )

        # Add connection to scene
        source_attrib.ParentSpace().AddMember( conn )
        # Add to IDMap
        self.__m_IDMap[ conn.ID() ] = conn

        # Add attrib-to-connection link
        source_attrib.BindConnection( conn )
        # Add connection-to-attrib link
        conn.BindSource( source_attrib )

        # Add attrib-to-connection link
        dest_attrib.BindConnection( conn )
        # Add connection-to-attrib link
        conn.BindDestination( dest_attrib )

        return conn



    def __AddNodeToScene( self, nodeDesc, pos, size, name=None, object_id=None, attrib_ids=None, parent_id=None ):

        nodeType = nodeDesc.ObjectType()
        parent = self.__m_IDMap[parent_id] if parent_id else self.__m_Root
        parent_name = parent.FullKey('|')

        # Publish unique name
        node_name = None
        if( name ):
            node_name = self.__ResolveKeyConflict( parent_name + name ).replace( parent_name, '' )
        else:
            idx = 1
            while( self.__m_KeyMap.IsAlreadyUsed( parent_name + nodeType + str(idx).zfill(3) ) ): idx += 1
            node_name = nodeType + str(idx).zfill(3)

        # Create node Object
        node = NENodeObject( node_name, nodeType, object_id )
        parent.AddMember( node )

        # Create Input Attributes
        for i, attribDesc in enumerate(nodeDesc.InputAttribDescs()):
            node.AddAttribute( attribDesc, attrib_ids[0][i] if attrib_ids else None )

        # Create Output Attributes
        for i, attribDesc in enumerate(nodeDesc.OutputAttribDescs()):
            node.AddAttribute( attribDesc, attrib_ids[1][i] if attrib_ids else None )

        # Set position and size
        node.SetTranslation( pos )
        node.SetSize( size )

        # Add Node to NodeGraph
        self.__m_KeyMap.Add( node )
        self.__m_IDMap[ node.ID() ] = node

        return node



    def __RemoveNodeFromScene( self, node ):
        # Remove from IDMap
        del self.__m_IDMap[ node.ID() ]

        # Remove KeyMap entry
        self.__m_KeyMap.Remove( node )

        # Remove node from root
        node.Release()
        del node



    def __AddGroupToScene( self, pos, size, name=None, object_id=None, parent_id=None ):

        parent = self.__m_IDMap[parent_id] if parent_id else self.__m_Root
        parent_name = parent.FullKey('|')

        # Publish unique name
        group_name = None
        if( name ):
            group_name = self.__ResolveKeyConflict( parent_name + name ).replace( parent_name, '' )
        else:
            idx = 1
            while( self.__m_KeyMap.IsAlreadyUsed( parent_name + 'Group' + str(idx).zfill(3) ) ): idx += 1
            group_name = 'Group' + str(idx).zfill(3)

        # Create group Object
        group = NEGroupObject( group_name, object_id )
        parent.AddMember( group )

        # Set position and size
        group.SetTranslation( pos )
        group.SetSize( size )

        # Add Node to NodeGraph
        self.__m_KeyMap.Add( group )
        self.__m_IDMap[ group.ID() ] = group

        return group



    def __RemoveGroupFromScene( self, group ):
        
        # Reassign children to group's parent
        group.UnbindAllSymbolicLinks()
        group.UngroupChildren()

        # Remove from IDMap
        del self.__m_IDMap[ group.ID() ]

        # Remove from KeyMap
        self.__m_KeyMap.Remove( group )

        # Remove SymbolicLinks from IDMap/KeyMap
        for groupio in group.GroupIOs():
            for linknode in groupio.SymbolicLinks().values():
                self.__m_KeyMap.Remove( linknode )
                del self.__m_IDMap[ linknode.ID() ]

        # release parent child relations
        group.Release()
        del group


        
    def __RemoveConnectionFromScene( self, conn ):

        conn_id = conn.ID()

        # Remove attrib-to-connection link
        conn.Source().UnbindConnection( conn )
        # Remove connection-to-attrib link
        conn.UnbindSource()

        # Remove attrib-to-connection link
        conn.Destination().UnbindConnection( conn )
        # Remove connection-to-attrib link
        conn.UnbindDestination()

        # Release parent child relations
        conn.Release()

        # Remove from IDMap
        del self.__m_IDMap[ conn_id ]



    def __AddSymbolicLinkToScene( self, group, attribdesc, value, name, symboliclink_idset ):

        parent_space =group
        parent_space_name = parent_space.FullKey('|')
        
        # Publish unique name
        symboliclink_name = self.__ResolveKeyConflict( parent_space_name + name if name else attribdesc.Name() ).replace( parent_space_name, '' )
        
        # Create Symboliclink
        nodeType = 'InputSymbolicLink' if  attribdesc.IsInputFlow() else 'OutputSymbolicLink'
        symboliclink = NESymbolicLink( symboliclink_name, nodeType, attribdesc, value, symboliclink_idset[0], (symboliclink_idset[1], symboliclink_idset[2]) )# localkey
        
        # Add Symboliclink to NodeGraph
        self.__m_KeyMap.Add( symboliclink )
        self.__m_IDMap[ symboliclink.ID() ] = symboliclink

        return symboliclink



    def __RemoveSymbolicLinkFromScene( self, symboliclink ):
        # Remove from IDMap
        del self.__m_IDMap[ symboliclink.ID() ]

        # Remove KeyMap entry
        self.__m_KeyMap.Remove( symboliclink )

        # Remove node from root
        symboliclink.Release()
        del symboliclink



    def __AddGroupIOToScene( self, dataflow, pos, group_id, object_id=None ):

        group = self.__m_IDMap[group_id]

        # Create GroupIO
        groupio = NEGroupIOObject( dataflow, object_id )# groupio_name, 
        group.AddMember( groupio )# Add GroupIO to NodeGraph
        groupio.SetTranslation( pos )# (0, 0) Set GroupIO's position to local-space origin.
        
        # Add GroupIO to NodeGraph
        self.__m_KeyMap.Add( groupio )
        self.__m_IDMap[ groupio.ID() ] = groupio

        return groupio



    def __RemoveGroupIOFromScene( self, groupio ):
        # Remove from IDMap
        del self.__m_IDMap[ groupio.ID() ]

        # Remove KeyMap entry
        self.__m_KeyMap.Remove( groupio )

        # Remove node from root
        groupio.Release()
        del groupio



    def __UpdateTransform( self, object_id ):
        try:
            obj = self.__m_IDMap[ object_id ]
            if( isinstance(obj,NERootObject) ):
                return

            #print( '//---------- NENodeGraph::__UpdateTransform()... ----------//' )
        
            # Gather parents to space_stack[ space, parent, grandparent... ]
            space_deque = deque()
            while( not isinstance(obj,NERootObject) ):
                space_deque.appendleft( obj )
                obj = obj.Parent()

            
            # Propagate transform update.
            for i, val in enumerate(space_deque):
                if( val.IsDirty() ):# If 'Dirty' ancestor found, propagate transform to descendants.
                    for j in range(i, len(space_deque)):
                        space_deque[j].UpdateTransform()
                    break

        except:
            traceback.print_exc()



    # Resolve UnderScore. currley must be fullpath
    def __ResolveKeyConflict( self, currkey ):

        newkey = currkey

        # Create group Object. publish unique name
        while( self.__m_KeyMap.IsAlreadyUsed(newkey) ):
            newkey += '_'

        return newkey




###### TODO: ツリー構造内ノード群を歯抜け選択した場合でも階層構造を維持してコピペしたい。そのためのスナップショット生成機能試験実装. #############

# https://www.geeksforgeeks.org/lca-n-ary-tree-constant-query-o1/


    @staticmethod
    def ConstructEulerDepth_rec( node, d, euler, depth, typefilter ):
    
        if( type(node) in typefilter ):
            euler.append( node.ID() )#(node.Key(), node.ID()) )
            depth.append( d )

        for child in node.Children().values():
            NENodeGraph.ConstructEulerDepth_rec( child, d+1, euler, depth, typefilter )
            if( type(child) in typefilter ):
                euler.append( node.ID() )#(node.Key(), node.ID()) )
                depth.append( d )



    @staticmethod
    def GetLowestCommonAncestor( euler, depth, obj_id_list ):

        # calculate depth search range using euler list
        indices = []
        for obj_id in obj_id_list:
            if( obj_id in euler ):
                indices.append( euler.index(obj_id) )
   
        # expand search range in order to check neighbors'(parent or child) euler distances.
        slice_min = min(indices) - 1
        slice_max = max(indices) + 1

        #print( depth )
        #print( indices )
        #print( slice_min, slice_max )

        partial_depth = depth[ slice_min:slice_max ]
        return partial_depth.index( min(partial_depth) ) + slice_min



    @staticmethod
    def GenerateTraverseOrder( euler, depth, idx_lca ):

        depth_lca = depth[idx_lca]
        
        # Lowest Common Ancestorよりも階層が深いノードだけ抽出する.
        euler_lca = []
        for i, elm in list(enumerate(euler)):
            if( depth[i] > depth_lca ):
                euler_lca.append( elm )

        # Euler Depth配列を線形探索し、重複要素を除去しつつ、親子階層の浅い順にtraverse_orderにオブジェクトIDを格納する
        traverse_order = []
        [ traverse_order.append(x) for x in euler_lca if not x in traverse_order ]
        return reversed(traverse_order)# traverse_orderを逆順にする(イテレータを返す)ことで、深度の深いオブジェクトから探索できるようにする



    @staticmethod
    def GenerateChildList( id_map, lca_id, obj_id_list ):

        descendants = defaultdict(list)# { ParentID:[ChildID, ...], ParentID:[ChildID, ...], ... }

        for curr_id in obj_id_list:
            if( not curr_id in descendants ):
                descendants[ curr_id ] = []

            while( curr_id != lca_id ):
                parent_id = id_map[curr_id].ParentID()
                if( curr_id in descendants[ parent_id ] ):# 既に登録済みの親子階層に到達した場合は終了.
                    break
                descendants[ parent_id ].append( curr_id )
                curr_id = parent_id                

        for obj_id, child_ids in descendants.items():
            print( 'descendants[ \'%s\' ] = [ ' % (id_map[obj_id].Key()), end='' )
            for child_id in child_ids:
                print( id_map[child_id].Key(), end=', ' )
            print( ']' )

        return descendants



    def PrepareSnapshot( self, obj_id_list ):

        typefilter =( NERootObject, NENodeObject, NEGroupObject )
        euler = []# object id list.(traverse order)
        depth = []#
        idx_lca = 0

        # Create euler depth list from entire nodegraph
        self.ConstructEulerDepth_rec( self.__m_Root, 0, euler, depth, typefilter )

        # Get Lowest Common Ancestors of obj_id_list
        idx_lca = self.GetLowestCommonAncestor( euler, depth, obj_id_list )
        
        # Generate Traverse Order
        iter_traverse_order = self.GenerateTraverseOrder( euler, depth, idx_lca )
        
        # Generate Children list
        descendants = self.GenerateChildList( self.__m_IDMap, euler[idx_lca], obj_id_list )

        # Generate Snapshot
        snapshot_gen_list = [ obj_id for obj_id in iter_traverse_order if obj_id in descendants ]# 処理終了後iter_traverse_orderは探索終わって使えなくなってるので注意

        print( 'EulerDepth: ' )
        #for i, obj_id in enumerate(euler):
        #    print( '    %s: %d' % ( self.__m_IDMap[obj_id].Key(), depth[i]) )

        for i in range(len(euler)):
            print( '    %s: %d' % ( self.__m_IDMap[euler[i]].Key(), depth[i]) )

        print( 'LowestCommonAncestor: %s' % self.__m_IDMap[ euler[idx_lca] ].Key() )

        print( 'SnapshotGenList: ' )
        for i, obj_id in enumerate( snapshot_gen_list ):
            print( '    [%d]: %s' % (i, self.__m_IDMap[obj_id].Key() ) )
            #for dec_id in descendants[obj_id]):
            #    print( '      - %s' % self.__m_IDMap[dec_id].Key() )

        return snapshot_gen_list, descendants



###########################################################################################