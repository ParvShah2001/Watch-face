# Dial Layout, PCD Geometry & Complications

## Coordinate System & PCD Geometry

The canvas is defined on a standard **$450 \times 450$ px** circular canvas with center $(C_x, C_y) = (225, 225)$.

### 4-Complication Pitch Circle Diameter (PCD) Alignment

All 4 complication slots are aligned on an exact **Pitch Circle Diameter (PCD) of $276\text{ px}$** ($R_{\text{PCD}} = 138\text{ px}$) symmetrically spaced at **$45^\circ$ diagonal angles** from the cardinal axes:

$$\theta \in \{45^\circ, 135^\circ, 225^\circ, 315^\circ\}$$

$$\text{Slot Center } (X, Y) = (225 + 138 \cdot \cos\theta,\; 225 + 138 \cdot \sin\theta)$$

| Slot ID | Position | Angle ($\theta$) | Center $(X, Y)$ | Box $(x, y, w, h)$ | Default Provider |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Slot 1** | Top-Left | $225^\circ$ (NW) | $(127, 127)$ | `x="88" y="88" w="78" h="78"` | Watch Battery (`WATCH_BATTERY`) |
| **Slot 2** | Top-Right | $315^\circ$ (NE) | $(323, 127)$ | `x="284" y="88" w="78" h="78"` | Steps / Activity |
| **Slot 3** | Bottom-Left | $135^\circ$ (SW) | $(127, 323)$ | `x="88" y="284" w="78" h="78"` | Heart Rate / Health |
| **Slot 4** | Bottom-Right | $45^\circ$ (SE) | $(323, 323)$ | `x="284" y="284" w="78" h="78"` | Weather / Date |

This placement guarantees:
- Complete optical symmetry on round Wear OS displays.
- Zero collision with the central digital clock typography (`y = 182..268`).
- Clearance for both analog hands reaching the outer dial rim.

---

## Dual Analog & Digital Hand System

### 1. Central Digital Clock & AM/PM Tag
- **Font**: Google Sans Bold, `size="76"`.
- **Docking**: Centered at $(X, Y) = (204, 225)$ with right-docked AM/PM badge (`size="24"`).
- **Format**: 12-hour format (`format="hh:mm"`).

### 2. Peripheral Analog Hands Architecture
The analog indicators are rendered at the outer perimeter:
- **Hour Hand**: Features an opaque, high-contrast `"H"` emblem positioned along its inner body.
- **Minute Hand**: Extends to the outer bezel rim and displays a distinct `"M"` indicator.
- **Overlap Visibility**: When the hour and minute hands overlap (e.g. at 12:00:00), the hands are layered such that the `"M"` emblem remains fully visible beyond the hour hand tip.
- **Sweeping Seconds Dot**: A smooth 15 Hz sweeping indicator (`<Sweep frequency="15" />`) positioned on the dial track. A user configuration option (`showSeconds`) allows toggling this indicator on or off.

---

## Sprite Sequence Specs

Animations are rendered as smooth loop walk cycles placed below the digital clock at `x="169" y="266" w="112" h="112"`:

| Character | Walk Cycle Frames | Frame Rate | Ambient Silhouette |
| :--- | :---: | :---: | :---: |
| **Mickey Mouse** | 10 frames (`mickey_walk_0..9`) | 10 fps | `mickey_aod.png` |
| **Doraemon** | 8 frames (`doraemon_walk_0..7`) | 10 fps | `doraemon_aod.png` |
| **Shin-chan** | 7 frames (`shinchan_walk_0..6`) | 10 fps | `shinchan_aod.png` |
| **Pikachu** | 4 frames (`pikachu_walk_0..3`) | 8 fps | `pikachu_aod.png` |
| **Goku** | 12 frames (`goku_walk_0..11`) | 12 fps | `goku_aod.png` |
| **Oggy** | 18 frames (`oggy_walk_0..17`) | 12 fps | `oggy_aod.png` |

---

## Color Theme Palette

The watch face provides 7 selectable two-tone color themes dynamically applied to complication arcs, digits, and analog hand accents:

| Theme ID | Name | Primary Accent | Secondary / Background |
| :--- | :--- | :---: | :---: |
| `amber` (Default) | Amber Warmth | `#FFFFA726` | `#FFFFCC80` |
| `lime` | Electric Lime | `#FFD4E157` | `#FFE6EE9C` |
| `coral` | Sunset Coral | `#FFFF7043` | `#FFFFAB91` |
| `teal` | Deep Ocean Teal | `#FF26A69A` | `#FF80CBC4` |
| `lavender` | Royal Lavender | `#FFAB47BC` | `#FFCE93D8` |
| `mint` | Fresh Mint | `#FF66BB6A` | `#FFA5D6A7` |
| `white` | Monochrome White | `#FFE0E0E0` | `#FF9E9E9E` |
