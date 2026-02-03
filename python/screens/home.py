import pygame 
import utils.constants as C

def home_screen(screen,clock):
    font_title = pygame.font.SysFont(None,64)
    font_btn = pygame.font.SysFont(None,36)

    start_rect = pygame.Rect(C.WIDTH // 2 -120 , C.HEIGHT // 2 -20 ,240 ,50 )
    exit_rect = pygame.Rect(C.WIDTH // 2 -120 , C.HEIGHT // 2 + 50 ,240 ,50 )

    while True :
        #------SCREEN SETTINGS----------------------
        clock.tick(C.FPS)
        screen.fill(C.BACKGROUND_COLOR)

        #------TITLE----------------------
        title= font_title.render("ACT-3",True,C.WHITE)
        screen.blit(title,title.get_rect(center=(C.WIDTH//2 , 200)))

        #------BUTTONS ----------------------
        pygame.draw.rect(screen,C.ACCENT_COLOR,start_rect,border_radius=8)
        pygame.draw.rect(screen,C.RED, exit_rect,border_radius = 8)

        start_text = font_btn.render("START",True,C.BLACK)
        exit_text = font_btn.render("EXIT",True,C.WHITE)

        screen.blit(start_text,start_text.get_rect(center =start_rect.center))
        screen.blit(exit_text,start_text.get_rect(center =exit_rect.center))

        #------EVENTS----------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                return "EXIT"
            if event.type == pygame.MOUSEBUTTONDOWN and  event.button == 1 :
                if start_rect.collidepoint(event.pos):
                    return "SIMULATION"
                if exit_rect.collidepoint(event.pos):
                    return "EXIT"
                

        pygame.display.flip()