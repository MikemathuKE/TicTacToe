"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
WINDOW_TITLE = "TIC TAC TOE"

SQUARE_SPACING = 300
SQUARE_WIDTH = 300
SQUARE_HEIGHT = 300

FONT_SIZE = 200
FONT_SPACING = 50

NUM_GRID = 3

class MenuView(arcade.View):
    def on_show_view(self):
        self.window.background_color = arcade.color.WHITE

    def on_draw(self):
        self.clear()
        arcade.draw_text("TIC TAC TOE", WINDOW_WIDTH / 2, WINDOW_WIDTH / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to Play.", WINDOW_WIDTH / 2, WINDOW_WIDTH / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game = GameView()
        self.window.show_view(game)


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        self.window.background_color = arcade.color.ORANGE

    def on_draw(self):
        self.clear()
        arcade.draw_text("PAUSED", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         WINDOW_WIDTH / 2,
                         WINDOW_HEIGHT / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Enter to reset",
                         WINDOW_WIDTH / 2,
                         WINDOW_HEIGHT / 2 - 30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # reset game
            game = GameView()
            self.window.show_view(game)

class GameOverView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        self.window.background_color = arcade.color.ORANGE

    def on_draw(self):
        self.clear()
        arcade.draw_text(f"{self.game_view.curr_player} has Won!!", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Enter to reset",
                         WINDOW_WIDTH / 2,
                         WINDOW_HEIGHT / 2 - 30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ENTER:  # reset game
            game = GameView()
            self.window.show_view(game)

class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.GRAY
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.curr_player = "X"

        # If you have sprite lists, you should create them here,
        # and set them to None

    def change_player(self):
        if self.curr_player == "X":
            self.curr_player = "O"
        else:
            self.curr_player = "X"

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
            gameoverview = GameOverView(self)
            self.window.show_view(gameoverview)
            return True
    
        return False
        

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # --- Draw all the grids
        for x in range(0, WINDOW_WIDTH, SQUARE_SPACING):
            for y in range(0, WINDOW_HEIGHT, SQUARE_SPACING):
                arcade.draw_rect_outline(arcade.rect.XYWH(x + SQUARE_WIDTH/2, y + SQUARE_HEIGHT/2, SQUARE_WIDTH, SQUARE_HEIGHT),
                                        arcade.color.WHITE, 1)
                
        
                
        # Print the timing
        for x in range(3):
            for y in range(3):
                if self.board[x][2-y]:
                    arcade.draw_text(self.board[x][2-y], (x * SQUARE_WIDTH) + FONT_SPACING , (y * SQUARE_HEIGHT) + FONT_SPACING, arcade.color.YELLOW, FONT_SIZE)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """

        if button == arcade.MOUSE_BUTTON_LEFT:
            for x_grid in range(NUM_GRID):
                for y_grid in range(NUM_GRID):
                    if (x >= x_grid * SQUARE_WIDTH) and (x < (x_grid*SQUARE_WIDTH) + SQUARE_WIDTH) and (y >= y_grid * SQUARE_HEIGHT) and (y < (y_grid * SQUARE_HEIGHT)+ SQUARE_HEIGHT):
                        if not self.board[x_grid][2-y_grid]:
                            self.board[x_grid][2-y_grid] = self.curr_player
                            if not self.has_player_won():
                                self.change_player()

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    menu = MenuView()

    # Show GameView on screen
    window.show_view(menu)

    # Start the arcade game loop
    arcade.run()



if __name__ == "__main__":
    main()