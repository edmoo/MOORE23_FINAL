import pygame
import sqlite3
import ast
from const import *
import pygame.gfxdraw
from math import atan2, degrees, hypot

# Define the size and position of each UI element
wins_label_rect = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 32)
losses_label_rect = pygame.Rect(WIDTH // 4, HEIGHT // 3 + 40, WIDTH // 2, 32)
draws_label_rect = pygame.Rect(WIDTH // 4, HEIGHT // 3 + 80, WIDTH // 2, 32)
colour_one_rect = pygame.Rect(WIDTH // 4, (HEIGHT // 2+20), WIDTH // 2, 32)
colour_two_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 60, WIDTH // 2, 32)
audio_toggle_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, 32)
voice_toggle_rect = pygame.Rect(WIDTH // 4, HEIGHT // 1.5+40, WIDTH // 2, 32)
sett_quit_field = pygame.Rect(WIDTH // 4, HEIGHT // 1.5+80, WIDTH // 2, 32)
title_font = pygame.font.SysFont("Oswald", 120)

COLOR_WHEEL_CENTER = (colour_one_rect.right-(colour_one_rect.width//4), colour_one_rect.bottom)
COLOR_WHEEL_RADIUS = 75
#to see if we are clicking on the wheel 
colour_wheel_rect = pygame.Rect(
    COLOR_WHEEL_CENTER[0] - COLOR_WHEEL_RADIUS,
    COLOR_WHEEL_CENTER[1] - COLOR_WHEEL_RADIUS,
    COLOR_WHEEL_RADIUS * 2,
    COLOR_WHEEL_RADIUS * 2
)

class Settings:

    def __init__(self, audio_enabled,username):
        self.audio_enabled = audio_enabled
        self.username = username

    # Show methods

    def show_screen(self, surface, wins, losses, draws, selected_button, audioFeedback, voiceCommands):
        # Clear the surface
        surface.fill(COLOUR_ONE)
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        # Retrieve the white and black colors from the database for this user
        c.execute("SELECT white, black FROM user_stats WHERE username = ?", (self.username,))
        row = c.fetchone()
        if row is not None:
            self.selected_color = ast.literal_eval(row[0])
            self.selected_colour2 = ast.literal_eval(row[1])
        else:
            # If no data was found in the database for this user, set default values
            self.selected_color = (255, 255, 255)
            self.selected_colour2 = (0, 0, 0)
        # Draw the Wins label
        pygame.draw.rect(surface, COLOUR_TWO, wins_label_rect)
        wins_label_text = font.render(f"Wins: {wins}", True, BLACK)
        wins_label_text_pos = wins_label_text.get_rect(center=wins_label_rect.center)
        surface.blit(wins_label_text, wins_label_text_pos)

        # Draw the Losses label
        pygame.draw.rect(surface, COLOUR_TWO, losses_label_rect)
        losses_label_text = font.render(f"Losses: {losses}", True, BLACK)
        losses_label_text_pos = losses_label_text.get_rect(center=losses_label_rect.center)
        surface.blit(losses_label_text, losses_label_text_pos)

        # Draw the Draws label
        pygame.draw.rect(surface, COLOUR_TWO, draws_label_rect)
        draws_label_text = font.render(f"Draws: {draws}", True, BLACK)
        draws_label_text_pos = draws_label_text.get_rect(center=draws_label_rect.center)
        surface.blit(draws_label_text, draws_label_text_pos)

        pygame.draw.rect(surface, COLOUR_TWO, colour_one_rect)
        colour_one_text = font.render("White Team:", True, BLACK)
        colour_one_text_pos = colour_one_text.get_rect(center=(colour_one_rect.left + 130, colour_one_rect.centery))
        surface.blit(colour_one_text, colour_one_text_pos)
        pygame.draw.rect(surface, self.selected_color, (colour_one_rect.left + 230, colour_one_rect.top, 32, 32))
 
        pygame.draw.rect(surface, COLOUR_TWO, colour_two_rect)
        colour_two_text = font.render("Black Team:", True, BLACK)
        colour_two_text_pos = colour_two_text.get_rect(center=(colour_two_rect.left + 130, colour_two_rect.centery))
        surface.blit(colour_two_text, colour_two_text_pos)
        pygame.draw.rect(surface, self.selected_colour2, (colour_two_rect.left + 230, colour_two_rect.top, 32, 32))
         
        pygame.draw.rect(surface, COLOUR_TWO, audio_toggle_rect)
        audio_text = font.render("Toggle Audio:", True, BLACK)
        audio_text_pos = audio_text.get_rect(center=(audio_toggle_rect.left + 130, audio_toggle_rect.centery))
        surface.blit(audio_text, audio_text_pos)
        pygame.draw.rect(surface, (255,255,255), (audio_toggle_rect.left + 230, audio_toggle_rect.top, 32, 32))
        if(audioFeedback):
            small_rect_size = (16, 16)

            # Calculate the x and y coordinates of the smaller rectangle to center it within the larger rectangle
            small_rect_x = audio_toggle_rect.left + 230 + (32 - small_rect_size[0]) // 2
            small_rect_y = audio_toggle_rect.top + (32 - small_rect_size[1]) // 2

            # Draw the smaller rectangle
            pygame.draw.rect(surface, (0, 0, 0), (small_rect_x, small_rect_y, small_rect_size[0], small_rect_size[1]))
            pygame.draw.rect(surface, (255, 255, 255), (small_rect_x, small_rect_y, small_rect_size[0], small_rect_size[1]), width=1)


        pygame.draw.rect(surface, COLOUR_TWO, voice_toggle_rect)
        voice_text = font.render("Toggle Voice:", True, BLACK)
        voice_text_pos = voice_text.get_rect(center=(voice_toggle_rect.left + 130, voice_toggle_rect.centery))
        surface.blit(voice_text, voice_text_pos)
        pygame.draw.rect(surface, (255,255,255), (voice_toggle_rect.left + 230, voice_toggle_rect.top, 32, 32))
        if(voiceCommands):
            small_rect_size = (16, 16)

            # Calculate the x and y coordinates of the smaller rectangle to center it within the larger rectangle
            small_rect_x = voice_toggle_rect.left + 230 + (32 - small_rect_size[0]) // 2
            small_rect_y = voice_toggle_rect.top + (32 - small_rect_size[1]) // 2

            # Draw the smaller rectangle
            pygame.draw.rect(surface, (0, 0, 0), (small_rect_x, small_rect_y, small_rect_size[0], small_rect_size[1]))
            pygame.draw.rect(surface, (255, 255, 255), (small_rect_x, small_rect_y, small_rect_size[0], small_rect_size[1]), width=1)

        pygame.draw.rect(surface, COLOUR_TWO, sett_quit_field)
        back_text = font.render(f"Back", True, BLACK)
        back_text_pos = back_text.get_rect(center=sett_quit_field.center)
        surface.blit(back_text, back_text_pos)    

        #write header
        title_text = title_font.render("Settings", True, COLOUR_THREE)
        surface.blit(title_text, (WIDTH // 3 - 10, 40))
        if(selected_button == 1 or selected_button == 2):
            #draws colour wheel to screen if user selecting colour
            draw_color_wheel(surface)


#draws the colour wheel
def draw_color_wheel(surface):
    for y in range(-COLOR_WHEEL_RADIUS, COLOR_WHEEL_RADIUS):
        for x in range(-COLOR_WHEEL_RADIUS, COLOR_WHEEL_RADIUS):
            distance = hypot(x, y)
            if distance <= COLOR_WHEEL_RADIUS:
                angle = degrees(atan2(y, x)) % 360
                color = pygame.Color(0)
                color.hsva = (angle, distance / COLOR_WHEEL_RADIUS * 100, 100, 100)
                surface.set_at((COLOR_WHEEL_CENTER[0] + x, COLOR_WHEEL_CENTER[1] + y), color)

#updates the team colours
def update_color(surface, selected_button,username):
    conn = sqlite3.connect('users.db')
    x, y = pygame.mouse.get_pos()
    color = surface.get_at((x, y))
    if color.a != 0:
        if(selected_button == 2):
            selected_color = color[0:3]
            #update black in db
            c = conn.cursor()
            c.execute("UPDATE user_stats SET black = ? WHERE username = ?", (str(selected_color), username))
            conn.commit()
        elif(selected_button == 1):
            selected_colour2 = color[0:3]
            #update white in db
            c = conn.cursor()
            c.execute("UPDATE user_stats SET white = ? WHERE username = ?", (str(selected_colour2), username))
            conn.commit()
    conn.close()
