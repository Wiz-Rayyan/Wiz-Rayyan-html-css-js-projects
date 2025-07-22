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
font = pygame.font.SysFont("segoeuiemoji", 24)
small_font = pygame.font.SysFont("Arial", 12)
large_font = pygame.font.SysFont("segoeuiemoji", 36)

# Game elements
class Element:
    def __init__(self, emoji, name, category="basic", discovered=False):
        self.emoji = emoji
        self.name = name
        self.category = category
        self.discovered = discovered

# Expanded elements list (100+ elements)
all_elements = [
    # Basic Elements (always discovered)
    Element("🔥", "Fire", "basic", True),
    Element("💧", "Water", "basic", True),
    Element("🌪️", "Wind", "basic", True),
    Element("🪨", "Earth", "basic", True),
    Element("⚡", "Lightning", "basic", True),
    Element("❄️", "Ice", "basic", True),
    
    # Advanced Elements
    Element("🌱", "Plant", "nature"),
    Element("💨", "Steam", "element"),
    Element("🌊", "Wave", "element"),
    Element("🪙", "Metal", "material"),
    Element("🏆", "Gold", "material"),
    Element("💎", "Diamond", "material"),
    
    # Life Forms
    Element("🐍", "Snake", "animal"),
    Element("🦅", "Eagle", "animal"),
    Element("🐉", "Dragon", "mythical"),
    Element("🦄", "Unicorn", "mythical"),
    Element("🦩", "Flamingo", "animal"),
    Element("🐝", "Bee", "animal"),
    
    # Celestial
    Element("☀️", "Sun", "celestial"),
    Element("🌙", "Moon", "celestial"),
    Element("⭐", "Star", "celestial"),
    Element("🌠", "Shooting Star", "celestial"),
    Element("🌌", "Galaxy", "celestial"),
    Element("🪐", "Planet", "celestial"),
    
    # Magical
    Element("🧙", "Wizard", "magic"),
    Element("🧚", "Fairy", "magic"),
    Element("👻", "Ghost", "magic"),
    Element("🧛", "Vampire", "magic"),
    Element("🧜", "Mermaid", "magic"),
    Element("🧞", "Genie", "magic"),
    
    # Technology
    Element("🔋", "Battery", "tech"),
    Element("💻", "Computer", "tech"),
    Element("📱", "Phone", "tech"),
    Element("🤖", "Robot", "tech"),
    Element("🛸", "UFO", "tech"),
    Element("🔭", "Telescope", "tech"),
    
    # Special
    Element("💀", "Death", "special"),
    Element("❤️", "Heart", "special"),
    Element("✨", "Magic", "special"),
    Element("♾️", "Infinity", "special"),
    Element("🌀", "Vortex", "special"),
    Element("🌈", "Rainbow", "special"),
    
    # Food
    Element("🍎", "Apple", "food"),
    Element("🍞", "Bread", "food"),
    Element("🍯", "Honey", "food"),
    Element("🍕", "Pizza", "food"),
    Element("🍣", "Sushi", "food"),
    Element("🍭", "Lollipop", "food"),
    
    # Objects
    Element("🗡️", "Sword", "object"),
    Element("🛡️", "Shield", "object"),
    Element("🔑", "Key", "object"),
    Element("💍", "Ring", "object"),
    Element("🏺", "Vase", "object"),
    Element("🕯️", "Candle", "object"),
    
    # More Mythical
    Element("🧌", "Troll", "mythical"),
    Element("🧟", "Zombie", "mythical"),
    Element("👹", "Ogre", "mythical"),
    Element("👽", "Alien", "mythical"),
    Element("🐲", "Dragon Face", "mythical"),
    Element("🦖", "T-Rex", "mythical"),
    
    # More Tech
    Element("🖥️", "Desktop", "tech"),
    Element("🎮", "Controller", "tech"),
    Element("📡", "Satellite", "tech"),
    Element("⏱️", "Stopwatch", "tech"),
    Element("💾", "Floppy Disk", "tech"),
    Element("🧪", "Test Tube", "tech"),
    
    # More Nature
    Element("🌵", "Cactus", "nature"),
    Element("🍄", "Mushroom", "nature"),
    Element("🌻", "Sunflower", "nature"),
    Element("🌲", "Evergreen", "nature"),
    Element("🍁", "Maple Leaf", "nature"),
    Element("🌹", "Rose", "nature"),
    
    # More Materials
    Element("🧱", "Brick", "material"),
    Element("🪵", "Wood", "material"),
    Element("🪶", "Feather", "material"),
    Element("🪸", "Coral", "material"),
    Element("🪨", "Rock", "material"),
    Element("🧶", "Yarn", "material"),
    
    # More Special
    Element("⚰️", "Coffin", "special"),
    Element("🕰️", "Clock", "special"),
    Element("🧿", "Evil Eye", "special"),
    Element("🔮", "Crystal Ball", "special"),
    Element("📜", "Scroll", "special"),
    Element("🗝️", "Old Key", "special")
]

