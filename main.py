import arcade
from arcade.types import Color
from pathlib import Path
from pyglet.graphics import Batch
import math

WINDOW_TITLE = "Return of the Kingdom"
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900

SWORD_SPEED = 10
SWORD_MAX_ATTACK = 100
PLAYER_SWORD_SPEED = 10
PLAYER_SWORD_MAX_ATTACK = 200
KNIGF_HEALTH = 100
SKELETON_HEALTH = 50
PLAYER_SWORD_DAMAGE = 50
SKELETON_SWORD_DAMAGE = 15

BOSS_SWORD_MAX_ATTACK = 500

TILE_SCALING = 2.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING * 2
KNIGF_MOVEMENT_SPEED = 1
SKELETON_MOVEMENT_SPEED = 0.8

GRAVITY = 0

FOLLOW_DECAY_CONST = 0.1
MOVEMENT_SPEED = 5

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.batch = Batch()
        self.pause_text = arcade.Text("Пауза", self.window.width / 2, self.window.height / 2,
                                      arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми SPACE, чтобы продолжить", self.window.width / 2,
                                      self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(self.game_view)

class Enemy(arcade.Sprite):
    def __init__(self, texture, scale=0.5, health=100, damage=20, attack_cooldown=60, attack_range=300, sword_max_range=SWORD_MAX_ATTACK):
        super().__init__(texture, scale=scale)
        self.health = health
        self.max_health = health
        self.damage = damage
        self.attack_cooldown = attack_cooldown
        self.current_cooldown = 0
        self.is_alive = True
        self.attack_range = attack_range
        self.sword_max_range = sword_max_range

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            return True
        return False

    def update_cooldown(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def can_attack(self):
        return self.is_alive and self.current_cooldown == 0

    def coldown(self):
        self.current_cooldown = self.attack_cooldown


class EnemySword(arcade.Sprite):
    def __init__(self, texture, scale, damage, max_range=SWORD_MAX_ATTACK):
        super().__init__(texture, scale=scale)
        self.damage = damage
        self.start_x = 0
        self.start_y = 0
        self.max_range = max_range


class Boss(Enemy):
    def __init__(self, texture):
        super().__init__(texture, scale=1.5, health=400, damage=10, attack_cooldown=180,
                         attack_range=1000, sword_max_range=BOSS_SWORD_MAX_ATTACK)
        self.movement_speed = 0.1
        self.sword_texture = "assets/images/меч_1.png"
        self.sword_scale = 0.4
        self.sword_speed = 10
        self.enemy_type = "boss"
        self.score_value = 300


class Ghost(Enemy):
    def __init__(self, texture):
        super().__init__(texture, scale=0.3, health=120, damage=10, attack_cooldown=60, attack_range=300)
        self.movement_speed = KNIGF_MOVEMENT_SPEED
        self.sword_texture = "assets/images/меч_1.png"
        self.sword_scale = 0.1
        self.sword_speed = SWORD_SPEED
        self.enemy_type = "ghost"
        self.score_value = 15


class Goblin(Enemy):
    def __init__(self, texture, scale=0.5):
        super().__init__(texture, scale=scale, health=80, damage=10, attack_cooldown=60, attack_range=300)
        self.movement_speed = KNIGF_MOVEMENT_SPEED
        self.sword_texture = "assets/images/меч_1.png"
        self.sword_scale = 0.05
        self.sword_speed = SWORD_SPEED
        self.enemy_type = "goblin"
        self.score_value = 15


class Knigf(Enemy):
    def __init__(self, texture, scale=0.5):
        super().__init__(texture, scale=scale, health=KNIGF_HEALTH, damage=20, attack_cooldown=60, attack_range=300)
        self.movement_speed = KNIGF_MOVEMENT_SPEED
        self.sword_texture = "assets/images/меч_1.png"
        self.sword_scale = 0.1
        self.sword_speed = SWORD_SPEED
        self.enemy_type = "knigf"
        self.score_value = 15


class Spider(Enemy):
    def __init__(self, texture, scale=0.5):
        super().__init__(texture, scale=scale, health=25, damage=5, attack_cooldown=30, attack_range=300)
        self.movement_speed = 1.5
        self.sword_texture = "assets/images/паутина1.png"
        self.sword_scale = 0.1
        self.sword_speed = SWORD_SPEED
        self.enemy_type = "spider"
        self.score_value = 5


class Skeleton(Enemy):
    def __init__(self, texture, scale=0.5):
        super().__init__(texture, scale=scale, health=SKELETON_HEALTH,
                         damage=SKELETON_SWORD_DAMAGE, attack_cooldown=90, attack_range=300)
        self.movement_speed = SKELETON_MOVEMENT_SPEED
        self.sword_texture = "assets/images/кост_меч.png"
        self.sword_scale = 0.3
        self.sword_speed = SWORD_SPEED * 0.8
        self.enemy_type = "skeleton"
        self.score_value = 5

class Poison(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("assets/images/зелье.png", scale=0.3)
        self.center_x = x
        self.center_y = y

class New_sword(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("assets/images/меч_1.png", scale=0.1)
        self.center_x = x
        self.center_y = y


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.sword_sound = arcade.Sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.Sound(":resources:sounds/hit2.wav")
        self.pickup_sound = arcade.Sound(":resources:sounds/coin1.wav")
        self.sword_list = arcade.SpriteList()
        self.player_sword_list = arcade.SpriteList()
        self.player_health = 1000
        self.max_health = 1000
        self.heal_rate = 1
        self.heal_timer = 0
        self.player_damage = PLAYER_SWORD_DAMAGE

        self.frame_count = 0


        self.player_texture = arcade.load_texture("assets/images/рыцарь.png")
        self.knigf_texture = arcade.load_texture("assets/images/темный_рыцарь.png")
        self.skeleton_texture = arcade.load_texture("assets/images/скелет.png")
        self.spider_texture = arcade.load_texture("assets/images/паук.png")
        self.goblin_texture = arcade.load_texture("assets/images/гоблин.png")
        self.ghost_texture = arcade.load_texture("assets/images/призрак.png")
        self.boss_texture = arcade.load_texture("assets/images/темный_рыцарь.png")

        self.camera_sprites = arcade.Camera2D()
        self.camera_bounds = self.window.rect
        self.camera_gui = arcade.Camera2D()

        self.scene = self.create_scene()

        self.player_sprite = arcade.Sprite(self.player_texture, scale=0.2)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128

        self.player_sprite.change_x = 0

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["castle1"]
        )

        self.score = 0


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

    def reload(self):
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.score = 0
        self.player_health = self.max_health
        self.scene = self.create_scene()
        self.scene.add_sprite("Player", self.player_sprite)
        self.new_sword_list = arcade.SpriteList()
        new_sword_sprite = New_sword(600, 600)
        self.new_sword_list.append(new_sword_sprite)
        for i in self.new_sword_list:
            self.scene.add_sprite("New_sword", i)
        self.poison_list = arcade.SpriteList()
        poison_sprite = Poison(700,700)
        self.poison_list.append(poison_sprite)
        for i in self.poison_list:
            self.scene.add_sprite("Poison", i)

        self.all_enemies = arcade.SpriteList()
        goblin_sprite = Goblin(self.goblin_texture, scale=0.2)
        goblin_sprite.center_x = 1000
        goblin_sprite.center_y = 1000
        self.all_enemies.append(goblin_sprite)

        spider_sprite = Spider(self.spider_texture, scale=0.1)
        spider_sprite.center_x = 800
        spider_sprite.center_y = 800
        self.all_enemies.append(spider_sprite)

        boss_sprite = Boss(self.boss_texture)
        boss_sprite.center_x = 1200
        boss_sprite.center_y = 1600
        self.all_enemies.append(boss_sprite)

        ghost_sprite = Ghost(self.ghost_texture)
        ghost_sprite.center_x = 800
        ghost_sprite.center_y = 400
        self.all_enemies.append(ghost_sprite)

        knigf_sprite = Knigf(self.knigf_texture, scale=0.5)
        knigf_sprite.center_x = 500
        knigf_sprite.center_y = 500
        self.all_enemies.append(knigf_sprite)

        knigf_sprite = Knigf(self.knigf_texture, scale=0.5)
        knigf_sprite.center_x = 200
        knigf_sprite.center_y = 200
        self.all_enemies.append(knigf_sprite)

        skeleton_sprite = Skeleton(self.skeleton_texture, scale=0.04)
        skeleton_sprite.center_x = 300
        skeleton_sprite.center_y = 300
        self.all_enemies.append(skeleton_sprite)

        skeleton_sprite = Skeleton(self.skeleton_texture, scale=0.04)
        skeleton_sprite.center_x = 400
        skeleton_sprite.center_y = 400
        self.all_enemies.append(skeleton_sprite)

        skeleton_sprite = Skeleton(self.skeleton_texture, scale=0.04)
        skeleton_sprite.center_x = 600
        skeleton_sprite.center_y = 600
        self.all_enemies.append(skeleton_sprite)

        for enemy in self.all_enemies: # добавление в сцену
            self.scene.add_sprite(enemy.enemy_type, enemy)

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
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN or key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.D or key == arcade.key.A:
            self.player_sprite.change_x = 0

    def first_monstr(self):
        first_enemy = None
        closest_distance = 100000000

        for enemy in self.all_enemies:
            if not enemy.is_alive:
                continue

            distance = math.sqrt(
                (enemy.center_x - self.player_sprite.center_x) ** 2 +
                (enemy.center_y - self.player_sprite.center_y) ** 2
            )

            if distance < closest_distance:
                closest_distance = distance
                first_enemy = enemy

        return first_enemy

    def player_attack(self): # создание меча игрока
        if self.player_attack_cooldown > 0:
            return None

        first_enemy = self.first_monstr()

        if first_enemy is None:
            return None

        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y

        dest_x = first_enemy.center_x
        dest_y = first_enemy.center_y

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
        arcade.play_sound(self.sword_sound)

    def take_damage(self, uron):
        self.player_health -= uron
        arcade.play_sound(self.hit_sound)
        if self.player_health < 0:
            self.player_health = 0
            self.game_over()

        self.update_health_table()

    def game_over(self):
        self.reload()

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

    def enemy_attack(self, enemy):
        if not enemy.is_alive:
            return

        start_x = enemy.center_x
        start_y = enemy.center_y
        dest_x = self.player_sprite.center_x
        dest_y = self.player_sprite.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = -math.atan2(y_diff, x_diff) + 3.14 / 2
        sword = EnemySword(enemy.sword_texture, scale=enemy.sword_scale,
                          damage=enemy.damage, max_range=enemy.sword_max_range)
        sword.center_x = start_x
        sword.center_y = start_y

        sword.start_x = start_x
        sword.start_y = start_y

        sword.angle = math.degrees(angle) - 90

        sword.change_x = math.sin(angle) * enemy.sword_speed
        sword.change_y = math.cos(angle) * enemy.sword_speed

        self.sword_list.append(sword)
        enemy.coldown()

    def dead_enemies_del(self):
        for i in self.all_enemies:
            if not i.is_alive and i in self.all_enemies:
                self.all_enemies.remove(i)
                i.remove_from_sprite_lists()

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

        for i in self.all_enemies:
            if not i.is_alive:
                continue

            i.update_cooldown()

            if self.player_sprite.center_x < i.center_x:
                i.center_x -= i.movement_speed
            elif self.player_sprite.center_x > i.center_x:
                i.center_x += i.movement_speed
            if self.player_sprite.center_y < i.center_y:
                i.center_y -= i.movement_speed
            elif self.player_sprite.center_y > i.center_y:
                i.center_y += i.movement_speed

            if i.can_attack():
                distance_to_player = math.sqrt(
                    (i.center_x - self.player_sprite.center_x) ** 2 +
                    (i.center_y - self.player_sprite.center_y) ** 2
                )

                if distance_to_player < i.attack_range:
                    self.enemy_attack(i)

        for sword in self.sword_list:
            distance_traveled = math.sqrt(
                (sword.center_x - sword.start_x) ** 2 +
                (sword.center_y - sword.start_y) ** 2
            )
            if distance_traveled > sword.max_range:
                sword.remove_from_sprite_lists()
                continue

            if arcade.check_for_collision(self.player_sprite, sword):
                sword.remove_from_sprite_lists()
                damage_amount = sword.damage
                self.take_damage(damage_amount)

        for sword in self.player_sword_list:
            distance_traveled = math.sqrt(
                (sword.center_x - sword.start_x) ** 2 +
                (sword.center_y - sword.start_y) ** 2
            )
            if distance_traveled > PLAYER_SWORD_MAX_ATTACK:
                sword.remove_from_sprite_lists()
                continue

            for j in self.all_enemies:
                if not j.is_alive:
                    continue

                if arcade.check_for_collision(sword, j):
                    sword.remove_from_sprite_lists()


                    dead = j.take_damage(self.player_damage)

                    if dead:
                        j.is_alive = False
                        self.dead_enemies_del()
                        self.score += j.score_value

                    break

        for i in self.poison_list:
            if arcade.check_for_collision(self.player_sprite, i):
                arcade.play_sound(self.pickup_sound)

                if self.max_health - self.player_health >= 200:
                    self.player_health += 200
                else:
                    self.player_health = self.max_health
                i.remove_from_sprite_lists()
        for i in self.new_sword_list:
            if arcade.check_for_collision(self.player_sprite, i):
                self.player_damage = 1000
                arcade.play_sound(self.pickup_sound)

                i.remove_from_sprite_lists()


        self.dead_enemies_del()

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
    game.reload()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()