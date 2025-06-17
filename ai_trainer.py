import ai
import time

NUM_GRID = 3
initiator = 'X'

class AI_Trainer:
    def __init__(self):
        ai_ = ai.AI(representation='X', train=True, q_table_file="AI_X.json")
        opponent = ai.AI(representation='O', train=True, q_table_file="AI_O.json")
        self.ai_players = [ai_, opponent]
        self.board = [[None for _ in range(NUM_GRID)] for _ in range(NUM_GRID)]
        self.curr_player = initiator
        self.thinking = False

    def reset_game(self):
        global initiator
        self.board = [[None for _ in range(NUM_GRID)] for _ in range(NUM_GRID)]
        self.curr_player = 'X' if initiator == 'O' else 'O'
        initiator = self.curr_player
        self.thinking = False

    def has_player_won(self):
        horizontal_match = False
        vertical_match = False
        diagonal_match = False

        # Check for Horizontal Match
        for x in range(NUM_GRID):
            horizontal_match = False            
            for y in range(NUM_GRID):
                if self.board[x][y] == self.curr_player:
                    horizontal_match = True
                else:
                    horizontal_match = False
                    if x == y:
                        diagonal_match = False
                    break
            if horizontal_match:
                break
        
        if not horizontal_match:
            # Check for Vertical Match              
            for y in range(NUM_GRID):
                vertical_match = False
                for x in range(NUM_GRID):
                    if self.board[x][y] == self.curr_player:
                        vertical_match = True
                    else:
                        vertical_match = False
                        break
                if vertical_match:
                    break
            
            if not vertical_match:
                diagonal_match = False
                # Check for Diagonal Match left to right
                for point in range(NUM_GRID):
                    if self.board[point][point] == self.curr_player:
                        diagonal_match = True
                    else:
                        diagonal_match = False
                        break
                
                if not diagonal_match:
                    # Check for Diagonal Match right to left
                    for point in range(NUM_GRID):
                        if self.board[point][2-point] == self.curr_player:
                            diagonal_match = True
                        else:
                            diagonal_match = False
                            break

        if vertical_match or horizontal_match or diagonal_match:
            return True
    
        return False
    
    def change_player(self):
        if self.curr_player == "X":
            self.curr_player = "O"
        else:
            self.curr_player = "X"

    def is_draw(self):
        """
        Check if the game is a draw.
        A draw occurs when the board is full and no player has won.
        """
        for row in self.board:
            if None in row:
                return False
        return not self.has_player_won()
    
    def ai_thinking(self):
        """
        Simulate AI thinking time.
        """
        self.thinking = True
        for ai_player in self.ai_players:
            if ai_player and ai_player.representation == self.curr_player:
                # AI's turn to play
                action = ai_player.get_action(self.board)
                if action:
                    x, y = action
                    prev_board = self.board.copy()
                    if not self.board[x][y]:
                        self.board[x][y] = self.curr_player
                        if not self.has_player_won():
                            ai_player.update_q_table(prev_board, action, ai.NO_REWARD)                                
                            self.change_player()
                        else:
                            ai_player.update_q_table(prev_board, action, ai.WIN_REWARD)
                            for other_ai_player in self.ai_players:
                                if other_ai_player.representation != self.curr_player:
                                    other_ai_player.update_q_table(prev_board, action, ai.LOSE_REWARD)


if __name__ == "__main__":
    # Initialize the AI trainer with a specified number of episodes
    start = time.time()
    episodes=10000
    trainer = AI_Trainer()
    def train_ai():
        for episode in range(episodes):
            trainer.reset_game()
            while not trainer.has_player_won() and not trainer.is_draw():
                # AI thinking process
                trainer.ai_thinking()
            print(f"Episode {episode + 1}/{episodes} completed.")
    train_ai()
    stop = time.time()
    print(f"Training time: {stop - start} seconds")
    print("AI training finished.")