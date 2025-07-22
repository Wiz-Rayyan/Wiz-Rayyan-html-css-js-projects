import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🧪 Ultimate Emoji Alchemy Lab 🧪")

# Colors
BACKGROUND = (20, 20, 30)
PANEL_BG = (30, 30, 50)
TERMINAL_BG = (10, 10, 20)
SCROLLBAR_COLOR = (80, 80, 90)
SCROLLBAR_HANDLE = (120, 120, 130)
CRUCIBLE_COLORS = {
    "fusion": (255, 100, 100),
    "purge": (100, 255, 100),
    "amplify": (100, 100, 255),
    "fracture": (255, 255, 100),
    "chaos": (200, 100, 255)
}

# Fonts
try:
    font = pygame.font.SysFont("segoeuiemoji", 24)
    small_font = pygame.font.SysFont("Arial", 12)
    large_font = pygame.font.SysFont("segoeuiemoji", 36)
except:
    font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 12)
    large_font = pygame.font.SysFont(None, 36)

# Game state
terminal_text = ["Welcome to the Ultimate Alchemy Lab!"]
terminal_scroll = 0
elements_scroll = 0
selected_element = None
show_discovered = True

# Initialize these before they're used in add_log
terminal_visible_lines = 12  # Temporary value, will be set properly later
terminal_line_height = 20

# Rest of your element and crucible definitions...
# [Previous element and crucible definitions remain the same...]

def add_log(message):
    global terminal_scroll  # Declare we're using the global variable
    terminal_text.append(message)
    # Only auto-scroll if we're already at the bottom
    if terminal_scroll >= len(terminal_text) - terminal_visible_lines - 1:
        terminal_scroll = max(0, len(terminal_text) - terminal_visible_lines)
    update_terminal_scroll()

def update_terminal_scroll():
    global terminal_scroll_handle
    total_lines = len(terminal_text)
    if total_lines <= terminal_visible_lines:
        terminal_scroll_handle.y = terminal_scrollbar.y
        terminal_scroll_handle.height = terminal_scrollbar.height
    else:
        handle_height = max(30, terminal_scrollbar.height * terminal_visible_lines // total_lines)
        max_y = terminal_scrollbar.y + terminal_scrollbar.height - handle_height
        scroll_pos = terminal_scrollbar.y + (terminal_scrollbar.height - handle_height) * terminal_scroll / max(1, (total_lines - terminal_visible_lines))
        terminal_scroll_handle.y = min(max_y, scroll_pos)
        terminal_scroll_handle.height = handle_height

# Initialize UI components after defining the functions that use them
terminal_rect = pygame.Rect(400, 600, 450, 250)
terminal_scrollbar = pygame.Rect(840, 600, 10, 250)
terminal_scroll_handle = pygame.Rect(840, 600, 10, 50)
terminal_dragging = False
terminal_visible_lines = terminal_rect.height // terminal_line_height  # Now properly initialized

# [Rest of your code remains the same...]

def main():
    global terminal_scroll, elements_scroll, selected_element, show_discovered
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        # [Your main game loop code...]
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()

    # this may hang . the issue is that the game loop is not properly structured to handle events...

    '''
    this what copilot suggested:
    Your Pygame game is hanging because the main game loop in your `main()` function is empty—it does not handle any events, including the quit event. As a result, the window becomes unresponsive, and you cannot close it normally.

**Key issue:**
```python
while running:
    # [Your main game loop code...]
    pygame.display.flip()
    clock.tick(60)
```
There is no code inside the loop to process events like `pygame.QUIT`. Without this, the window cannot respond to user actions, and the OS marks it as "not responding" (hangs).

**How to fix:**  
You must add an event loop inside your main loop to handle events, especially quitting:

```python
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # ...rest of your game logic...
    pygame.display.flip()
    clock.tick(60)
```

**Summary:**  
Your game hangs because you are not processing Pygame events in your main loop. Add an event loop to handle user input and window events.
    '''