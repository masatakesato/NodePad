import queue
import traceback
import functools
from collections import defaultdict


from ..component.descriptors import *
from ..component.nedata import NEData
from ..component.nedatabuffer import NEDataBuffer
from ..component.nedatablock import NEDataBlock




def ComputePassThrough( dataBlock ):
    in0 = dataBlock.GetInput(0)
    print( 'ComputePassThrough()...', in0 )
    dataBlock.SetOutput( 0, dataBlock.GetInput(0) )





class Pipeline():

    def __init__( self ):
        self.__m_DataBlockArray = {}# key: node/symboliclink's ID. value: NEDataBlock instance.
        self.__m_DataBufferArray = {}# key: node/symboliclink's ID. value: NEDataBuffer instance.
        self.__m_ComputeFuncArray = {}# key: node/symboliclink's ID. value: reference to Plugin's Compute() function


    def Release( self ):
        self.__m_DataBlockArray.clear()
        self.__m_DataBufferArray.clear()
        self.__m_ComputeFuncArray .clear()


    def Clear( self ):
        self.__m_DataBlockArray.clear()
        self.__m_DataBufferArray.clear()
        self.__m_ComputeFuncArray .clear()


    def IsEvaluable( self, object_id ):
        return object_id in self.__m_DataBufferArray


    def AllocateDataBlock( self, nodeDesc ):

        object_id = nodeDesc.ObjectID()

        #print( 'Pipeline::AllocateDataBlock(', object_id, ')' )

        #=============== Allocate Databuffer =================#
        self.__m_DataBufferArray[ object_id ] = NEDataBuffer()
        refDataBuffer = self.__m_DataBufferArray[ object_id ]

        # Allocate Input/Output Attribute data
        for attribDesc in nodeDesc.InputAttribDescs():
            refDataBuffer.AllocateInput( attribDesc )

        for attribDesc in nodeDesc.OutputAttribDescs():
            refDataBuffer.AllocateOutput( attribDesc )
        
        #=============== Allocate NEDataBlock ================#
        self.__m_DataBlockArray[ object_id ] = NEDataBlock( refDataBuffer )
        
        return refDataBuffer


    def ReleaseDataBlock( self, object_id ):
        try:
            #print( 'Pipeline::ReleaseDataBlock(', object_id, ')' )

            self.__m_DataBlockArray[ object_id ].Release()
            del self.__m_DataBlockArray[ object_id ]

            self.__m_DataBufferArray[ object_id ].Release()
            del self.__m_DataBufferArray[ object_id ]

            #del self.__m_ComputeFuncArray [ object_id ]

        except:
            traceback.print_exc()



    #def Connect( self, srcattrib_id, dstattrib_id ):

    #    data1 = self.__m_DataBufferArray[ srcattrib_id[0] ].Output[ srcattrib_id[1] ]
    #    data2 = self.__m_DataBufferArray[ srcattrib_id[0] ].Input[ srcattrib_id[1] ]

    #    data1.BindReference( data2 )
    #    data2.BindReference( data1 )
        

    def RegisterComputeFunc( self, object_id, callback ):

        if( callback==None ):
            self.__m_ComputeFuncArray[ object_id ] = functools.partial( ComputePassThrough, dataBlock=self.__m_DataBlockArray[ object_id ] )
        else:
            self.__m_ComputeFuncArray[ object_id ] = functools.partial( callback, dataBlock=self.__m_DataBlockArray[ object_id ] )


    def ReleaseComputeFunc( self, object_id ):
        try:
            self.__m_ComputeFuncArray[ object_id ]
        except:
            traceback.print_exc()


    # Dirtyフラグを伝播させる.コネクション変更時/アトリビュート値変更時に実行
    def PropagateDirty( self, object_id ):
        try:
            print( 'Pipeline::Evaluate()...', object_id )
            q = queue.Queue()
            q.put( object_id )

            while( not q.empty() ):
                for output in self.__m_DataBufferArray[ q.get() ].Outputs().values():
                    output.SetDirty()# Dirtyフラグをセットする
                    for input in output.References():# 接続先ノードを辿る
                        if( input.IsDirty() ):
                            continue
                        input.SetDirty()
                        block_id = input.ParentID()
                        if( not block_id in q.queue ):
                            q.put( block_id )# block_idを重複登録しないようにする

        except:
            traceback.print_exc()


    # 指定ノード(object_id)を基点として上流Dirtyノードを辿り、Computeを順次計算する.
    def Evaluate( self, object_id ):
        try:
            print( 'Pipeline::Evaluate()...', object_id )

            if( not object_id in self.__m_DataBufferArray ):
                print( '  aborting:  object does not exist.' )
                return False

            #==================== Collect dirty nodes ====================#
            dirtyNodeIds = []
            
            q = queue.Queue()
            q.put( object_id )

            while( not q.empty() ):
                buffer_id = q.get()
                dirtyNodeIds.append( buffer_id )

                for input in self.__m_DataBufferArray[ buffer_id ].Inputs().values():
                    for output in input.References():
                        if( output.IsDirty() ):# DirtyフラグのついたOutputだけトラバースする
                            q.put( output.ParentID() )
            
            #==================== Compute dirty nodes ====================#
            while( dirtyNodeIds ):
                node_id = dirtyNodeIds.pop()
                self.__m_ComputeFuncArray[ node_id ]()
                self.__m_DataBufferArray[ node_id ].SetClean()

            return True

        except:
            traceback.print_exc()
            return False



    #######################################################################################################################

    # 下流から上流へ遡るDAG
    # ノードグラフのDAG(dictを使用)の例. key: destination node id, value: source node id list
    # test DAG
    #DAG = {'7': [], '5': [], '3': [], '11': ['7', '5'], '8': ['7', '3'],
    #       '2': ['11'], '9': ['11', '8'], '10': ['11', '3']}
    
    # test 10->9->8 circular dependency
    #notDAG = {'7': [], '5': [], '3': [], '11': ['7', '5'], '8': ['7', '3', '10'],
    #          '2': ['11'], '9': ['11', '8'], '10': ['11', '3', '9']}
    
    def ConstructBackwardDAG( self, extra_dependencies ):

        # Initialize DAG using dataflow graph
        dag = defaultdict(list)
        
        for obj_id, obj in self.__m_DataBufferArray.items():
            dag[ obj_id ].clear()
            for data in obj.Inputs().values():
                for idx in range( data.NumReferences() ):# 上流NEDataのノードIDを取得し、dagに登録する
                    dag[ obj_id ].append( data.Reference(idx).ParentID() )# dag[ノードID].append(上流ノードID)
        
        # Add extra dependencies from predefined dependencies
        for src, dst in extra_dependencies.items():
            dag[ dst ].append( src )

        return dag


    # 上流から下流へ辿るDAG(dictを使用)の例. key: source node id, value: destination node id list
    def ConstructForwardDAG( self, extra_dependencies ):

        # Initialize DAG using dataflow graph
        dag = defaultdict(list)

        for obj_id, obj in self.__m_DataBufferArray.items():
            dag[ obj_id ].clear()
            for data in obj.Outputs().values():
                for idx in range( data.NumReferences() ):# 下流NEDataのノードIDを取得し、dagに登録する
                    dag[ obj_id ].append( data.Reference(idx).ParentID() )# dag[ノードID].append(下流ノードID)
        
        # Add extra dependencies from predefined dependencies
        for src, dst in extra_dependencies.items():
            dag[ src ].append( dst )

        return dag



    # DAGに対してトポロジカルソートを実行し、循環がないかどうかをチェックする.
    # 戻り値：True(循環なし), False(循環あり)
    def __TopologicalSort( self, DAG ):
        """
        Kahn ('62) topological sort.

        :param DAG: directed acyclic graph
        :type DAG: dict
        """
        L = []
        S = [k for k, v in DAG.items() if not v]
        while S:
            n = S.pop(0)
            L.append(n)
            for m in (k for k, v in DAG.items() if n in v):
                DAG[m] = list(set(DAG[m]).difference([n]))
                if not DAG[m]:
                    S.append(m)

        if( any([bool(v) for v in DAG.values()]) ):
            print( 'Cycle(s) detected...' )
            return False

        print( 'Ready to build. No cycle(s) detected...' )
        return True

    
    def CheckLoop( self, extra_dependencies=None ):

        print( 'Checking cycles...' )

        if( extra_dependencies is None ):
            return True

        # Construct DAG
        dag = self.ConstructForwardDAG( extra_dependencies )
        
        # Detect loop by topological sorting
        return self.__TopologicalSort( dag )
