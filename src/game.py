import arcade
import math
from pathlib import Path
from src.constants import *
from src.views import PauseView, OverMenuView
from src.enemies import EnemySword, Skeleton, Spider, Knigf, Ghost, Goblin, Boss
from src.items import Poison, NewSword


class GameView(arcade.View):
    def __init__(self, final_score=0):
        super().__init__()
        self.sword_sound = arcade.Sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.Sound(":resources:sounds/hit2.wav")
        self.pickup_sound = arcade.Sound(":resources:sounds/coin1.wav")
        self.level_complete_sound = arcade.Sound(":resources:sounds/coin2.wav")
        self.sword_list = arcade.SpriteList()
        self.player_sword_list = arcade.SpriteList()
        self.player_health = 1000
        self.max_health = 1000
        self.heal_rate = 1
        self.heal_timer = 0
        self.player_damage = 50
        self.final_score = final_score
        self.level_score = 0
        self.total_score = self.level_score + final_score
        self.current_level = 1
        self.level_complete = False
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
            y=WINDOW_HEIGHT / 100 * 94,
            color=arcade.csscolor.WHITE,
            font_size=18,
        )
        self.health_table_background = arcade.SpriteSolidColor(
            width=200,
            height=20,
            color=arcade.color.DARK_RED
        )
        self.health_table_background.center_x = 200
        self.health_table_background.center_y = WINDOW_HEIGHT / 100 * 95

        self.health_table = arcade.SpriteSolidColor(
            width=200,
            height=20,
            color=arcade.color.GREEN
        )
        self.health_table.center_x = 200
        self.health_table.center_y = WINDOW_HEIGHT / 100 * 95
        self.gui_sprites = arcade.SpriteList()
        self.gui_sprites.append(self.health_table_background)
        self.gui_sprites.append(self.health_table)
        self.player_attack_cooldown = 0
        self.player_attack_max_cooldown = 60

    def setup_level_1(self):
        self.all_enemies = arcade.SpriteList()
        self.poison_list = arcade.SpriteList()
        self.new_sword_list = arcade.SpriteList()
        skeleton1 = Skeleton(self.skeleton_texture, scale=0.04)
        skeleton1.center_x = 300
        skeleton1.center_y = 300
        self.all_enemies.append(skeleton1)
        skeleton2 = Skeleton(self.skeleton_texture, scale=0.04)
        skeleton2.center_x = 400
        skeleton2.center_y = 400
        self.all_enemies.append(skeleton2)
        spider = Spider(self.spider_texture, scale=0.1)
        spider.center_x = 500
        spider.center_y = 500
        self.all_enemies.append(spider)
        poison = Poison(600, 600)
        self.poison_list.append(poison)
        new_sword = NewSword(700, 700)
        self.new_sword_list.append(new_sword)

    def setup_level_2(self):
        self.all_enemies = arcade.SpriteList()
        self.poison_list = arcade.SpriteList()
        self.new_sword_list = arcade.SpriteList()
        knigf1 = Knigf(self.knigf_texture, scale=0.5)
        knigf1.center_x = 300
        knigf1.center_y = 300
        self.all_enemies.append(knigf1)

        knigf2 = Knigf(self.knigf_texture, scale=0.5)
        knigf2.center_x = 500
        knigf2.center_y = 500
        self.all_enemies.append(knigf2)
        ghost = Ghost(self.ghost_texture)
        ghost.center_x = 700
        ghost.center_y = 700
        self.all_enemies.append(ghost)

        goblin = Goblin(self.goblin_texture, scale=0.2)
        goblin.center_x = 900
        goblin.center_y = 900
        self.all_enemies.append(goblin)
        poison1 = Poison(400, 400)
        self.poison_list.append(poison1)
        poison2 = Poison(800, 800)
        self.poison_list.append(poison2)
        new_sword = NewSword(600, 600)
        self.new_sword_list.append(new_sword)

    def setup_level_3(self):
        self.all_enemies = arcade.SpriteList()
        self.poison_list = arcade.SpriteList()
        self.new_sword_list = arcade.SpriteList()
        boss = Boss(self.boss_texture)
        boss.center_x = 1000
        boss.center_y = 1000
        self.all_enemies.append(boss)

        ghost1 = Ghost(self.ghost_texture)
        ghost1.center_x = 800
        ghost1.center_y = 800
        self.all_enemies.append(ghost1)
        ghost2 = Ghost(self.ghost_texture)
        ghost2.center_x = 1200
        ghost2.center_y = 1200
        self.all_enemies.append(ghost2)

        knigf1 = Knigf(self.knigf_texture, scale=0.5)
        knigf1.center_x = 600
        knigf1.center_y = 600
        self.all_enemies.append(knigf1)
        knigf2 = Knigf(self.knigf_texture, scale=0.5)
        knigf2.center_x = 1400
        knigf2.center_y = 1400
        self.all_enemies.append(knigf2)
        poison1 = Poison(500, 500)
        self.poison_list.append(poison1)

        poison2 = Poison(1100, 1100)
        self.poison_list.append(poison2)

        poison3 = Poison(1500, 1500)
        self.poison_list.append(poison3)
        new_sword1 = NewSword(700, 700)
        self.new_sword_list.append(new_sword1)
        new_sword2 = NewSword(1300, 1300)
        self.new_sword_list.append(new_sword2)

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
            self.window.background_color = arcade.Color.from_iterable(tile_map.background_color)
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
        self.player_health = self.max_health
        self.level_complete = False
        self.scene = self.create_scene()
        self.scene.add_sprite("Player", self.player_sprite)
        if self.current_level == 1:
            self.setup_level_1()
        elif self.current_level == 2:
            self.setup_level_2()
        elif self.current_level == 3:
            self.setup_level_3()
        for enemy in self.all_enemies:
            self.scene.add_sprite(enemy.enemy_type, enemy)
        for poison in self.poison_list:
            self.scene.add_sprite("Poison", poison)
        for sword in self.new_sword_list:
            self.scene.add_sprite("New_sword", sword)
        self.scene.add_sprite_list("Swords")
        self.scene.add_sprite_list("PlayerSwords")
        self.level_score = 0
        self.total_score = self.final_score + self.level_score
        self.update_health_table()

    def check_level_complete(self):
        if len(self.all_enemies) == 0 and not self.level_complete:
            self.level_complete = True
            arcade.play_sound(self.level_complete_sound)
            arcade.schedule(self.complete_level, 5.0)

    def complete_level(self, delta_time):
        arcade.unschedule(self.complete_level)
        total_score = self.final_score + self.level_score
        over_view = OverMenuView(score=total_score, level=self.current_level)
        self.window.show_view(over_view)

    def on_draw(self):
        self.clear()
        with self.camera_sprites.activate():
            self.scene.draw()
            self.sword_list.draw()
            self.player_sword_list.draw()
        with self.camera_gui.activate():
            self.gui_sprites.draw()
            self.score_display.text = f"Score: {self.level_score}"
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

    def player_attack(self):
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
        over_view = OverMenuView(score=self.total_score, level=self.current_level - 1)
        self.window.show_view(over_view)

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
                        self.level_score += j.score_value

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
                self.player_damage += 15
                arcade.play_sound(self.pickup_sound)
                i.remove_from_sprite_lists()

        self.dead_enemies_del()

        self.sword_list.update()
        self.player_sword_list.update()
        self.physics_engine.update()
        self.center_camera_to_player()
        if not self.level_complete:
            self.check_level_complete()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.camera_sprites.match_window()
        self.camera_gui.match_window(position=True)