class World:
    players
    def step(self):
        'single step of logic and rendering'
        for p in self.players:
            p.act(self)
        self.environmentalActions()
        self.resolveConflicts()
        self.render()
    def environmentalActions():
        'control anything neither player can directly influence'
        pass
    def resolveConflicts(self):
        'handle conflicts between the results of all state changes' 
        self.resolveCollisions()
        self.resolveEffects()
        self.resolveDeath()
    def resolveCollisions():
        'handle collisions between objects'
        pass
    def resolveEffects():
        'handle spell effects, and other time dependent game state'
        pass
    def resolveDeath():
        'handle the removal of sprites and other objects from the game world'
        pass
    def render():
        'draw Everything'
        pass
