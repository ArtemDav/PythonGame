import pygame
import time
import checkbox
from settings import Settings as setup


#################################
#       DEFINE COLOR
red = pygame.Color("red")
black = pygame.Color("black")
white = pygame.Color("white")
slateblue = pygame.Color("#191970")
blue = pygame.Color("#1E90FF")
#################################

pygame.init()
background_image = pygame.image.load("assets/Image/background.png")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = pygame.display.get_surface().get_size()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.music.load("assets/Sounds/Main_Music.wav")
pygame.mixer.music.play()
#################################
#       SETTINGS FROM BASE
base = setup()
#       CHECKBOX
boolean = str(base.load_settings("Sounds")).replace("True", "1").replace("False", "0")
sounds = checkbox.Checkbox(w // 4 + 20, h // 3 + 20, "Sounds", bool(int(boolean)))
#################################


class Button:
    def __init__(self, text, size_text, center=False, center_pos=0, color=white):
        self.color = color
        self.text = text
        self.size_text = size_text
        self.center = center
        self.center_pos = center_pos
        self.x, self.y = 0, 0
        self.text_w, self.text_h = 0, 0

    def draw(self):
        font = pygame.font.Font("assets/Font/18876.ttf", (w + h) // 40)
        text = font.render(self.text, 1, self.color)
        place = text.get_rect(center=(w // 2, h // 2 + self.center_pos))
        self.x = place[0]
        self.y = place[1]
        self.text_w = text.get_width()
        self.text_h = text.get_height()
        text_x = self.size_text[0]
        text_y = self.size_text[1]
        if self.center:
            screen.blit(text, place)

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.text_w + 20:
            if pos[1] > self.y + 20 and pos[1] < self.y + self.text_h:
                return True
        return False


def drawText(text, font_size, size_text, color=white):
    font = pygame.font.Font("assets/Font/18876.ttf", font_size)
    text = font.render(text, 1, color)
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = size_text[0]
    text_y = size_text[1]
    screen.blit(text, (text_x, text_y))

def drawMenu():
    text = "Main Menu"
    size = (w + h) // 40
    #################################
    #       DRAW MENU BOX
    pygame.draw.rect(screen, slateblue, (w // 4, h // 4, w // 2, h // 2), 0)
    pygame.draw.rect(screen, blue, (w // 4, h // 4, w // 2, h // 24), 0)
    pygame.draw.rect(screen, blue, (w // 4, h // 4, w // 6, h // 12), 0)
    pygame.draw.polygon(screen, blue, [(w // 2.4, h // 3.001), (w // 2.4, h // 3.5), (w // 2 - 60, h // 4)], 0)
    #################################
    if about:
        text = "About"
        drawText("PyGame Project: 1.0.0", size - 15, (w // 4 + 50, h // 2 - 100))
        drawText("Author: Artem Davydov (@ArtemDav)", size - 15, (w // 4 + 50, h // 2 - 55))
        drawText("To: Yandex Lyceum", size - 15, (w // 4 + 50, h // 2 - 15))
        drawText("Email: artemdavyd14@gmail.com", size - 15, (w // 4 + 50, h // 2 + 50))
    if settings:
        text = "Settings"
        sounds.update()
    drawText(text, size, (w // 4 + 5, h // 4), color=white)


#################################
# SOUNDS
click = pygame.mixer.Sound("assets/Sounds/click.wav")
target = pygame.mixer.Sound("assets/Sounds/target.wav")
target.set_volume(0.1)
#       BUTTONS
start_button = Button("Start", (0, 0), True, -45)
about_button = Button("About", (0, 0), True, 20)
settings_button = Button("Settings", (0, 0), True, 85)
exit_button = Button("Exit", (0, 0), True, 150)
return_button = Button("Return", (0, 0), True, 145)
#################################

play_sound = 0
about = False
settings = False

running = True
while running:
    if sounds.isChecked():
        pygame.mixer.music.set_volume(1)
    else:
        pygame.mixer.music.set_volume(0)
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if sounds.isOver(pos):
                sounds.changeState()
                flag = sounds.isChecked()
                play_sound = int(flag)
                base.cursor.execute("""UPDATE settings SET Value = '{0}' WHERE Name = '{1}'""".format(flag, "Sounds"))
                base.base.commit() 
            if not about and not settings:
                if start_button.isOver(pos):
                    click.play()
                    import game
                if about_button.isOver(pos):
                    click.play()
                    about = True
                if settings_button.isOver(pos):
                    click.play()
                    settings = True
                if exit_button.isOver(pos):
                    click.play()
                    running = False
            if return_button.isOver(pos):
                click.play()
                settings = False
                about = False
        if event.type == pygame.MOUSEMOTION:
            if not about and not settings:
                if start_button.isOver(pos):
                    start_button.color = red
                    if not play_sound:
                        target.play()
                else:
                    start_button.color = white

                if about_button.isOver(pos):
                    about_button.color = red
                    if not play_sound:
                        target.play()
                else:
                    about_button.color = white
                if exit_button.isOver(pos):
                    exit_button.color = red
                    if not play_sound:
                        target.play()
                else:
                    exit_button.color = white

                if settings_button.isOver(pos):
                    if not play_sound:
                        target.play()
                    settings_button.color = red
                else:
                    settings_button.color = white

            if return_button.isOver(pos):
                if not play_sound:
                    target.play()
                return_button.color = red
            else:
                return_button.color = white
            target.fadeout(500)

    screen.blit(background_image, [0, 0])
    drawMenu()
    if not about and not settings:
        start_button.draw()
        about_button.draw()
        exit_button.draw()
        settings_button.draw()
    else:
        return_button.draw()
    pygame.display.flip()
pygame.quit()