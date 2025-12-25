import arcade
from arcade.types import Color
from pathlib import Path
import math

WINDOW_TITLE = "Return of the Kingdom"
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900

SWORD_SPEED = 10
SWORD_MAX_ATTACK = 100
PLAYER_SWORD_SPEED = 10
PLAYER_SWORD_MAX_ATTACK = 150

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
        self.player_sword_list = arcade.SpriteList()
        self.player_health = 100
        self.max_health = 100
        self.heal_rate = 1
        self.heal_timer = 0

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
            x=100,
            y=100,
            color=arcade.csscolor.WHITE,
            font_size=18,
        )

        self.health_display = arcade.Text(
            f"Health: {self.player_health}/{self.max_health}",
            x=100,
            y=850,
            color=arcade.csscolor.WHITE,
            font_size=18,
        )

        self.health_table_background = arcade.SpriteSolidColor(
            width=200,
            height=20,
            color=arcade.color.DARK_RED
        )
        self.health_table_background.center_x = 200
        self.health_table_background.center_y = 860

        self.health_table = arcade.SpriteSolidColor(
            width=200,
            height=20,
            color=arcade.color.GREEN
        )
        self.health_table.center_x = 200
        self.health_table.center_y = 860
        self.gui_sprites = arcade.SpriteList()
        self.gui_sprites.append(self.health_table_background)
        self.gui_sprites.append(self.health_table)
        self.player_attack_cooldown = 0
        self.player_attack_max_cooldown = 60

    def create_scene(self):

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
            self.window.width / 2.0,
            tile_map.width * GRID_PIXEL_SIZE - self.window.width / 2.0,
            self.window.height / 2.0,
            tile_map.height * GRID_PIXEL_SIZE
        )

        return arcade.Scene.from_tilemap(tile_map)

    def reset(self):
        self.score = 0
        self.player_health = self.max_health
        self.scene = self.create_scene()
        self.scene.add_sprite("Player", self.player_sprite)
        for knigf in self.knigf_list:
            self.scene.add_sprite("knigf", knigf)
        self.scene.add_sprite_list("Swords")
        self.scene.add_sprite_list("PlayerSwords")
        self.update_health_table()

    def on_draw(self):
        self.clear()

        with self.camera_sprites.activate():
            self.scene.draw()
            self.sword_list.draw()
            self.player_sword_list.draw()

        with self.camera_gui.activate():
            self.gui_sprites.draw()
            self.score_display.text = f"Score: {self.score}"
            self.score_display.draw()

            self.health_display.text = f"Health: {self.player_health}/{self.max_health}"
            self.health_display.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            self.player_attack()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN or key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.D or key == arcade.key.A:
            self.player_sprite.change_x = 0

    def first_knigf(self):
        if len(self.knigf_list) == 0:
            return None

        first_knigf = None
        closest_distance = 100000000

        for knigf in self.knigf_list:
            distance = math.sqrt(
                (knigf.center_x - self.player_sprite.center_x) ** 2 +
                (knigf.center_y - self.player_sprite.center_y) ** 2
            )

            if distance < closest_distance:
                closest_distance = distance
                first_knigf = knigf

        return first_knigf

    def player_attack(self):
        if self.player_attack_cooldown > 0:
            return None

        first_knigf = self.first_knigf()

        if first_knigf == None:
            return None

        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y

        dest_x = first_knigf.center_x
        dest_y = first_knigf.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        sword = arcade.Sprite("assets/images/меч_1.png", scale=0.1)
        sword.center_x = start_x
        sword.center_y = start_y

        sword.start_x = start_x
        sword.start_y = start_y

        sword.angle = math.degrees(angle)

        sword.change_x = math.cos(angle) * PLAYER_SWORD_SPEED
        sword.change_y = math.sin(angle) * PLAYER_SWORD_SPEED

        self.player_sword_list.append(sword)

        self.player_attack_cooldown = self.player_attack_max_cooldown

    def take_damage(self, uron):

        self.player_health -= uron
        if self.player_health < 0:
            self.player_health = 0
            self.game_over()

        self.update_health_table()

    def game_over(self):  # сюда я в будущем добавлю окно проигрыша
        self.reset()

    def update_health_table(self):
        health_width = self.player_health / self.max_health
        self.health_table.width = 200 * health_width
        health_table_x = 200 - (200 - self.health_table.width) / 2
        self.health_table.center_x = health_table_x
        if health_width >= 0.5:
            self.health_table.color = arcade.color.GREEN
        elif health_width > 0.25:
            self.health_table.color = arcade.color.YELLOW
        else:
            self.health_table.color = arcade.color.RED

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

        self.heal_timer += delta_time
        if self.heal_timer >= 2 and self.player_health < self.max_health:
            self.player_health += self.heal_rate
            self.heal_timer = 0
            if self.player_health > self.max_health:
                self.player_health = self.max_health
            self.update_health_table()

        self.frame_count += 1

        if self.player_attack_cooldown > 0:
            self.player_attack_cooldown -= 1

        for knigf in self.knigf_list:
            if self.player_sprite.center_x < knigf.center_x:
                knigf.center_x -= KNIGF_MOVEMENT_SPEED
            elif self.player_sprite.center_x > knigf.center_x:
                knigf.center_x += KNIGF_MOVEMENT_SPEED
            if self.player_sprite.center_y < knigf.center_y:
                knigf.center_y -= KNIGF_MOVEMENT_SPEED
            elif self.player_sprite.center_y > knigf.center_y:
                knigf.center_y += KNIGF_MOVEMENT_SPEED

            start_x = knigf.center_x
            start_y = knigf.center_y
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

        for sword in self.sword_list:  # здесь я проверяю столкновение меча врага с игроком
            distance_traveled = math.sqrt(
                (sword.center_x - sword.start_x) ** 2 +
                (sword.center_y - sword.start_y) ** 2
            )

            if distance_traveled > SWORD_MAX_ATTACK:
                sword.remove_from_sprite_lists()

            if arcade.check_for_collision(self.player_sprite, sword):
                sword.remove_from_sprite_lists()
                self.take_damage(20)
        for sword in self.player_sword_list:
            distance_traveled = math.sqrt(
                (sword.center_x - sword.start_x) ** 2 +
                (sword.center_y - sword.start_y) ** 2
            )
            if distance_traveled > PLAYER_SWORD_MAX_ATTACK:
                sword.remove_from_sprite_lists()
                continue
            for knigf in self.knigf_list:  # Здесь я проверяю столкновение меча игрока с темным рыцарем
                if arcade.check_for_collision(sword, knigf):
                    sword.remove_from_sprite_lists()
                    knigf.remove_from_sprite_lists()
                    self.score += 10
                    break

        self.sword_list.update()
        self.player_sword_list.update()
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