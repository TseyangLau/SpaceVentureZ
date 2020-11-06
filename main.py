from ships import *
from obstacle import *


class SpaceVentureZ(Display):
    def __init__(self):
        Display.__init__(self)  # keeps the inheritance of Display

        # game variables life for entities
        self.playerHealthPoints = 100
        self.enemyHealthPoints = 20

        # score variable
        self.score = 0
        self.is_enemy_hit = False
        self.is_enemy_dead = False

        # temp invincibility variables
        self.collision_invincibility = False
        self.collision_time = 0
        '''creation of entities'''
        self.player_ship = Player(self.playerHealthPoints, 400, 400, 10, self.display)  # added display
        self.black_hole = BlackHole(random.randrange(100, self.width - 100, 64), random.randrange(100, 400, 64))

        # ASTEROID SPAWNING
        self.asteroids = [Asteroids(random.randint(100, self.width - 100), random.randint(100, self.height - 500)) for x in range(10)]

        # ENEMY SPAWNING
        #testing enemy2 class
        self.enemy2 = [Enemy2(self.enemyHealthPoints, random.randint(0, self.width-200), random.randint(0, self.height - 200), random.randint(3, 8)) for x in range(10)]

        self.enemy_max = 50
        self.enemies = list()
        for x in range(10):
            # get y spawn
            y_spawn = random.randrange(0, self.height - 200, 64)
            while y_spawn == self.black_hole.y or y_spawn == self.player_ship.y:
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



        ''' BLACK HOLE HANDLING '''
        self.black_hole.draw()
        for x in self.asteroids:
            x.draw()
            x.move()
            if x.hp <= 0:
                self.asteroids.remove(x)

        for x in self.enemies:
            x.draw(self.display)
        # for x in self.enemy2:
        #     x.draw()
        '''draws paused on display and handles unpause'''
        if self.pause:
            self.paused()


        ''' ENEMY HANDLING && collision handling '''
        #@tseyang moved your collision detection to before it enteres the enemy handling for loop
        if self.collision_invincibility:  # added this line idk how to explain but it needs to be here >.<
            if pygame.time.get_ticks() > self.collision_time:  # time in ms (milliseconds) 3000 == 3 seconds #changed this a little bit - isabel
                self.collision_invincibility = False
        if self.collision_invincibility == False:
            for x in self.enemies:
                x.auto_movement()
                #x.track(self.player_ship) # this is for enemy2 ships
                #print(x.health)
                if x.health <= 0:
                    self.enemies.remove(x)
                    self.is_enemy_dead = True

                #this block of code handles the collision with the ship, effects on health, and invincibility on hit.
                # @tseyang moved it to before the for loop above ^^

                if x.collision(self.player_ship.ship):
                    """if enemy ship collides with player ship, then player ship loses hp"""
                    #print("ships touching")
                    self.player_ship.health -= 30
                    # if x.health <= 0: # shouldnt be here, i moved it back up - isabel
                    #     self.enemies.remove(x)
                    #     self.is_enemy_dead = True
                    self.collision_invincibility = True
                #if self.collision_invincibility == True: # dont need this line its already true with the line above
                    self.collision_time = pygame.time.get_ticks() + 3000 # this is were you added the 3 seconds of wait to your collision time
                    #break # might not need this - isabel (ended not needed it)

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
        self.add_text("Score " + str(self.score), self.font, (255, 255, 255), self.display, 350, 0)
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
        self.enemy_hit = False
        self.collision_invincibility = False
        # Add entities
        self.player_ship = Player(self.playerHealthPoints, 400, 400, 10, self.display)  # added display
        self.black_hole = BlackHole(random.randrange(100, self.width - 100, 64), random.randrange(100, 400, 64))
        self.asteroids = [Asteroids(random.randint(100, self.width - 100), random.randint(100, self.height - 500)) for x in range(10)]
        self.enemy2 = [Enemy2(self.enemyHealthPoints, random.randint(0, self.width - 200), random.randint(0, self.height - 200),
                              random.randint(3, 10)) for x in range(10)]
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
    svz.run_game()

''' 
run() runs the game initially called in run_game in the Display class
self.display is the window (changed the name from self.window) 
'''
