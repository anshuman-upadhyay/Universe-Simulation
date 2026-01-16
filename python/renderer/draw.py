import pygame  

#Empty screen generation
def clear_screen(screen,color):
    screen.fill(color)

#Display text Function
def draw_text(screen,text,pos,font,color) :
    text_surface = font.render(text,True,color)
    screen.blit(text_surface,pos)

#Body Creation Function - currently just a circle
def draw_body(screen,body):
    pygame.draw.circle(
        screen,
        body.color,
        (int(body.position[0]),int(body.position[1])),
        body.radius
    )