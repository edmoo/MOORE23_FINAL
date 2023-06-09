import pygame
from const import *
pygame.font.init()

back_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)

host_field = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 32)
start_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)

class HostMenu:

    def __init__(self):
        pass
    #show methods

    def show_screen(self, surface, FEN, host_ip, client_joined):
        font_path = os.path.join(os.path.dirname(__file__), "OpenDyslexic-Regular.otf")
        FEN_font = pygame.font.Font(font_path, 12)
        #clear the surface
        surface.fill(COLOUR_ONE)
        text_surface = FEN_font.render(FEN, True, (0, 0, 0))

        pygame.draw.rect(surface, COLOUR_TWO, host_field, 2)
        host_text = font.render("1.FEN:", True, BLACK)
        surface.blit(host_text, (WIDTH // 4 - host_text.get_width() - 16, HEIGHT // 3))
        
        #draw start button
        pygame.draw.rect(surface, COLOUR_TWO, start_field)
        start_text = font.render("2.Start", True, BLACK)
        start_text_pos = start_text.get_rect(center = start_field.center)
        surface.blit(start_text, start_text_pos)

        #draw back button
        pygame.draw.rect(surface, COLOUR_TWO, back_button)
        back_text = font.render("3.Back", True, BLACK)
        back_text_pos = back_text.get_rect(center=back_button.center)
        surface.blit(back_text, back_text_pos)


        surface.blit(text_surface, (host_field.x+5, host_field.y+5))
        
        text_surface = FEN_font.render(FEN, True, (0, 0, 0))

        ip_surface = font.render("Local Ip: "+str(host_ip), True, BLACK)
        surface.blit(ip_surface, (10, 10))  #host can see their ip in the top left
        
        if(client_joined):
            client_connected = base_font.render("Client Joined", True, COLOUR_THREE)
            surface.blit(client_connected, (start_field.x, start_field.y+35))      
