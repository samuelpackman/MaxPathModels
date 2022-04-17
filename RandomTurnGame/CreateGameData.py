from Board import Board

def CreateGameData():
    #sys.stdout=open("/Users/Liz/Desktop/HammondGameSamRewrite/newdata.txt","w")

    print("BoardListListList = []")
    for i in range(20,21):
        print("#board size" + str(10 * i))
        print("BoardListList = []")
        for j in range(10):
            print("BoardList = []")
            print("#newgame")
            testBoard = Board(10*i)
            testBoard.game(player1,player2,True)
            print("BoardListList.append(BoardList)")
        print("BoardListListList.append(BoardListList)")


    #f.closesys.stdout.close()

CreateGameData()
