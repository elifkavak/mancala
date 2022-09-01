class Board:
    def __init__(self, board ):
        if board!=None:
            self.board = board[:]
        else:
            self.board=[0 for i in range(14)]
            for i in range(0,6,1): self.board[i]=4
            for i in range(7, 13, 1): self.board[i] = 4
    #move stone which choosen stone
    def move(self, i):
        j=i
        turn=False
        add=self.board[j]
        self.board[j] = 0
        if i>6:
            stones = add
            while(stones>0):
                i+=1
                i=i % 14
                if i==6 : continue
                else:
                    self.board[i%14]+=1
                stones-=1
            if i>6 and self.board[i]==1 and i!=13 and self.board[5-(i-7)]!=0:
                self.board[13]+=1+self.board[5-(i-7)]
                self.board[i]=0
                self.board[5-(i-7)]=0
            if i==13:
                turn = True
        else:
            stones = add
            while (stones > 0):
                i += 1
                i = i % 14
                if i == 13:
                    continue
                else:
                    self.board[i%14] += 1
                stones -= 1
            if i < 6 and self.board[i] == 1 and i !=6 and self.board[-i + 12]!=0:
                self.board[6] += 1 + self.board[-i + 12]
                self.board[i] = 0
                self.board[-i + 12] = 0
            if i == 6:
                turn = True
        return turn

    # check if the game is end
    def isEnd(self):
        if sum(self.board[0:6])==0 :
            self.board[13]+=sum(self.board[7:13])
            for i in range(14):
                if  (i != 13 and i != 6):
                    self.board[i] = 0

            return True
        elif sum(self.board[7:13])==0:
            self.board[6] += sum(self.board[0:6])
            for i in range(14):
                if  (i != 13 and i != 6):
                    self.board[i] = 0
            return True

        return False

    def printBoard(self):

        for i in range(12,6,-1):
            print('      ', i , '  ', end = '')
        print()
        for i in range(12,6,-1):
            print('    | ', self.board[i], ' | ', end = '')
        print('  ')
        print('|',self.board[13],'|                                                                 |',self.board[6], '|')

        for i in range(0,6,1):
            print('    | ', self.board[i], ' | ', end='')
        print('  ')

        for i in range(0,6,1):
            print('      ', i, '   ', end='')
        print()

    #high heuristic value denotes this state is good for AI agent
    def husVal(self):
        if self.isEnd():
            if self.board[13]>self.board[6]:
                return 100
            elif self.board[13]==self.board[6]:
                return 0
            else :
                 return -100
        else:
            return self.board[13]- self.board[6]

#this is implementation of minmax
def algorithm(board, depth, alpha, beta , minmax):
     if depth == 0 or board.isEnd():
         return board.husVal(),-1
     if minmax:
         v = -1000000
         move = -1
         for i in range(7,13,1):
             if board.board[i]==0: continue
             a=Board(board.board[:])
             minmax = a.move(i);
             newv,_ =  algorithm(a, depth-1, alpha, beta, minmax)
             if v< newv:
                 move=i
                 v =newv
             alpha = max(alpha, v)
             if alpha >= beta :
                 break
         return v, move
     else:
         v = 1000000
         move = -1
         for i in range(0, 6, 1):
             if board.board[i] == 0: continue
             a = Board(board.board[:])
             minmax = a.move(i);
             newv,_ = algorithm(a, depth - 1, alpha, beta, not minmax)
             if v > newv:
                 move = i
                 v = newv
             beta = min(beta, v)
             if alpha >= beta:
                 break
         return v, move



if __name__ == "__main__":
    print("Mancala Game")
    print("----------------------------------------------")
    j=Board(None)
    j.printBoard()

    while(True):
        if j.isEnd():
            break
        while(True):
            if j.isEnd():
                break
            print("---------------------------------------------")
            print("BOTS TURN ")
            _,k = algorithm(j,10,-100000,100000,True)
            print('move-->',k)
            t=j.move(k)
            j.printBoard()
            if not t:
                break
        while True:
            if j.isEnd():
                break
            print("---------------------------------------------")
            print("YOUR TURN (select 0-1-2-3-4-5) ")
            h= int(input())
            if h>5 or j.board[h]==0:
                print('you cannot play ')
                continue
            t=j.move(h)
            j.printBoard()
            if not t:
                break
    if j.mancala[0] < j.mancala[13]:
        print("---BOT WINS---")
    else:
        print("---YOU WIN---")
    print('---GAME ENDED---')
    j.printBoard()