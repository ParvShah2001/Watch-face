import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

res_dir = r'D:\watchface\CartoonWatchFace\app\src\main\res\drawable'
out_dir = r'D:\watchface\listing_assets'
art_dir = r'C:\Users\parvs\.gemini\antigravity\brain\e6bdb1ab-a11c-4db8-8305-376866d83e90'

os.makedirs(out_dir, exist_ok=True)
os.makedirs(art_dir, exist_ok=True)

# Fonts
font_title = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 54)
font_sub = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 28)
font_tag = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 18)
font_feat = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 22)
font_comp_val = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 20)
font_comp_lbl = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 13)
font_time = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 44)
font_ampm = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 20)
font_badge_text = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 20)

themes = {
    'amber': (255, 167, 38),
    'lime': (212, 225, 87),
    'coral': (255, 112, 67),
    'teal': (38, 166, 154),
    'lavender': (171, 71, 188),
    'mint': (102, 187, 106),
    'white': (230, 230, 230)
}

def render_dial(char_name='mickey', theme_name='amber', is_ambient=False, hour_deg=304, min_deg=48.8, sec_deg=192, show_sec=True):
    size = 450
    center = (225, 225)
    img = Image.new('RGBA', (size, size), (0, 0, 0, 255))
    theme_rgb = themes.get(theme_name, (255, 167, 38))
    
    # 1. Bezel
    if not is_ambient:
        bezel = Image.open(os.path.join(res_dir, 'dial_bezel.png')).convert('RGBA')
        img.alpha_composite(bezel)
        
    # 2. Complications
    draw = ImageDraw.Draw(img)
    comps = [
        (127, 127, '92%', 'BATTERY'),
        (323, 127, '8.4K', 'STEPS'),
        (127, 323, '78', 'HEART'),
        (323, 323, '24°', 'WEATHER')
    ]
    for cx, cy, val, label in comps:
        r = 35
        if not is_ambient:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(20, 20, 24, 255), outline=(50, 50, 56, 255), width=2)
            draw.arc([cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3], start=215, end=430, fill=theme_rgb, width=3)
            draw.text((cx, cy - 8), val, font=font_comp_val, fill=(255, 255, 255, 255), anchor='mm')
            draw.text((cx, cy + 13), label, font=font_comp_lbl, fill=theme_rgb, anchor='mm')
        else:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 0, 0, 255), outline=(40, 40, 40, 255), width=1)
            draw.text((cx, cy - 8), val, font=font_comp_val, fill=(200, 200, 200, 255), anchor='mm')
            draw.text((cx, cy + 13), label, font=font_comp_lbl, fill=(150, 150, 150, 255), anchor='mm')

    # 3. Central Time
    draw.text((215, 222), '10:08', font=font_time, fill=(255, 255, 255, 255), anchor='rm')
    ampm_col = theme_rgb if not is_ambient else (255, 255, 255)
    draw.text((220, 222), 'AM', font=font_ampm, fill=ampm_col, anchor='lm')
    
    # 4. Character
    char_file = f'{char_name}_aod.png' if is_ambient else f'{char_name}_walk_0.png'
    char_path = os.path.join(res_dir, char_file)
    if os.path.exists(char_path):
        char_img = Image.open(char_path).convert('RGBA')
        char_img = char_img.resize((104, 104), Image.Resampling.LANCZOS)
        img.alpha_composite(char_img, (173, 255))
        
    # 5. Hands:
    if not is_ambient and show_sec:
        hs = Image.open(os.path.join(res_dir, 'hand_second.png')).convert('RGBA')
        hs_arr = hs.load()
        for y in range(size):
            for x in range(size):
                if hs_arr[x, y][3] > 0:
                    hs_arr[x, y] = (theme_rgb[0], theme_rgb[1], theme_rgb[2], hs_arr[x, y][3])
        hs_rot = hs.rotate(-sec_deg, center=center, resample=Image.Resampling.BICUBIC)
        img.alpha_composite(hs_rot)
        
    hm = Image.open(os.path.join(res_dir, 'hand_minute.png')).convert('RGBA')
    hm_rot = hm.rotate(-min_deg, center=center, resample=Image.Resampling.BICUBIC)
    img.alpha_composite(hm_rot)
    
    hh_body = Image.open(os.path.join(res_dir, 'hand_hour_body.png')).convert('RGBA')
    hh_b_arr = hh_body.load()
    h_col = theme_rgb if not is_ambient else (255, 255, 255)
    for y in range(size):
        for x in range(size):
            if hh_b_arr[x, y][3] > 0:
                hh_b_arr[x, y] = (h_col[0], h_col[1], h_col[2], hh_b_arr[x, y][3])
    hh_b_rot = hh_body.rotate(-hour_deg, center=center, resample=Image.Resampling.BICUBIC)
    img.alpha_composite(hh_b_rot)

    hh_text = Image.open(os.path.join(res_dir, 'hand_hour_text.png')).convert('RGBA')
    hh_t_rot = hh_text.rotate(-hour_deg, center=center, resample=Image.Resampling.BICUBIC)
    img.alpha_composite(hh_t_rot)
    
    return img

