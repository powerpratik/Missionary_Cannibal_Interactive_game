import sys
import pygame
import os


def getkey():
    'Identifies currently pressed key and returns it via a variable'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame.image.save(window, "game-over.bmp")
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                sys.exit()
            if event.key in controls:
                key = controls[event.key]
                return key


def raft(who, step):
    'Performs the transport process of the actors to the other bank'
    done = False
    for actor in who:
        actor["rect"] = actor["rect"].move((step, 0))

        if not arena.contains(actor["rect"]):
            actor["rect"] = actor["rect"].move((-step, 0))
            actor["surf"] = \
                pygame.transform.flip(actor["surf"], True, False)
            done = True


    return done


def failure(size, color, delay):
    'Draws failure screen on top of the current game state'
    myfont = pygame.font.Font('freesansbold.ttf', size)
    msg = myfont.render("Failure", True, color)
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(delay)


def success(size, color, delay):
    'Draws success screen on top of the current game state'
    myfont = pygame.font.Font('freesansbold.ttf', font_size)
    msg = myfont.render("Success", True, color)
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(delay)

def currentstate(size,color,delay,misn,can,boatside):
    'Displays the current game states'
    global tot_misn,tot_canb
    global storedgamestate,n_misn,n_can

    if  boatside=="R":
        tot_misn=tot_misn-misn
        tot_canb=tot_canb-can
        n_misn,n_can=0,0
    else:
        tot_misn+=misn
        tot_canb+=can
        n_misn,n_can=0,0
    myfont = pygame.font.Font('freesansbold.ttf', font_size)
    msg = myfont.render("State:[%d,%d,%s]"%(tot_misn,tot_canb,boatside), True, color)
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, (width-600,height-100))



def instruction(size):
    'Displays game instructions'
    font=pygame.font.Font('freesansbold.ttf',18)
    msg=font.render("Instructions:\
    1:Move 2 cannibals\
    2:Move 2 Missionaries\
    3: Move each\
    4: Move 1 cannibal 5: Move 1 missionary",True,firered)
    window.blit(msg,(0,0))
# variables & parametres
width = 1000
height = 700
red = (255, 0, 0)
green = (127, 255, 0)
blue=(0,191,255)
firered=(178,34,34)
font_size = 80
delay = 1500
raft_step = -5
game_caption = "Cannibals & Missionaries"
storedgamestate="L"

# setting window parametres up
os.environ['SDL_VIDEO_WINDOW_POS'] = "center"
pygame.init()

window = pygame.display.set_mode((width, height))
pygame.display.set_caption(game_caption)
background = pygame.image.load("/home/pratik/AI project/cm_pygame-master/background.png")
arena = window.get_rect()
tot_misn=3
tot_canb=3
# assigning images
can1 = {"file": "/home/pratik/AI project/cm_pygame-master/cannibals.png"}
can2 = {"file": "/home/pratik/AI project/cm_pygame-master/cannibals.png"}
can3 = {"file": "/home/pratik/AI project/cm_pygame-master/cannibals.png"}
mis1 = {"file": "/home/pratik/AI project/cm_pygame-master/missionarys.png"}
mis2 = {"file": "/home/pratik/AI project/cm_pygame-master/missionarys.png"}
mis3 = {"file": "/home/pratik/AI project/cm_pygame-master/missionarys.png"}

n_misn,n_can=0,0
actors = [can1, can2, can3, mis1, mis2, mis3]

for i, actor in enumerate(actors):
    actor["surf"] = pygame.image.load(actor["file"])
    actor["rect"] = actor["surf"].get_rect()
    actor["rect"].midleft = (0, (i + 1) * arena.height / 7)

