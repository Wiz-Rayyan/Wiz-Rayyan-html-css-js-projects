import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🧪 Emoji Alchemy Lab Pro 🧪")

# Colors
BACKGROUND = (20, 20, 30)
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
font = pygame.font.SysFont("segoeuiemoji", 24)
large_font = pygame.font.SysFont("segoeuiemoji", 36)

# Game elements
class Element:
    def __init__(self, emoji, name, category="basic"):
        self.emoji = emoji
        self.name = name
        self.category = category

# Expanded elements list (50+ elements)
elements = [
    # Basic Elements
    Element("🔥", "Fire"), Element("💧", "Water"), 
    Element("🌪️", "Wind"), Element("🪨", "Earth"),
    Element("⚡", "Lightning"), Element("❄️", "Ice"),
    
    # Advanced Elements
    Element("🌱", "Plant"), Element("💨", "Steam"),
    Element("🌊", "Wave"), Element("🪙", "Metal"),
    Element("🏆", "Gold"), Element("💎", "Diamond"),
    
    # Life Forms
    Element("🐍", "Snake"), Element("🦅", "Eagle"),
    Element("🐉", "Dragon"), Element("🦄", "Unicorn"),
    
    # Celestial
    Element("☀️", "Sun"), Element("🌙", "Moon"),
    Element("⭐", "Star"), Element("🌠", "Shooting Star"),
    
    # Magical
    Element("🧙", "Wizard"), Element("🧚", "Fairy"),
    Element("👻", "Ghost"), Element("🧛", "Vampire"),
    
    # Technology
    Element("🔋", "Battery"), Element("💻", "Computer"),
    Element("📱", "Phone"), Element("🤖", "Robot"),
    
    # Special
    Element("💀", "Death"), Element("❤️", "Heart"),
    Element("✨", "Magic"), Element("♾️", "Infinity")
]

# Enhanced recipes with crucible-specific reactions
recipes = {
    # Fusion Crucible (Combination)
    "fusion": [
        ("🔥", "💧", "💨", "Steam"),
        ("🪨", "💧", "🌱", "Plant"),
        ("🌱", "☀️", "🌻", "Sunflower"),
        ("🪙", "🔥", "🏆", "Gold"),
        ("🧙", "✨", "🧚", "Fairy")
    ],
    
    # Purge Crucible (Subtraction)
    "purge": [
        ("🍎", "🐍", "🧠", "Knowledge"),
        ("💀", "❤️", "👻", "Ghost"),
        ("🌊", "🌪️", "💧", "Pure Water"),
        ("🏆", "🪙", "💎", "Diamond")
    ],
    
    # Amplifier Crucible (Multiplication)
    "amplify": [
        ("🐜", "🔥", "🐜🔥", "Fire Ant Swarm"),
        ("💀", "♾️", "💀💀💀", "Ossuary Dimension"),
        ("🌱", "☀️", "🌳🌳🌳", "Forest"),
        ("⚡", "🌪️", "🌩️🌩️", "Thunderstorm")
    ],
    
    # Fracture Crucible (Division)
    "fracture": [
        ("🧙", "✨", "🧚🧚", "Twin Fairies"),
        ("💎", "🪙", "💎💎", "Gem Shards"),
        ("🌕", "🌑", "🌓🌓", "Crescent Moons"),
        ("🏆", "🔥", "🪙🪙", "Melted Gold")
    ],
    
    # Chaos Crucible (Random)
    "chaos": [
        ("🌈", "🦄", "🌈🦄", "Prismatic Unicorn"),
        ("🚽", "👑", "🚽👑", "Golden Throne"),
        ("🤖", "🐑", "🤖🐑", "Cyber-Sheep"),
        ("🧦", "🐇", "🧦🐇", "Rabbit Hole")
    ]
}

# Crucible types with positions
crucibles = [
    {"type": "fusion", "emoji": "🧪🔥", "pos": (150, 400)},
    {"type": "purge", "emoji": "🧪💨", "pos": (300, 400)},
    {"type": "amplify", "emoji": "🧪⚡", "pos": (450, 400)},
    {"type": "fracture", "emoji": "🧪💥", "pos": (600, 400)},
    {"type": "chaos", "emoji": "🧪🌀", "pos": (750, 400)}
]

# Cauldron animation
cauldron_pos = (900, 400)
cauldron_state = "idle"  # idle, bubbling, pouring, reaction
cauldron_color = (100, 100, 200)
cauldron_elements = []
last_reaction_time = 0

# Terminal display
terminal_rect = pygame.Rect(50, 500, 800, 250)
terminal_text = ["Welcome to the Alchemy Lab!"]
terminal_scroll = 0
scrollbar_rect = pygame.Rect(830, 500, 20, 250)
scrollbar_handle_rect = pygame.Rect(830, 500, 20, 50)
scrollbar_dragging = False
line_height = 20
visible_lines = terminal_rect.height // line_height

