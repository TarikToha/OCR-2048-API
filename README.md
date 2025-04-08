# 🧩 2048 OCR API

A full-stack app to extract 4×4 tile values from 2048 game screenshots using OpenCV and Tesseract. It includes a
web-based frontend and a FastAPI backend.

---

## 🌟 Features

- Upload 2048 screenshots via browser
- Backend detects and crops the board
- OCR performed using Tesseract
- Clean 4×4 grid output with logs

---

## 🗂️ Files

```
.
├── index.html         # Frontend UI
├── ocr_api.py         # FastAPI backend
├── requirements.txt   # Python packages
```

---

## 📸 Example

<table>
  <tr>
    <td><strong>Input</strong></td>
    <td><strong>Output</strong></td>
  </tr>
  <tr>
    <td><img src="screencaps/screenshot265.png" width="150"></td>
    <td valign="top">
      <pre><code>
🧩 OCR 2048 Board:
   2   4   4   8
  32  16   4   2
   2  64  16   4
  32   8   4   2
      </code></pre>
    </td>
  </tr>
</table>

---

## 🚀 Run Locally

### Backend

```bash
pip install -r requirements.txt
uvicorn ocr_api:app --reload
```

### Frontend

```bash
python -m http.server
```

Then open `index.html` in your browser.

---

## 📄 License

MIT © 2024