# Enhanced recipes with crucible-specific reactions
recipes = {
    # Fusion Crucible (Combination)
    "fusion": [
        ("🔥", "💧", "💨", "Steam"),
        ("🪨", "💧", "🌱", "Plant"),
        ("🌱", "☀️", "🌻", "Sunflower"),
        ("🪙", "🔥", "🏆", "Gold"),
        ("🧙", "✨", "🧚", "Fairy"),
        ("🐉", "🦄", "🐲", "Dragon Hybrid"),
        ("💻", "🤖", "🦾", "Cyborg"),
        ("🌌", "🪐", "🚀", "Spaceship")
    ],
    
    # Purge Crucible (Subtraction)
    "purge": [
        ("🍎", "🐍", "🧠", "Knowledge"),
        ("💀", "❤️", "👻", "Ghost"),
        ("🌊", "🌪️", "💧", "Pure Water"),
        ("🏆", "🪙", "💎", "Diamond"),
        ("🧟", "🧠", "💀", "Skeleton"),
        ("🌻", "☀️", "🌱", "Seed"),
        ("🤖", "🔋", "⚙️", "Gear")
    ],
    
    # Amplifier Crucible (Multiplication)
    "amplify": [
        ("🐜", "🔥", "🐜🔥", "Fire Ant Swarm"),
        ("💀", "♾️", "💀💀💀", "Ossuary Dimension"),
        ("🌱", "☀️", "🌳🌳🌳", "Forest"),
        ("⚡", "🌪️", "🌩️🌩️", "Thunderstorm"),
        ("🧚", "✨", "🧚🧚🧚", "Fairy Circle"),
        ("🪙", "💎", "💎💎💎", "Gem Cluster"),
        ("🦄", "🌈", "🌈🦄🌈", "Prismatic Unicorn")
    ],
    
    # Fracture Crucible (Division)
    "fracture": [
        ("🧙", "✨", "🧚🧚", "Twin Fairies"),
        ("💎", "🪙", "💎💎", "Gem Shards"),
        ("🌕", "🌑", "🌓🌓", "Crescent Moons"),
        ("🏆", "🔥", "🪙🪙", "Melted Gold"),
        ("🐉", "🪶", "🐲🐲", "Baby Dragons"),
        ("🌌", "🪐", "⭐⭐", "Star Pair"),
        ("🧿", "🔮", "👁️👁️", "All-Seeing Eyes")
    ],
    
    # Chaos Crucible (Random)
    "chaos": [
        ("🌈", "🦄", "🌈🦄", "Prismatic Unicorn"),
        ("🚽", "👑", "🚽👑", "Golden Throne"),
        ("🤖", "🐑", "🤖🐑", "Cyber-Sheep"),
        ("🧦", "🐇", "🧦🐇", "Rabbit Hole"),
        ("🍕", "🌪️", "🍕🌪️", "Pizza Tornado"),
        ("🔋", "💧", "⚡", "Electric Water"),
        ("🧟", "🌹", "🧟🌹", "Zombie Rose")
    ]
}

# Crucible types with positions (2x2 grid)
crucibles = [
    {"type": "fusion", "emoji": "🧪🔥", "pos": (900, 200), "contents": [], "active": False},
    {"type": "purge", "emoji": "🧪💨", "pos": (1100, 200), "contents": [], "active": False},
    {"type": "amplify", "emoji": "🧪⚡", "pos": (900, 400), "contents": [], "active": False},
    {"type": "fracture", "emoji": "🧪💥", "pos": (1100, 400), "contents": [], "active": False},
    {"type": "chaos", "emoji": "🧪🌀", "pos": (1000, 600), "contents": [], "active": False}
]

