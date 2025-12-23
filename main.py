
import arcade
from arcade.types import Color
from pathlib import Path
import math


WINDOW_TITLE = "Return of the Kingdom"
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900

SWORD_SPEED = 10
SWORD_MAX_ATTAK = 100


CHARACTER_SCALING = 1
TILE_SCALING = 2.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING * 2
KNIGF_MOVEMENT_SPEED = 1

PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 0


FOLLOW_DECAY_CONST = 0.1
MOVEMENT_SPEED = 5


class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        self.sword_list = arcade.SpriteList()

        self.frame_count = 0

        self.player_texture = arcade.load_texture("assets/images/рыцарь.png")
        self.knigf_texture = arcade.load_texture("assets/images/темный_рыцарь.png")
        self.tile_map = None

        self.camera_sprites = arcade.Camera2D()

        self.camera_bounds = self.window.rect

        self.camera_gui = arcade.Camera2D()

        self.scene = self.create_scene()

        self.player_sprite = arcade.Sprite(self.player_texture, scale=0.2)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.knigf_list = arcade.SpriteList()
        knigf_sprite = arcade.Sprite(self.knigf_texture, scale=0.5)
        knigf_sprite.center_x = 500
        knigf_sprite.center_y = 500
        self.knigf_list.append(knigf_sprite)
        knigf_sprite = arcade.Sprite(self.knigf_texture, scale=0.5)
        knigf_sprite.center_x = 200
        knigf_sprite.center_y = 200
        self.knigf_list.append(knigf_sprite)
        self.player_sprite.change_x = 0



        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["castle1"]
        )

        self.score = 0

        self.left_key_down = False
        self.right_key_down = False
        self.left_key_up = False

        self.score_display = arcade.Text(
            "Score: 0",
            x=10,
            y=10,
            color=arcade.csscolor.WHITE,
            font_size=18,
        )

    def create_scene(self) -> arcade.Scene:

        map_path = Path("assets/maps/map_4.tmx")

        layer_options = {
            "castle1": {
                "use_spatial_hash": True,
            },
        }
        tile_map = arcade.load_tilemap(
            map_path,
            scaling=TILE_SCALING,
            layer_options=layer_options,
        )

        if tile_map.background_color:
            self.window.background_color = Color.from_iterable(tile_map.background_color)


        self.camera_bounds = arcade.LRBT(
            self.window.width/2.0,
            tile_map.width * GRID_PIXEL_SIZE - self.window.width/2.0,
            self.window.height/2.0,
            tile_map.height * GRID_PIXEL_SIZE
        )



        return arcade.Scene.from_tilemap(tile_map)

    def reset(self):

        self.score = 0

        self.scene = self.create_scene()

        self.scene.add_sprite("Player", self.player_sprite)
        for j in self.knigf_list:
            self.scene.add_sprite("Knigf", j)

        self.scene.add_sprite_list("Swords")

    def on_draw(self):


        self.clear()

        with self.camera_sprites.activate():
            self.scene.draw()
            self.sword_list.draw()

        with self.camera_gui.activate():
            self.score_display.text = f"Score: {self.score}"
            self.score_display.draw()

    def update_player_speed(self):


        if self.left_key_down and not self.right_key_down:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_key_down and not self.left_key_down:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED




    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED



    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.DOWN or key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.D or key == arcade.key.A:
            self.player_sprite.change_x = 0



    def center_camera_to_player(self):
        self.camera_sprites.position = arcade.math.smerp_2d(
            self.camera_sprites.position,
            self.player_sprite.position,
            self.window.delta_time,
            FOLLOW_DECAY_CONST,
        )

        self.camera_sprites.view_data.position = arcade.camera.grips.constrain_xy(
            self.camera_sprites.view_data, self.camera_bounds
        )

    def on_update(self, delta_time: float):
        self.frame_count += 1
        for i in self.knigf_list:
            if self.player_sprite.center_x < i.center_x:
                i.center_x -= KNIGF_MOVEMENT_SPEED
            elif self.player_sprite.center_x > i.center_x:
                i.center_x += KNIGF_MOVEMENT_SPEED
            if self.player_sprite.center_y < i.center_y:
                i.center_y -= KNIGF_MOVEMENT_SPEED
            elif self.player_sprite.center_y > i.center_y:
                i.center_y += KNIGF_MOVEMENT_SPEED
            start_x = i.center_x
            start_y = i.center_y


            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y


            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = -math.atan2(y_diff, x_diff) + 3.14 / 2
            if self.frame_count % 60 == 0:
                sword = arcade.Sprite("assets/images/меч_1.png", scale=0.1)
                sword.center_x = start_x
                sword.center_y = start_y

                sword.start_x = start_x
                sword.start_y = start_y

                sword.angle = math.degrees(angle) - 90

                sword.change_x = math.sin(angle) * SWORD_SPEED
                sword.change_y = math.cos(angle) * SWORD_SPEED

                self.sword_list.append(sword)
        for sword in self.sword_list:
            distance_traveled = math.sqrt(
                (sword.center_x - sword.start_x) ** 2 +
                (sword.center_y - sword.start_y) ** 2
            )

            if distance_traveled > SWORD_MAX_ATTAK:
                sword.remove_from_sprite_lists()
            if arcade.check_for_collision(self.player_sprite, sword):
                print("Collision detected!")

        self.sword_list.update()




        self.physics_engine.update()


        self.center_camera_to_player()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.camera_sprites.match_window()
        self.camera_gui.match_window(position=True)


def main():

    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    game.reset()

    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()