from abc import abstractmethod, ABC


class FourPlayersAbstractGameState(ABC):

    @abstractmethod
    def game_result(self):
        """
        this property should return:
        a list with all the player winner in case of draw
        else a lis with one player
        Returns
        -------
         List[Jugador]

        """
        pass

    @abstractmethod
    def is_game_over(self):
        """
        boolean indicating if the game is over,
        simplest implementation may just be
        `return self.game_result() is not None`

        Returns
        -------
        boolean

        """
        pass

    @abstractmethod
    def move(self, action):
        """
        consumes action and returns resulting FourPlayersAbstractGameState

        Parameters
        ----------
        action: AbstractGameAction

        Returns
        -------
        FourPlayersAbstractGameState

        """
        pass

    @abstractmethod
    def get_legal_actions(self, pieces: list) -> list:
        """
        returns list of legal action at current game state
        Returns
        -------
        list of AbstractGameAction

        """
        pass


class AbstractGameAction(ABC):
    pass
