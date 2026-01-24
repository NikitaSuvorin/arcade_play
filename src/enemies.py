import arcade
from src.constants import *

class Enemy(arcade.Sprite):
    def __init__(self, texture, scale=0.5, health=100, damage=20, attack_cooldown=60, attack_range=300,
                 sword_max_range=SWORD_MAX_ATTACK):
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
        super().__init__(texture, scale=1.5, health=1000, damage=100, attack_cooldown=180,
                         attack_range=1000, sword_max_range=BOSS_SWORD_MAX_ATTACK)
        self.movement_speed = 0.1
        self.sword_texture = "assets/images/меч_1.png"
        self.sword_scale = 0.4
        self.sword_speed = 10
        self.enemy_type = "boss"
        self.score_value = 300


class Ghost(Enemy):
    def __init__(self, texture):
        super().__init__(texture, scale=0.3, health=120, damage=30, attack_cooldown=60, attack_range=300)
        self.movement_speed = KNIGF_MOVEMENT_SPEED
        self.sword_texture = "assets/images/меч_1.png"
        self.sword_scale = 0.1
        self.sword_speed = SWORD_SPEED
        self.enemy_type = "ghost"
        self.score_value = 15


class Goblin(Enemy):
    def __init__(self, texture, scale=0.5):
        super().__init__(texture, scale=scale, health=80, damage=20, attack_cooldown=60, attack_range=300)
        self.movement_speed = KNIGF_MOVEMENT_SPEED
        self.sword_texture = "assets/images/меч_1.png"
        self.sword_scale = 0.05
        self.sword_speed = SWORD_SPEED
        self.enemy_type = "goblin"
        self.score_value = 15


class Knigf(Enemy):
    def __init__(self, texture, scale=0.5):
        super().__init__(texture, scale=scale, health=150, damage=40, attack_cooldown=60, attack_range=300)
        self.movement_speed = KNIGF_MOVEMENT_SPEED
        self.sword_texture = "assets/images/меч_1.png"
        self.sword_scale = 0.1
        self.sword_speed = SWORD_SPEED
        self.enemy_type = "knigf"
        self.score_value = 15


class Spider(Enemy):
    def __init__(self, texture, scale=0.5):
        super().__init__(texture, scale=scale, health=25, damage=20, attack_cooldown=30, attack_range=300)
        self.movement_speed = 1.5
        self.sword_texture = "assets/images/паутина1.png"
        self.sword_scale = 0.1
        self.sword_speed = SWORD_SPEED
        self.enemy_type = "spider"
        self.score_value = 5


class Skeleton(Enemy):
    def __init__(self, texture, scale=0.5):
        super().__init__(texture, scale=scale, health=100, damage=20, attack_cooldown=90, attack_range=300)
        self.movement_speed = SKELETON_MOVEMENT_SPEED
        self.sword_texture = "assets/images/кост_меч.png"
        self.sword_scale = 0.3
        self.sword_speed = SWORD_SPEED * 0.8
        self.enemy_type = "skeleton"
        self.score_value = 5