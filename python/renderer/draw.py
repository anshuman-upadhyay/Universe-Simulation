import pygame  
import utils.constants as C
#Empty screen generation
def clear_screen(screen,color):
    screen.fill(color)

#Display text Function
def draw_text(screen,text,pos,font,color) :
    text_surface = font.render(text,True,color)
    screen.blit(text_surface,pos)

#Body Creation Function - currently just a circle
def draw_body(screen, body, font):
    pygame.draw.circle(
        screen,
        body.color,
        (int(body.position[0]), int(body.position[1])),
        body.radius
    )

    # Draw ID text
    text_surface = font.render(str(body.id), True, (0, 0, 0))
    text_rect = text_surface.get_rect(
        center=(
            int(body.position[0]),
            int(body.position[1])
        )
    )
    screen.blit(text_surface, text_rect)


def draw_active_shadow(screen,body) :
    SHADOW_COLOR = C.LIGHT_GRAY
    SHADOW_RADIUS = body.radius+ 4
    pygame.draw.circle(
        screen,
        SHADOW_COLOR,
        (int(body.position[0]),int(body.position[1])),
        SHADOW_RADIUS
    )