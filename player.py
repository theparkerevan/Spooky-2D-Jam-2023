import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, directory):
        # Access to other objects
        self.directory = directory

        # Dimensions
        self.x = 0
        self.y = 0

        self.width = 94
        self.height = 94

        # Rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitbox = pygame.Rect(self.x - 16, self.y - 16, self.width + 32, self.height + 32)

        # Art
        self.art = {"idle":[], "walkL":[], "walkR":[], "eyes":[]}
        self.loadArt()

        # Sounds
        pygame.mixer.init()
        self.sounds = {"footstep": pygame.mixer.Sound("data/sounds/Sand.wav")}

        # Movement
        self.speed = 3
        self.frame = 0
        self.moving_left = False
        self.moving_right = False

        self.direction = 'right'
    

    def loadArt(self):
        self.art["idle"].append(pygame.transform.scale(pygame.image.load("data/assets/little_guy/little_guy1.png"), (94, 94)))
        self.art["idle"].append(pygame.transform.flip(pygame.transform.scale(pygame.image.load("data/assets/little_guy/little_guy1.png"), (94, 94)), 1, 0))

        self.art["walkR"].append(pygame.transform.scale(pygame.image.load("data/assets/little_guy/little_guy1.png"), (94, 94)))
        self.art["walkR"].append(pygame.transform.scale(pygame.image.load("data/assets/little_guy/little_guy2.png"), (94, 94)))
        self.art["walkR"].append(pygame.transform.scale(pygame.image.load("data/assets/little_guy/little_guy1.png"), (94, 94)))
        self.art["walkR"].append(pygame.transform.scale(pygame.image.load("data/assets/little_guy/little_guy3.png"), (94, 94)))
        
        self.art["walkL"].append(pygame.transform.flip(pygame.transform.scale(pygame.image.load("data/assets/little_guy/little_guy1.png"), (94, 94)), 1, 0))
        self.art["walkL"].append(pygame.transform.flip(pygame.transform.scale(pygame.image.load("data/assets/little_guy/little_guy2.png"), (94, 94)), 1, 0))
        self.art["walkL"].append(pygame.transform.flip(pygame.transform.scale(pygame.image.load("data/assets/little_guy/little_guy1.png"), (94, 94)), 1, 0))
        self.art["walkL"].append(pygame.transform.flip(pygame.transform.scale(pygame.image.load("data/assets/little_guy/little_guy3.png"), (94, 94)), 1, 0))

        self.art["eyes"].append(pygame.transform.scale(pygame.image.load("data/assets/little_guy/eyes.png"), (94, 94)))
        self.art["eyes"].append(pygame.transform.flip(pygame.transform.scale(pygame.image.load("data/assets/little_guy/eyes.png"), (94, 94)), 1, 0))


    def interact(self):
        # If the interact button is pressed, check for interactables and activate them
        # If one is activated, stop searching, only one should activate at a time.
        # This may cause problems eventually, but multiple objects shouldn't be that close to each other.
        for obj in self.directory.objects:
            if obj.rect.colliderect(self.hitbox):
                obj.activate()
                return


    def update(self):
        ## Player Movement ##
        dx = 0
        
        # Check movement flags
        if self.moving_left:
            dx -= 1
        
        if self.moving_right:
            dx += 1
        
        # Player go zoom (at speed of self.speed)
        dx = dx * self.speed

        # Check to see if player tries to go out of bounds
        if self.rect.right + dx > self.directory.level.borders[1]:
            dx = self.directory.level.borders[1] - self.rect.right
        elif self.x + dx < self.directory.level.borders[0]:
            dx = self.directory.level.borders[0] - self.x
        
        # Then, if player moved, check for objects in hitbox, if so, highlight
        for obj in self.directory.objects:
            if obj.rect.colliderect(self.hitbox):
                obj.highlighted = True
            else:
                obj.highlighted = False
                
            # Redraw highlight layer

        
        # Move the player
        # Player will not move vertically
        if dx != 0:
            self.move(dx, 0)
    

    # Moves the player a given number of pixels
    def move(self, dx, dy):
        ## Move player's position ##
        # Change coordinates
        self.x += dx
        self.y += dy

        if dx > 0:
            self.direction = 'right'
        else:
            self.direction = 'left'

        # Move rect
        self.rect.move_ip(dx, dy)
        self.hitbox.move_ip(dx, dy)
    

    # Plops player down in a completely new location
    def moveTo(self, new_x, new_y):
        # Calculate dx
        dx = new_x - self.x
        dy = new_y - self.y
        
        # Update Position
        self.x += dx
        self.y += dy

        # Update rects
        self.rect.move_ip(dx, dy)
        self.hitbox.move_ip(dx, dy)
    

    # Draw
    def draw(self):
        # Fill surface with transparent pixels
        self.directory.surfaces['player'].fill((0, 0, 0, 0))
        self.directory.surfaces['eyes'].fill((0, 0, 0, 0))

        # Draw rects
        #pygame.draw.rect(self.directory.surfaces['player'], (100, 200, 200, 125), self.hitbox)
        #pygame.draw.rect(self.directory.surfaces['player'], (200, 200, 200), self.rect)

        # Drawing
        # If Moving
        if self.moving_left or self.moving_right:
            if self.direction == 'left':
                self.directory.surfaces['player'].blit(self.art["walkL"][self.frame // 10], (self.x, self.y))
                self.directory.surfaces['eyes'].blit(self.art["eyes"][1], (self.x, self.y))
            elif self.direction == 'right':
                self.directory.surfaces['player'].blit(self.art["walkR"][self.frame // 10], (self.x, self.y))
                self.directory.surfaces['eyes'].blit(self.art["eyes"][0], (self.x, self.y))
            
            if (self.frame) % 20 == 0:
                self.sounds["footstep"].play()

            self.frame += 1
            if self.frame > 39:
                self.frame = 0
        
        else:
            self.frame = 0
            if self.direction == 'left':
                self.directory.surfaces['player'].blit(self.art["idle"][1], (self.x, self.y))
                self.directory.surfaces['eyes'].blit(self.art["eyes"][1], (self.x, self.y))
            elif self.direction == 'right':
                self.directory.surfaces['player'].blit(self.art["idle"][0], (self.x, self.y))
                self.directory.surfaces['eyes'].blit(self.art["eyes"][0], (self.x, self.y))