import random

class Graph:
    def __init__(self, player0win,player1win):
        self.player0win = player0win #should be negative
        self.player1win = player1win #should be positive
        self.current_pos = 0
        self.player0money = 1
        self.player1money = 1


    def __str__(self):
        return f'Player 0 Win: {self.player0win} \n Player 1 Win: {self.player1win} \n Current Position: {self.current_pos}'

    def display(self):
        print("|" + (self.current_pos - self.player0win) * "-" + "o" + (self.player1win - self.current_pos) * "-" + "|")

    def turn(self):
        player1bid = self.player1money * .6 * 0.9 ** abs(self.current_pos - self.player0win)
        player0bid = self.player0money * .6 * 0.9 ** abs(self.current_pos - self.player1win)

        self.player0money -= player0bid
        self.player1money -= player1bid

        print(f'Player 0 Bid: {int(player0bid)}, Player 1 Bid: {int(player1bid)}', end =' ')

        if random.random() < player0bid/(player0bid + player1bid):
            self.current_pos -= 1
        else:
            self.current_pos += 1


    def game(self):
        self.current_pos = 0
        self.player0money = 1000
        self.player1money = 1000

        self.display()
        while self.current_pos < self.player1win and self.current_pos > self.player0win:
            self.turn()
            self.display()
        if self.current_pos == self.player1win:
            print("Player 1 Wins!")
        if self.current_pos == self.player0win:
            print("Player 0 Wins!")

test = Graph(-10,10)

test.game()
