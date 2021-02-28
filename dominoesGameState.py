from random import shuffle
from typing import List

from common import FourPlayersAbstractGameState, AbstractGameAction
from jugador import Jugador


class DominoesMove(AbstractGameAction):

    def __init__(self, value):
        self.value = value


class DominoesGameState(FourPlayersAbstractGameState):

    def __init__(self, state: List[tuple], players: List[Jugador]):
        self.table = state
        self.head1 = self.table[0][0]
        self.head2 = self.table[-1][-1]
        self.players = players

    def hand_round(self, pieces: list):
        shuffle(pieces)
        for i in range(10):
            for player in self.players:
                player.repartiendo(pieces.pop(0))

    @property
    def game_result(self):
        result = list(filter(lambda x: len(x.fichas) == 0, self.players))
        if result:
            result[0].points += sum([x.sum() for x in self.players])
            return result
        early_stop = []
        for player in self.players:
            pieces = []
            for f in player.fichas:
                pieces.append(f[0])
                pieces.append(f[1])
            if self.table[0][0] not in pieces and \
                    self.table[-1][-1] not in pieces:
                early_stop.append(player)

        if len(early_stop) == len(self.players):
            winner = min(self.players, key=lambda x: x.sum())
            winner.points += sum([x.sum() for x in self.players if x != winner])
            return [winner]

    def is_move_legal(self, move):
        if move[0] == self.head1 or move[0] == self.head2 or \
                move[1] == self.head1 or move[1] == self.head2:
            return True
        return False

    def is_game_over(self):
        game_result = self.game_result
        return game_result if game_result is not None else False

    def move(self, move: DominoesMove, *head):
        if self.head1 == -1 and self.head2 == -1:
            self.head1, self.head2 = move.value
            self.table.clear()
            new_table = self.table.copy()
            new_table.append(move.value)

            return DominoesGameState(new_table, self.players)
        else:
            if not move.value or not self.is_move_legal(move.value):
                return DominoesGameState(self.table, self.players)
            else:
                new_table = self.table.copy()
                if head[0] != -1:
                    if head[0] == self.head1:
                        if move.value[0] == self.head1:
                            new_table.insert(0, move.value[-1::-1])
                        else:
                            new_table.insert(0, move.value)
                    else:
                        if move.value[0] == self.head2:
                            new_table.append(move.value)
                        else:
                            new_table.append(move.value[-1::-1])
                else:
                    if move.value[0] == self.head1:
                        new_table.insert(0, move.value[-1::-1])
                    elif move.value[1] == self.head1:
                        new_table.insert(0, move.value)
                    elif move.value[0] == self.head2:
                        new_table.append(move.value)
                    elif move.value[1] == self.head2:
                        new_table.append(move.value[-1::-1])

                return DominoesGameState(new_table, self.players)

    def get_legal_actions(self, pieces):
        return [DominoesMove(x) for x in pieces if self.head1 in x or
                self.head2 in x]

    def next_player(self, actual):
        pos_actual = self.players.index(actual)
        if pos_actual + 1 > len(self.players) - 1:
            return self.players[0]
        else:
            return self.players[pos_actual + 1]
