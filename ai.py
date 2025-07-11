import json
import os
import copy
import random

WIN_REWARD = 1
LOSE_REWARD = -1
NO_REWARD = 0
Q_TABLE = {}

class AI:
    INITIAL_STATE_VALUE: int = 0
    DISCOUNT_FACTOR: float = 0.9
    LEARNING_RATE: float = 0.5

    def __init__(self, value_rep: str, train: bool = False):
        
        self.load_qtable()
        self.value_rep = value_rep
        self.train = train

    def get_board_state(self, board: list[list]):
        state = ""
        for x in board:
            for y in x:
                if not y:
                    state += "-"
                else:
                    if self.value_rep == y:
                        state += "1"
                    else:
                        state += "0"
        return state
    
    def get_action_state(self, board: list[list], action: tuple[int]):
        new_board = copy.deepcopy(board)
        x, y = action
        new_board[x][y] = self.value_rep
        return self.get_board_state(new_board)

    def get_possible_actions(self, board: list[list]):
        possible_actions : list[tuple] = []
        for x in range(3):
            for y in range(3):
                if board[x][y] == None:
                    possible_actions.append((x, y))
        return possible_actions
    
    def get_best_action(self, board, possible_actions):
        best_value = -1
        best_action: tuple = None

        if len(possible_actions) == 1:
            return possible_actions[0]

        if self.train:
            best_value = random.randint(0, len(possible_actions)-1)
            best_action = possible_actions[best_value]
        else:
            for action in possible_actions:
                action_state = self.get_action_state(board, action)

                if not action_state in Q_TABLE.keys():
                    Q_TABLE[action_state] = self.INITIAL_STATE_VALUE 


                action_value = Q_TABLE[action_state]
                if action_value > best_value:
                    best_value = action_value
                    best_action = action
        return best_action
    
    def get_next_move(self, board: list[list]):
        current_state = self.get_board_state(board)
        if not current_state in Q_TABLE.keys():
            Q_TABLE[current_state] = self.INITIAL_STATE_VALUE

        possible_actions = self.get_possible_actions(board)
        return self.get_best_action(board, possible_actions)
    
    def update_qtable(self, board: list[list], action: tuple[int], reward: int):
        if self.train:
            current_state = self.get_board_state(board)
            if not current_state in Q_TABLE:
                Q_TABLE[current_state] = self.INITIAL_STATE_VALUE
            current_value = Q_TABLE[current_state]

            new_state = self.get_action_state(board, action)
            if not new_state in Q_TABLE:
                Q_TABLE[new_state] = self.INITIAL_STATE_VALUE
            new_state_value = Q_TABLE[new_state]

            update_value = current_value + self.LEARNING_RATE * (reward + (self.DISCOUNT_FACTOR * new_state_value) - current_value )
            Q_TABLE[current_state] = update_value

            self.save_qtable()

    def save_qtable(self):
        with open("brain.json", "w") as file:
            file.write(json.dumps(Q_TABLE))

    def load_qtable(self):
        if not os.path.exists("brain.json"):
            loaded_qtable = {}
        else:
            with open("brain.json", "r") as file:
                loaded_qtable = json.loads(file.read())
        Q_TABLE = loaded_qtable