# Terminal display
terminal_rect = pygame.Rect(400, 600, 450, 250)
terminal_text = ["Welcome to the Ultimate Alchemy Lab!"]
terminal_scroll = 0
terminal_scrollbar = pygame.Rect(840, 600, 10, 250)
terminal_scroll_handle = pygame.Rect(840, 600, 10, 50)
terminal_dragging = False
terminal_line_height = 20
terminal_visible_lines = terminal_rect.height // terminal_line_height

# Elements panel
elements_rect = pygame.Rect(50, 50, 300, 500)
elements_scroll = 0
elements_scrollbar = pygame.Rect(340, 50, 10, 500)
elements_scroll_handle = pygame.Rect(340, 50, 10, 100)
elements_dragging = False
element_button_height = 50
elements_visible_count = elements_rect.height // element_button_height

# UI state
selected_element = None
show_discovered = True  # Toggle between discovered/all elements
view_mode_button = pygame.Rect(50, 560, 300, 30)
last_reaction_time = 0

def render_text(text, x, y, color=(255, 255, 255), font_obj=None, center=False):
    font_obj = font_obj or font
    text_surface = font_obj.render(text, True, color)
    if center:
        x -= text_surface.get_width() // 2
    screen.blit(text_surface, (x, y))

def add_log(message):
    terminal_text.append(message)
    # Auto-scroll to bottom unless user has scrolled up
    if terminal_scroll >= len(terminal_text) - terminal_visible_lines - 1:
        terminal_scroll = max(0, len(terminal_text) - terminal_visible_lines)
    update_terminal_scroll()

def update_terminal_scroll():
    total_lines = len(terminal_text)
    if total_lines <= terminal_visible_lines:
        terminal_scroll_handle.y = terminal_scrollbar.y
        terminal_scroll_handle.height = terminal_scrollbar.height
    else:
        handle_height = max(30, terminal_scrollbar.height * terminal_visible_lines // total_lines)
        max_y = terminal_scrollbar.y + terminal_scrollbar.height - handle_height
        scroll_pos = terminal_scrollbar.y + (terminal_scrollbar.height - handle_height) * terminal_scroll / (total_lines - terminal_visible_lines)
        terminal_scroll_handle.y = min(max_y, scroll_pos)
        terminal_scroll_handle.height = handle_height

def update_elements_scroll():
    element_count = len([e for e in all_elements if e.discovered]) if show_discovered else len(all_elements)
    if element_count <= elements_visible_count:
        elements_scroll_handle.y = elements_scrollbar.y
        elements_scroll_handle.height = elements_scrollbar.height
    else:
        handle_height = max(30, elements_scrollbar.height * elements_visible_count / element_count)
        max_y = elements_scrollbar.y + elements_scrollbar.height - handle_height
        scroll_pos = elements_scrollbar.y + (elements_scrollbar.height - handle_height) * elements_scroll / (element_count - elements_visible_count)
        elements_scroll_handle.y = min(max_y, scroll_pos)
        elements_scroll_handle.height = handle_height

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

def draw_crucible(crucible):
    color = CRUCIBLE_COLORS[crucible["type"]]
    if crucible["active"]:
        color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))
    
    # Crucible body
    pygame.draw.ellipse(screen, color, (crucible["pos"][0], crucible["pos"][1], 150, 100))
    pygame.draw.rect(screen, color, (crucible["pos"][0]+25, crucible["pos"][1]+50, 100, 80))
    
    # Crucible neck
    pygame.draw.rect(screen, color, (crucible["pos"][0]+60, crucible["pos"][1]-30, 30, 30))
    
    # Crucible contents animation
    if crucible["active"]:
        for i in range(5):
            x = crucible["pos"][0] + 50 + random.randint(0, 50)
            y = crucible["pos"][1] + 30 + random.randint(0, 40)
            pygame.draw.circle(screen, (200, 200, 255, 150), (x, y), random.randint(3, 8))
    
    # Contents display
    if crucible["contents"]:
        content_text = "".join(crucible["contents"])
        render_text(content_text, crucible["pos"][0]+75, crucible["pos"][1]+70, font_obj=large_font, center=True)
    
    # Label
    render_text(crucible["emoji"], crucible["pos"][0]+75, crucible["pos"][1]-50, font_obj=large_font, center=True)
    render_text(crucible["type"].capitalize(), crucible["pos"][0]+75, crucible["pos"][1]-10, center=True)