# all possible scenarios (gamestates)
gamegraph = {
            "Lcccmmm-": {
                        "1": "Rcmmm-cc", "2": "Rcccm-mm",
                        "3": "Rccmm-cm", "4": "Rccmmm-c",
                        "5": "Rcccmm-m"
                        },
            "Rccmm-cm": {
                        "1": "Rccmm-cm", "2": "Rccmm-cm",
                        "3": "Lcccmmm-", "4": "Lcccmm-m",
                        "5": "Lccmmm-c"
                        },
            "Lccmm-cm": {
                        "1": "Rmm-cccm", "2": "Rcc-cmmm",
                        "3": "Rcm-ccmm", "4": "Rcmm-ccm",
                        "5": "Rccm-cmm"
                        },
            "Rccmmm-c": {
                        "1": "Rccmmm-c", "2": "Rccmmm-c",
                        "3": "Rccmmm-c", "4": "Lcccmmm-",
                        "5": "Rccmmm-c"
                        },
            "Lccmmm-c": {
                        "1": "Rmmm-ccc", "2": "Rccm-cmm",
                        "3": "Rcmm-ccm", "4": "Rcmmm-cc",
                        "5": "Rccmm-cm"
                        },
            "Rmmm-ccc": {
                        "1": "Lccmmm-c", "2": "Rmmm-ccc",
                        "3": "Rmmm-ccc", "4": "Lcmmm-cc",
                        "5": "Rmmm-ccc"
                        },
            "Rcmmm-cc": {
                        "1": "Lcccmmm-", "2": "Rcmmm-cc",
                        "3": "Rcmmm-cc", "4": "Lccmmm-c",
                        "5": "Rcmmm-cc"
                        },
            "Lcmmm-cc": {
                        "1": "Lcmmm-cc", "2": "Rcm-ccmm",
                        "3": "Rmm-cccm", "4": "Rmmm-ccc",
                        "5": "Rcmm-ccm"
                        },
            "Rcm-ccmm": {
                        "1": "Lcccm-mm", "2": "Lcmmm-cc",
                        "3": "Lccmm-cm", "4": "Lccm-cmm",
                        "5": "Lcmm-ccm"
                        },
            "Rcc-cmmm": {
                        "1": "Rcc-cmmm", "2": "Lccmm-cm",
                        "3": "Lcccm-mm", "4": "Lccc-mmm",
                        "5": "Lccm-cmm"
                        },
            "Lccc-mmm": {
                        "1": "Rc-ccmmm", "2": "Lccc-mmm",
                        "3": "Lccc-mmm", "4": "Rcc-cmmm",
                        "5": "Lccc-mmm"
                        },
            "Rc-ccmmm": {
                        "1": "Lccc-mmm", "2": "Lcmm-ccm",
                        "3": "Lccm-cmm", "4": "Lcc-cmmm",
                        "5": "Lcm-ccmm"
                        },
            "Lccmmm-c": {
                        "1": "Rmmm-ccc", "2": "Rccm-cmm",
                        "3": "Rcmm-ccm", "4": "Rcmmm-cc",
                        "5": "Rccmm-cm"
                        },
            "Lcc-cmmm": {
                        "1": "-cccmmm", "2": "Lcc-cmmm",
                        "3": "Lcc-cmmm", "4": "Rc-ccmmm",
                        "5": "Lcc-cmmm"
                        },
            "Lcm-ccmm": {
                        "1": "Lcm-ccmm", "2": "Lcm-ccmm",
                        "3": "-cccmmm", "4": "Lcm-ccmm",
                        "5": "Lcm-ccmm"
                        },
            "Rcccmm-m": "failure",
            "Rcccm-mm": "failure",
            "Rccm-cmm": "failure",
            "Rm-cccmm": "failure",
            "Rmm-cccm": "failure",
            "Rcmm-ccm": "failure",
            "Lcccmm-m": "failure",
            "Lcccm-mm": "failure",
            "Lccm-cmm": "failure",
            "Lm-cccmm": "failure",
            "Lmm-cccm": "failure",
            "Lcmm-ccm": "failure",
            "-cccmmm": "success"
            }

gamestate = "Lcccmmm-"  # initial gamestate
controls = {
            pygame.K_1: "1",
            pygame.K_2: "2",
            pygame.K_3: "3",
            pygame.K_4: "4",
            pygame.K_5: "5"
            }
action = "listen"