# Game state
selected_element = None
current_crucible = None
discovered = [e.emoji for e in elements if e.category == "basic"]
log_messages = []

def render_text(text, x, y, color=(255, 255, 255), font_obj=None):
    font_obj = font_obj or font
    text_surface = font_obj.render(text, True, color)
    screen.blit(text_surface, (x, y))

def add_log(message):
    terminal_text.append(message)
    # Update scrollbar handle position
    update_scrollbar_handle()

def update_scrollbar_handle():
    total_lines = len(terminal_text)
    if total_lines <= visible_lines:
        scrollbar_handle_rect.y = scrollbar_rect.y
        scrollbar_handle_rect.height = scrollbar_rect.height
    else:
        handle_height = max(20, scrollbar_rect.height * visible_lines // total_lines)
        max_y = scrollbar_rect.y + scrollbar_rect.height - handle_height
        scroll_pos = min(max_y, scrollbar_rect.y + (scrollbar_rect.height - handle_height) * terminal_scroll / (total_lines - visible_lines))
        scrollbar_handle_rect.y = scroll_pos
        scrollbar_handle_rect.height = handle_height

def mix_elements(e1, e2, crucible_type):
    # Check crucible-specific recipes first
    for r in recipes[crucible_type]:
        if (e1 == r[0] and e2 == r[1]) or (e2 == r[0] and e1 == r[1]):
            return r[2], r[3]
    
    # Default behavior for each crucible type
    if crucible_type == "fusion":
        return f"{e1}{e2}", "Combined Element"
    elif crucible_type == "purge":
        return e1, "Purified " + e1  # Keeps first element
    elif crucible_type == "amplify":
        return f"{e1}{e1}{e1}", "Amplified " + e1
    elif crucible_type == "fracture":
        return f"{e1[:len(e1)//2]}", "Fragment of " + e1
    else:  # chaos
        outcomes = [
            (f"{e1}{e2}", "Chaos Fusion"),
            ("💥", "Explosion"),
            ("❓", "Unknown Reaction"),
            (random.choice(["✨", "⚡", "🔥", "💧"]), "Elemental Essence")
        ]
        return random.choice(outcomes)

def draw_cauldron():
    # Cauldron base
    pygame.draw.ellipse(screen, cauldron_color, 
                       (cauldron_pos[0]-75, cauldron_pos[1]-50, 150, 100))
    
    # Animation states
    if cauldron_state == "bubbling":
        for i in range(5):
            x = cauldron_pos[0] - 50 + random.randint(0, 100)
            y = cauldron_pos[1] - 30 - random.randint(0, 20)
            pygame.draw.circle(screen, (200, 200, 255), (x, y), random.randint(2, 5))
    elif cauldron_state == "pouring":
        pygame.draw.polygon(screen, CRUCIBLE_COLORS[current_crucible], [
            (cauldron_pos[0]-30, cauldron_pos[1]-80),
            (cauldron_pos[0], cauldron_pos[1]-100),
            (cauldron_pos[0]+30, cauldron_pos[1]-80)
        ])
    elif cauldron_state == "reaction":
        pygame.draw.circle(screen, (255, 255, 0), cauldron_pos, 60, 3)
    
    # Contents display
    if cauldron_elements:
        render_text("".join(cauldron_elements), cauldron_pos[0]-20, cauldron_pos[1]-20, font_obj=large_font)

def draw_terminal():
    # Terminal background
    pygame.draw.rect(screen, TERMINAL_BG, terminal_rect)
    pygame.draw.rect(screen, (50, 50, 70), terminal_rect, 2)
    
    # Draw visible text lines
    total_lines = len(terminal_text)
    start_line = max(0, min(terminal_scroll, total_lines - visible_lines))
    
    for i in range(visible_lines):
        line_idx = start_line + i
        if line_idx < total_lines:
            render_text(terminal_text[line_idx], 
                       terminal_rect.x + 10, 
                       terminal_rect.y + 10 + i * line_height)
    
    # Draw scrollbar
    pygame.draw.rect(screen, SCROLLBAR_COLOR, scrollbar_rect)
    pygame.draw.rect(screen, SCROLLBAR_HANDLE, scrollbar_handle_rect)

def draw_elements_panel():
    pygame.draw.rect(screen, (30, 30, 50), (50, 50, 300, 400))
    render_text("Discovered Elements:", 60, 60)
    
    # Display elements in a grid
    for i, element in enumerate([e for e in elements if e.emoji in discovered]):
        row = i // 4
        col = i % 4
        pygame.draw.rect(screen, (50, 50, 70), (60 + col * 70, 100 + row * 60, 60, 50))
        render_text(element.emoji, 75 + col * 70, 105 + row * 60)
        render_text(element.name, 75 + col * 70, 125 + row * 60, (200, 200, 200), pygame.font.SysFont("Arial", 10))

def draw_crucibles():
    for crucible in crucibles:
        color = CRUCIBLE_COLORS[crucible["type"]]
        if current_crucible == crucible["type"]:
            color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))
        
        # Crucible body
        pygame.draw.ellipse(screen, color, (crucible["pos"][0], crucible["pos"][1], 80, 60))
        pygame.draw.rect(screen, color, (crucible["pos"][0]+10, crucible["pos"][1]+30, 60, 40))
        
        # Crucible neck
        pygame.draw.rect(screen, color, (crucible["pos"][0]+30, crucible["pos"][1]-20, 20, 20))
        render_text(crucible["emoji"], crucible["pos"][0]+30, crucible["pos"][1]-50)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BACKGROUND)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            
            # Check element selection
            for i, element in enumerate([e for e in elements if e.emoji in discovered]):
                row = i // 4
                col = i % 4
                if 60 + col * 70 <= x <= 120 + col * 70 and 100 + row * 60 <= y <= 150 + row * 60:
                    selected_element = element.emoji
                    add_log(f"Selected: {element.emoji} {element.name}")
            
            # Check crucible selection
            for crucible in crucibles:
                if (crucible["pos"][0] <= x <= crucible["pos"][0] + 80 and 
                    crucible["pos"][1]-20 <= y <= crucible["pos"][1] + 70):
                    
                    if selected_element:
                        # Start pouring animation
                        current_crucible = crucible["type"]
                        cauldron_state = "pouring"
                        cauldron_color = CRUCIBLE_COLORS[crucible["type"]]
                        last_reaction_time = time.time()
                        
                        # Add to cauldron (limit 2 elements)
                        if len(cauldron_elements) < 2:
                            cauldron_elements.append(selected_element)
                            add_log(f"Added {selected_element} to cauldron")
                        
                        # If cauldron has 2 elements, mix them
                        if len(cauldron_elements) == 2:
                            result_emoji, result_name = mix_elements(
                                cauldron_elements[0], 
                                cauldron_elements[1], 
                                crucible["type"]
                            )
                            
                            # Check if new element
                            if result_emoji not in discovered:
                                elements.append(Element(result_emoji, result_name))
                                discovered.append(result_emoji)
                                add_log(f"DISCOVERY: {cauldron_elements[0]} + {cauldron_elements[1]} = {result_emoji} ({result_name})")
                            else:
                                add_log(f"Reaction: {cauldron_elements[0]} + {cauldron_elements[1]} = {result_emoji}")
                            
                            # Show reaction
                            cauldron_state = "reaction"
                            cauldron_elements = [result_emoji]
                        selected_element = None
            
            # Check scrollbar click
            if scrollbar_rect.collidepoint(x, y):
                if scrollbar_handle_rect.collidepoint(x, y):
                    scrollbar_dragging = True
                else:
                    # Jump to clicked position
                    total_lines = len(terminal_text)
                    if total_lines > visible_lines:
                        rel_y = y - scrollbar_rect.y
                        frac = rel_y / scrollbar_rect.height
                        terminal_scroll = int(frac * (total_lines - visible_lines))
                        update_scrollbar_handle()
        
        if event.type == pygame.MOUSEBUTTONUP:
            scrollbar_dragging = False
        
        if event.type == pygame.MOUSEMOTION and scrollbar_dragging:
            total_lines = len(terminal_text)
            if total_lines > visible_lines:
                rel_y = event.pos[1] - scrollbar_rect.y
                frac = rel_y / scrollbar_rect.height
                terminal_scroll = min(max(0, int(frac * (total_lines - visible_lines))), total_lines - visible_lines)
                update_scrollbar_handle()
        
        if event.type == pygame.MOUSEWHEEL:
            terminal_scroll = max(0, min(terminal_scroll - event.y, len(terminal_text) - visible_lines))
            update_scrollbar_handle()
    
    # Update animations
    if cauldron_state == "pouring" and time.time() - last_reaction_time > 1:
        cauldron_state = "bubbling"
    elif cauldron_state == "reaction" and time.time() - last_reaction_time > 2:
        cauldron_state = "idle"
    
    # Drawing
    draw_elements_panel()
    draw_crucibles()
    draw_cauldron()
    draw_terminal()
    
    # Show selected element
    if selected_element:
        render_text(f"Selected: {selected_element}", 50, 470, (255, 255, 0))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()