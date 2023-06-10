#
# Panelund.py 2020/9/15
#
import random
import pyxel

BOARD_X,    BOARD_Y    =   2,  34
P1_STAND_X, P1_STAND_Y =  17,   1
P2_STAND_X, P2_STAND_Y =  17, 222
P1, P2 = 1, 2
OPP = {P1:P2, P2:P1}
VACANT, KING, QUEEN, GOLD, SILVER, ROOK, KNIGHT, OUT = 0, 1, 2, 3, 4, 5, 6, 99
PIECE_MOVE = {VACANT: [],
              KING:   [ -7, -6,-5,-1, 1, 5,  6,  7],
              QUEEN:  [ -7, -6,-5,-1, 1, 5,  6,  7],
              GOLD:   [ -6, -1, 1, 6],
              SILVER: [ -7, -5, 5, 7],
              ROOK:   [-12, -2, 2,12],
              KNIGHT: [-13,-11,-8,-4, 4, 8, 11, 13]}
AROUND  = { 0:(1,6,7), 1:(-1,1,5,6,7), 2:(-1,1,5,6,7), 3:(-1,1,5,6,7), 4:(-1,1,5,6,7) ,5:(-1,5,6),
            6:(-6,-5,1,6,7), 12:(-6,-5,1,6,7), 18:(-6,-5,1,6,7), 24:(-6,-5,1,6,7),
           11:(-7,-6,-1,5,6), 17:(-7,-6,-1,5,6), 23:(-7,-6,-1,5,6), 29:(-7,-6,-1,5,6),
           30:(-6,-5,1), 31:(-7,-6,-5,-1,1), 32:(-7,-6,-5,-1,1), 33:(-7,-6,-5,-1,1), 34:(-7,-6,-5,-1,1), 35:(-7,-6,-1)}
AROUND8 = (-7,-6,-5,-1,1,5,6,7)

STATUS_TITLE               = 110
STATUS_START               = 120
STATUS_PLAYER              = 130
STATUS_COM_CHECK_WIN       = 210
STATUS_COM_CHECK_NOTLOSE   = 220
STATUS_COM_CHECK_AROUND    = 230
STATUS_COM_RANDOM          = 240
STATUS_COM_CHOOSE          = 250
STATUS_MAN_SELECT          = 310
STATUS_MAN_DROP            = 320
STATUS_SLIDE               = 410
STATUS_WINLOSE             = 420
STATUS_MESSAGE             = 430
STATUS_END                 = 510

