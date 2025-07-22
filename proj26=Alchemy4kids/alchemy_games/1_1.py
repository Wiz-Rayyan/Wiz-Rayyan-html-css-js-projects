
# Emoji Alchemy Lab Game
# A simple Pygame-based game where players can mix emojis to discover new elements.


import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🔥 Emoji Alchemy Lab 🔥")

# Colors
BACKGROUND = (30, 30, 40)
CRUCIBLE_COLORS = {
    "fusion": (255, 100, 100),
    "purge": (100, 255, 100),
    "amplify": (100, 100, 255),
    "fracture": (255, 255, 100),
    "chaos": (200, 100, 255)
}

# Fonts
font = pygame.font.SysFont("segoeuiemoji", 24)  # Changed to a font that supports emojis

# Game elements
class Element:
    def __init__(self, emoji, name, category="basic"):
        self.emoji = emoji
        self.name = name
        self.category = category

# Starting elements
elements = [
    Element("🔥", "Fire"),
    Element("💧", "Water"),
    Element("🌪️", "Wind"),
    Element("🪨", "Earth")
]

# Known recipes (emoji1, emoji2, result_emoji, result_name)
recipes = [
    ("🔥", "💧", "💨", "Steam"),
    ("🌪️", "🔥", "🌪️🔥", "Firestorm"),
    ("🪨", "💧", "🌱", "Plant"),
    ("🌱", "☀️", "🌻", "Sunflower"),
    ("🔥", "🪨", "🪙", "Metal"),
    ("💧", "🌪️", "🌊", "Wave"),
    ("🪙", "🔥", "🏆", "Golden Chalice"),
    ("💀", "♾️", "💀💀💀", "Ossuary Dimension"),
    ("🧙", "✨", "🧚", "Fairy"),
    ("🌈", "🦄", "🌈🦄", "Prismatic Unicorn"),
    ("🚽", "👑", "🚽👑", "Golden Throne")
]

# Crucible types
crucibles = [
    {"type": "fusion", "emoji": "🧪🔥", "pos": (150, 400)},
    {"type": "purge", "emoji": "🧪💨", "pos": (300, 400)},
    {"type": "amplify", "emoji": "🧪⚡", "pos": (450, 400)},
    {"type": "fracture", "emoji": "🧪💥", "pos": (600, 400)},
    {"type": "chaos", "emoji": "🧪🌀", "pos": (750, 400)}
]

# Game state
selected_element = None
current_crucible = None
crucible_contents = {}
discovered = [e.emoji for e in elements]
log_messages = []

def render_text(text, x, y, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def add_log(message):
    log_messages.append(message)
    if len(log_messages) > 10:
        log_messages.pop(0)

def mix_elements(e1, e2, crucible_type):
    # Check known recipes first
    for r in recipes:
        if (e1 == r[0] and e2 == r[1]) or (e2 == r[0] and e1 == r[1]):
            return r[2], r[3]

    # Chaos Crucible does random things
    if crucible_type == "chaos":
        outcomes = [
            (f"{e1}{e2}", "Mystery Fusion"),
            ("💥", "Explosion"),
            ("❓", "Unknown Reaction")
        ]
        return random.choice(outcomes)

    # Default: just combine emojis
    return f"{e1}{e2}", "Unknown Compound"

def draw_elements():
    for i, element in enumerate(elements):
        pygame.draw.rect(screen, (50, 50, 70), (50, 50 + i * 60, 200, 50))
        render_text(f"{element.emoji} {element.name}", 60, 60 + i * 60)

def draw_crucibles():
    for crucible in crucibles:
        color = CRUCIBLE_COLORS[crucible["type"]]
        if current_crucible == crucible["type"]:
            color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))
        pygame.draw.rect(screen, color, (crucible["pos"][0], crucible["pos"][1], 100, 100))
        render_text(crucible["emoji"], crucible["pos"][0] + 30, crucible["pos"][1] + 40)

        # Show contents
        if crucible["type"] in crucible_contents:
            content_emoji = crucible_contents[crucible["type"]]
            render_text(content_emoji, crucible["pos"][0] + 40, crucible["pos"][1] + 20)

def draw_log():
    pygame.draw.rect(screen, (20, 20, 30), (650, 50, 300, 400))
    for i, msg in enumerate(log_messages):
        render_text(msg, 660, 60 + i * 30, (200, 200, 255))

# Main game loop
running = True
while running:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            # Check if an element is clicked
            for i, element in enumerate(elements):
                if 50 <= x <= 250 and 50 + i * 60 <= y <= 100 + i * 60:
                    selected_element = element.emoji

            # Check if a crucible is clicked
            for crucible in crucibles:
                cx, cy = crucible["pos"]
                if cx <= x <= cx + 100 and cy <= y <= cy + 100:
                    if selected_element:
                        if crucible["type"] in crucible_contents:
                            # Mix!
                            e1 = crucible_contents[crucible["type"]]
                            e2 = selected_element
                            result_emoji, result_name = mix_elements(e1, e2, crucible["type"])

                            # Add to discovered elements
                            if result_emoji not in discovered:
                                elements.append(Element(result_emoji, result_name))
                                discovered.append(result_emoji)
                                add_log(f"[NEW] {e1} + {e2} = {result_emoji} ({result_name})")
                            else:
                                add_log(f"[MIX] {e1} + {e2} = {result_emoji}")

                            # Reset crucible
                            crucible_contents.pop(crucible["type"])
                        else:
                            # Add first element
                            crucible_contents[crucible["type"]] = selected_element
                            add_log(f"[ADD] {selected_element} → {crucible['emoji']}")

                        selected_element = None
                    current_crucible = crucible["type"]

    # Draw everything
    draw_elements()
    draw_crucibles()
    draw_log()

    # Show selected element
    if selected_element:
        render_text(f"Selected: {selected_element}", 50, HEIGHT - 50, (255, 255, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()