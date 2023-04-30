import pygame
from const import *

login_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)
reg_button = pygame.Rect(WIDTH // 4, login_button.bottom + 10, WIDTH // 2, 32)

title_font = pygame.font.SysFont("Oswald", 120)

username_field = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 32)
password_field = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 32)
passwordAUTH_field = pygame.Rect(WIDTH // 4, HEIGHT // 1, WIDTH // 2, 32)

confirm_password_field = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 50, WIDTH // 2, 32)
email_field = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, 32)

REGusername_field = pygame.Rect(WIDTH // 4, HEIGHT // 5, WIDTH // 2, 32)
REGpassword_field = pygame.Rect(WIDTH // 4, HEIGHT // 5 + 50, WIDTH // 2, 32)
REGpassAuth_field = pygame.Rect(WIDTH // 4, HEIGHT // 5 + 100, WIDTH // 2, 32)
REGemail_field = pygame.Rect(WIDTH // 4, HEIGHT // 5 + 150, WIDTH // 2, 32)
back_text = font.render('6.Back', True, (0,0,0))
back_rect = pygame.Rect(50, 400, 100, 50)
register_button = pygame.Rect(WIDTH // 4, HEIGHT // 5 + 210, WIDTH // 2, 32)

class Login:

    def __init__(self):
        pass

    #show methods

    def show_screen(self, surface, username, password):
        
        #clear surface
        surface.fill(COLOUR_ONE)
        text_surface = base_font.render(username, True, (0, 0, 0))
        passStar = ""
        for i in password:
            passStar += "*"

        pass_surface = base_font.render(passStar, True, (0,0,0))

        # Draw username field
        pygame.draw.rect(surface, COLOUR_TWO, username_field, 2)

        # Render username label and blit to surface
        username_text = font.render("1.Username:", True, BLACK)
        username_text_pos = (username_field.left - username_text.get_width() - 16, HEIGHT // 3)
        surface.blit(username_text, username_text_pos)

        #draw password field
        pygame.draw.rect(surface, COLOUR_TWO, password_field, 2)
        password_text = font.render("2.Password:", True, BLACK)
        surface.blit(password_text, (WIDTH // 4 - password_text.get_width() - 16, HEIGHT // 2))
        
        #draw login button
        pygame.draw.rect(surface, COLOUR_TWO, login_button)
        login_text = font.render("3.Login", True, BLACK)
        surface.blit(login_text, (WIDTH // 2 - login_text.get_width() // 2, HEIGHT // 1.5))

        #draw register button
        pygame.draw.rect(surface, COLOUR_TWO, reg_button)
        register_text = font.render("4.Register New Account", True, BLACK)
        surface.blit(register_text, (WIDTH // 2 - register_text.get_width() // 2, login_button.bottom + 8))
        
        #draw title
        title_text = title_font.render("ChessPAL", True, COLOUR_THREE)
        surface.blit(title_text, (WIDTH // 3 - 10, 40))

        surface.blit(text_surface, (username_field.x+5, username_field.y+5))
        surface.blit(pass_surface, (password_field.x+5, password_field.y+5))
    


    def register(self, surface, username, password, passAuth, email):
        #clear the surface
        surface.fill(COLOUR_ONE)

        #draw the username field
        pygame.draw.rect(surface, COLOUR_TWO, REGusername_field, 2)
        username_text = font.render("1.Username:", True, BLACK)
        surface.blit(username_text, (WIDTH // 4 - username_text.get_width() - 16, HEIGHT // 5))

        #draw the password field
        pygame.draw.rect(surface, COLOUR_TWO, REGpassword_field, 2)
        password_text = font.render("2.Password:", True, BLACK)
        surface.blit(password_text, (WIDTH // 4 - password_text.get_width() - 16, HEIGHT // 5 + 50))

        #draw the password authentication field
        pygame.draw.rect(surface, COLOUR_TWO, REGpassAuth_field, 2)
        passAuth_text = font.render("3.Confirm Password:", True, BLACK)
        surface.blit(passAuth_text, (WIDTH // 4 - passAuth_text.get_width() - 16, HEIGHT // 5 + 100))

        #draw the email field
        pygame.draw.rect(surface, COLOUR_TWO, REGemail_field, 2)
        email_text = font.render("4.Email:", True, BLACK)
        surface.blit(email_text, (WIDTH // 4 - email_text.get_width() - 16, HEIGHT // 5 + 150))

        #draw the register button
        pygame.draw.rect(surface, COLOUR_TWO, register_button)
        register_text = font.render("5.Register", True, BLACK)
        surface.blit(register_text, (WIDTH // 2 - register_text.get_width() // 2, HEIGHT // 5 + 210))

        #render the input text
        username_surface = base_font.render(username, True, BLACK)
        pass_surface = base_font.render("*" * len(password), True, BLACK)
        passAuth_surface = base_font.render("*" * len(passAuth), True, BLACK)
        email_surface = base_font.render(email, True, BLACK)

        pygame.draw.rect(surface, COLOUR_TWO, back_rect)
        surface.blit(back_text, (back_rect.x + 15, back_rect.y + 10))

        #blit the input text to the surface
        surface.blit(username_surface, (REGusername_field.x + 5, REGusername_field.y + 5))
        surface.blit(pass_surface, (REGpassword_field.x + 5, REGpassword_field.y + 5))
        surface.blit(passAuth_surface, (REGpassAuth_field.x + 5, REGpassAuth_field.y + 5))
        surface.blit(email_surface, (REGemail_field.x + 5, REGemail_field.y +5))