def create_mockup(dial_img):
    c_size = 650
    mcx, mcy = c_size // 2, c_size // 2
    mock = Image.new('RGBA', (c_size, c_size), (0, 0, 0, 0))
    d = ImageDraw.Draw(mock)
    
    # 1. Straps
    strap_w = 200
    strap_col = (25, 26, 30, 255)
    strap_border = (42, 44, 52, 255)
    d.rounded_rectangle([mcx - strap_w//2, 8, mcx + strap_w//2, 135], radius=10, fill=strap_col, outline=strap_border, width=2)
    d.rounded_rectangle([mcx - strap_w//2, c_size - 135, mcx + strap_w//2, c_size - 8], radius=10, fill=strap_col, outline=strap_border, width=2)
    
    # Strap texture ribs
    for ry in [35, 60, 85, 110]:
        d.line([(mcx - strap_w//2 + 15, ry), (mcx + strap_w//2 - 15, ry)], fill=(34, 36, 42, 255), width=2)
    for ry in [c_size - 110, c_size - 85, c_size - 60, c_size - 35]:
        d.line([(mcx - strap_w//2 + 15, ry), (mcx + strap_w//2 - 15, ry)], fill=(34, 36, 42, 255), width=2)

    # 2. Case Drop Shadow
    case_r = 252
    shadow = Image.new('RGBA', (c_size, c_size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([mcx - case_r - 6, mcy - case_r + 14, mcx + case_r + 6, mcy + case_r + 30], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    mock.alpha_composite(shadow)
    
    # 3. Outer Titanium Case
    d.ellipse([mcx - case_r, mcy - case_r, mcx + case_r, mcy + case_r], fill=(36, 38, 44, 255), outline=(78, 82, 94, 255), width=3)
    d.ellipse([mcx - case_r + 6, mcy - case_r + 6, mcx + case_r - 6, mcy + case_r - 6], fill=(18, 19, 22, 255), outline=(48, 50, 56, 255), width=2)
    
    # 4. Watch Crown Button
    crown_x = mcx + case_r - 4
    crown_y = mcy - 22
    d.rounded_rectangle([crown_x, crown_y, crown_x + 16, crown_y + 44], radius=5, fill=(58, 62, 72, 255), outline=(90, 95, 108, 255), width=2)

    # 5. Dial (resized to 472x472)
    dial_scaled = dial_img.resize((472, 472), Image.Resampling.LANCZOS)
    mask = Image.new('L', (472, 472), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, 472, 472], fill=255)
    mock.paste(dial_scaled, (mcx - 236, mcy - 236), mask)
    
    # 6. Glass Glare
    glare = Image.new('RGBA', (c_size, c_size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.arc([mcx - 234, mcy - 234, mcx + 234, mcy + 234], start=215, end=315, fill=(255, 255, 255, 55), width=4)
    mock.alpha_composite(glare)
    
    return mock

def create_play_card(mockup_img, tag, title, subtitle, theme_rgb):
    # 1080 x 1080 Play Store Card
    W, H = 1080, 1080
    card = Image.new('RGBA', (W, H), (12, 13, 16, 255))
    
    # 1. Subtle radial ambient glow behind watch
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gcx, gcy = W // 2, 640
    gr = 340
    # Gradient glow circles
    for r in range(gr, 0, -15):
        alpha = int(38 * (1.0 - r / gr))
        col = (theme_rgb[0], theme_rgb[1], theme_rgb[2], alpha)
        gd.ellipse([gcx - r, gcy - r, gcx + r, gcy + r], fill=col)
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    card.alpha_composite(glow)
    
    draw = ImageDraw.Draw(card)
    
    # 2. Header Text
    # Category Tag Badge
    tag_w = draw.textlength(tag, font=font_tag) + 32
    tag_h = 34
    tag_x = (W - tag_w) // 2
    tag_y = 65
    draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=17, fill=(24, 26, 32, 255), outline=theme_rgb, width=2)
    draw.text((W // 2, tag_y + tag_h // 2), tag, font=font_tag, fill=theme_rgb, anchor='mm')
    
    # Title
    draw.text((W // 2, 145), title, font=font_title, fill=(255, 255, 255, 255), anchor='mm')
    
    # Subtitle
    draw.text((W // 2, 205), subtitle, font=font_sub, fill=(180, 185, 195, 255), anchor='mm')
    
    # 3. Paste Smartwatch Mockup (scaled to 750x750)
    mock_scaled = mockup_img.resize((760, 760), Image.Resampling.LANCZOS)
    card.alpha_composite(mock_scaled, ((W - 760) // 2, 265))
    
    return card

# --- GENERATE ASSETS ---
print('Generating store assets...')

# 1. Seven Screenshots (1080x1080)
screenshots = [
    ('mickey', 'amber', False, 'CLASSIC ICON', 'MICKEY MOUSE', 'Smooth 15Hz Sweeping Seconds & Dual Tier Hands', 'screenshot_1_mickey.png'),
    ('doraemon', 'teal', False, 'ICONIC ANIME', 'DORAEMON', '4 Live Dynamic Complications with Progress Arcs', 'screenshot_2_doraemon.png'),
    ('pikachu', 'lime', False, 'FAN FAVORITE', 'PIKACHU', 'Hybrid Analog Rim with Sharp Digital Time', 'screenshot_3_pikachu.png'),
    ('goku', 'coral', False, 'SUPER SAIYAN', 'GOKU', 'Bold Typography & Vibrant Coral Color Theme', 'screenshot_4_goku.png'),
    ('shinchan', 'mint', False, 'CHEEKIEST HERO', 'SHIN-CHAN', 'Playful Animations & Crisp AMOLED Black Theme', 'screenshot_5_shinchan.png'),
    ('oggy', 'lavender', False, 'CARTOON LEGEND', 'OGGY', 'Full Wear OS 4 & 5 Native Format Compatibility', 'screenshot_6_oggy.png'),
    ('mickey', 'white', True, 'ALWAYS-ON DISPLAY', 'ULTRA BATTERY SAVER', 'Pure Black AMOLED Outlines for Maximum Efficiency', 'screenshot_7_aod.png')
]

for char, theme, aod, tag, title, sub, filename in screenshots:
    dial = render_dial(char_name=char, theme_name=theme, is_ambient=aod)
    mock = create_mockup(dial)
    card = create_play_card(mock, tag, title, sub, themes[theme])
    card.save(os.path.join(out_dir, filename))
    card.save(os.path.join(art_dir, filename))
    print(f'Generated {filename}')

# 2. App Icon (512x512)
def generate_app_icon():
    S = 512
    icon = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(icon)
    
    # Rounded squircle base
    d.rounded_rectangle([16, 16, S - 16, S - 16], radius=110, fill=(16, 17, 22, 255), outline=(45, 48, 58, 255), width=4)
    
    # Outer glowing bezel ring
    ring_r = 215
    cx, cy = S // 2, S // 2
    for r in range(ring_r, ring_r - 8, -1):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 167, 38, 255), width=2)
    
    # Dial inside
    dial = render_dial('mickey', 'amber', is_ambient=False, hour_deg=304, min_deg=48.8, sec_deg=192)
    dial_cropped = dial.resize((410, 410), Image.Resampling.LANCZOS)
    mask = Image.new('L', (410, 410), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, 410, 410], fill=255)
    icon.paste(dial_cropped, (cx - 205, cy - 205), mask)
    
    # Gloss highlight on top left
    gloss = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gloss)
    gd.arc([cx - 200, cy - 200, cx + 200, cy + 200], start=210, end=320, fill=(255, 255, 255, 75), width=6)
    icon.alpha_composite(gloss)
    
    icon.save(os.path.join(out_dir, 'icon_512.png'))
    icon.save(os.path.join(art_dir, 'icon_512.png'))
    print('Generated icon_512.png')

generate_app_icon()

# 3. Feature Graphic (1024x500)
def generate_feature_graphic():
    W, H = 1024, 500
    fg = Image.new('RGBA', (W, H), (14, 15, 19, 255))
    
    # Background subtle ambient glow
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([640, -100, 1150, 600], fill=(255, 167, 38, 45))
    gd.ellipse([750, 100, 1050, 450], fill=(255, 112, 67, 35))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    fg.alpha_composite(glow)
    
    draw = ImageDraw.Draw(fg)
    
    # Left Side: Typography & Badges
    # Wear OS pill
    draw.rounded_rectangle([60, 45, 250, 80], radius=17, fill=(24, 26, 34, 255), outline=(255, 167, 38, 255), width=2)
    draw.text((155, 62), 'WEAR OS WATCH', font=font_tag, fill=(255, 167, 38, 255), anchor='mm')
    
    # Main Title
    draw.text((60, 100), 'CARTOON', font=ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 62), fill=(255, 255, 255, 255))
    draw.text((60, 168), 'WATCH FACE', font=ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 48), fill=(255, 167, 38, 255))
    
    # Tagline
    draw.text((60, 240), 'Iconic Animated Classics on Your Smartwatch', font=font_sub, fill=(185, 190, 202, 255))
    
    # Feature Badges
    badges = [
        '6 Iconic Animated Characters',
        'Smooth 15Hz Sweeping Seconds',
        '4 Live Health & Weather Complications',
        'Ultra-Low Power AOD Ambient Mode'
    ]
    by = 296
    for b in badges:
        # Glowing bullet dot
        draw.ellipse([60, by + 7, 72, by + 19], fill=(255, 167, 38, 255))
        draw.text((82, by), b, font=font_feat, fill=(230, 235, 245, 255))
        by += 42
        
    # Right Side: Smartwatch Mockup
    dial = render_dial('mickey', 'amber', is_ambient=False, hour_deg=304, min_deg=48.8, sec_deg=192)
    mock = create_mockup(dial)
    mock_scaled = mock.resize((480, 480), Image.Resampling.LANCZOS)
    fg.alpha_composite(mock_scaled, (560, 10))
    
    # Flatten to RGB (Google Play requirement: no alpha)
    fg_rgb = Image.new('RGB', (W, H), (14, 15, 19))
    fg_rgb.paste(fg, mask=fg.split()[3])
    
    fg_rgb.save(os.path.join(out_dir, 'feature_graphic_1024x500.png'), quality=95)
    fg_rgb.save(os.path.join(art_dir, 'feature_graphic_1024x500.png'), quality=95)
    print('Generated feature_graphic_1024x500.png')

generate_feature_graphic()

# 4. Export Mipmap Icons for the App
icon_img = Image.open(os.path.join(out_dir, 'icon_512.png')).convert('RGBA')
mipmaps = {
    'mipmap-mdpi': 48,
    'mipmap-hdpi': 72,
    'mipmap-xhdpi': 96,
    'mipmap-xxhdpi': 144,
    'mipmap-xxxhdpi': 192
}
app_res = r'D:\watchface\CartoonWatchFace\app\src\main\res'
for m_dir, sz in mipmaps.items():
    t_dir = os.path.join(app_res, m_dir)
    os.makedirs(t_dir, exist_ok=True)
    scaled = icon_img.resize((sz, sz), Image.Resampling.LANCZOS)
    scaled.save(os.path.join(t_dir, 'ic_launcher.webp'), 'WEBP')
    scaled.save(os.path.join(t_dir, 'ic_launcher_round.webp'), 'WEBP')
print('Exported mipmap launcher icons!')
print('All listing assets successfully created!')
