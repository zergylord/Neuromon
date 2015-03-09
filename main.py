pygame.init()
if len(sys.argv) > 1:
    useGlue = (sys.argv[1] == 'True')
else:
    useGlue = False
black = 0,0,0
screen = pygame.display.set_mode([size[0],int(size[1]+size[1]*(4/3.0))])#,pygame.FULLSCREEN)
count = 0
if len(sys.argv) > 2:
    p1Type = int(sys.argv[2])
else:
    p1Type = 0
if len(sys.argv) > 3:
    p2Type = int(sys.argv[3])
else:
    p2Type = 1
if useGlue:
    EnvironmentLoader.loadEnvironment(World(p1Type,2))
else:
    world = World(p1Type,p2Type)
    world.start()
    while True:
        world.step()
