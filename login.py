import pygame
from const import *

pygame.font.init()


# Create the login button
login_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)
# Create the font for the username and password fields
font = font = pygame.font.SysFont("Arial", 32)
base_font = pygame.font.Font(None, 32)

# Create the username and password fields
username_field = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 32)
password_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)



class Login:

    def __init__(self):
        pass

    #show methods

    def show_screen(self, surface, username, password):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)

        # Clear the surface
        surface.fill(WHITE)
        text_surface = base_font.render(username, True, (0, 0, 0))
        passStar = ""
        for i in password:
            passStar += "*"

        pass_surface = base_font.render(passStar, True, (0,0,0))

        # Draw the username field
        pygame.draw.rect(surface, BLACK, username_field, 2)
        username_text = font.render("Username:", True, BLACK)
        surface.blit(username_text, (WIDTH // 4 - username_text.get_width() - 16, HEIGHT // 3 + 8))
        
        # Draw the password field
        pygame.draw.rect(surface, BLACK, password_field, 2)
        password_text = font.render("Password:", True, BLACK)
        surface.blit(password_text, (WIDTH // 4 - password_text.get_width() - 16, HEIGHT // 2 + 8))
        
        # Draw the login button
        pygame.draw.rect(surface, BLACK, login_button, 2)
        login_text = font.render("Login", True, BLACK)
        surface.blit(login_text, (WIDTH // 2 - login_text.get_width() // 2, HEIGHT // 1.5 + 8))
        
        surface.blit(text_surface, (username_field.x+5, username_field.y+5))
        surface.blit(pass_surface, (password_field.x+5, password_field.y+5))

