from ships import *
from obstacle import *


class SpaceVentureZ(Display):
    def __init__(self):
        Display.__init__(self)  # keeps the inheritance of Display
        # game variables life for entities
        self.playerHealthPoints = 100
        self.enemyHealthPoints = 20

        # score aka Star Points variable
        self.score = 0
        self.is_enemy_hit = False
        self.is_enemy_dead = False
        self.score_text = pygame.image.load('game_images/star-points-text.png').convert()

        # temp invincibility variables
        self.collision_invincibility = False
        self.collision_time = 0

        # true if currently fighting boss
        self.boss_fight = False

        # track if player restarted game
        self.is_restarting = False

        '''creation of entities'''
        self.player_ship = Player(self.playerHealthPoints, self.width/2, self.height-64-20, 10, self.display)  # added display
        self.black_hole = BlackHole(self.width/2, 350)
        # creates a list of obstacles starting with 10 asteroids
        self.obstacles_ = [Asteroids(random.randint(100, self.width - 100), random.randint(100, self.height - 500)) for x in range(10)]

        # ENEMY SPAWNING
        # testing enemy2 class
        # self.enemy2 = [Enemy2(self.enemyHealthPoints, random.randint(0, self.width-200), random.randint(0, self.height - 200), random.randint(3, 8)) for x in range(3)]

        self.enemies = list()
        for x in range(10):
            # get y spawn
            y_spawn = random.randrange(0, self.height - 200, 64)
            while y_spawn == self.black_hole.y or (350 < y_spawn < 450):
                y_spawn = random.randrange(0, self.height - 200, 64)
            # spawn enemy
            self.enemies.append(Enemy(self.enemyHealthPoints, random.randrange(0, self.width - 200, 64), y_spawn, 2))

        self.boss = None

    def run(self):
        # check screen size in case of resize
        w, h = pygame.display.get_surface().get_size()
        keys = pygame.key.get_pressed()

        '''Scrolling Background Drawing. Has to be first to be in the back/bottom of other images.'''
        self.update_background()
        self.render_background()

        ''' PLAYER HANDLING '''
        self.player_ship.movement(keys, (w, h))
        self.player_ship.fire_laser(keys)
        self.player_ship.draw(self.display)
        self.player_ship.is_sound_on = self.is_sound_on
        ''' invincibility handling '''

        ''' BLACK HOLE Drawing '''
        self.black_hole.draw()
        self.black_hole.is_sound_on = self.is_sound_on

        #can be here to keep it with black hole
        ''' Obstacle Handling: Movement, Drawing, Removing '''
        for x in self.obstacles_:
            x.draw()
            x.move()
            if isinstance(x, Asteroids) and x.hp <= 0:
                self.obstacles_.remove(x)
                temp = random.randint(1,7)
                if temp %2 == 0:
                    self.obstacles_.append(StarPrize(x.x, x.y))
                else:
                    self.obstacles_.append(HealthPrize(x.x, x.y))
            if x.collision(self.player_ship.ship):
                if isinstance(x, Asteroids):
                    self.player_ship.health -= 5
                elif isinstance(x, HealthPrize):
                    self.player_ship.health += 25
                    if self.player_ship.health >= self.playerHealthPoints:
                        self.player_ship.health = self.playerHealthPoints
                    self.obstacles_.remove(x)
                elif isinstance(x, StarPrize):
                    self.score += x.points
                    self.obstacles_.remove(x)
            if isinstance(x, StarPrize):
                if x.off_screen():
                    self.obstacles_.remove(x)

        for x in self.enemies:
            x.draw(self.display)

        # ALL BOSS HANDLING MUST BE IN HERE
        if self.boss_fight is True:
            self.boss[0].draw()
            self.boss[0].auto_movement(self.player_ship)

        '''draws paused on display and handles unpause'''
        if self.pause:
            self.paused()

        ''' ENEMY HANDLING && Collision handling '''
        if pygame.time.get_ticks() > self.collision_time:
            self.collision_invincibility = False

        if self.collision_invincibility is False:
            if self.boss_fight is True:
                if self.boss[0].collision(self.player_ship.ship):
                    self.player_ship.health -= 30
                    self.collision_invincibility = True
                    self.collision_time = pygame.time.get_ticks() + 3000

            for x in self.enemies:
                x.auto_movement()
                x.draw(self.display)
                if x.health <= 0:
                    self.enemies.remove(x)
                    self.is_enemy_dead = True

                if x.collision(self.player_ship.ship):
                    """if enemy ship collides with player ship, then player ship loses hp"""
                    self.player_ship.health -= 30

                    self.collision_invincibility = True
                    self.collision_time = pygame.time.get_ticks() + 3000

                    '''black-hole handling for enemy ships currently removes enemy or teleports by random chance'''
                    if self.black_hole.entered_bh(x.ship):
                        random_num = random.randint(0, 2)
                        if random_num != 1:
                            self.enemies.remove(x)
                        else:
                            x.x, x.y = random.randint(64, self.width-64), random.randint(64, self.height-64)

        ''' BLACK HOLE HANDLING for player ship '''
        if self.black_hole.entered_bh(self.player_ship.ship):
            self.black_hole.pulse()
            self.player_ship.x, self.player_ship.y = random.randint(0, self.width-64), random.randint(64, self.height)

        '''Laser handling with enemy ships'''
        for p_laser in self.player_ship.lasers:
            '''Delete laser when they go off screen'''
            if p_laser.y <= 0:
                # print("OUT OF BOUNDS")
                self.player_ship.lasers.remove(p_laser)
                # print(len(self.player_ship.lasers.sprites()))
            '''if laser goes into black hole the laser is deleted'''
            if self.black_hole.entered_bh(p_laser.laser):
                self.player_ship.lasers.remove(p_laser)
            '''if the laser goes into enemy ship?? life of ship decreases by 5? -isabel'''
            for x in self.enemies:
                if x.collision(p_laser.laser):
                    x.health -= 1
                    self.player_ship.lasers.remove(p_laser.laser)
                    self.is_enemy_hit = True
            for x in self.obstacles_:
                if isinstance(x, Asteroids) and x.collision(p_laser.laser):
                    x.hp -= 5
            if self.boss_fight is True:
                if self.boss[0].collision(p_laser.laser):
                    self.boss[0].health -= 10
                    self.player_ship.lasers.remove(p_laser.laser)
                    self.is_enemy_hit = True


        '''Player Score'''
        # draw score on screen
        self.add_image(self.score_text, 213, 30, self.display, 230, 5)
        self.add_text(str(self.score), self.font, (255, 255, 255), self.display, 460, 5)
        # add to score on enemy kill
        if (self.is_enemy_hit is True) and (self.is_enemy_dead is True):
            self.score += 100
            self.is_enemy_hit = False
            self.is_enemy_dead = False

        '''Drawing the player ship health bar'''
        #self.player_ship.draw_health_bar(self.display, 5, 5, self.player_ship.health) #original placement
        # For healthbar to move along with the player ship.
        bar_loc_x = self.player_ship.x
        bar_loc_y = self.player_ship.y + 70
        self.player_ship.draw_health_bar(self.display, bar_loc_x, bar_loc_y, self.player_ship.health)

        ''' CHECKING FOR END OF GAME (WIN/LOSS)'''
        if self.player_ship.health <= 0:
            # Loss
            self.game_over = True
            self.end_screen("Defeat")
        if len(self.enemies) == 0 and self.boss_fight is False:
            # spawn boss
            self.boss_fight = True
            self.boss = [Enemy2(5000, 150, 150, 2)]
        if self.boss_fight is True and self.boss[0].health <= 0:
            # win
            self.game_over = True
            self.end_screen("Victory")

    def restart(self):
        # Removes all objects
        for x in self.enemies:
            self.enemies.remove(x)
        for y in self.obstacles_:
            self.obstacles_.remove(y)
        del self.black_hole
        del self.player_ship
        # Reset player health
        self.playerHealthPoints = 100
        # Reset score
        self.score = 0
        # Reset states
        self.is_enemy_hit = False
        self.is_enemy_dead = False
        self.collision_invincibility = False
        self.boss_fight = False
        self.is_restarting = True
        # Add entities
        self.player_ship = Player(self.playerHealthPoints, 400, 400, 10, self.display)  # added display
        self.black_hole = BlackHole(self.width/2, 350)
        self.obstacles_ = [Asteroids(random.randint(100, self.width - 100), random.randint(100, self.height - 500)) for x in range(10)]
        # self.enemy2 = [Enemy2(self.enemyHealthPoints, random.randint(0, self.width - 200), random.randint(0, self.height - 200),
        #                      random.randint(3, 10)) for x in range(3)]
        for x in range(10):
            # get y spawn
            y_spawn = random.randrange(0, self.height - 200, 64)
            while y_spawn == self.black_hole.y or y_spawn == self.player_ship.y:
                y_spawn = random.randrange(0, self.height - 200, 64)
            # spawn enemy
            self.enemies.append(Enemy(self.enemyHealthPoints, random.randrange(0, self.width - 200, 64), y_spawn, 2))
        self.run_game()

if __name__ == '__main__':
    # create SpaceVentureZ game instance and run it
    svz = SpaceVentureZ()
    #svz.menu()
    svz.run_game()

''' 
run() runs the game initially called in run_game in the Display class
self.display is the window (changed the name from self.window) 
'''