def draw_terminal():
    # Terminal background
    pygame.draw.rect(screen, TERMINAL_BG, terminal_rect)
    pygame.draw.rect(screen, (50, 50, 70), terminal_rect, 2)
    
    # Draw visible text lines
    total_lines = len(terminal_text)
    start_line = max(0, min(terminal_scroll, total_lines - terminal_visible_lines))
    
    clip_rect = pygame.Rect(terminal_rect.x, terminal_rect.y, terminal_rect.width-15, terminal_rect.height)
    screen.set_clip(clip_rect)
    
    for i in range(terminal_visible_lines):
        line_idx = start_line + i
        if line_idx < total_lines:
            render_text(terminal_text[line_idx], 
                       terminal_rect.x + 10, 
                       terminal_rect.y + 10 + i * terminal_line_height)
    
    screen.set_clip(None)
    
    # Draw scrollbar
    pygame.draw.rect(screen, SCROLLBAR_COLOR, terminal_scrollbar)
    pygame.draw.rect(screen, SCROLLBAR_HANDLE, terminal_scroll_handle)

def draw_elements_panel():
    # Panel background
    pygame.draw.rect(screen, PANEL_BG, elements_rect)
    pygame.draw.rect(screen, (50, 50, 70), elements_rect, 2)
    
    # Title
    render_text("Elements Inventory", elements_rect.x + 10, elements_rect.y + 10)
    
    # View mode button
    pygame.draw.rect(screen, (70, 70, 90), view_mode_button)
    mode_text = "Showing: " + ("Discovered" if show_discovered else "All")
    render_text(mode_text, view_mode_button.x + 10, view_mode_button.y + 8)
    
    # Filter elements based on view mode
    display_elements = [e for e in all_elements if not show_discovered or e.discovered]
    element_count = len(display_elements)
    
    # Draw visible elements
    start_idx = max(0, min(elements_scroll, element_count - elements_visible_count))
    
    clip_rect = pygame.Rect(elements_rect.x, elements_rect.y, elements_rect.width-15, elements_rect.height-40)
    screen.set_clip(clip_rect)
    
    for i in range(elements_visible_count):
        element_idx = start_idx + i
        if element_idx < element_count:
            element = display_elements[element_idx]
            y_pos = elements_rect.y + 50 + i * element_button_height
            
            # Highlight selected element
            if element.emoji == selected_element:
                pygame.draw.rect(screen, (80, 80, 100), 
                               (elements_rect.x + 5, y_pos - 5, elements_rect.width - 15, element_button_height))
            
            # Draw element
            pygame.draw.rect(screen, (60, 60, 80), 
                           (elements_rect.x + 10, y_pos, elements_rect.width - 20, element_button_height - 10))
            render_text(f"{element.emoji} {element.name}", elements_rect.x + 20, y_pos + 10)
            
            # Show discovery status if in "all" view
            if not show_discovered and not element.discovered:
                render_text("?", elements_rect.x + elements_rect.width - 30, y_pos + 10, (200, 200, 200))
    
    screen.set_clip(None)
    
    # Draw scrollbar
    pygame.draw.rect(screen, SCROLLBAR_COLOR, elements_scrollbar)
    pygame.draw.rect(screen, SCROLLBAR_HANDLE, elements_scroll_handle)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BACKGROUND)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            
            # Check view mode toggle
            if view_mode_button.collidepoint(x, y):
                show_discovered = not show_discovered
                elements_scroll = 0
                update_elements_scroll()
            
            # Check element selection
            display_elements = [e for e in all_elements if not show_discovered or e.discovered]
            start_idx = max(0, min(elements_scroll, len(display_elements) - elements_visible_count))
            
            for i in range(elements_visible_count):
                element_idx = start_idx + i
                if element_idx < len(display_elements):
                    element = display_elements[element_idx]
                    y_pos = elements_rect.y + 50 + i * element_button_height
                    
                    if (elements_rect.x + 10 <= x <= elements_rect.x + elements_rect.width - 10 and
                        y_pos <= y <= y_pos + element_button_height - 10):
                        
                        if element.discovered or not show_discovered:
                            selected_element = element.emoji
                            add_log(f"Selected: {element.emoji} {element.name}")
            
            # Check crucible selection
            for crucible in crucibles:
                if (crucible["pos"][0] <= x <= crucible["pos"][0] + 150 and
                    crucible["pos"][1] - 30 <= y <= crucible["pos"][1] + 130):
                    
                    if selected_element:
                        crucible["active"] = True
                        crucible["contents"].append(selected_element)
                        add_log(f"Added {selected_element} to {crucible['type']} crucible")
                        
                        # If crucible has 2 elements, mix them
                        if len(crucible["contents"]) == 2:
                            result_emoji, result_name = mix_elements(
                                crucible["contents"][0],
                                crucible["contents"][1],
                                crucible["type"]
                            )
                            
                            # Find or create the result element
                            result_element = next((e for e in all_elements if e.emoji == result_emoji), None)
                            if not result_element:
                                result_element = Element(result_emoji, result_name, "special", True)
                                all_elements.append(result_element)
                            
                            # Mark as discovered
                            result_element.discovered = True
                            
                            add_log(f"DISCOVERY: {crucible['contents'][0]} + {crucible['contents'][1]} = {result_emoji} ({result_name})")
                            
                            # Reset crucible after short delay
                            pygame.time.set_timer(pygame.USEREVENT + crucibles.index(crucible), 2000, True)
                            
                            # Show result in crucible
                            crucible["contents"] = [result_emoji]
                        
                        selected_element = None
            
            # Terminal scrollbar
            if terminal_scrollbar.collidepoint(x, y):
                if terminal_scroll_handle.collidepoint(x, y):
                    terminal_dragging = True
                else:
                    # Jump to clicked position
                    rel_y = y - terminal_scrollbar.y
                    frac = rel_y / terminal_scrollbar.height
                    terminal_scroll = int(frac * (len(terminal_text) - terminal_visible_lines))
                    update_terminal_scroll()
            
            # Elements scrollbar
            if elements_scrollbar.collidepoint(x, y):
                if elements_scroll_handle.collidepoint(x, y):
                    elements_dragging = True
                else:
                    # Jump to clicked position
                    element_count = len([e for e in all_elements if not show_discovered or e.discovered])
                    rel_y = y - elements_scrollbar.y
                    frac = rel_y / elements_scrollbar.height
                    elements_scroll = int(frac * (element_count - elements_visible_count))
                    update_elements_scroll()
        
        if event.type == pygame.MOUSEBUTTONUP:
            terminal_dragging = False
            elements_dragging = False
        
        if event.type == pygame.MOUSEMOTION:
            # Terminal scroll dragging
            if terminal_dragging:
                rel_y = event.pos[1] - terminal_scrollbar.y
                frac = rel_y / terminal_scrollbar.height
                terminal_scroll = min(max(0, int(frac * (len(terminal_text) - terminal_visible_lines))), 
                                    len(terminal_text) - terminal_visible_lines)
                update_terminal_scroll()
            
            # Elements scroll dragging
            if elements_dragging:
                element_count = len([e for e in all_elements if not show_discovered or e.discovered])
                rel_y = event.pos[1] - elements_scrollbar.y
                frac = rel_y / elements_scrollbar.height
                elements_scroll = min(max(0, int(frac * (element_count - elements_visible_count))), 
                                    element_count - elements_visible_count)
                update_elements_scroll()
        
        if event.type == pygame.MOUSEWHEEL:
            # Terminal scrolling
            if terminal_rect.collidepoint(pygame.mouse.get_pos()):
                terminal_scroll = max(0, min(terminal_scroll - event.y, len(terminal_text) - terminal_visible_lines))
                update_terminal_scroll()
            
            # Elements panel scrolling
            elif elements_rect.collidepoint(pygame.mouse.get_pos()):
                element_count = len([e for e in all_elements if not show_discovered or e.discovered])
                elements_scroll = max(0, min(elements_scroll - event.y, element_count - elements_visible_count))
                update_elements_scroll()
        
        # Crucible reset timer
        if event.type >= pygame.USEREVENT and event.type < pygame.USEREVENT + len(crucibles):
            crucible_idx = event.type - pygame.USEREVENT
            crucibles[crucible_idx]["contents"] = []
            crucibles[crucible_idx]["active"] = False
    
    # Drawing
    draw_elements_panel()
    
    # Draw crucibles in 2x2 grid + chaos in center bottom
    for crucible in crucibles:
        draw_crucible(crucible)
    
    draw_terminal()
    
    # Show selected element
    if selected_element:
        element = next((e for e in all_elements if e.emoji == selected_element), None)
        if element:
            render_text(f"Selected: {element.emoji} {element.name}", 50, 570, (255, 255, 0))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()