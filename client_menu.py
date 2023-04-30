import pygame
from const import *

back_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)

client_field = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 32)
join_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)



class ClientMenu:

    def __init__(self):
        pass

    def show_screen(self, surface, ipInput):

        #clear surface
        surface.fill(COLOUR_ONE)
        text_surface = base_font.render(ipInput, True, (0, 0, 0))

        pygame.draw.rect(surface, COLOUR_TWO, client_field, 2)
        client_text = font.render("1.IP:", True, BLACK)
        surface.blit(client_text, (WIDTH // 4 - client_text.get_width() - 16, HEIGHT // 3))
        
        pygame.draw.rect(surface, COLOUR_TWO, join_field)
        join_text = font.render("2.Join", True, BLACK)
        join_text_pos = join_text.get_rect(center=join_field.center)
        surface.blit(join_text, join_text_pos)

        #draw back button
        pygame.draw.rect(surface, COLOUR_TWO, back_button)
        back_text = font.render("3.Back", True, BLACK)
        back_text_pos = back_text.get_rect(center=back_button.center)
        surface.blit(back_text, back_text_pos)

        surface.blit(text_surface, (client_field.x+5, client_field.y+5))