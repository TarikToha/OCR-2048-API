from threading import Thread

import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageOps, ImageFilter
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS for frontend support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Core Functions ---
def load_and_crop_board_from_array(img_array: np.ndarray) -> Image.Image:
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        aspect = w / h
        if 0.85 < aspect < 1.15 and w * h > 30000:
            candidates.append((x, y, w, h))

    if not candidates:
        raise ValueError("⚠️ Board not found in the image!")

    x, y, w, h = max(candidates, key=lambda b: b[2] * b[3])
    board = Image.fromarray(cv2.cvtColor(img_array[y:y + h, x:x + w], cv2.COLOR_BGR2RGB))
    return board


def split_into_tiles(board: Image.Image) -> list:
    tile_size = board.width // 4
    return [
        board.crop((c * tile_size, r * tile_size, (c + 1) * tile_size, (r + 1) * tile_size))
        for r in range(4) for c in range(4)
    ]


def remove_tile_border(tile: Image.Image, margin_ratio=0.15) -> Image.Image:
    w, h = tile.size
    return tile.crop((
        int(w * margin_ratio),
        int(h * margin_ratio),
        int(w * (1 - margin_ratio)),
        int(h * (1 - margin_ratio))
    ))


def preprocess_tile(tile: Image.Image) -> Image.Image:
    tile = tile.convert("L")
    tile = ImageOps.autocontrast(tile)
    tile = tile.point(lambda x: 255 if x > 150 else 0)
    if np.array(tile).mean() < 100:
        tile = ImageOps.invert(tile)
    tile = tile.filter(ImageFilter.MedianFilter(3))
    tile = remove_tile_border(tile)
    return tile


def ocr_tile(tile: Image.Image, val_idx: int, values: list):
    tile = preprocess_tile(tile)
    config = "--psm 10 -c tessedit_char_whitelist=0123456789"
    text = pytesseract.image_to_string(tile, config=config).strip()
    if text.isdigit():
        val = int(text)
        if val in [2 ** i for i in range(1, 12)] + [32, 128, 512]:
            values[val_idx] = val
            return
    values[val_idx] = 0


def ocr_board(tiles: list) -> np.ndarray:
    values = [-1] * 16
    threads = []
    for idx, tile in enumerate(tiles):
        t = Thread(target=ocr_tile, args=(tile, idx, values))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return np.array(values).reshape((4, 4))


# --- FastAPI Endpoint ---
@app.post("/ocr")
async def ocr_endpoint(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        img_array = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)

        board = load_and_crop_board_from_array(img_array)
        tiles = split_into_tiles(board)
        board_array = ocr_board(tiles)

        return {"board": board_array.tolist()}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
