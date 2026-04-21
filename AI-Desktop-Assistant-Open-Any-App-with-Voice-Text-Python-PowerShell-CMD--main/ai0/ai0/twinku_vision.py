import os
import datetime
import pyautogui
from PIL import Image
import google.generativeai as genai

_vision_model = None

def init_vision_system(api_key: str):
    global _vision_model
    genai.configure(api_key=api_key)
    # Utilize high speed gemini-2.5-flash suitable for image tasks.
    _vision_model = genai.GenerativeModel('gemini-2.5-flash')

def _capture_screen(save_screenshot=False) -> Image.Image:
    # Captures current primary monitor
    screenshot = pyautogui.screenshot()
    
    # Optional logic to save the screenshot if the boss wants physical proof
    if save_screenshot:
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/twinku_capture_{timestamp}.png"
        screenshot.save(filename)
        print(f"📸 Screenshot saved to {filename}")
        
    return screenshot

def analyze_screen(query: str, save_screenshot=False) -> str:
    """Answers a question about the current screen."""
    if not _vision_model:
        return "[Vision Error: Vision model not initialized. Tell the Boss.]"
    
    print("📸 Twinku is looking at the screen...")
    img = _capture_screen(save_screenshot)
    
    try:
        response = _vision_model.generate_content([query, img])
        return response.text
    except Exception as e:
        return f"[Vision API Error: Failed to analyze screen: {str(e)}]"

def detect_errors_on_screen() -> dict:
    """Scans screen solely for visible error dialogs, crashes, or stacktraces."""
    if not _vision_model:
        return {"has_error": False, "message": "[Vision Error: Vision model not initialized.]"}
    
    print("📸 Twinku is scanning for errors...")
    img = _capture_screen(False)
    
    prompt = (
        "Scan this screen carefully. Is there an error dialog, exception stacktrace, warning message, "
        "or crash notification visible? If yes, start your response with 'YES:' followed by what the error is "
        "and a brief suggestion on how to fix it. If no error is visible at all, reply exactly with 'NO.'."
    )
    
    try:
        response = _vision_model.generate_content([prompt, img])
        text = response.text.strip()
        if text.upper().startswith("YES:"):
            return {"has_error": True, "message": text[4:].strip()}
        return {"has_error": False, "message": ""}
    except Exception as e:
        return {"has_error": False, "message": f"[Vision API Error: {str(e)}]"}

def read_text_on_screen() -> str:
    """Extracts raw text currently visible on the screen."""
    if not _vision_model:
        return "[Vision Error: Vision model not initialized.]"
    
    print("📸 Twinku is reading text from the screen...")
    img = _capture_screen(False)
    prompt = "Perform OCR on this screenshot. Return all the visible text logically. Do not describe the GUI or colors, just extract the text."
    
    try:
        response = _vision_model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"[Vision API Error: {str(e)}]"
