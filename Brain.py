from collections import deque
import itertools
import random
import copy
from datetime import datetime
import numpy as np

class Brain:
    """Brain プレイヤーの脳。からだの外にある。盤面の評価値計算、最善手の探索。"""
    def __init__(self, block_data, weights=(1,1,1,1)):
        self.max_depth = 5
        self.block_data = block_data
        self.weights=weights

    def get_setting_info(self,real_board,blocks_field):
        """
        最終的に置くと判断したブロックと場所をリストに入れて返す。
        0を最初に置くブロックとする。
        """
        results,eval = self.search_all_permutation_blocks(real_board, blocks_field)
        return results,eval
    
    def search_all_permutation_blocks(self,board,blocks):
        """
        ①blocksに含まれるブロックを置く順番それぞれについて、最も評価値の高い置き方を取得する
        ②それらの中からゲーム続行が長く続くもの＆最も評価値の高い順番を取得して返す
        """
        results = deque()
        size=len(blocks)
        for p in [list(p_list) for p_list in itertools.permutations(range(size),size)]:
            results.appendleft(self.search_blocks_of_a_permutation_setting(board,blocks,p))


        s = sorted(results
                      , key=lambda rs : [r.playable for r in rs[0]].count(True)
                      , reverse=True)
        max_result,eval = sorted(results, key=lambda rs : rs[1], reverse=True)[0]
        

        #for r_que in results:
        #    print(f"  all_result_eval:{r_que[1]}")
        #print(f"selected_eval:{eval}")
        return max_result,eval


    def search_blocks_of_a_permutation_setting(self,board,blocks,permutation,depth=0):
        """
        一度配布されたブロックぶんについて、ある順序で置く時のベストな置き方の場所を出す。
        permutationでブロックの置き順を呼び出し側から指定する。
        再帰呼出しでdepthを深くすることでpermutationを追う方法でやってみてる
        返り値：deque(Result_Calc),Int
        """
        results = deque()
        tmp_results = deque()
        eval = -float("inf")
        tmp_eval = 0

        if(depth > (len(blocks)-1) or depth > self.max_depth):
            eval = self.calc_evaluation_value(board, blocks, weights=self.weights)
            return results,eval

        target_block = blocks[permutation[depth]]
        settable_points = self.search_settable_point(board,target_block)
        if(len(settable_points)>5):
            #パフォーマンス問題ありそうならここで刈り込みしないとだめ。
            #ボードサイズの2倍だとサイズ10でもう終わらない。10個でもだめ。
            #端に近い方から5個だけ選ぶことにする
            s_tmp = sorted(settable_points
                                     , key=lambda p : abs(board.size/2-list(p)[0])
                                     , reverse=True)
            settable_points = sorted(s_tmp
                                     , key=lambda p : abs(board.size/2-list(p)[1])
                                     , reverse=True)[:5]

        if(len(settable_points) < 1):
            #置けない
            results.appendleft(Result_Calc(target_block))
            eval = self.calc_evaluation_value(board,blocks)
            return results,eval

        for i,j in settable_points:
            tmp_board = board.copy()
            tmp_board.set_block(target_block,i,j)
            tmp_results,tmp_eval = self.search_blocks_of_a_permutation_setting(tmp_board,blocks,permutation,depth+1)
            tmp_results.appendleft(Result_Calc(target_block,i,j,True))
            if tmp_eval >= eval:
                eval = tmp_eval
                results = copy.deepcopy(tmp_results)
        return results,eval


    def search_settable_point(self,board,block):
        """
        与えられた盤面に与えられたブロックが置ける位置を全てリストアップ
        """
        settable_points = []
        #ブロックの上下サイズで探索範囲を絞る
        for i,j in [(x,y) for x in range(board.size) \
                          for y in range(board.size) \
                    #      if x <= board.size - block.w and y <= board.size - block.h
                    ]:
            if(board.can_set(block,i,j)):
                settable_points.append((i,j))
        return settable_points

    def calc_evaluation_value(self,board,blocks,weights=(1,1,1,1)):
        #残りブロックが少ないほど良い
        #print(f"    spaces {datetime.now()}")
        spaces =  self.count_space((board.size * board.size), board.now)
        #ブロックが固まってるほど良い
        #print(f"    around_blocks {datetime.now()}")
        around_blocks = self.count_around_block(board)
        #置けるブロックの種類が多いほど良い
        #print(f"    kinds {datetime.now()}")
        kinds = self.count_settable_kinds_of_block(board, self.block_data.pattern_to_block())
        #消えてる列が多いほど良い
        #print(f"    empty_lines {datetime.now()}")
        empty_lines = self.count_empty_line(board)
        #print(f"    end")
        return sum([w*v for w,v in zip(weights,(spaces, around_blocks, kinds, empty_lines))])

    def count_space(self, all_count,board_list):
        return all_count - sum([p for line in board_list for p in line])

    def count_settable_kinds_of_block(self, board, blocks):
        kinds = []
        for b in blocks:
            for i,j in itertools.product(range(board.size), range(board.size)):
                if board.can_set(b,i,j):
                    kinds.append(b)
                    break

        return len(kinds)

    def count_around_block(self,board):
        sum_around_blocks = 0
        #周りに0を配置してスライスして足す
        ar = np.zeros((board.size+2,board.size+2), dtype=object)
        ar_one = np.ones((board.size,board.size), dtype=object) #xorして1/0反転させる用
        bd = np.array(board.now)
        b_ar_zero = ar[1:-1,1:-1] = bd
        #上下左右
        #+ななめ
        around_blocks_list = ar[:-2,1:-1]+ar[2:,1:-1]+ar[1:-1,:-2]+ar[1:-1,2:] \
                           + ar[:-2,:-2]+ar[:-2,2:]+ar[2:,:-2]+ar[2:,2:]
        #ブロックが置いてあるところを足す
        #sum_around_blocks = sum(sum(around_blocks_list * bd))
        #空いている位置の周りが埋まってたら孤立しているので駄目
        sum_empty_around_blocks = sum(sum(around_blocks_list * (bd ^ ar_one)))

        return sum_around_blocks - sum_empty_around_blocks

    def count_empty_line(self,board):
        bd = np.array(board.now)
        cnt = np.sum(np.all(bd==0,axis=0)) \
             + np.sum(np.all(bd==0,axis=1))
            
        return cnt


class Result_Calc:
    """
    一つのブロックを置く場所の結果
    playableがFalseの場合、ほかの要素は初期値
    """
    def __init__(self, block, x=0, y=0, playable=False):
        self.x = x
        self.y = y
        self.block = block
        self.playable = playable

    def copy(self):
        return copy.deepcopy(self)
