import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2

class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2
        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        if self.acceleration:
            self.velocity += (self.acceleration * dt, 0)
            self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
        else:
            # Wenn keine Taste für Beschleunigung gedrückt ist, die Geschwindigkeit auf null setzen
            self.velocity.x = 0.0

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

ppu = 32

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def draw_parking_lines(self):
        # Linien für Parklücke 1
        pygame.draw.line(self.screen, (255, 255, 255), (100, 0), (100, 200), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (100, 200), (200, 200), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (200, 200), (200, 0), 2)

        # Linien für Parklücke 2
        pygame.draw.line(self.screen, (255, 255, 255), (400, 0), (400, 150), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (400, 150), (500, 150), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (500, 150), (500, 0), 2)

        # Linien für Parklücke 3
        pygame.draw.line(self.screen, (255, 255, 255), (800, 0), (800, 100), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (800, 100), (900, 100), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (900, 100), (900, 0), 2)

    def limit_car_position(self, car):
        car.position.x = max(car.length / 2, min(car.position.x, 1280 / ppu - car.length / 2))
        car.position.y = max(car.length / 2, min(car.position.y, 720 / ppu - car.length / 2))

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path)
        car = Car(0, 0)
    

        while not self.exit:
            dt = self.clock.get_time() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                car.acceleration = car.max_acceleration
            elif pressed[pygame.K_DOWN]:
                car.acceleration = -car.max_acceleration
            else:
                car.acceleration = 0

            if not pressed[pygame.K_UP] and not pressed[pygame.K_DOWN]:
                # Wenn keine Taste für Beschleunigung gedrückt ist, die Geschwindigkeit auf null setzen
                car.acceleration = 0

            if pressed[pygame.K_SPACE]:
                if abs(car.velocity.x) > dt * car.brake_deceleration:
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
                else:
                    car.acceleration = -car.velocity.x / dt

            if pressed[pygame.K_RIGHT]:
                car.steering = -car.max_steering
            elif pressed[pygame.K_LEFT]:
                car.steering = car.max_steering
            else:
                car.steering = 0

            car.update(dt)
            self.limit_car_position(car)

            self.screen.fill((0, 0, 0))
            self.draw_parking_lines()

            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
            pygame.display.flip()

            self.clock.tick(self.ticks)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()