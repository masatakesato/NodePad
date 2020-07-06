from oreorelib.math import util as mathutil
#import oreorelib.ui.pyqt5.stylesheet as UIStyle

from ..component.neobject import *


class NEGraphObject(NEObject):

    def __init__( self, key, objtype, obj_id=None ):
        super(NEGraphObject, self).__init__( key, objtype, obj_id )

        self.__m_Parent = None
        self.__m_Children = {}

        self.__m_Visible = True
        self.__m_Position = mathutil.vector2(0, 0)#(0, 0)#pos# 親空間内での座標.
        self.__m_Size = [0, 0]# 表示図形の幅, 高さ
###################### TODO: Implement Transformation Matrix ########################
        self.__m_LocalTransform = mathutil.IdentityMat3()# Local transformation matrix of THIS object
        self.__m_DerivedTransform = mathutil.IdentityMat3()# Transform matrix accumulated from parent space.
#####################################################################################



    def Release( self ):
        self.SetParent(None)
        self.ClearChildren()
        mathutil.SetVec2( self.__m_Position, 0.0, 0.0 )#self.__m_Position = (0.0, 0.0)
###################### TODO: Implement Transformation Matrix ########################
        mathutil.SetIdentityMat3( self.__m_LocalTransform )
        mathutil.SetIdentityMat3( self.__m_DerivedTransform )
#####################################################################################



    def NumChildren( self ):
        return len( self.__m_Children )



    def Child( self, id ):
        try:
            return self.__m_Children[id]
        except:
            return None



    def Children( self ):
        return self.__m_Children



    def ChildrenID( self ):
        #return [ v.ID for v in self.__m_Children.values() ]
        return list(self.__m_Children.keys())# dictのキー値にID使ってるのでこれで大丈夫



    def HasChildren( self ):
        return bool(self.__m_Children)



    def HasKey( self, key ):
        return key in self.__m_Children



    def ClearChildren( self ):

        for child in list(self.Children().values())[:]:
            if( child.HasChildren() ):  child.ClearChildren()

        #print( self.Key() + '.ClearChildren()...' )
        self.SetParent(None)
        self.__m_Children.clear()



    def Parent( self ):
        return self.__m_Parent



    def ParentID( self ):
        return self.__m_Parent._NEObject__m_ID



    def ParentKey( self ):
        return self.__m_Parent._NEObject__m_Key



    def SetParent( self, parent, bRegisterAsChild=True ):
        if( self.__m_Parent ):
            self.__m_Parent.__PopChild( self._NEObject__m_ID )

        self.__m_Parent = parent
        if( self.__m_Parent and bRegisterAsChild ):
            self.__m_Parent.__AddChild( self )
###################### TODO: Implement Transformation Matrix ########################
            self.__m_DerivedTransform = self.__m_LocalTransform * self.__m_Parent.__m_DerivedTransform
#####################################################################################



    def FullKey( self, suffix='' ):
        if( self.__m_Parent ):
            return self.__m_Parent.FullKey('.') + self._NEObject__m_Key + suffix
        else:
            return self._NEObject__m_Key + suffix



    def GetPosition( self ):
        return ( self.__m_Position[0], self.__m_Position[1] )



    def SetTranslation( self, pos ):
        mathutil.SetVec2( self.__m_Position, pos[0], pos[1] )
        #self.__m_Position = pos
###################### TODO: Implement Transformation Matrix ########################
        mathutil.SetTranslateMat3( self.__m_LocalTransform, pos[0], pos[1] )
        self.__m_DerivedTransform = self.__m_LocalTransform * self.__m_Parent.__m_DerivedTransform
#####################################################################################




####################### TODO: Implement Size parameters #############################

    def SetSize( self, size ):
        self.__m_Size = size



    def GetSize( self ):
        return self.__m_Size



    #def GetWidth( self ):
    #    return self.__m_Size[0]



    #def SetWidth( self, value ):
    #    self.__m_Size[0] = value



    #def GetHeight( self ):
    #    return self.__m_Size[1]



    #def SetHeight( self, value ):
    #    self.__m_Size[1] = value

#####################################################################################



    def SetVisible( self, flag ):
        self.__m_Visible = flag



    def Visibility( self ):
        return self.__m_Visible



    def GetDesc( self ):
        return None



    def Info( self ):
        print( 'ObjectType: ', self._NEObject__m_ObjectType )
        print(self.FullKey())



    def CollectAllDescendants( self ):
        obj_list = []
        self.__DepthFirstScan( self, obj_list )
        return obj_list



    def GetSnapshot( self ):
        return None # Override at subclass.



    def __AddChild( self, child ):
        self.__m_Children[ child._NEObject__m_ID ] = child
        child.__m_Parent = self



    def __PopChild( self, key ):# key指定した子供をリストから除外する
        if( key in self.__m_Children ):
            child = self.__m_Children.pop( key )
            child.__m_Parent = None
            return child

        return None



    def __DepthFirstScan( self, obj, obj_list ):
        obj_list.append( obj )
        for child in obj.Children().values():
            self.__DepthFirstScan( child, obj_list )