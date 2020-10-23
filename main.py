from ships import *
from obstacle import *


class SpaceVentureZ(Display):
    def __init__(self):
        Display.__init__(self)  # keeps the inheritance of Display

        # game variables life for entities
        self.playerHealthPoints = 100
        self.enemyHealthPoints = 1

        self.collision_invincibility = False
        '''creation of entities'''
        self.player_ship = Player(self.playerHealthPoints, 400, 400, 10, self.display)  # added display
        self.black_hole = BlackHole(random.randrange(100, self.width - 100, 64), random.randrange(100, 400, 64))
        #self.asteroid = Asteroids(random.randint(100, self.width - 100), random.randint(100, self.height - 500))

        # ASTEROID SPAWNING
        self.asteroids = list()
        for x in range(10):
            self.asteroids.append(Asteroids(random.randint(100, self.width - 100),
                                            random.randint(100, self.height - 500)))

        # ENEMY SPAWNING
        self.enemy_max = 50
        self.enemies = list()
        for x in range(10):
            # get y spawn
            y_spawn = random.randrange(0, self.height - 200, 64)
            while y_spawn == self.black_hole.y:
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

        ''' BLACK HOLE HANDLING '''
        self.black_hole.draw()
        for x in self.asteroids:
            x.draw()
            x.move()
            if x.hp <= 0:
                self.asteroids.remove(x)

        for x in self.enemies:
            x.draw(self.display)

        '''draws paused on display and handles unpause'''
        if self.pause:
            self.paused()

        '''asteroid handling for testing'''
       # self.asteroid.move()

        ''' ENEMY HANDLING '''
        # while self.pause == False:
        for x in self.enemies:
            # x.draw(self.display) draws it before handling
            x.collision(self.player_ship.ship)
            x.auto_movement()
            print(x.health)

            self.collision_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.collision_time > 3000:
                self.collision_invincibility = False
            if x.collision(self.player_ship.ship):
                """if enemy ship collides with player ship, then player ship loses hp"""
                print("they touching")
                self.player_ship.health -= 1
                self.collision_invincibility = True
                #self.collision_time = pygame.time.get_ticks()
                #
                if self.player_ship.health <= 0:
                    print ("you died")
                    pass
                # del the player object
            # handle enemies dying when health goes to 0 -isabel
            if x.health <= 0:
                self.enemies.remove(x)

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
            for x in self.asteroids:
                if x.coll(p_laser.laser):
                    x.hp -= 5

        '''Drawing the player ship health bar'''
        self.player_ship.draw_health_bar(self.display, 5, 5, self.player_ship.health)


if __name__ == '__main__':
    # create SpaceVentureZ game instance and run it
    svz = SpaceVentureZ()
    svz.run_game()

''' 
run() runs the game initially called in run_game in the Display class
self.display is the window (changed the name from self.window) 
'''