class App:
    def reset_start(self):
        self.board = [0]*36
        self.board[14], self.board[21] = -KING, KING
        self.inhand_p1 = [-QUEEN, -GOLD, -SILVER, -ROOK, -KNIGHT]
        self.inhand_p2 = [ QUEEN,  GOLD,  SILVER,  ROOK,  KNIGHT]
        self.allmove = []
        self.winmove = []
        self.notlosemove = []
        self.turn = random.choice((P1, P2))
        self.select_pos = -1
        #self.drop_piece = 0
        #self.selected_pos = -1
        self.dropped_pos  = -1
        self.slide_x = self.slide_y = 0
        self.winplayer = 0
        self.com_move = []
        self.winaroundpos = []
        self.bgcolor = random.choice([1, 4, 5])
        self.char_opt = random.randint(0, 1)

    def __init__(self):
        pyxel.init(191, 255, title='Panelund')
        pyxel.load('assets/Panelund.pyxres')
        pyxel.mouse(True)
        self.man_man = self.com_com = self.com_lv1 = self.com_lv2 = self.com_lv3 = False
        self.reset_start()
        self.status = STATUS_TITLE
        pyxel.run(self.update, self.draw)

    def checkchain(self, cp_bd, pos):
        if cp_bd[pos]:
            if pos in self.piece_chain_pos:
                pass
            else:
                self.piece_chain_pos.append(pos)
                for i in AROUND.get(pos, AROUND8):
                    self.checkchain(cp_bd, pos+i)
    
    def iswin(self, turn, bd):
        cp_bd = bd[:]
        if bd[24] or bd[25] or bd[26] or bd[27] or bd[28] or bd[29]:
            cp_bd[0] = cp_bd[1] = cp_bd[2] = cp_bd[3] = cp_bd[4] = cp_bd[5] = OUT
        if bd[30] or bd[31] or bd[32] or bd[33] or bd[34] or bd[35]:
            cp_bd[6] = cp_bd[7] = cp_bd[8] = cp_bd[9] = cp_bd[10] = cp_bd[11] = OUT
        if bd[6] or bd[7] or bd[8] or bd[9] or bd[10] or bd[11]:
            cp_bd[30] = cp_bd[31] = cp_bd[32] = cp_bd[33] = cp_bd[34] = cp_bd[35] = OUT
        if bd[0] or bd[1] or bd[2] or bd[3] or bd[4] or bd[5]:
            cp_bd[24] = cp_bd[25] = cp_bd[26] = cp_bd[27] = cp_bd[28] = cp_bd[29] = OUT
        if bd[4] or bd[10] or bd[16] or bd[22] or bd[28] or bd[34]:
            cp_bd[0] = cp_bd[6] = cp_bd[12] = cp_bd[18] = cp_bd[24] = cp_bd[30] = OUT
        if bd[5] or bd[11] or bd[17] or bd[23] or bd[29] or bd[35]:
            cp_bd[1] = cp_bd[7] = cp_bd[13] = cp_bd[19] = cp_bd[25] = cp_bd[31] = OUT
        if bd[1] or bd[7] or bd[13] or bd[19] or bd[25] or bd[31]:
            cp_bd[5] = cp_bd[11] = cp_bd[17] = cp_bd[23] = cp_bd[29] = cp_bd[35] = OUT
        if bd[0] or bd[6] or bd[12] or bd[18] or bd[24] or bd[30]:
            cp_bd[4] = cp_bd[10] = cp_bd[16] = cp_bd[22] = cp_bd[28] = cp_bd[34] = OUT
        self.winaroundpos = []
        kingpos = cp_bd.index(KING if turn == P1 else -KING)
        kingaroundnum = 0
        for i in {-6,-1,1,6} & set(AROUND.get(kingpos, AROUND8)):
            #if not cp_bd[kingpos+i]:
            #    break
            if cp_bd[kingpos+i]:
                kingaroundnum += 1
                if cp_bd[kingpos+i] != OUT:
                    self.winaroundpos.append(kingpos+i)
        #else:
        #    return kingaroundnum
        #self.winaroundpos = []
        return kingaroundnum
    
    def slide_piece(self, bd, drop_pos):
        cp_bd = bd[:]
        sx = sy = 0
        if drop_pos in (0,1,2,3,4,5):
            cp_bd = [0,0,0,0,0,0]+cp_bd[:30]
            sy = -31
        if drop_pos in (0,6,12,18,24,30):
            cp_bd = [0]+cp_bd[:5]+[0]+cp_bd[6:11]+[0]+cp_bd[12:17]+[0]+cp_bd[18:23]+[0]+cp_bd[24:29]+[0]+cp_bd[30:35]
            sx = -31
        if drop_pos in (5,11,17,23,29,35):
            cp_bd = cp_bd[1:6]+[0]+cp_bd[7:12]+[0]+cp_bd[13:18]+[0]+cp_bd[19:24]+[0]+cp_bd[25:30]+[0]+cp_bd[31:]+[0]
            sx = 31
        if drop_pos in (30,31,32,33,34,35):
            cp_bd = cp_bd[6:]+[0,0,0,0,0,0]
            sy = 31
        return cp_bd, sx, sy

    def canmove_bd2bd(self, turn, bd, ih_p1, ih_p2, src_pos, diff):
        ret = []
        if diff in (-14, -12, -10, -2, 2, 10, 12, 14):
            diff //= 2
            lp = True
        else:
            lp = False
        dst_pos = src_pos + diff
        while True:
            cp_bd = bd[:]
            cp_ih_p1 = ih_p1[:]
            cp_ih_p2 = ih_p2[:]
            if dst_pos < 0 or 36 <= dst_pos:
                break
            dst_piece = bd[dst_pos]
            if dst_piece or (dst_pos in (0,6,12,18,24,30)) and (diff in (-11,-5,-4,1,7,8,13)) or \
                    (dst_pos in (1,7,13,19,25,31)) and (diff in (-4,8)) or \
                    (dst_pos in (4,10,16,22,28,34)) and (diff in (-8,4)) or \
                    (dst_pos in (5,11,17,23,29,35)) and (diff in (-13,-8,-7,-1,4,5,11)):  # 両辺飛び越え
                break
            cp_bd[dst_pos] = bd[src_pos]
            cp_bd[src_pos] = VACANT
            piece_exist_pos = [i for i in range(36) if cp_bd[i]]
            if ((dst_pos in (0,1,2,3,4,5) and set(piece_exist_pos) & {25,26,27,28}) or \
                    (dst_pos in (0,6,12,18,24,30) and set(piece_exist_pos) & {10,16,22,28}) or \
                    (dst_pos in (5,11,17,23,29,35) and set(piece_exist_pos) & {7,13,19,25}) or \
                    (dst_pos in (30,31,32,33,34,35) and set(piece_exist_pos) & {7,8,9,10})):  # 4x4内
                break
            self.piece_chain_pos = []  # すべて接続
            self.checkchain(cp_bd, piece_exist_pos[0])
            if set(piece_exist_pos) == set(self.piece_chain_pos):
                if self.iswin(OPP[turn], cp_bd) != 4:  # 自負手
                    cp_bd, sx, sy = self.slide_piece(cp_bd, dst_pos)
                    ret.append([cp_bd, cp_ih_p1, cp_ih_p2, src_pos, dst_pos, sx, sy])            
            if not lp:
                break
            dst_pos += diff
        return ret
    
    def canmove_bd2ih(self, turn, bd, ih_p1, ih_p2, src_pos):
        cp_bd = bd[:]
        cp_ih_p1 = ih_p1[:]
        cp_ih_p2 = ih_p2[:]
        cp_ih_p1.append(cp_bd[src_pos]) if turn == P1 else cp_ih_p2.append(cp_bd[src_pos])
        cp_bd[src_pos] = VACANT
        piece_exist_pos = [i for i in range(36) if cp_bd[i]]
        self.piece_chain_pos = []
        self.checkchain(cp_bd, piece_exist_pos[0])
        if set(piece_exist_pos) == set(self.piece_chain_pos):  # 全接続
            if self.iswin(OPP[turn], cp_bd) != 4:  # 自負手
                return [cp_bd, cp_ih_p1, cp_ih_p2, src_pos, len(cp_ih_p1)-1+100 if turn == P1 else len(cp_ih_p2)-1+200, 0, 0]
    
    def canmove_ih2bd(self, turn, bd, ih_p1, ih_p2):
        ret = []
        parmitdroppos = []
        for pos in (7,8,9,10, 13,14,15,16, 19,20,21,22, 25,26,27,28): #  手持ち
            if (turn == P1 and bd[pos] < 0) or (turn == P2 and bd[pos] > 0):
                for diff in (-7,-6,-5,-1, 1, 5, 6, 7):  # 自接
                    if bd[pos+diff] == VACANT:
                        parmitdroppos.append(pos+diff)
        parmitdroppos = list(set(parmitdroppos))
        oppkingpos = bd.index(KING if turn == P1 else -KING) 
        for diff in (-6,-1, 1, 6): #  KING隣不可
            if oppkingpos+diff in parmitdroppos:
                parmitdroppos.remove(oppkingpos+diff)
        for src_pos in range(len(ih_p1)) if turn == P1 else range(len(ih_p2)):
            for dst_pos in parmitdroppos:
                cp_bd    = bd[:]
                cp_ih_p1 = ih_p1[:]
                cp_ih_p2 = ih_p2[:]
                cp_bd[dst_pos] = cp_ih_p1.pop(src_pos) if turn == P1 else cp_ih_p2.pop(src_pos)
                piece_exist_pos = [i for i in range(36) if cp_bd[i]]
                if ((dst_pos in (0,1,2,3,4,5) and set(piece_exist_pos) & {25,26,27,28}) or \
                        (dst_pos in (0,6,12,18,24,30) and set(piece_exist_pos) & {10,16,22,28}) or \
                        (dst_pos in (5,11,17,23,29,35) and set(piece_exist_pos) & {7,13,19,25}) or \
                        (dst_pos in (30,31,32,33,34,35) and set(piece_exist_pos) & {7,8,9,10})): #  4x4内
                    pass
                else:
                    if self.iswin(OPP[turn], cp_bd) != 4:  # 自負手
                        cp_bd, sx, sy = self.slide_piece(cp_bd, dst_pos)
                        ret.append([cp_bd, cp_ih_p1, cp_ih_p2, src_pos+(100 if turn == P1 else 200), dst_pos, sx, sy])
        return ret

    def canmove(self, turn, bd, ih_p1, ih_p2):
        ret = []
        for src_pos in (7,8,9,10, 13,14,15,16, 19,20,21,22, 25,26,27,28):
            if (turn == P1 and bd[src_pos] < 0) or (turn == P2 and bd[src_pos] > 0):
                for diff in PIECE_MOVE[abs(bd[src_pos])]:  # 盤面から盤面
                    ret.extend(self.canmove_bd2bd(turn, bd, ih_p1, ih_p2, src_pos, diff))
                if (turn == P1 and bd[src_pos] != -KING) or (turn == P2 and bd[src_pos] != KING):  # 盤面から手持ち
                    apd = self.canmove_bd2ih(turn, bd, ih_p1, ih_p2, src_pos)
                    if apd:
                        ret.append(apd)
        ret.extend(self.canmove_ih2bd(turn, bd, ih_p1, ih_p2))  # 手持ちから盤面
        return ret
    
    def update(self):
        if self.com_com and pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT):  # RIGHT_BUTTON_UP/中断
            self.reset_start()
            self.status = STATUS_TITLE

        if self.status == STATUS_TITLE:
            self.man_man = (BOARD_X+ 40<pyxel.mouse_x<BOARD_X+145 and BOARD_Y+  5<pyxel.mouse_y<BOARD_Y+ 14)
            self.com_com = (BOARD_X+ 40<pyxel.mouse_x<BOARD_X+145 and BOARD_Y+ 16<pyxel.mouse_y<BOARD_Y+ 25)
            self.com_lv1 = (BOARD_X+ 40<pyxel.mouse_x<BOARD_X+145 and BOARD_Y+155<pyxel.mouse_y<BOARD_Y+164)
            self.com_lv2 = (BOARD_X+ 40<pyxel.mouse_x<BOARD_X+145 and BOARD_Y+166<pyxel.mouse_y<BOARD_Y+175)
            self.com_lv3 = (BOARD_X+ 40<pyxel.mouse_x<BOARD_X+145 and BOARD_Y+177<pyxel.mouse_y<BOARD_Y+186)
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # LEFT_BUTTON_UP
                if self.man_man or self.com_com or self.com_lv1 or self.com_lv2 or self.com_lv3:
                    self.status = STATUS_START

        elif self.status == STATUS_START:
            self.allmove = self.canmove(self.turn, self.board, self.inhand_p1, self.inhand_p2)  # 自分の手
            self.winmove = []
            self.notlosemove = []
            for each1 in self.allmove:
                if self.iswin(self.turn, each1[0]) == 4:
                    self.winmove.append(each1)
                oppmove = self.canmove(OPP[self.turn], each1[0], each1[1], each1[2])  # 次(相手)
                for each2 in oppmove:
                    if self.iswin(OPP[self.turn], each2[0]) == 4:
                        break
                else:
                    self.notlosemove.append(each1)
            self.status = STATUS_PLAYER
        
        elif self.status == STATUS_PLAYER:
            if self.com_com or ((self.com_lv1 or self.com_lv2 or self.com_lv3) and self.turn == P1):
                self.status = STATUS_COM_CHECK_WIN
            else:
                self.status = STATUS_MAN_SELECT
        
        elif self.status == STATUS_COM_CHECK_WIN:  # 勝つ手
            if self.winmove:
                self.com_move = random.choice(self.winmove)
                self.status = STATUS_COM_CHOOSE
            else:
                self.status = STATUS_COM_CHECK_NOTLOSE

        elif self.status == STATUS_COM_CHECK_NOTLOSE:  # 相手が勝つ次の手以外
            if not self.notlosemove or self.com_lv1:  # Lv1
                self.status = STATUS_COM_RANDOM
            elif self.com_com or self.com_lv2:  # com_com/Lv2
                self.com_move = random.choice(self.notlosemove)
                self.status = STATUS_COM_CHOOSE
            else:  # Lv3
                self.status = STATUS_COM_CHECK_AROUND
        
        elif self.status == STATUS_COM_CHECK_AROUND:  # ボスの周りの数で判断
            opparound = self.iswin(self.turn, self.board)
            ownaround = self.iswin(OPP[self.turn], self.board)
            around1move = []
            around2move = []
            for each in self.notlosemove:
                eachopparound = self.iswin(self.turn, each[0])
                eachownaround = self.iswin(OPP[self.turn], each[0])
                if eachopparound >= opparound and eachownaround <= ownaround:
                    if eachopparound > opparound or eachownaround < ownaround:
                        around1move.append(each)
                    else:
                        around2move.append(each)
            if around1move:  # 自分の周りが減/相手の周りが増
                self.com_move = random.choice(around1move)
            elif around2move:  # 自分相手の周りに変化なし
                self.com_move = random.choice(around2move)
            else:
                self.com_move = random.choice(self.notlosemove)
            self.status = STATUS_COM_CHOOSE

        elif self.status == STATUS_COM_RANDOM:  # ランダム
            self.com_move = random.choice(self.allmove)
            self.status = STATUS_COM_CHOOSE
        
        elif self.status == STATUS_COM_CHOOSE:  # 手を決める
            self.board        = self.com_move[0]
            self.inhand_p1    = self.com_move[1]
            self.inhand_p2    = self.com_move[2]
            #self.selected_pos = self.com_move[3]
            self.dropped_pos  = self.com_move[4]
            self.slide_x      = self.com_move[5]
            self.slide_y      = self.com_move[6]
            self.status = STATUS_SLIDE

        elif self.status == STATUS_MAN_SELECT:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # LEFT_BUTTON_UP
                select_x = (pyxel.mouse_x-BOARD_X)//31
                select_y = (pyxel.mouse_y-BOARD_Y)//31
                if 0 <= select_x < 6 and 0 <= select_y < 6:
                    self.select_pos = select_y*6+select_x
                    if self.select_pos in [v[3] for v in self.allmove]:
                        self.status = STATUS_MAN_DROP
                else:
                    if self.turn == P1:
                        select_x = (pyxel.mouse_x-P1_STAND_X)//31
                        select_y = (pyxel.mouse_y-P1_STAND_Y)//31
                        if select_y == 0 and 0 <= select_x < 5:
                            n = 4-select_x
                            self.select_pos = 100+n
                            if self.select_pos in [v[3] for v in self.allmove]:
                                self.status = STATUS_MAN_DROP
                    else:
                        select_x = (pyxel.mouse_x-P2_STAND_X)//31
                        select_y = (pyxel.mouse_y-P2_STAND_Y)//31
                        if select_y == 0 and 0 <= select_x < 5:
                            n = select_x
                            self.select_pos = 200+n
                            if self.select_pos in [v[3] for v in self.allmove]:
                                self.status = STATUS_MAN_DROP
    
        elif self.status == STATUS_MAN_DROP:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT):  # RIGHT_BUTTON_UP
                self.status = STATUS_MAN_SELECT
            elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # LEFT_BUTTON_UP
                select_x = (pyxel.mouse_x-BOARD_X)//31
                select_y = (pyxel.mouse_y-BOARD_Y)//31
                new_drop_pos = select_y*6+select_x
                if 0 <= select_x < 6 and 0 <= select_y < 6:
                    for i in range(len(self.allmove)):
                        if self.select_pos == self.allmove[i][3] and new_drop_pos == self.allmove[i][4]:
                            self.board        = self.allmove[i][0]
                            self.inhand_p1    = self.allmove[i][1]
                            self.inhand_p2    = self.allmove[i][2]
                            #self.selected_pos = self.allmove[i][3]
                            self.dropped_pos  = self.allmove[i][4]
                            self.slide_x     = self.allmove[i][5]
                            self.slide_y     = self.allmove[i][6]
                            self.status = STATUS_SLIDE
                            break
                    else:
                        self.status = STATUS_MAN_SELECT
                else:
                    if self.turn == P1:
                        select_x = (pyxel.mouse_x-P1_STAND_X)//31
                        select_y = (pyxel.mouse_y-P1_STAND_Y)//31
                        if select_y == 0 and 0 <= select_x < 5:
                            new_drop_pos = 100+4-select_x
                            for i in range(len(self.allmove)):
                                if self.select_pos == self.allmove[i][3] and new_drop_pos == self.allmove[i][4]:
                                    self.board        = self.allmove[i][0]
                                    self.inhand_p1    = self.allmove[i][1]
                                    self.inhand_p2    = self.allmove[i][2]
                                    #self.selected_pos = self.allmove[i][3]
                                    #self.dropped_pos  = self.allmove[i][4]
                                    self.status = STATUS_WINLOSE
                                    break
                            else:
                                self.status = STATUS_MAN_SELECT
                    else:
                        select_x = (pyxel.mouse_x-P2_STAND_X)//31
                        select_y = (pyxel.mouse_y-P2_STAND_Y)//31
                        if select_y == 0 and 0 <= select_x < 5:
                            new_drop_pos = 200+select_x
                            for i in range(len(self.allmove)):
                                if self.select_pos == self.allmove[i][3] and new_drop_pos == self.allmove[i][4]:
                                    self.board        = self.allmove[i][0]
                                    self.inhand_p1    = self.allmove[i][1]
                                    self.inhand_p2    = self.allmove[i][2]
                                    #self.selected_pos = self.allmove[i][3]
                                    #self.dropped_pos  = self.allmove[i][4]
                                    self.status = STATUS_WINLOSE
                                    break
                            else:
                                self.status = STATUS_MAN_SELECT
        
        elif self.status == STATUS_SLIDE:
            if self.slide_x > 0:
                self.slide_x -= 1
            elif self.slide_x < 0:
                self.slide_x += 1
            if self.slide_y > 0:
                self.slide_y -= 1
            elif self.slide_y < 0:
                self.slide_y += 1
            if self.slide_x == 0 and self.slide_y == 0:
                self.status = STATUS_WINLOSE
        
        elif self.status == STATUS_WINLOSE:
            self.winplayer = 0
            if self.iswin(self.turn, self.board) == 4:
                self.winplayer = self.turn
            self.status = STATUS_MESSAGE
        
        elif self.status == STATUS_MESSAGE:
            self.turn = OPP[self.turn]
            if self.winplayer:
                self.status = STATUS_END
            else:
                self.status = STATUS_START

        elif self.status == STATUS_END:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # LEFT_BUTTON_UP
                self.reset_start()
                self.status = STATUS_TITLE
    
    def draw_title(self):
        pyxel.text(BOARD_X+54, BOARD_Y+  8, '   Human vs Human',      (pyxel.frame_count//2%5)+3 if self.man_man else 7)
        pyxel.text(BOARD_X+54, BOARD_Y+ 19, 'Computer vs Computer',   (pyxel.frame_count//2%5)+3 if self.com_com else 7)
        pyxel.text(BOARD_X+54, BOARD_Y+158, 'Computer vs Human Lv.1', (pyxel.frame_count//2%5)+3 if self.com_lv1 else 7)
        pyxel.text(BOARD_X+54, BOARD_Y+169, 'Computer vs Human Lv.2', (pyxel.frame_count//2%5)+3 if self.com_lv2 else 7)
        pyxel.text(BOARD_X+54, BOARD_Y+180, 'Computer vs Human Lv.3', (pyxel.frame_count//2%5)+3 if self.com_lv3 else 7)

    def draw_board(self):
        bd_up = bd_left = 0
        bd_down = bd_right = 6
        if self.board[25] or self.board[26] or self.board[27] or self.board[28]:
            bd_up = 1
        if not self.board[7] and not self.board[8] and not self.board[9] and not self.board[10]:
            bd_up = 1
            if not self.board[13] and not self.board[14] and not self.board[15] and not self.board[16]:
                bd_up = 2
                if not self.board[19] and not self.board[20] and not self.board[21] and not self.board[22]:
                    bd_up = 3
        if self.board[7] or self.board[8] or self.board[9] or self.board[10]:
            bd_down = 5
        if not self.board[25] and not self.board[26] and not self.board[27] and not self.board[28]:
            bd_down = 5
            if not self.board[19] and not self.board[20] and not self.board[21] and not self.board[22]:
                bd_down = 4
                if not self.board[13] and not self.board[14] and not self.board[15] and not self.board[16]:
                    bd_down = 3
        if self.board[10] or self.board[16] or self.board[22] or self.board[28]:
            bd_left = 1
        if not self.board[7] and not self.board[13] and not self.board[19] and not self.board[25]:
            bd_left = 1
            if not self.board[8] and not self.board[14] and not self.board[20] and not self.board[26]:
                bd_left = 2
                if not self.board[9] and not self.board[15] and not self.board[21] and not self.board[27]:
                    bd_left = 3
        if self.board[7] or self.board[13] or self.board[19] or self.board[25]:
            bd_right = 5
        if not self.board[10] and not self.board[16] and not self.board[22] and not self.board[28]:
            bd_right = 5
            if not self.board[9] and not self.board[15] and not self.board[21] and not self.board[27]:
                bd_right = 4
                if not self.board[8] and not self.board[14] and not self.board[20] and not self.board[26]:
                    bd_right = 3
        pyxel.rect(BOARD_X+31*bd_left+self.slide_x, BOARD_Y+31*bd_up+self.slide_y, \
                    31*(bd_right-bd_left), 31*(bd_down-bd_up), 3)
        for i in range(bd_left, bd_right+1):
            pyxel.line(BOARD_X+31*i+self.slide_x, BOARD_Y+31*bd_up+self.slide_y, \
                    BOARD_X+31*i+self.slide_x, BOARD_Y+31*bd_down+self.slide_y, 0)
        for i in range(bd_up, bd_down+1):
            pyxel.line(BOARD_X+31*bd_left+self.slide_x, BOARD_Y+31*i+self.slide_y, \
                    BOARD_X+31*bd_right+self.slide_x, BOARD_Y+31*i+self.slide_y, 0)
        #pyxel.rectb(P1_STAND_X  , P1_STAND_Y  , 156, 32, 0)
        #pyxel.rect( P1_STAND_X+1, P1_STAND_Y+1, 154, 30, 3)
        #pyxel.rectb(P2_STAND_X  , P2_STAND_Y  , 156, 32, 0)
        #pyxel.rect( P2_STAND_X+1, P2_STAND_Y+1, 154, 30, 3)
    
    def draw_piece(self):
        for i in range(6):
            for j in range(6):
                p = self.board[i*6+j]
                if p:
                    pyxel.blt(BOARD_X+2+j*31+self.slide_x, BOARD_Y+2+i*31+self.slide_y, 0, \
                            p*32-30 if p>0 else -p*32-30, 66+self.char_opt*32 if p>0 else 34, 28, 28 if p>0 else -28, 1)
    
    def draw_inhand(self):
        for i, p in enumerate(self.inhand_p1):
            pyxel.blt(P1_STAND_X+126-i*31, P1_STAND_Y+2, 0, -p*32-30, 34, 28, -28, 1)
        for i, p in enumerate(self.inhand_p2):
            pyxel.blt(P2_STAND_X+2+i*31, P2_STAND_Y+2, 0, p*32-30, 66+self.char_opt*32, 28, 28, 1)
    
    def draw_name(self, col=7):
        pyxel.text(P1_STAND_X-15, P1_STAND_Y+14, 'MAN' if self.man_man else 'Lv.1' \
                if self.com_lv1 else 'Lv.2' if self.com_lv2 else 'Lv.3' if self.com_lv3 else 'COM', col)
        pyxel.text(P2_STAND_X+157, P2_STAND_Y+14, 'COM' if self.com_com else 'MAN', col)
    
    def draw_select(self, col=10):
        for i in set([v[3] for v in self.allmove]):  # src_pos
            if i < 100:
                pyxel.rect(BOARD_X+1+(i%6)*31, BOARD_Y+1+(i//6)*31, 30, 30, col)
            elif i < 200:
                pyxel.rect(P1_STAND_X+125-(i-100)*31, P1_STAND_Y+1, 30, 30, col)
            else:
                pyxel.rect(P2_STAND_X+1+(i-200)*31, P2_STAND_Y+1, 30, 30, col)
    
    def draw_drop(self, col_select=10, col_drop=10):
        if self.select_pos < 100:
            pyxel.rect(BOARD_X+1+(self.select_pos%6)*31, BOARD_Y+1+(self.select_pos//6)*31, 30, 30, col_select)
        elif self.select_pos < 200:
            pyxel.rect(P1_STAND_X+125-(self.select_pos-100)*31, P1_STAND_Y+1, 30, 30, col_select)
        else:
            pyxel.rect(P2_STAND_X+1+(self.select_pos-200)*31, P2_STAND_Y+1, 30, 30, col_select)
        for i in range(len(self.allmove)):
            if self.select_pos == self.allmove[i][3]:
                if self.allmove[i][4] < 100:
                    pyxel.circ(BOARD_X+1+(self.allmove[i][4]%6)*31+15, BOARD_Y+1+(self.allmove[i][4]//6)*31+15, 2, col_drop)
                elif self.allmove[i][4] < 200:
                    pyxel.circ(P1_STAND_X+125-(self.allmove[i][4]-100)*31+15, P1_STAND_Y+1+15, 2, col_drop)
                else:
                    pyxel.circ(P2_STAND_X+1+(self.allmove[i][4]-200)*31+15, P2_STAND_Y+1+15, 2, col_drop)
    
    def draw_winlose(self):
        pyxel.text(P1_STAND_X+157, P1_STAND_Y+14, 'WIN' if self.winplayer == P1 else 'LOSE', \
                (pyxel.frame_count//2%5)+3 if self.winplayer == P1 else 13)
        pyxel.text(P2_STAND_X-15, P2_STAND_Y+14, 'WIN' if self.winplayer == P2 else 'LOSE', \
                (pyxel.frame_count//2%5)+3 if self.winplayer == P2 else 13)
        for i in self.winaroundpos:
            pyxel.rect(BOARD_X+1+(i%6)*31, BOARD_Y+1+(i//6)*31, 30, 30, (pyxel.frame_count//2%5)+3)

    def draw(self):
        pyxel.cls(self.bgcolor)
        self.draw_board()
        if self.status == STATUS_TITLE:
            self.draw_title()
        elif self.status == STATUS_MAN_SELECT:
            self.draw_select()
        elif self.status == STATUS_MAN_DROP:
            self.draw_drop()
        elif self.status == STATUS_END:
            self.draw_winlose()
        self.draw_piece()
        self.draw_inhand()
        self.draw_name()

App()
