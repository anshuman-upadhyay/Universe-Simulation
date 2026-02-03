# ============================================================
# Simulation Screen (UI Wrapper)
# ============================================================
# This file is responsible for:
#   - Displaying simulation-level UI (END button)
#   - Delegating physics + rendering to core logic
#   - Deciding when to return to HOME or EXIT
# ============================================================

import pygame
import utils.constants as C

from core.simulation_loop import run_simulation


# ------------------------------------------------------------
# Simulation Screen
# ------------------------------------------------------------

def simulation_screen(screen,clock): 
    font= pygame.font.SysFont(None,24)
    end_btn = pygame.Rect(C.WIDTH- 160 ,20 ,140 ,40)

    while True :
        # ----------------------------------------------------
        # Run one frame of the simulation
        # ----------------------------------------------------
        
        result = run_simulation(screen,clock)
        
        # ----------------------------------------------------
        # Draw END button overlay
        # ----------------------------------------------------
        pygame.draw.rect(screen, C.RED, end_btn, border_radius=6)
        end_text = font.render("END", True, C.WHITE)
        screen.blit(end_text, end_text.get_rect(center=end_btn.center))

        pygame.display.flip()


        # ----------------------------------------------------
        # Handle UI-level events (navigation only)
        # ----------------------------------------------------

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return "EXIT"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 :
                if end_btn.collidepoint(event.pos) :
                    return "HOME"
                
        # ----------------------------------------------------
        # If simulation loop explicitly ended
        # ----------------------------------------------------
        if result == "EXIT":
            return "EXIT"