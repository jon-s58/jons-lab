#!/usr/bin/env python3
"""Clean and vectorize the Jon's Lab logo.

Pipeline:
  1. Load the source PNG and threshold to a binary "ink" mask.
  2. Drop small connected components (kills the Gemini watermark).
  3. Tight-crop to the remaining ink with a small padding.
  4. Emit a transparent PNG (raster fallback).
  5. Run `potrace` on a clean PBM to produce the vector SVG.
  6. Post-process the SVG: use currentColor and add a viewBox-only sizing
     so CSS controls color and dimensions.

Re-run anytime by editing knobs near the top and running:
    python3 scripts/process_logo.py
"""

import re
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

# --- Config -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "jons-lab-logo.png"
STATIC = ROOT / "static"
STATIC.mkdir(exist_ok=True)

INK_THRESHOLD = 180          # gray < this = ink
MAJOR_COMPONENT_SIZE = 500   # blobs this big define the shield's region
NOISE_FLOOR = 4              # drop pure noise components below this size
BBOX_MARGIN = 8              # slack around the shield bbox in pixels
PAD = 24                     # cropping padding in pixels
TURDSIZE = 8                 # potrace: ignore tiny specks (lower = more detail)
ALPHAMAX = 1.0               # potrace: corner smoothness (0..1.34)
OPTTOLERANCE = 0.4           # potrace: curve simplification

# --- 1. Load + threshold ---------------------------------------------------
print(f"reading {SRC.name}")
gray = np.array(Image.open(SRC).convert("L"))
ink = gray < INK_THRESHOLD
print(f"  size: {gray.shape}  ink pixels: {ink.sum():,}")

# --- 2. Spatial filter: keep everything inside the shield's region ---------
# Strategy: use the *major* components (large enough to be part of the main
# linework) to define a spatial bounding box. Then keep every non-noise
# component whose center falls inside that bbox. This preserves small wood-
# grain curves and short circuit traces while dropping anything in the
# corners (e.g. the Gemini watermark).
labels, n = ndimage.label(ink)
sizes = ndimage.sum(ink, labels, index=np.arange(n + 1))
slices = ndimage.find_objects(labels)

major_ids = [i for i in range(1, n + 1) if sizes[i] >= MAJOR_COMPONENT_SIZE]
if not major_ids:
    raise SystemExit("no major components found — lower MAJOR_COMPONENT_SIZE")

main_y0 = min(slices[i - 1][0].start for i in major_ids) - BBOX_MARGIN
main_y1 = max(slices[i - 1][0].stop  for i in major_ids) + BBOX_MARGIN
main_x0 = min(slices[i - 1][1].start for i in major_ids) - BBOX_MARGIN
main_x1 = max(slices[i - 1][1].stop  for i in major_ids) + BBOX_MARGIN

keep = np.zeros(n + 1, dtype=bool)
for i in range(1, n + 1):
    sl = slices[i - 1]
    if sl is None or sizes[i] < NOISE_FLOOR:
        continue
    cy = (sl[0].start + sl[0].stop) // 2
    cx = (sl[1].start + sl[1].stop) // 2
    if main_y0 <= cy <= main_y1 and main_x0 <= cx <= main_x1:
        keep[i] = True

mask = keep[labels]
removed = n - int(keep.sum())
print(f"  components: {n}  kept: {int(keep.sum())}  removed: {removed}  "
      f"(major: {len(major_ids)})")
print(f"  shield bbox: y[{main_y0}:{main_y1}] x[{main_x0}:{main_x1}]")

# --- 3. Crop to bounding box -----------------------------------------------
ys, xs = np.where(mask)
y0 = max(0, ys.min() - PAD)
y1 = min(mask.shape[0], ys.max() + 1 + PAD)
x0 = max(0, xs.min() - PAD)
x1 = min(mask.shape[1], xs.max() + 1 + PAD)
mask_c = mask[y0:y1, x0:x1]
gray_c = gray[y0:y1, x0:x1]
print(f"  cropped to: {mask_c.shape}")

# --- 4. Transparent PNG fallback -------------------------------------------
# Anti-aliased edges from the original grayscale, masked by the kept blobs.
h, w = gray_c.shape
INK_RGB = (54, 36, 18)  # warm dark brown
rgba = np.zeros((h, w, 4), dtype=np.uint8)
rgba[..., 0] = INK_RGB[0]
rgba[..., 1] = INK_RGB[1]
rgba[..., 2] = INK_RGB[2]
alpha = (255 - gray_c).astype(np.uint8)
alpha[~mask_c] = 0
rgba[..., 3] = alpha
png_out = STATIC / "logo.png"
Image.fromarray(rgba, "RGBA").save(png_out, optimize=True)
print(f"  wrote {png_out.relative_to(ROOT)}")

# --- 5. Vectorize via potrace ----------------------------------------------
pbm_path = ROOT / "_logo_temp.pbm"
# Pillow mode "1": 0 = black ink, 255 = white background
binary_img = Image.fromarray(((~mask_c).astype(np.uint8)) * 255, mode="L").convert("1")
binary_img.save(pbm_path)

svg_out = STATIC / "logo.svg"
subprocess.run(
    [
        "potrace",
        "-s",
        "-o", str(svg_out),
        "--turdsize", str(TURDSIZE),
        "--alphamax", str(ALPHAMAX),
        "--opttolerance", str(OPTTOLERANCE),
        str(pbm_path),
    ],
    check=True,
)
pbm_path.unlink()
print(f"  wrote {svg_out.relative_to(ROOT)}")

# --- 6. Post-process SVG ----------------------------------------------------
# - swap hardcoded fill #000000 -> currentColor so CSS controls color
# - drop fixed width/height so the viewBox handles sizing
# - strip the XML declaration, DOCTYPE, and metadata so it can be inlined
#   directly into HTML (Zola will load_data this file)
svg = svg_out.read_text()
svg = svg.replace('fill="#000000"', 'fill="currentColor"')
svg = re.sub(r'\swidth="[^"]+"', "", svg, count=1)
svg = re.sub(r'\sheight="[^"]+"', "", svg, count=1)
svg = re.sub(r"<\?xml[^?]*\?>\s*", "", svg)
svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg)
svg = re.sub(r"<metadata>.*?</metadata>\s*", "", svg, flags=re.DOTALL)
svg_out.write_text(svg.strip() + "\n")
print("  post-processed svg (currentColor, viewBox-only, inline-safe)")

print("done.")
