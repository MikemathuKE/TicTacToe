import os
import json
import random

Q_TABLE_FILE = "q_table.json"
WIN_REWARD = 1
LOSE_REWARD = -1
NO_REWARD = 0
DISCOUNT_FACTOR = 0.9
LEARNING_RATE = 0.1

class AI:
    def __init__(self, representation: str, train: bool = False, learning_rate=LEARNING_RATE, disount_factor=DISCOUNT_FACTOR, q_table_file: str = Q_TABLE_FILE):
        self.q_table_file = q_table_file
        self.load_q_table()
        self.train = train
        self.name = "AI"
        self.representation = representation
        self.learning_rate = learning_rate
        self.discount_factor = disount_factor
        self.first_move = True

    def load_q_table(self):
        """Load the Q-table from a file."""
        if os.path.exists(self.q_table_file):
            with open(self.q_table_file, 'r') as file:
                self.q_table = json.load(file)
        else:
            self.q_table = {}


    def save_q_table(self):
        """Save the Q-table to a file."""
        with open(self.q_table_file, 'w') as file:
            json.dump(self.q_table, file, indent=4)

    def decode_state(self, board):
        """Convert the board state into a string representation."""
        representation = ""
        for row in board:
            for cell in row:
                if cell is None:
                    representation += '-'
                else:
                    representation += '1' if cell == self.representation else '0'
        return representation
    
    def get_available_actions(self, board):
        """Get a list of valid actions based on the current board state."""
        return [(i, j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] is None]
    
    def random_action(self, board):
        """Choose a random valid action from the available moves."""
        available_moves = self.get_available_actions(board)
        if available_moves:
            selected=available_moves[random.randint(0, len(available_moves) - 1)]
            return selected
        
        return None
    
    def decode_action(self, state, action):
        """Convert an action tuple into a string representation."""
        state_list = list(state)
        state_list[action[0] * 3 + action[1]] = "1"
        new_state = ''.join(state_list)
        if new_state not in self.q_table:
            self.q_table[new_state] = 0
        return new_state
    
    def best_action(self, state, available_actions):
        """Get the best action based on the Q-table for the current board state."""
        
        best_action = max(available_actions, key=lambda action: self.q_table.get(self.decode_action(state, action)))
        return best_action
    
    def get_action(self, board):
        """Get the best action for the current board state."""
        state = self.decode_state(board)
        if state not in self.q_table:
            self.q_table[state] = 0

        if self.train or self.first_move:
            # Training mode: choose a random action
            self.first_move = False
            return self.random_action(board)
        
        else:
            # Inference mode: choose the best action based on Q-values
            available_actions = self.get_available_actions(board)
            if not available_actions:
                return None
            
            best_action = self.best_action(state, available_actions)
            return best_action
        
    def update_q_table(self, board, action, reward):
        """Update the Q-table based on the action taken and the reward received."""

        state = self.decode_state(board)
        if state not in self.q_table:
            self.q_table[state] = 0

        new_state = self.decode_action(state, action)
        if new_state not in self.q_table:
            self.q_table[new_state] = reward
        
        # Update the Q-value for the state-action pair
        self.q_table[state] += self.learning_rate * (reward + self.discount_factor * self.q_table[new_state] - self.q_table[state])
        
        # Save the updated Q-table
        self.save_q_table()

