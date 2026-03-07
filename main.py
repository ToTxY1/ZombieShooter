import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Zombie Shooter")
        self.clock = pygame.time.Clock()
        self.running = True
        self.gravity = 0
        self.movement = 0
        self.facing = True

        """
        player making
        """
        self.playerSurface = pygame.image.load("Graphics/Player Right Gun.png").convert_alpha()
        self.playerSurface = pygame.transform.scale(self.playerSurface, (200, 150))
        self.playerMask = pygame.mask.from_surface(self.playerSurface)
        self.playerRectangle = self.playerSurface.get_rect(center=(100, 100))

        self.mirroredPlayerSurface = pygame.image.load("Graphics/Player Left Gun.png").convert_alpha()
        self.mirroredPlayerSurface = pygame.transform.scale(self.mirroredPlayerSurface, (200, 150))
        self.mirroredPlayerMask = pygame.mask.from_surface(self.mirroredPlayerSurface)
        self.mirroredPlayerRectangle = self.mirroredPlayerMask.get_rect(center=(100, 100))

        #todo: add base player walking tracking movement variable to see if the player is moving and in which direction
        #Images are uploaded

        """
        background making
        """
        self.gameBackground = pygame.image.load("Graphics/game Background.png").convert_alpha()
        self.gameBackground = pygame.transform.scale(self.gameBackground, (1280,720))


        self.rightMovementPressed = False
        self.leftMovementPressed = False

    def player_regenerating(self):
        self.playerMask = pygame.mask.from_surface(self.playerSurface)
        self.playerRectangle = self.playerMask.get_rect(center=(self.playerRectangle.x, self.playerRectangle.y))


    def handle_events(self):
        #Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_RIGHT:
                    if (not self.rightMovementPressed):
                        self.rightMovementPressed = True
                        print(self.facing)
                if event.key == pygame.K_LEFT:
                    if (not self.leftMovementPressed):
                        self.leftMovementPressed = True
                        print(self.facing)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.rightMovementPressed = False
                if event.key == pygame.K_LEFT:
                    self.leftMovementPressed = False

        #variable updating
        self.gravity +=1
        if (self.rightMovementPressed and self.leftMovementPressed or not self.leftMovementPressed and not self.rightMovementPressed):
            self.movement = 0

        if (self.rightMovementPressed and not self.leftMovementPressed):
            self.movement = 4
            if (not self.facing):
                self.facing = True
        if (self.leftMovementPressed and not self.rightMovementPressed):
            self.movement = -4
            if (self.facing):
                self.facing = False

        if (self.playerRectangle.bottom >= 600):
            self.gravity = 0


    def update(self):
        self.playerRectangle.x += self.movement
        self.playerRectangle.y += self.gravity
        pass

    def render(self):
        self.screen.fill('purple')
        self.screen.blit(self.gameBackground, (0, 0))
        if (self.facing):
            self.screen.blit(self.playerSurface, (self.playerRectangle.x, self.playerRectangle.y))
        elif (not self.facing):
            self.screen.blit(self.mirroredPlayerSurface, (self.playerRectangle.x, self.playerRectangle.y))

        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()