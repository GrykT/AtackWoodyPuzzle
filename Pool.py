class Pool:
    """Pool 次のブロックの保管場所"""
    def __init__(self, size, blocks):
        self.__pool_size = size
        self.blocks = blocks
        self.stock = []

    def get_blocks(self):
        """
        サイズに応じたブロックをランダムに取得する
        """
        self.stock = [self.blocks.get_block_random() for i in range(self.__pool_size)]
        return self.stock

    def pop_block(self,position):
        """
        ストックから指定した位置のブロックをpopする
        """
        return self.stock.pop(position)