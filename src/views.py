import arcade
from arcade.gui import UIManager, UITextureButton, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from pyglet.graphics import Batch
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class OverMenuView(arcade.View):
    def __init__(self, score=0, level=1):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        self.score = score
        self.level = level
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        if self.level == 3:
            label = UILabel(text=f"ВЫ ПРОШЛИ ИГРУ:",
                            font_size=20,
                            text_color=arcade.color.GOLD,
                            width=300,
                            align="center")
            self.box_layout.add(label)
        label = UILabel(text=f"ВАШ СЧЁТ: {self.score}",
                        font_size=20,
                        text_color=arcade.color.GOLD,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")
        if self.level < 3:
            next_level_button = UITextureButton(
                text=f"Следующий уровень {self.level + 1}",
                texture=texture_normal,
                texture_hovered=texture_hovered,
                texture_pressed=texture_pressed,
                scale=1.0
            )
            next_level_button.on_click = lambda e: self.next_level_button(e)
            self.box_layout.add(next_level_button)

        end_button = UITextureButton(text="Выйти из игры",
                                     texture=texture_normal,
                                     texture_hovered=texture_hovered,
                                     texture_pressed=texture_pressed,
                                     scale=1.0)
        self.box_layout.add(end_button)
        end_button.on_click = self.end_game

        sellect_button = UITextureButton(text="Выбрать уровень",
                                         texture=texture_normal,
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         scale=1.0)
        sellect_button.on_click = self.level_select_button
        self.box_layout.add(sellect_button)

    def next_level_button(self, event):
        from src.game import GameView # простите но если так не сделать будет круговой импорт
        game_view = GameView(final_score=self.score)
        game_view.current_level = self.level + 1
        game_view.reload()
        self.window.show_view(game_view)

    def level_select_button(self, event):
        level_view = LevelSelectView()
        self.window.show_view(level_view)


    def on_draw(self):
        self.clear()
        self.manager.draw()

    def end_game(self, button_text):
        arcade.exit()


class LevelSelectView(arcade.View):
    def __init__(self, score=0):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        self.score = score
        self.manager = UIManager()
        self.manager.enable()
        self.setup_widgets()

    def setup_widgets(self):
        layout = UIBoxLayout(vertical=True, space_between=10)
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")

        title = UILabel(
            text=f"УРОВНИ",
            font_size=32,
            text_color=arcade.color.GOLD,
            width=400,
            align="center"
        )
        layout.add(title)

        for level_num in range(1, 4):
            level_text = f"Уровень {level_num}"
            button = UITextureButton(
                text=level_text,
                texture=texture_normal,
                texture_hovered=texture_hovered,
                texture_pressed=texture_pressed,
                width=250,
                height=100
            )
            button.on_click = lambda e, num=level_num: self.start_level(num)
            layout.add(button)

        back_button = UITextureButton(
            text="Вернуться в меню",
            texture=texture_normal,
            texture_hovered=texture_hovered,
            texture_pressed=texture_pressed,
            width=200,
            height=50
        )
        back_button.on_click = self.back_to_menu
        layout.add(back_button)

        anchor = UIAnchorLayout()
        anchor.add(layout)
        self.manager.add(anchor)

    def start_level(self, level_num):
        from src.game import GameView
        game_view = GameView(final_score=self.score)
        game_view.current_level = level_num
        game_view.reload()
        self.window.show_view(game_view)

    def back_to_menu(self, event):
        menu_view = MenuView()
        self.window.show_view(menu_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        label = UILabel(text="Привет, Это игра Return of the Kingdom",
                        font_size=20,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(label)
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")
        start_button = UITextureButton(text="Начать игру",
                                       texture=texture_normal,
                                       texture_hovered=texture_hovered,
                                       texture_pressed=texture_pressed,
                                       scale=1.5)
        self.box_layout.add(start_button)
        start_button.on_click = self.start_game
        end_button = UITextureButton(text="Выйти из игры",
                                     texture=texture_normal,
                                     texture_hovered=texture_hovered,
                                     texture_pressed=texture_pressed,
                                     scale=1.5)
        self.box_layout.add(end_button)

        end_button.on_click = self.end_game
        sellect_button = UITextureButton(text="Выбрать уровень",
                                         texture=texture_normal,
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         scale=1.5)
        self.box_layout.add(sellect_button)
        sellect_button.on_click = self.level_select_button


    def level_select_button(self, event):
        level_view = LevelSelectView()
        self.window.show_view(level_view)


    def on_draw(self):
        self.clear()
        self.manager.draw()

    def end_game(self, button_text):
        arcade.exit()

    def start_game(self, button_text):
        from src.game import GameView
        game_view = GameView(final_score=0)
        game_view.reload()
        self.window.show_view(game_view)


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.batch = Batch()
        self.pause_text = arcade.Text("Пауза", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                                      arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми SPACE, чтобы продолжить", WINDOW_WIDTH / 2,
                                      WINDOW_HEIGHT / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(self.game_view)