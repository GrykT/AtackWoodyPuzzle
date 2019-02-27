from collections import deque
import itertools
import random
import copy

class Brain:
    """Brain プレイヤーの脳。からだの外にある。盤面の評価値計算、最善手の探索。"""
    def __init__(self):
        self.max_depth = 5

    def get_setting_info(self,real_board,blocks_field):
        """
        最終的に置くと判断したブロックと場所をリストに入れて返す。
        0を最初に置くブロックとする。
        """
        results = self.search_all_permutation_blocks(real_board, blocks_field)
        return results
    
    def search_all_permutation_blocks(self,board,blocks):
        """
        ①blocksに含まれるブロックを置く順番それぞれについて、最も評価値の高い置き方を取得する
        ②それらの中から最も評価値の高い順番を取得して返す
        """
        results = deque()
        size=len(blocks)
        for p in [list(p_list) for p_list in itertools.permutations(range(size),size)]:
            results.appendleft(self.search_blocks_of_a_permutation_setting(board,blocks,p))

        max_result,eval = sorted(results, key=lambda rs : rs[1], reverse=True)[0]
        return max_result


    def search_blocks_of_a_permutation_setting(self,board,blocks,permutation,depth=0):
        """
        一度配布されたブロックぶんについて、ある順序で置く時のベストな置き方の場所を出す。
        permutationでブロックの置き順を呼び出し側から指定する。
        再帰呼出しでdepthを深くすることでpermutationを追う方法でやってみてる
        返り値：deque(Result_Calc),Int
        """
        results = deque()
        tmp_results = deque()
        eval = 0
        tmp_eval = 0

        if(depth > (len(blocks)-1) or depth > self.max_depth):
            eval = self.calc_evaluation_value(board.now)
            return results,eval

        settable_points = self.search_settable_point(board,blocks[depth])

        if(len(settable_points) >  board.size * 2):
            #パフォーマンス問題ありそうならここで刈り込みしないとだめ。取り敢えずボードサイズの2倍くらい目処
            settable_points = [(x,y) for x,y in settable_points[:board.size * 2]]

        if(len(settable_points) < 1):
            #置けない
            results.appendleft(Result_Calc(blocks[depth]))
            return results,eval

        
        for i,j in settable_points:
            tmp_board = board.copy()
            tmp_board.set_block(blocks[depth],i,j)
            tmp_results,tmp_eval = self.search_blocks_of_a_permutation_setting(tmp_board,blocks,permutation,depth+1)
            tmp_results.appendleft(Result_Calc(blocks[depth],i,j,True))
            if tmp_eval >= eval:
                eval = tmp_eval
                results = copy.deepcopy(tmp_results)

        return results,eval


    def search_settable_point(self,board,block):
        """
        与えられた盤面に与えられたブロックが置ける位置を全てリストアップ
        """
        settable_points = []
        for i,j in [(x,y) for x in range(board.size) \
                          for y in range(board.size) \
                          if board.now[x][y] != 1]:
            if(board.can_set(block,i,j)):
                settable_points.append((i,j))
        return settable_points

    def calc_evaluation_value(self,board):
        #仮実装 1～9ランダムで
        return random.randrange(1,9)

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
