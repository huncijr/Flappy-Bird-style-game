import pygame
import random
import os
import time


# Screen settings
szelesseg = 600
magassag = 600
FPS = 60
oraja = pygame.time.Clock()

# Colors
VILAGOS_KEK = (173, 216, 230)
ZOLD = (0, 255, 0)
SARGA = (255, 255, 0)
KOMBO = (255, 0, 0)
PIROS = "#FF0000"

# Bird settings
madar_szelesseg = 30
madar_magassag = 30
madar_x = 50
madar_y = magassag / 2
madar_y_vel = 0
gravitacio = 0.3
ugras_ero = -10
mozgasi_ero = 5

# Pipe settings
csoveles = 80
csokozon = 200
pipe_distance = 300
csovek = []
coin = 0

# Game texts
Eredmeny = 0
pygame.mixer.init()
sound_effect1 = pygame.mixer.Sound(r"penclicking.mp3")
sound_effect2 = pygame.mixer.Sound(r"ending.mp3")

# Define functions
def rajzolas(kepernyo, madar_y, csovek, Eredmeny, font):
    kepernyo.fill(VILAGOS_KEK)
    pygame.draw.rect(kepernyo, KOMBO, (madar_x, madar_y, madar_szelesseg, madar_magassag))

    for csov in csovek:
        pygame.draw.rect(kepernyo, ZOLD, (csov[0], 0, csoveles, csov[1]))  # Felső cső
        pygame.draw.rect(kepernyo, ZOLD, (csov[0], csov[1] + csokozon, csoveles, magassag - csov[1] - csokozon))  # Alsó cső

        if csov[2]:  
            kor_x = csov[0] + csoveles // 2 
            kor_y = csov[1] + csokozon // 2  
            pygame.draw.circle(kepernyo, PIROS, (kor_x, kor_y), 15, width=4)  

    score_text = font.render(f'Eredmeny: {Eredmeny * 10:03}', True, SARGA if Eredmeny >= 30 else (255, 255, 255))
    kepernyo.blit(score_text, (10, 10))
    pont_text = font.render(f'Coinok: {coin}', True, (255, 255, 255))
    coin_x = szelesseg - pont_text.get_width() - 10
    coin_y = 10
    kepernyo.blit(pont_text, (coin_x, coin_y))
    pygame.display.update()

def mozgatas(madar_y, madar_y_vel):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, madar_y, madar_y_vel
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                madar_y_vel = ugras_ero * 1.1
            elif event.key == pygame.K_UP:
                madar_y_vel = -mozgasi_ero
            elif event.key == pygame.K_DOWN:
                madar_y_vel = mozgasi_ero * 1.1
    madar_y_vel += gravitacio
    madar_y += madar_y_vel
    if madar_y < 0:
        madar_y = 0
    if madar_y + madar_magassag > magassag:
        madar_y = magassag - madar_magassag
    return True, madar_y, madar_y_vel

def csovelet(csovek, Eredmeny, coin, madar_x, madar_y):
    if len(csovek) == 0 or csovek[-1][0] < szelesseg - pipe_distance:
        csov_magas = random.randint(50, magassag - csokozon - 50)
        csovek.append([szelesseg, csov_magas, True])  # Az új cső és egy flag a coinhoz

    csovek_to_remove = []  

    for csov in csovek:
        csov[0] -= 4
        if csov[0] + csoveles < madar_x and csov[2]:
            Eredmeny += 1
            csov[2] = False

        kor_x = csov[0] + csoveles // 2
        kor_y = csov[1] + csokozon // 2

        if madar_x + madar_szelesseg > kor_x - 15 and madar_x < kor_x + 15:
            if madar_y + madar_magassag / 2 > kor_y - 15 and madar_y + madar_magassag / 2 < kor_y + 15:
                if csov[2]:
                    sound_effect1.play()
                    Eredmeny += 1
                    coin += 1
                    csov[2] = False  

        if csov[0] + csoveles < 0:
            csovek_to_remove.append(csov)

    for csov in csovek_to_remove:
        csovek.remove(csov)

    return csovek, Eredmeny, coin

def Init():
    pygame.init()

def futo(callback):
    global madar_y_vel, coin
    coin = 0
    font = pygame.font.SysFont('Arial', 36)
    madar_y = magassag / 2
    madar_y_vel = 0
    csovek = []
    Eredmeny = 0
    kepernyo = pygame.display.set_mode((szelesseg, magassag))
    pygame.display.set_caption("Flappy Bird")

    try:
        while True:
            continue_running, madar_y, madar_y_vel = mozgatas(madar_y, madar_y_vel)
            if not continue_running:
                break
            csovek, Eredmeny, coin = csovelet(csovek, Eredmeny, coin, madar_x, madar_y)
            rajzolas(kepernyo, madar_y, csovek, Eredmeny, font)

            if ellenorzes(madar_y, csovek):
                pontszam_mentese(Eredmeny, coin)
                break
            oraja.tick(FPS)
    except Exception as e:
        print(f"Hiba történt a játék futása közben: {e}")
    finally:
        pygame.display.set_mode((800, 600), flags=pygame.HIDDEN)
        callback()

def pontszam_mentese(Eredmeny, coin):
    file_path = "pontszam.txt"
    folder_path = os.path.dirname(file_path)

    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"Mappa létrehozva: {folder_path}")
        except Exception as e:
            print(f"Hiba történt a mappa létrehozása közben: {e}")
            return
    try:
        with open(file_path, "a") as file:
            file.write(f"{Eredmeny * 10} {coin}\n")
            print(" ")
    except Exception as e:
        print(f"Hiba történt a fájl mentése közben: {e}")

    except FileNotFoundError:
        print("A fájl nem létezik")
    except PermissionError:
        print("Nincs jogosultságod a fájl olvasásához")
    except Exception as e:
        print(f"Hiba történt a fájl olvasása közben: {e}")

def ellenorzes(madar_y, csovek):
    for csov in csovek:
        if madar_x + madar_szelesseg > csov[0] and madar_x < csov[0] + csoveles:
            if madar_y < csov[1] or madar_y + madar_magassag > csov[1] + csokozon:
                sound_effect2.play()
                time.sleep(4)
                return True
    return False

def fajl_torol():
    file_path = "pontszam.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
    # else:
    #     print("a fajl nem talalhato")


