import pygame
import math
import random
import webbrowser
import os
import urllib.request

pygame.init()

# ---------------------------------------------------------
# ফুল স্ক্রিন ও রেসপন্সিভ সেটআপ
# ---------------------------------------------------------
info = pygame.display.Info()
WIDTH = info.current_w if info.current_w > 0 else 450
HEIGHT = info.current_h if info.current_h > 0 else 850

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("AMIT MOJUMDAR - Cyber UI Exact Replica")

clock = pygame.time.Clock()

PROFILE_IMAGE_URL = "https://files.catbox.moe/jv9tf7.png" 

# ---------------------------------------------------------
# মূল কালার প্যালেন্ট (Exact Image Match)
# ---------------------------------------------------------
BG_DARK = (1, 10, 15)
CARD_BG = (2, 22, 30)
TEXT_WHITE = (255, 255, 255)
TEXT_CYAN = (0, 240, 250)
TEXT_MUTED = (210, 240, 245)
BORDER_CYAN = (0, 200, 220)

# বড় স্টাইলিশ ফন্ট
font_title = pygame.font.SysFont("impact", int(WIDTH * 0.095))
font_subtitle = pygame.font.SysFont("arial black", int(WIDTH * 0.038))
font_body = pygame.font.SysFont("arial", int(WIDTH * 0.035), bold=True)
font_btn_title = pygame.font.SysFont("arial", int(WIDTH * 0.046), bold=True)
font_btn_val = pygame.font.SysFont("arial", int(WIDTH * 0.038))

# ---------------------------------------------------------
# হেক্সাগন ড্রয়ার
# ---------------------------------------------------------
def draw_hexagon(surface, color, center, radius, width=0, angle_offset=0):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30 + angle_offset
        angle_rad = math.radians(angle_deg)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, width)
    return points

# ---------------------------------------------------------
# প্রোফাইল ছবি লোড ও হেক্সাগন মাস্ক
# ---------------------------------------------------------
hex_size = (int(WIDTH * 0.54), int(WIDTH * 0.54))
profile_surf = None

