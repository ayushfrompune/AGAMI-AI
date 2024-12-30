import sounddevice as sd
import numpy as np
import pygame
import sys
import os
import tkinter as tk

# Dynamically fetch screen resolution using tkinter
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

# Define window size
window_width, window_height = 600, 600

# Calculate position for top-right corner
x_position = screen_width - window_width
y_position = 0  # Top of the screen

# Set Pygame window position
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x_position},{y_position}"

# Set volume threshold (you may need to adjust this value)
volume_threshold = 1  # Set a reasonable threshold for speech

# Function to monitor microphone input and detect if you're speaking
def audio_callback(indata, frames, time, status):
    global speaking
    if status:
        print(f"Audio input error: {status}")

    # Calculate RMS volume (root mean square)
    volume = np.linalg.norm(indata) * 10  # We multiply by 10 for scaling the volume

    # Determine if we're speaking based on volume exceeding threshold
    if volume > volume_threshold:
        speaking = True  # Set speaking to True if the volume exceeds threshold
    else:
        speaking = False  # Set speaking to False if the volume is below threshold

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 100, 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AGAMI AI - Voice Triggered Circle")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
colors = [
    (173, 216, 230),  # Light Blue
    (0, 191, 255),  # Deep Sky Blue
    (30, 144, 255),  # Dodger Blue
    (0, 0, 255),  # Pure Blue
    (65, 105, 225),  # Royal Blue
    (72, 61, 139),  # Dark Slate Blue
    (75, 0, 130),  # Indigo
    (138, 43, 226)
]
# Font setup for the "A"
font = pygame.font.SysFont("Jua", 50)
text_surface = font.render("A", True, WHITE)
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Circle properties
center_x, center_y = WIDTH // 2, HEIGHT // 2
max_radius = 50
min_radius = 30
radius = min_radius
pulse_speed = 0.5
pulse_direction = 1

# Global variable to track speaking
speaking = False

# Start microphone monitoring in a separate thread
import threading
microphone_thread = threading.Thread(target=lambda: sd.InputStream(callback=audio_callback, channels=1, samplerate=44100).start(), daemon=True)
microphone_thread.start()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    if speaking:
        # Calculate the pulsing radius when speaking
        radius += pulse_speed * pulse_direction
        if radius >= max_radius or radius <= min_radius:
            pulse_direction *= -1

        # Draw the glowing circle
        for i, color in enumerate(colors):
            layers = 10
            alpha = int(255 * (1 - (i / layers)))  # Gradual transparency
            glow_color = (*color, alpha)  # Color with transparency
            glowing_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(screen, color, (center_x, center_y), int(radius - i * 5), 1)
    else:
        radius=min_radius
    # Draw the "A" in the center of the circle
    screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
