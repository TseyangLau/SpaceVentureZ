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
        '''creation of entities'''
        self.player_ship = Player(self.playerHealthPoints, 400, 400, 10, self.display)  # added display
        self.black_hole = BlackHole(self.width/2, self.height-450)
        self.asteroids = [Asteroids(random.randint(100, self.width - 100), random.randint(100, self.height - 500)) for x in range(10)]

        # ENEMY SPAWNING
        #testing enemy2 class
        #self.enemy2 = [Enemy2(self.enemyHealthPoints, random.randint(0, self.width-200), random.randint(0, self.height - 200), random.randint(3, 8)) for x in range(3)]

        self.enemy_max = 50
        self.enemies = list()
        for x in range(10):
            # get y spawn
            y_spawn = random.randrange(0, self.height - 200, 64)
            while y_spawn == self.black_hole.y or (350 < y_spawn < 450):
                y_spawn = random.randrange(0, self.height - 200, 64)
            # spawn enemy
            self.enemies.append(Enemy(self.enemyHealthPoints, random.randrange(0, self.width - 200, 64), y_spawn, 2))

    def run(self):
        # check screen size in case of resize
        w, h = pygame.display.get_surface().get_size()
        keys = pygame.key.get_pressed()

        ''' PLAYER HANDLING '''
        self.player_ship.movement(keys, (w, h))
        self.player_ship.fire_laser(keys)
        self.player_ship.draw(self.display)
        ''' invincibility handling '''

        ''' BLACK HOLE Drawing '''
        self.black_hole.draw()

        ''' Asteroid Drawing '''
        for x in self.asteroids:
            x.draw()
            x.move()
            if x.hp <= 0:
                self.asteroids.remove(x)
            '''aestroid handling with player ship'''
            if x.coll(self.player_ship.ship):
                self.player_ship.health -= 10

        for x in self.enemies:
            x.draw(self.display)
        #for x in self.enemy2:
        #    x.draw()
        '''draws paused on display and handles unpause'''
        if self.pause:
            self.paused()


        ''' ENEMY HANDLING && Collision handling '''
        if pygame.time.get_ticks() > self.collision_time:
            self.collision_invincibility = False
        if self.collision_invincibility == False:
            #for x in self.enemy2:
            #    x.track(self.player_ship)
            for x in self.enemies:
                x.auto_movement()
                #x.track(self.player_ship) # this is for enemy2 ships
                #print(x.health)
                if x.health <= 0:
                    self.enemies.remove(x)
                    self.is_enemy_dead = True

                if x.collision(self.player_ship.ship):
                    """if enemy ship collides with player ship, then player ship loses hp"""
                    #print("ships touching")
                    self.player_ship.health -= 30

                    self.collision_invincibility = True
                    self.collision_time = pygame.time.get_ticks() + 3000

                    '''black-hole handling for enemy ships currently removes enemy or teleports by random chance'''
                    if self.black_hole.entered_bh(x.ship):
                        random_num = random.randint(0, 2)
                        if random_num != 1:
                            self.enemies.remove(x)
                        # elif self.enemy_max >= len(self.enemies):
                            # self.black_hole.pulse()
                            # self.enemies.append(Enemy(self.playerHealthPoints, random.randint(0, 750), random.randint(0, 750), 2))
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
                print("OUT OF BOUNDS")
                self.player_ship.lasers.remove(p_laser)
                print(len(self.player_ship.lasers.sprites()))
            '''if laser goes into black hole the laser is deleted'''
            if self.black_hole.entered_bh(p_laser.laser):
                self.player_ship.lasers.remove(p_laser)
            '''if the laser goes into enemy ship?? life of ship decreases by 5? -isabel'''
            for x in self.enemies:
                if x.collision(p_laser.laser):
                    x.health -= 1
                    self.player_ship.lasers.remove(p_laser.laser)
                    self.is_enemy_hit = True
            for x in self.asteroids:
                if x.coll(p_laser.laser):
                    x.hp -= 5


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
        if len(self.enemies) == 0:
            # Win
            self.game_over = True
            self.end_screen("Victory")


    def restart(self):
        # Removes all objects
        for x in self.enemies:
            self.enemies.remove(x)
        for y in self.asteroids:
            self.asteroids.remove(y)
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
        # Add entities
        self.player_ship = Player(self.playerHealthPoints, 400, 400, 10, self.display)  # added display
        self.black_hole = BlackHole(random.randrange(100, self.width - 100, 64), random.randrange(100, 400, 64))
        self.asteroids = [Asteroids(random.randint(100, self.width - 100), random.randint(100, self.height - 500)) for x in range(10)]
       #self.enemy2 = [Enemy2(self.enemyHealthPoints, random.randint(0, self.width - 200), random.randint(0, self.height - 200),
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
