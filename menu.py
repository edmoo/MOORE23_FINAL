import pygame
from const import *

host_button = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 32)
account_button = pygame.Rect(WIDTH // 4, (HEIGHT // 2.5)+10, WIDTH // 2, 32)
join_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)
quit_field = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)
title_font = pygame.font.SysFont("Oswald", 120)

class Menu:

    def __init__(self):
        pass

    #show methods

    def show_screen(self, surface):

        # Clear the surface
        surface.fill(COLOUR_ONE)

        # Draw the Host button
        pygame.draw.rect(surface, COLOUR_TWO, host_button)
        host_text = font.render("1.Host", True, BLACK)
        host_text_pos = host_text.get_rect(center=host_button.center)
        surface.blit(host_text, host_text_pos)

        # Draw the Account Settings button
        pygame.draw.rect(surface, COLOUR_TWO, account_button)
        account_text = font.render("2.Account Settings", True, BLACK)
        account_text_pos = account_text.get_rect(center=account_button.center)
        surface.blit(account_text, account_text_pos)

        # Draw the Join button
        pygame.draw.rect(surface, COLOUR_TWO, join_field)
        join_text = font.render("3.Join", True, BLACK)
        join_text_pos = join_text.get_rect(center=join_field.center)
        surface.blit(join_text, join_text_pos)

        # Draw the Quit button
        pygame.draw.rect(surface, COLOUR_TWO, quit_field)
        quit_text = font.render("4.Quit", True, BLACK)
        quit_text_pos = quit_text.get_rect(center=quit_field.center)
        surface.blit(quit_text, quit_text_pos)

        #Draw the title
        title_text = title_font.render("ChessPAL", True, COLOUR_THREE)
        surface.blit(title_text, (WIDTH // 3 - 10, 40))

