from .negraphobject import NEGraphObject




class NERootObject(NEGraphObject):

    def __init__( self, name, obj_id=None ):
        super(NERootObject, self).__init__( name, 'Root', obj_id=obj_id )



    def Release( self ):
        super(NERootObject, self).Release()



    def Parent( self ):
        return None



    def ParentID( self ):
        return self.ID()



    def SetParent( self, parent ):
        pass



    def Key( self ):
        return ''



    def FullKey( self, prefix='', suffix='' ):
        return ''



    def AddMember( self, obj ):
        obj.SetParent(self)

        #if( not isinstance(obj, NEConnectionObject) ):# ルートノードの位置は常にゼロ. 座標変換の必要なし
        #    obj_pos = obj.GetPosition()
        #    obj.SetTranslation( ( obj_pos[0]-self._NEGraphObject__m_Position[0], obj_pos[1]-self._NEGraphObject__m_Position[1] ) )
        


    def RemoveMember( self, obj_id ):
        obj = self.Child(obj_id)
        obj.SetParent(None)

        #obj_pos = obj.GetPosition()# ルートノードの位置は常にゼロ. 座標変換の必要なし
        #obj.SetTranslation( ( obj_pos[0]+self._NEGraphObject__m_Position[0], obj_pos[1]+self._NEGraphObject__m_Position[1] ) )



    #def AddMembers( self, obj_list ):
    #    for obj in obj_list:
    #        obj.SetParent(self)



    # Override NEGraphObject::UpdateTransform.
    def UpdateTransform( self ):
        print( 'NERootObject::UpdateTransform()...DoNothing' )
        pass# Root node doesn't need transform update.