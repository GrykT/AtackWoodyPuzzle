from collections import deque

class Player:
    """Player プレイヤー　保管場所からブロックを選んで置けるところに置く"""
    def __init__(self, ipool,iboard,ibrain,max=10000,logger=None):
        self.pool = ipool
        self.playing_board = iboard
        self.my_brain = ibrain
        self.max_count=max
        self.logger = logger
        if(self.logger == None):
            #logger未指定の場合もエラーにしない
            class dummy(object):
                pass
            self.logger = dummy()
            setattr(self.logger,"write",lambda s:-1)

    def start(self):
        """
        ゲームを進める。終わったら結果を返す
        """
        playable_game = True
        self.result_set_blocks_num = 0
        results_que = deque()
        cnt = 0

        self.logger.write("start!")
        self.logger.write(self.get_boardstate())

        while(playable_game and cnt < self.max_count):
            self.logger.write("---------------------------------------")
            blocks_field = self.pool.get_blocks()
            names = ",".join([b.name for b in blocks_field])
            self.logger.write(f"New get Blocks:{names}")
            results_que,eval = self.my_brain.get_setting_info(self.playing_board, blocks_field)
            while(len(results_que) > 0):
                result = results_que.popleft()
                if result.playable:
                    self.set_block(result.block, result.x, result.y)
                    self.result_set_blocks_num += 1
                    self.logger.write(f"Use Block:{result.block.name}  Set:({result.x},{result.y})")
                else:
                    self.logger.write("置けないよ")
                self.logger.write(self.get_boardstate())
                playable_game = result.playable
                cnt += 1
            self.logger.write(f"thie eval:{eval}")

        self.logger.write(f"【結果】\n置いたブロック数：{self.result_set_blocks_num}")
        self.logger.write("ゲームオーバー。。。")
    
        return self.result_set_blocks_num

    def set_block(self,block,x,y):
        self.playing_board.set_block(block,x,y)

    def get_boardstate(self):
        """
        現在のボードを返す
        """
        return self.playing_board.out_state()
        