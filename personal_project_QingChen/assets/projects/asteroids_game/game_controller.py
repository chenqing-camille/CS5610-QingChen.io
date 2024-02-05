from laserbeam import LaserBeam
from asteroid import Asteroid
from spaceship import Spaceship
import math


class GameController:
    """
    Maintains the state of the game
    and manages interactions of game elements.
    """

    def __init__(self, SPACE, fadeout):
        """Initialize the game controller"""
        self.SPACE = SPACE
        self.fadeout = fadeout

        self.spaceship_hit = False
        self.asteroid_destroyed = False
        self.asteroids = [Asteroid(self.SPACE)]
        self.laser_beams = []
        self.spaceship = Spaceship(self.SPACE)
        self.laser_asteroid_intersect = False

    def update(self):
        """Updates game state on every frame"""
        self.do_intersections()

        for asteroid in self.asteroids:
            asteroid.display()

        # ======================================================
        # Once over 100 frames, the laser disappears
        for laser in range(len(self.laser_beams)):
            if self.laser_beams[laser].lifespan > 0:
                self.laser_beams[laser].display()

        # End problem 3, part 2 code changes
        # =======================================================

        self.spaceship.display()

        # Carries out necessary actions if game over
        if self.spaceship_hit:
            if self.fadeout <= 0:
                fill(1)
                textSize(30)
                text("YOU HIT AN ASTEROID",
                     self.SPACE['w']/2 - 165, self.SPACE['h']/2)
            else:
                self.fadeout -= 1

        if self.asteroid_destroyed:
            fill(1)
            textSize(30)
            text("YOU DESTROYED THE ASTEROIDS!!!",
                 self.SPACE['w']/2 - 250, self.SPACE['h']/2)

    def fire_laser(self, x, y, rot):
        """Add a laser beam to the game"""
        x_vel = sin(radians(rot))
        y_vel = -cos(radians(rot))
        self.laser_beams.append(
            LaserBeam(self.SPACE, x, y, x_vel, y_vel)
        )

    def handle_keypress(self, key, keycode=None):
        if (key == ' '):
            if self.spaceship.intact:
                self.spaceship.control(' ', self)
        if (keycode):
            if self.spaceship.intact:
                self.spaceship.control(keycode)

    def handle_keyup(self):
        if self.spaceship.intact:
            self.spaceship.control('keyup')

    def do_intersections(self):
        # ======================================================
        # Begin code changes for Problem 3, Part 1: Intersections
        for i in self.laser_beams:
            for j in self.asteroids:
                # calculate the distance between laser and asteroid
                distance = dist(i.x, i.y, j.x, j.y)
                if distance <= i.radius + j.radius:
                    # they are intersected:
                    self.laser_asteroid_intersect = True
                    # blow up the asteroid
                    self.blow_up_asteroid(i, j)

        # End of code changes for Problem 4, Part 1: Intersections
        # ======================================================

        # If the space ship still hasn't been blown up
        if self.spaceship.intact:
            # Check each asteroid for intersection
            for i in range(len(self.asteroids)):
                if (
                    abs(self.spaceship.x - self.asteroids[i].x)
                    < max(self.asteroids[i].radius, self.spaceship.radius)
                    and
                    abs(self.spaceship.y - self.asteroids[i].y)
                        < max(self.asteroids[i].radius, self.spaceship.radius)):
                    # We've intersected an asteroid
                    self.spaceship.blow_up(self.fadeout)
                    self.spaceship_hit = True

    def blow_up_asteroid(self, i, j):
        # ======================================================
        # Begin code changes for Problem 4, Part 2: Asteroid blow-up
        # use constant to ajust the asteroid speed
        SPEED_UP = 5
        SPEED_DOWN = 2
        if self.laser_asteroid_intersect:
            # collect the direction of laser to be removed
            laser_x_vel = i.x_vel
            laser_y_vel = i.y_vel
            self.laser_beams.remove(i)
            if j.asize == 'Large':
                # split the large into two medium asteroids
                # fly off perpendicularly
                new_asteroid1 = Asteroid(
                    self.SPACE, 'Med', j.y, j.y, -j.x_vel*SPEED_UP,
                    j.y_vel*SPEED_UP)
                new_asteroid2 = Asteroid(
                    self.SPACE, 'Med', j.y, j.y,
                    j.x_vel*SPEED_UP, -j.y_vel*SPEED_UP)
                self.asteroids.append(new_asteroid1)
                self.asteroids.append(new_asteroid2)
                self.asteroids.remove(j)
            elif j.asize == 'Med':
                # split the medium into three medium asteroids
                # start at the same (x,y) and fly off perpendicularly
                new_asteroid1 = Asteroid(
                    self.SPACE, 'Small', j.x, j.y, j.x_vel, -j.y_vel)
                new_asteroid2 = Asteroid(
                    # fly off along the direction of the laser
                    self.SPACE, 'Small', j.x, j.y,
                    laser_x_vel/SPEED_DOWN, laser_y_vel/SPEED_DOWN)
                new_asteroid3 = Asteroid(
                    self.SPACE, 'Small', j.x, j.y, j.x_vel, j.y_vel)
                self.asteroids.append(new_asteroid1)
                self.asteroids.append(new_asteroid2)
                self.asteroids.append(new_asteroid3)
                self.asteroids.remove(j)
            else:
                self.asteroids.remove(j)
                # if there is no more asteroid, you win
                if len(self.asteroids) == 0:
                    self.asteroid_destroyed = True
