import pygame
import random
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_SIZE = (1400, 900)
FPS = 60
ELEMENT_SIZE = 60
CRUCIBLE_SIZE = (160, 200)

# Colors
DARK_BG = (20, 20, 30)
PANEL_COLOR = (35, 35, 55)
SCROLLBAR_COLOR = (70, 70, 90)
HIGHLIGHT_COLOR = (100, 100, 140)

# Setup display
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("🔥 Ultimate Emoji Alchemy Lab 🔥")
clock = pygame.time.Clock()

# Fonts
try:
    emoji_font = pygame.font.SysFont('segoeuiemoji', 36)
    medium_font = pygame.font.SysFont('arial', 24)
    small_font = pygame.font.SysFont('arial', 16)
except:
    emoji_font = pygame.font.SysFont(None, 36)
    medium_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 16)

class Element:
    def __init__(self, emoji, name, category='basic', discovered=False):
        self.emoji = emoji
        self.name = name
        self.category = category
        self.discovered = discovered
        self.rect = pygame.Rect(0, 0, ELEMENT_SIZE, ELEMENT_SIZE)
        
    def draw(self, x, y):
        self.rect.topleft = (x, y)
        pygame.draw.rect(screen, (50, 50, 70), self.rect, border_radius=5)
        text = emoji_font.render(self.emoji, True, (255, 255, 255))
        screen.blit(text, (x + ELEMENT_SIZE//2 - text.get_width()//2, 
                         y + ELEMENT_SIZE//2 - text.get_height()//2))
        
        if not self.discovered:
            pygame.draw.rect(screen, (0, 0, 0, 150), self.rect, border_radius=5)
            text = medium_font.render("?", True, (200, 200, 200))
            screen.blit(text, (x + ELEMENT_SIZE//2 - text.get_width()//2, 
                              y + ELEMENT_SIZE//2 - text.get_height()//2))

class Crucible:
    def __init__(self, x, y, c_type):
        self.rect = pygame.Rect(x, y, *CRUCIBLE_SIZE)
        self.type = c_type
        self.color = self.get_crucible_color()
        self.contents = []
        self.active = False
        self.bubble_time = 0
        
    def get_crucible_color(self):
        colors = {
            'fusion': (220, 80, 80),
            'purge': (80, 220, 80),
            'amplify': (80, 80, 220),
            'fracture': (220, 220, 80),
            'chaos': (180, 80, 220)
        }
        return colors.get(self.type, (150, 150, 150))
        
    def draw(self):
        # Main body
        pygame.draw.ellipse(screen, self.color, self.rect)
        
        # Neck
        neck_rect = pygame.Rect(
            self.rect.x + self.rect.width//2 - 20,
            self.rect.y - 30,
            40, 40
        )
        pygame.draw.rect(screen, self.color, neck_rect, border_radius=5)
        
        # Contents
        if self.contents:
            content_text = "".join(self.contents)
            text_surf = emoji_font.render(content_text, True, (255, 255, 255))
            screen.blit(text_surf, (
                self.rect.x + self.rect.width//2 - text_surf.get_width()//2,
                self.rect.y + 50
            ))
        
        # Bubbles animation
        if self.active:
            self.bubble_time += 1
            for _ in range(3):
                x = random.randint(self.rect.left + 20, self.rect.right - 20)
                y = random.randint(self.rect.top + 20, self.rect.bottom - 20)
                size = random.randint(3, 8)
                alpha = min(255, 100 + abs(150 - (self.bubble_time % 300)))
                bubble_color = (*self.color[:3], alpha)
                
                bubble_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(bubble_surf, bubble_color, (size, size), size)
                screen.blit(bubble_surf, (x - size, y - size))
        
        # Label
        label = medium_font.render(self.type.capitalize(), True, (240, 240, 240))
        screen.blit(label, (
            self.rect.x + self.rect.width//2 - label.get_width()//2,
            self.rect.y + self.rect.height + 10
        ))

class ScrollablePanel:
    def __init__(self, x, y, w, h, item_h=60):
        self.rect = pygame.Rect(x, y, w, h)
        self.scroll = 0
        self.scroll_drag = False
        self.item_height = item_h
        self.scrollbar = pygame.Rect(x + w - 12, y, 12, h)
        self.scroll_handle = pygame.Rect(x + w - 12, y, 12, 100)
        
    def update_scroll(self, item_count):
        visible_items = self.rect.height // self.item_height
        max_scroll = max(0, item_count - visible_items)
        self.scroll = min(max_scroll, self.scroll)
        
        # Update scroll handle
        if item_count > visible_items:
            handle_height = max(30, self.rect.height * visible_items / item_count)
            scroll_ratio = self.scroll / max(1, max_scroll)
            self.scroll_handle.height = handle_height
            self.scroll_handle.y = self.scrollbar.y + scroll_ratio * (self.scrollbar.height - handle_height)
        else:
            self.scroll_handle.height = self.scrollbar.height
            self.scroll_handle.y = self.scrollbar.y
        
    def draw(self, title, items, draw_item_callback, highlight_index=None):
        # Panel background
        pygame.draw.rect(screen, PANEL_COLOR, self.rect, border_radius=8)
        
        # Title
        title_surf = medium_font.render(title, True, (240, 240, 240))
        screen.blit(title_surf, (self.rect.x + 15, self.rect.y + 10))
        
        # Content area
        content_rect = pygame.Rect(
            self.rect.x + 5,
            self.rect.y + 40,
            self.rect.width - 20,
            self.rect.height - 50
        )
        
        # Clip drawing to content area
        clip_rect = screen.get_clip()
        screen.set_clip(content_rect)
        
        # Draw visible items
        visible_count = content_rect.height // self.item_height
        start_idx = min(self.scroll, max(0, len(items) - visible_count))
        
        for i in range(visible_count + 1):
            idx = start_idx + i
            if idx < len(items):
                y_pos = content_rect.y + i * self.item_height - self.scroll % 1 * self.item_height
                
                # Highlight if needed
                if idx == highlight_index:
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, 
                        (content_rect.x, y_pos, content_rect.width, self.item_height), border_radius=4)
                
                # Draw item
                draw_item_callback(items[idx], content_rect.x + 10, y_pos + 5)
        
        screen.set_clip(clip_rect)
        
        # Draw scrollbar if needed
        if len(items) > visible_count:
            pygame.draw.rect(screen, SCROLLBAR_COLOR, self.scrollbar, border_radius=6)
            pygame.draw.rect(screen, (120, 120, 150), self.scroll_handle, border_radius=6)
        
        # Border
        pygame.draw.rect(screen, (60, 60, 80), self.rect, 2, border_radius=8)

# Game Data
elements = [
    Element("🔥", "Fire", "element", True),
    Element("💧", "Water", "element", True),
    Element("🌪️", "Wind", "element", True),
    Element("🪨", "Earth", "element", True),
    Element("⚡", "Lightning", "element", True),
    Element("❄️", "Ice", "element"),
    Element("🌱", "Plant", "nature"),
    Element("💨", "Steam", "element"),
    Element("🌊", "Wave", "element"),
    Element("🪙", "Metal", "material"),
    Element("🏆", "Gold", "material"),
    Element("💎", "Diamond", "material"),
    Element("🐍", "Snake", "animal"),
    Element("🦅", "Eagle", "animal"),
    Element("🐉", "Dragon", "mythical"),
    Element("🦄", "Unicorn", "mythical"),
    Element("☀️", "Sun", "celestial"),
    Element("🌙", "Moon", "celestial"),
    Element("⭐", "Star", "celestial"),
    Element("🌠", "Shooting Star", "celestial"),
    Element("🧙", "Wizard", "magic"),
    Element("🧚", "Fairy", "magic"),
    Element("👻", "Ghost", "magic"),
    Element("🧛", "Vampire", "magic"),
    Element("🔋", "Battery", "tech"),
    Element("💻", "Computer", "tech"),
    Element("📱", "Phone", "tech"),
    Element("🤖", "Robot", "tech"),
    Element("💀", "Death", "special"),
    Element("❤️", "Heart", "special"),
    Element("✨", "Magic", "special"),
    Element("♾️", "Infinity", "special")
]

recipes = {
    'fusion': [
        (["🔥", "💧"], "💨", "Steam"),
        (["🪨", "💧"], "🌱", "Plant"),
        (["🌱", "☀️"], "🌻", "Sunflower"),
        (["🪙", "🔥"], "🏆", "Gold"),
        (["🧙", "✨"], "🧚", "Fairy"),
        (["🐉", "🦄"], "🐲", "Dragon Hybrid"),
        (["💻", "🤖"], "🦾", "Cyborg")
    ],
    'purge': [
        (["🍎", "🐍"], "🧠", "Knowledge"),
        (["💀", "❤️"], "👻", "Ghost"),
        (["🌊", "🌪️"], "💧", "Pure Water"),
        (["🏆", "🪙"], "💎", "Diamond"),
        (["🧟", "🧠"], "💀", "Skeleton")
    ],
    'amplify': [
        (["🐜", "🔥"], "🐜🔥", "Fire Ant Swarm"),
        (["💀", "♾️"], "💀💀💀", "Ossuary Dimension"),
        (["🌱", "☀️"], "🌳🌳🌳", "Forest"),
        (["⚡", "🌪️"], "🌩️🌩️", "Thunderstorm"),
        (["🧚", "✨"], "🧚🧚🧚", "Fairy Circle")
    ],
    'fracture': [
        (["🧙", "✨"], "🧚🧚", "Twin Fairies"),
        (["💎", "🪙"], "💎💎", "Gem Shards"),
        (["🌕", "🌑"], "🌓🌓", "Crescent Moons"),
        (["🏆", "🔥"], "🪙🪙", "Melted Gold"),
        (["🐉", "🪶"], "🐲🐲", "Baby Dragons")
    ],
    'chaos': [
        (["🌈", "🦄"], "🌈🦄", "Prismatic Unicorn"),
        (["🚽", "👑"], "🚽👑", "Golden Throne"),
        (["🤖", "🐑"], "🤖🐑", "Cyber-Sheep"),
        (["🧦", "🐇"], "🧦🐇", "Rabbit Hole"),
        (["🍕", "🌪️"], "🍕🌪️", "Pizza Tornado")
    ]
}

# UI Setup
elements_panel = ScrollablePanel(50, 50, 350, 500)
terminal_panel = ScrollablePanel(450, 50, 500, 300)
view_mode = "discovered"  # or "all"

# Crucible Setup
crucibles = [
    Crucible(1000, 150, 'fusion'),
    Crucible(1200, 150, 'purge'),
    Crucible(1000, 400, 'amplify'),
    Crucible(1200, 400, 'fracture'),
    Crucible(1100, 650, 'chaos')
]

# Game State
selected_element = None
terminal_messages = ["Welcome to the Ultimate Alchemy Lab!"]
discovery_count = 4  # Starting with 4 basic elements

def draw_element_item(element, x, y):
    element.draw(x, y)
    if element.discovered:
        name = small_font.render(element.name, True, (200, 200, 200))
        screen.blit(name, (x + ELEMENT_SIZE + 10, y + ELEMENT_SIZE//2 - name.get_height()//2))

def draw_terminal_item(message, x, y):
    text = small_font.render(message, True, (220, 220, 220))
    screen.blit(text, (x, y))

def mix_elements(e1, e2, crucible_type):
    # Check recipes first
    for recipe in recipes[crucible_type]:
        if {e1, e2} == set(recipe[0]):
            return recipe[1], recipe[2]
    
    # Default behaviors
    if crucible_type == 'fusion':
        return f"{e1}{e2}", "Combined Element"
    elif crucible_type == 'purge':
        return e1, f"Purified {e1}"
    elif crucible_type == 'amplify':
        return f"{e1}{e1}{e1}", f"Amplified {e1}"
    elif crucible_type == 'fracture':
        return e1[:len(e1)//2], f"Fragment of {e1}"
    else:  # chaos
        outcomes = [
            (f"{e1}{e2}", "Chaos Fusion"),
            ("💥", "Explosion"),
            ("❓", "Unknown Reaction"),
            (random.choice(["✨", "⚡", "🔥", "💧"]), "Elemental Essence")
        ]
        return random.choice(outcomes)

def discover_element(emoji, name):
    global discovery_count
    for element in elements:
        if element.emoji == emoji:
            if not element.discovered:
                element.discovered = True
                discovery_count += 1
                terminal_messages.append(f"Discovered: {emoji} {name}!")
                return True
    return False

def main():
    global selected_element, view_mode, discovery_count
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            elif event.type == KEYDOWN:
                if event.key == K_TAB:
                    view_mode = "all" if view_mode == "discovered" else "discovered"
            
            elif event.type == MOUSEBUTTONDOWN:
                # Check element selection
                visible_elements = [e for e in elements if view_mode == "all" or e.discovered]
                elements_panel.update_scroll(len(visible_elements))
                
                visible_count = elements_panel.rect.height // elements_panel.item_height
                start_idx = min(elements_panel.scroll, max(0, len(visible_elements) - visible_count))
                
                for i in range(visible_count + 1):
                    idx = start_idx + i
                    if idx < len(visible_elements):
                        y_pos = (elements_panel.rect.y + 40 + 
                                i * elements_panel.item_height - 
                                elements_panel.scroll % 1 * elements_panel.item_height)
                        
                        if (elements_panel.rect.x + 5 <= mouse_pos[0] <= elements_panel.rect.right - 20 and
                            y_pos <= mouse_pos[1] <= y_pos + elements_panel.item_height):
                            selected_element = visible_elements[idx].emoji
                            terminal_messages.append(f"Selected: {visible_elements[idx].emoji} {visible_elements[idx].name}")
                
                # Check crucible clicks
                for crucible in crucibles:
                    if crucible.rect.collidepoint(mouse_pos):
                        if selected_element:
                            if len(crucible.contents) < 2:
                                crucible.contents.append(selected_element)
                                crucible.active = True
                                terminal_messages.append(f"Added {selected_element} to {crucible.type} crucible")
                                
                                # If we have 2 elements, mix them
                                if len(crucible.contents) == 2:
                                    result_emoji, result_name = mix_elements(
                                        crucible.contents[0],
                                        crucible.contents[1],
                                        crucible.type
                                    )
                                    
                                    # Check if this is a new discovery
                                    discovered = discover_element(result_emoji, result_name)
                                    
                                    if discovered:
                                        terminal_messages.append(f"NEW DISCOVERY: {result_emoji} {result_name}!")
                                    else:
                                        terminal_messages.append(f"Created: {result_emoji} {result_name}")
                                    
                                    # Show result temporarily
                                    crucible.contents = [result_emoji]
                                    pygame.time.set_timer(
                                        USEREVENT + crucibles.index(crucible), 
                                        2000,  # 2 second display
                                        True
                                    )
                            
                            selected_element = None
            
            elif event.type == MOUSEBUTTONUP:
                elements_panel.scroll_drag = False
                terminal_panel.scroll_drag = False
            
            elif event.type == MOUSEMOTION:
                # Handle panel scrolling
                if elements_panel.scroll_drag:
                    visible_elements = [e for e in elements if view_mode == "all" or e.discovered]
                    elements_panel.scroll = min(max(0, 
                        (mouse_pos[1] - elements_panel.scrollbar.y) / 
                        elements_panel.scrollbar.height * 
                        max(0, len(visible_elements) - elements_panel.rect.height // elements_panel.item_height)
                    ), max(0, len(visible_elements) - elements_panel.rect.height // elements_panel.item_height))
                
                if terminal_panel.scroll_drag:
                    terminal_panel.scroll = min(max(0, 
                        (mouse_pos[1] - terminal_panel.scrollbar.y) / 
                        terminal_panel.scrollbar.height * 
                        max(0, len(terminal_messages) - terminal_panel.rect.height // terminal_panel.item_height)
                    ), max(0, len(terminal_messages) - terminal_panel.rect.height // terminal_panel.item_height))
            
            elif event.type == MOUSEWHEEL:
                # Scroll panels with mouse wheel
                if elements_panel.rect.collidepoint(mouse_pos):
                    elements_panel.scroll = max(0, elements_panel.scroll - event.y)
                
                if terminal_panel.rect.collidepoint(mouse_pos):
                    terminal_panel.scroll = max(0, terminal_panel.scroll - event.y)
            
            elif event.type >= USEREVENT and event.type < USEREVENT + len(crucibles):
                # Crucible reset timer
                crucible_idx = event.type - USEREVENT
                crucibles[crucible_idx].contents = []
                crucibles[crucible_idx].active = False
                crucibles[crucible_idx].bubble_time = 0
        
        # Update
        visible_elements = [e for e in elements if view_mode == "all" or e.discovered]
        elements_panel.update_scroll(len(visible_elements))
        terminal_panel.update_scroll(len(terminal_messages))
        
        # Draw
        screen.fill(DARK_BG)
        
        # Draw panels
        elements_panel.draw(
            f"Elements ({discovery_count}/{len(elements)})",
            visible_elements,
            draw_element_item,
            highlight_index=next((i for i, e in enumerate(visible_elements) 
                              if e.emoji == selected_element), None)
        )

        terminal_panel.draw(
            "Alchemy Log",
            terminal_messages,
            draw_terminal_item
        )
        
        # Draw crucibles
        for crucible in crucibles:
            crucible.draw()
        
        # Draw selected element
        if selected_element:
            selected_pos = (mouse_pos[0] - ELEMENT_SIZE//2, mouse_pos[1] - ELEMENT_SIZE//2)
            element = next((e for e in elements if e.emoji == selected_element), None)
            if element:
                element.draw(*selected_pos)
        
        # Draw view mode toggle
        mode_text = f"View: {view_mode.capitalize()} (TAB to toggle)"
        mode_surf = small_font.render(mode_text, True, (200, 200, 200))
        screen.blit(mode_surf, (50, SCREEN_SIZE[1] - 30))
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()