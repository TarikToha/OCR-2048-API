# 2048 OCR API

## Overview

FastAPI backend that detects the 2048 game board from a screenshot, segments it, and uses Tesseract OCR to extract tile
values.

## Features

- `/ocr` endpoint accepts screenshot uploads.
- Detects and crops board area.
- Splits into 16 tiles (4×4).
- Preprocesses each tile for OCR.
- Multithreaded OCR with Tesseract.
- Returns 4×4 board as JSON.

## Stack

- Python 3.10+
- FastAPI, OpenCV, Pillow, pytesseract, NumPy
- Tesseract OCR

## API

### `POST /ocr`

**Input:**

- `image`: screenshot (form-data)

**Output:**

```json
{
  "board": [
    [
      2,
      4,
      4,
      8
    ],
    [
      32,
      16,
      4,
      2
    ],
    [
      2,
      64,
      16,
      4
    ],
    [
      32,
      8,
      4,
      2
    ]
  ]
}
```

**Error Example:**

```json
{
  "error": "⚠️ Board not found in the image!"
}
```

## Run

```bash
pip install -r requirements.txt
uvicorn ocr_api:app --reload
```

## Notes

- Requires Tesseract installed in system PATH.
- Accuracy depends on image clarity.
- Uses digit whitelist and `--psm 10` mode.

## License

MIT