fpsClock = pygame.time.Clock()
while True:

    # defining potential passengers regarding current gamestate
    if gamestate == "Lcccmmm-":
        candbl = [can1, can2]
        misdbl = [mis1, mis2]
        mix = [can1, mis1]
        cansng = [can1]
        missng = [mis1]
    elif gamestate == "Rccmm-cm":
        mix = [can1, mis1]
        cansng = [can1]
        missng = [mis1]
    elif gamestate == "Lccmm-cm":
        candbl = [can2, can3]
        misdbl = [mis2, mis3]
        mix = [can2, mis2]
        cansng = [can2]
        missng = [mis2]
    elif gamestate == "Rccmmm-c":
        cansng = [can1]
    elif gamestate == "Lccmmm-c":
        candbl = [can2, can3]
        misdbl = [mis1, mis2]
        mix = [can2, mis1]
        cansng = [can2]
        missng = [mis1]
    elif gamestate == "Rmmm-ccc":
        candbl = [can2, can3]
        cansng = [can3]
    elif gamestate == "Rcmmm-cc":
        candbl = [can1, can2]
        cansng = [can2]
    elif gamestate == "Lcmmm-cc":
        misdbl = [mis1, mis2]
        mix = [can3, mis1]
        cansng = [can3]
        missng = [mis1]
    elif gamestate == "Rcm-ccmm":
        candbl = [can1, can2]
        misdbl = [mis1, mis2]
        mix = [can2, mis2]
        cansng = [can2]
        missng = [mis2]
    elif gamestate == "Rcc-cmmm":
        misdbl = [mis2, mis3]
        mix = [can1, mis3]
        cansng = [can1]
        missng = [mis3]
    elif gamestate == "Lccc-mmm":
        candbl = [can1, can2]
        cansng = [can1]
    elif gamestate == "Rc-ccmmm":
        candbl = [can1, can2]
        misdbl = [mis2, mis3]
        mix = [can2, mis3]
        cansng = [can2]
        missng = [mis3]
    elif gamestate == "Lccmmm-c":
        candbl = [can2, can3]
        misdbl = [mis1, mis2]
        mix = [can2, mis1]
        cansng = [can2]
        missng = [mis1]
    elif gamestate == "Lcc-cmmm":
        candbl = [can2, can3]
        cansng = [can2]
    elif gamestate == "Lcm-ccmm":
        mix = [can3, mis3]
    passengers = {"1": candbl,
                  "2": misdbl,
                  "3": mix,
                  "4": cansng,
                  "5": missng
                  }
    if action == "listen":
        if gamestate == "-cccmmm":
            action = "success"
        else:
            key = getkey()

            if key in gamegraph[gamestate]:
                old_gamestate = gamestate
                gamestate = gamegraph[gamestate][key]
                print(gamestate)
                storedgamestate=gamestate[0]
                if not gamestate == old_gamestate:
                    raft_who = passengers[key]
                    if passengers[key]==passengers["1"]:
                        n_can=2
                        n_misn=0
                        #currentstate(font_size,red,delay,n_can,n_misn,gamestate[0])

                    if passengers[key]==passengers["2"]:
                        n_can=0
                        n_misn=2
                        #currentstate(font_size,red,delay,n_can,n_misn,gamestate[0])
                    if passengers[key]==passengers["3"]:
                        n_can=1
                        n_misn=1
                        #currentstate(font_size,red,delay,n_can,n_misn,gamestate[0])
                    if passengers[key]==passengers["4"]:
                        n_can=1
                        n_misn=0
                        #currentstate(font_size,red,delay,n_can,n_misn,gamestate[0])
                    if passengers[key]==passengers["5"]:
                        n_can=0
                        n_misn=1
                        #currentstate(font_size,red,delay,n_can,n_misn,gamestate[0])

                    raft_step = -raft_step
                    action = "raft"
    if action == "raft":
        done = raft(raft_who, raft_step)
        if done:
            if gamegraph[gamestate] == "failure":
                action = "failure"
            else:
                action = "listen"
    if action == "failure":
        failure(font_size, red, delay)
        sys.exit()
    if action == "success":
        success(font_size, green, delay)
        sys.exit()
    window.blit(background, (0, 0))
    instruction(18)
    currentstate(font_size,red,delay,n_can,n_misn,storedgamestate)
    for actor in actors:
        window.blit(actor["surf"], actor["rect"])
    pygame.display.flip()
    fpsClock.tick(120)
