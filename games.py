from collections import Counter
from random import shuffle
from typing import List

from dominoesGameState import DominoesMove, DominoesGameState
from jugador import Cantidad3, Aleatorio, Jugador
from jugador_inteligente import Inteligente


class Data:
    uno = Inteligente('3', [0.36760645349812066, 0.079849156030557131,
                            0.068292140445869134, 0.61909221402983905,
                            0.15014843724360663, 0.94146798512271024])
    dos = Inteligente('3',
                      [0.50319271, 0.89254, 0.05187015, 0.42540609, 0.19632677,
                       0.92883179])

    tres = Inteligente('3', [0.50328748, 0.89258251, 0.05182548, 0.42549345,
                             0.19590833, 0.92901494])
    players = [Cantidad3('1'), Aleatorio('2'), tres, Cantidad3('4')]
    fichas = []

    def __init__(self):
        self.winners = []
        self.list_states = []
        for i in range(10):
            for j in range(i + 1):
                self.fichas.append((i, j))
        pieces = self.fichas.copy()
        self.table = [(-1, -1)]
        shuffle(self.players)
        for p in self.players:
            p.fichas.clear()

        self.state = DominoesGameState(self.table, self.players)
        self.state.hand_round(pieces)

    def game(self):
        while True:
            for player in self.players:
                if len(self.table) != 1:
                    wins = self.state.is_game_over()
                    if wins is not False:
                        for winner in wins:
                            self.winners.append(winner)
                        return self.winners

                move, heads = player.jugar(self.state.head1, self.state.head2,
                                           *self.state.next_player(
                                               player).cant_move)
                new_table = self.state.move(DominoesMove(move), heads).table
                self.state = DominoesGameState(new_table, self.players)
                self.list_states.append(self.state)

    @staticmethod
    def reset_players_points(player_list: List[Jugador]):
        for plr in player_list:
            plr.points = 0


class Tournament:
    def __init__(self, data: Data):
        self.data = data

    def start(self):
        while not list(filter(lambda x: x.points >= 200, self.data.players)):
            data_winner = self.data.game()
            print(data_winner, data_winner[0].nombre, data_winner[0].points)

        winner = list(filter(lambda x: x.points >= 200, self.data.players))
        print(winner, winner[0].nombre, winner[0].points)
        self.data.reset_players_points(self.data.players)
        return winner


tournament_winners = []
for x in range(1000):
    play = Data()
    t = Tournament(play)
    tournament_winners.append(t.start()[0].nombre)
print(Counter(tournament_winners))