if PROFILE_IMAGE_URL.startswith("http"):
    try:
        req = urllib.request.Request(PROFILE_IMAGE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp, open("user_photo.png", 'wb') as f:
            f.write(resp.read())
        
        if os.path.exists("user_photo.png"):
            raw_img = pygame.image.load("user_photo.png")
            scaled_img = pygame.transform.smoothscale(raw_img, hex_size)
            
            mask = pygame.Surface(hex_size, pygame.SRCALPHA)
            draw_hexagon(mask, (255, 255, 255, 255), (hex_size[0] // 2, hex_size[1] // 2), hex_size[0] // 2 - 2, 0)
            
            profile_surf = pygame.Surface(hex_size, pygame.SRCALPHA)
            profile_surf.blit(scaled_img, (0, 0))
            profile_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    except Exception:
        profile_surf = None

# ---------------------------------------------------------
# সোশ্যাল আইকন লোডার
# ---------------------------------------------------------
icons_urls = {
    "ph": ("https://cdn-icons-png.flaticon.com/512/724/724664.png", "ph.png"),
    "wa": ("https://cdn-icons-png.flaticon.com/512/3670/3670051.png", "wa.png"),
    "tt": ("https://cdn-icons-png.flaticon.com/512/3046/3046124.png", "tt.png"),
    "fb": ("https://cdn-icons-png.flaticon.com/512/5968/5968764.png", "fb.png"),
    "yt": ("https://cdn-icons-png.flaticon.com/512/1384/1384060.png", "yt.png")
}

icon_surfaces = {}
ICON_SIZE = int(WIDTH * 0.092) 

for key, (url, filename) in icons_urls.items():
    if not os.path.exists(filename):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as resp, open(filename, 'wb') as f:
                f.write(resp.read())
        except Exception:
            pass
    if os.path.exists(filename):
        try:
            icon_img = pygame.image.load(filename)
            icon_surfaces[key] = pygame.transform.smoothscale(icon_img, (ICON_SIZE, ICON_SIZE))
        except Exception:
            icon_surfaces[key] = None

buttons = [
    ("Phone & WhatsApp", "+880 1302015218", "tel:01302015218", ["ph", "wa"]),
    ("TikTok Profile", "@amitmojumder08", "https://www.tiktok.com/@amitmojumder08", ["tt"]),
    ("Facebook Profile", "Amit Mojumdar", "https://www.facebook.com/share/1DD3727sGV/", ["fb"]),
    ("YouTube Channel", "@amitxguitar", "https://youtube.com/@amitxguitar", ["yt"])
]

# ---------------------------------------------------------
# ভাসমান তারা ও ডট অ্যারো গ্রাফিক্স
# ---------------------------------------------------------
stars = []
for _ in range(50):
    stars.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "vx": random.uniform(-0.6, 0.6),
        "vy": random.uniform(-1.0, -0.3),
        "radius": random.uniform(1.0, 3.2),
        "alpha": random.uniform(0.3, 1.0)
    })

def draw_chevron_dots(surface, start_x, start_y, direction=1):
    for col in range(5):
        num_dots = 5 - abs(col - 2)
        for row in range(num_dots):
            x = start_x + (col * 8 * direction)
            y = start_y + (row * 10) - (num_dots * 3)
            pygame.draw.circle(surface, (0, 200, 220), (x, y), 2)

# ---------------------------------------------------------
# মূল অ্যানিমেশন লুপ
# ---------------------------------------------------------
running = True
time_counter = 0

while running:
    time_counter += 0.05
    mouse_pos = pygame.mouse.get_pos()
    
    glow_val = (math.sin(time_counter) + 1) / 2
    glow_color = (0, int(210 + (45 * glow_val)), int(220 + (35 * glow_val)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, (name, label, url, icons) in enumerate(buttons):
                btn_y = int(HEIGHT * 0.50) + (i * int(HEIGHT * 0.093))
                btn_rect = pygame.Rect(int(WIDTH * 0.07), btn_y, int(WIDTH * 0.86), int(HEIGHT * 0.086))
                if btn_rect.collidepoint(mouse_pos):
                    webbrowser.open(url)

            if int(HEIGHT * 0.88) < mouse_pos[1] < int(HEIGHT * 0.98):
                webbrowser.open("https://www.facebook.com/share/1DD3727sGV/")

    screen.fill(BG_DARK)

    # ১. ভাসমান তারার এনিমেশন
    for st in stars:
        st["x"] += st["vx"]
        st["y"] += st["vy"]
        if st["y"] < -5 or st["x"] < -5 or st["x"] > WIDTH + 5:
            st["x"] = random.randint(0, WIDTH)
            st["y"] = HEIGHT + 5

        star_c = (0, int(200 * st["alpha"]), int(230 * st["alpha"]))
        pygame.draw.circle(screen, star_c, (int(st["x"]), int(st["y"])), int(st["radius"]))

    center_x = WIDTH // 2
    hex_center_y = int(HEIGHT * 0.19)

    # ২. ব্যাকগ্রাউন্ড সাইড ডট আর্ট
    draw_chevron_dots(screen, int(WIDTH * 0.12), hex_center_y - 20, direction=1)
    draw_chevron_dots(screen, int(WIDTH * 0.88), hex_center_y - 20, direction=-1)

    # ৩. আউটার বর্ডার (মোটা করা হয়েছে: width=6)
    pygame.draw.rect(screen, glow_color, (10, 10, WIDTH - 20, HEIGHT - 20), width=6, border_radius=18)

    # ৪. হেক্সাগন গ্লো ফ্রেম (মোটা করা হয়েছে: width=6 এবং width=4)
    radius = int(WIDTH * 0.28)
    draw_hexagon(screen, glow_color, (center_x, hex_center_y), radius + 6, width=6)
    draw_hexagon(screen, (0, 140, 160), (center_x, hex_center_y), radius + 14, width=4)

    if profile_surf:
        screen.blit(profile_surf, (center_x - hex_size[0] // 2, hex_center_y - hex_size[1] // 2))

    # ৫. বড় ও ডেকোরেটেড টেক্সট
    txt_y = hex_center_y + radius + 18

    # ৩ডি শ্যাডো সহ নাম
    shadow_surf = font_title.render("AMIT MOJUMDAR", True, (0, 80, 100))
    name_surf = font_title.render("AMIT MOJUMDAR", True, TEXT_WHITE)
    screen.blit(shadow_surf, (center_x - (name_surf.get_width() // 2) + 2, txt_y + 2))
    screen.blit(name_surf, (center_x - (name_surf.get_width() // 2), txt_y))

    # সাবটাইটেল ১ + সাইড লাইন
    tag_surf = font_subtitle.render("STUDENT  •  CREATOR", True, TEXT_CYAN)
    tag_x = center_x - (tag_surf.get_width() // 2)
    tag_y = txt_y + 45
    screen.blit(tag_surf, (tag_x, tag_y))
    
    pygame.draw.line(screen, glow_color, (tag_x - 30, tag_y + 10), (tag_x - 8, tag_y + 10), 3)
    pygame.draw.line(screen, glow_color, (tag_x + tag_surf.get_width() + 8, tag_y + 10), (tag_x + tag_surf.get_width() + 30, tag_y + 10), 3)

    # সাবটাইটেল ২ + সাইড লাইন
    sub_tag = font_body.render("Dream  •  Work  •  Create  •  Achieve", True, TEXT_MUTED)
    sub_x = center_x - (sub_tag.get_width() // 2)
    sub_y = tag_y + 32
    screen.blit(sub_tag, (sub_x, sub_y))

    pygame.draw.line(screen, (0, 160, 180), (sub_x - 22, sub_y + 8), (sub_x - 6, sub_y + 8), 3)
    pygame.draw.line(screen, (0, 160, 180), (sub_x + sub_tag.get_width() + 6, sub_y + 8), (sub_x + sub_tag.get_width() + 22, sub_y + 8), 3)

    # ৬. সোশ্যাল বাটন (বর্ডার মোটা করা হয়েছে: width=4)
    for i, (name, label, url, icons) in enumerate(buttons):
        btn_y = int(HEIGHT * 0.50) + (i * int(HEIGHT * 0.093))
        btn_rect = pygame.Rect(int(WIDTH * 0.07), btn_y, int(WIDTH * 0.86), int(HEIGHT * 0.086))
        is_hover = btn_rect.collidepoint(mouse_pos)

        card_col = (5, 32, 42) if is_hover else CARD_BG
        border_col = glow_color if is_hover else BORDER_CYAN

        pygame.draw.rect(screen, card_col, btn_rect, border_radius=18)
        pygame.draw.rect(screen, border_col, btn_rect, width=4, border_radius=18)

        start_x = btn_rect.x + 14
        for ic in icons:
            if icon_surfaces.get(ic):
                screen.blit(icon_surfaces.get(ic), (start_x, btn_rect.y + (btn_rect.height - ICON_SIZE) // 2))
                start_x += ICON_SIZE + 8

        txt_start = start_x + 10
        b_title = font_btn_title.render(name, True, TEXT_WHITE)
        b_val = font_btn_val.render(label, True, TEXT_CYAN)

        screen.blit(b_title, (txt_start, btn_rect.y + 8))
        screen.blit(b_val, (txt_start, btn_rect.y + 38))

        arrow_x = btn_rect.right - 22
        arrow_y = btn_rect.y + (btn_rect.height // 2)
        pygame.draw.line(screen, border_col, (arrow_x - 10, arrow_y - 8), (arrow_x, arrow_y), 4)
        pygame.draw.line(screen, border_col, (arrow_x - 10, arrow_y + 8), (arrow_x, arrow_y), 4)

    # ৭. ফুটার (বর্ডার ও বক্স মোটা করা হয়েছে)
    follow_y = int(HEIGHT * 0.88)
    f_btn = font_subtitle.render("Follow Me", True, TEXT_CYAN)
    
    pygame.draw.line(screen, BORDER_CYAN, (int(WIDTH * 0.12), follow_y + 14), (center_x - 70, follow_y + 14), 3)
    pygame.draw.line(screen, BORDER_CYAN, (center_x + 70, follow_y + 14), (int(WIDTH * 0.88), follow_y + 14), 3)

    f_box = pygame.Rect(center_x - 65, follow_y - 2, 130, 32)
    pygame.draw.rect(screen, CARD_BG, f_box, border_radius=16)
    pygame.draw.rect(screen, glow_color, f_box, width=4, border_radius=16)
    screen.blit(f_btn, (center_x - (f_btn.get_width() // 2), follow_y + 2))

    ic_keys = ["wa", "tt", "fb", "yt"]
    total_w = len(ic_keys) * (ICON_SIZE + 12)
    ic_start_x = center_x - (total_w // 2) + 6

    for idx, k in enumerate(ic_keys):
        ix = ic_start_x + (idx * (ICON_SIZE + 12))
        iy = follow_y + 40
        if icon_surfaces.get(k):
            screen.blit(icon_surfaces.get(k), (ix, iy))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
