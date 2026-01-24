import arcade
from src.views import MenuView
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    start_menu = MenuView()
    window.show_view(start_menu)
    arcade.run()

if __name__ == "__main__":
    main()