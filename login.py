import pygame
from const import *

pygame.font.init()


# Create the login button
login_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)
reg_button = pygame.Rect(WIDTH // 4, login_button.bottom + 10, WIDTH // 2, 32)

# Create the font for the username and password fields
font = font = pygame.font.SysFont("Arial", 32)
base_font = pygame.font.Font(None, 32)

# Create the username and password fields
username_field = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 32)
password_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)
passwordAUTH_field = pygame.Rect(WIDTH // 4, HEIGHT // 1, WIDTH // 2, 32)

confirm_password_field = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 50, WIDTH // 2, 32)
email_field = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, 32)

# Create the username, password, password authentication, and email fields
REGusername_field = pygame.Rect(WIDTH // 4, HEIGHT // 5, WIDTH // 2, 32)
REGpassword_field = pygame.Rect(WIDTH // 4, HEIGHT // 5 + 50, WIDTH // 2, 32)
REGpassAuth_field = pygame.Rect(WIDTH // 4, HEIGHT // 5 + 100, WIDTH // 2, 32)
REGemail_field = pygame.Rect(WIDTH // 4, HEIGHT // 5 + 150, WIDTH // 2, 32)
back_text = font.render('Back', True, (0,0,0))
back_rect = pygame.Rect(50, 400, 100, 50)
register_button = pygame.Rect(WIDTH // 4, HEIGHT // 5 + 210, WIDTH // 2, 32)

class Login:

    def __init__(self):
        pass

    #show methods

    def show_screen(self, surface, username, password):
        
        # Clear the surface
        surface.fill(COLOUR_ONE)
        text_surface = base_font.render(username, True, (0, 0, 0))
        passStar = ""
        for i in password:
            passStar += "*"

        pass_surface = base_font.render(passStar, True, (0,0,0))

        # Draw the username field
        pygame.draw.rect(surface, COLOUR_TWO, username_field, 2)
        username_text = font.render("Username:", True, COLOUR_TWO)
        surface.blit(username_text, (WIDTH // 4 - username_text.get_width() - 16, HEIGHT // 3 + 8))
        
        # Draw the password field
        pygame.draw.rect(surface, COLOUR_TWO, password_field, 2)
        password_text = font.render("Password:", True, COLOUR_TWO)
        surface.blit(password_text, (WIDTH // 4 - password_text.get_width() - 16, HEIGHT // 2 + 8))
        
        # Draw the login button
        pygame.draw.rect(surface, COLOUR_TWO, login_button, 2)
        login_text = font.render("Login", True, COLOUR_TWO)
        surface.blit(login_text, (WIDTH // 2 - login_text.get_width() // 2, HEIGHT // 1.5))

        # Draw the register button
        pygame.draw.rect(surface, COLOUR_TWO, reg_button, 2)
        register_text = font.render("Register New Account", True, COLOUR_TWO)
        surface.blit(register_text, (WIDTH // 2 - register_text.get_width() // 2, login_button.bottom + 8))
        
        surface.blit(text_surface, (username_field.x+5, username_field.y+5))
        surface.blit(pass_surface, (password_field.x+5, password_field.y+5))
    
    def register(self, surface, username, password, passAuth, email):
        # Clear the surface
        surface.fill(COLOUR_ONE)

        # Create the font for the fields
        font = pygame.font.SysFont("Arial", 32)
        base_font = pygame.font.Font(None, 32)

        # Draw the username field
        pygame.draw.rect(surface, COLOUR_TWO, REGusername_field, 2)
        username_text = font.render("Username:", True, COLOUR_TWO)
        surface.blit(username_text, (WIDTH // 4 - username_text.get_width() - 16, HEIGHT // 5 + 8))

        # Draw the password field
        pygame.draw.rect(surface, COLOUR_TWO, REGpassword_field, 2)
        password_text = font.render("Password:", True, COLOUR_TWO)
        surface.blit(password_text, (WIDTH // 4 - password_text.get_width() - 16, HEIGHT // 5 + 58))

        # Draw the password authentication field
        pygame.draw.rect(surface, COLOUR_TWO, REGpassAuth_field, 2)
        passAuth_text = font.render("Confirm Password:", True, COLOUR_TWO)
        surface.blit(passAuth_text, (WIDTH // 4 - passAuth_text.get_width() - 16, HEIGHT // 5 + 108))

        # Draw the email field
        pygame.draw.rect(surface, COLOUR_TWO, REGemail_field, 2)
        email_text = font.render("Email:", True, COLOUR_TWO)
        surface.blit(email_text, (WIDTH // 4 - email_text.get_width() - 16, HEIGHT // 5 + 158))

        # Draw the register button
        pygame.draw.rect(surface, COLOUR_TWO, register_button, 2)
        register_text = font.render("Register", True, COLOUR_TWO)
        surface.blit(register_text, (WIDTH // 2 - register_text.get_width() // 2, HEIGHT // 5 + 218))

        # Render the input text
        username_surface = base_font.render(username, True, COLOUR_TWO)
        pass_surface = base_font.render("*" * len(password), True, COLOUR_TWO)
        passAuth_surface = base_font.render("*" * len(passAuth), True, COLOUR_TWO)
        email_surface = base_font.render(email, True, COLOUR_TWO)

        pygame.draw.rect(surface, (128, 128, 128), back_rect, 2)
        surface.blit(back_text, (back_rect.x + 15, back_rect.y + 10))

        # Blit the input text to the surface
        surface.blit(username_surface, (REGusername_field.x + 5, REGusername_field.y + 5))
        surface.blit(pass_surface, (REGpassword_field.x + 5, REGpassword_field.y + 5))
        surface.blit(passAuth_surface, (REGpassAuth_field.x + 5, REGpassAuth_field.y + 5))
        surface.blit(email_surface, (REGemail_field.x + 5, REGemail_field.y +5))

