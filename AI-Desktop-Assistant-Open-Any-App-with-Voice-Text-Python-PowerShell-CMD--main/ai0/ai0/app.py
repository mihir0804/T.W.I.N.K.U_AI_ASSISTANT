import subprocess
import os
import time
import webbrowser
import urllib.parse
import pywhatkit
from glob import glob
# ── App aliases ───────────────────────────────────────────
APP_ALIASES = {
    # Browsers
    "chrome":                "chrome",
    "google chrome":         "chrome",
    "firefox":               "firefox",
    "edge":                  "msedge",
    "microsoft edge":        "msedge",
    "brave":                 "brave",

    # System tools
    "notepad":               "notepad",
    "notepad++":             "notepad++",
    "calculator":            "calc",
    "calc":                  "calc",
    "cmd":                   "cmd",
    "command prompt":        "cmd",
    "terminal":              "wt",          # Windows Terminal
    "task manager":          "taskmgr",
    "file explorer":         "explorer",
    "explorer":              "explorer",
    "paint":                 "mspaint",
    "ms paint":              "mspaint",
    "wordpad":               "wordpad",
    "snipping tool":         "snippingtool",
    "control panel":         "control",
    "settings":              "ms-settings:",

    # Dev tools
    "vscode":                "code",
    "vs code":               "code",
    "visual studio code":    "code",
    "pycharm":               "pycharm64",
    "git bash":              "git bash",
    "postman":               "postman",

    # ✅ FIX: UWP Apps — inhe PowerShell se kholna padta hai
    # cmd /c start se ye nahi khulti thi — YAHI MAIN BUG THA
    "whatsapp":   "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
    "telegram":   "telegram",
    "discord":    "discord",
    "zoom":       "zoom",
    "teams":      "teams",
    "microsoft teams": "teams",
    "slack":      "slack",
    "spotify":    "shell:AppsFolder\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify",

    # Office
    "word":                  "winword",
    "microsoft word":        "winword",
    "excel":                 "excel",
    "microsoft excel":       "excel",
    "powerpoint":            "powerpnt",
    "microsoft powerpoint":  "powerpnt",
    "outlook":               "outlook",

    # Media
    "vlc":                   "vlc",
    "vlc media player":      "vlc",
    "obs":                   "obs64",
    "obs studio":            "obs64",
}

#UWP shell:path--- inhe power shell se kholna padta hai, direct cmd se nahi khulte
#UWP apps ke liye "shell:AppsFolder\\PackageFamilyName!App"
UWP_PREFIXES = ["shell:AppsFolder\\", "ms-settings:", "shell:"]

PS=r"C:\Windows\System32\windowsPowerShell\v1.0\powershell.exe"

def is_uwp(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in UWP_PREFIXES)

def open_app(app_name:str) -> str:
    name = app_name.lower().strip()

    # ✅ Custom handler for YouTube (Website)
    if "youtube" in name:
        webbrowser.open("https://www.youtube.com")
        return "Right away, Boss. Opening YouTube for you... ❤️"

    search = APP_ALIASES.get(name)
    if not search:
        for key, value in APP_ALIASES.items():
            if name in key or key in name:
                search = value
                break
    
    if not search:
        search = name
        
    print(f"opening: '{search}' (requested as '{app_name}')")
    
    if is_uwp(search):
        try:
            subprocess.Popen([PS, "-NoProfile", "-WindowStyle", "Hidden", "-Command", f"Start-Process '{search}'"], 
                             creationflags=subprocess.CREATE_NO_WINDOW)
            return f"Of course, Boss. Opening {app_name} for you right now... ❤️"
        except Exception as e:
            print("UWP method failed, trying direct launch...", e)

    try:
        subprocess.Popen(["cmd", "/c", "start", "", search], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
        return f"Of course, Boss. Opening {app_name} for you right now... ❤️"
    except Exception as e1:
        print("Direct launch failed, trying shell=True...", e1)
        try:
            subprocess.Popen(search, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            return f"Of course, Boss. Opening {app_name} for you right now... ❤️"
        except Exception as e2:
            print("All conventional methods failed...", e2)
            try:
                cmd = f"(Get-AppxPackage -Name *{search}*).PackageFamilyName"
                r = subprocess.run([PS, "-NoProfile", "-Command", cmd], capture_output=True, text=True, timeout=8)
                package_family = r.stdout.strip()
                if package_family:
                    cmd_app_id = f"(Get-AppxPackageManifest (Get-AppxPackage -Name '{package_family}')).Package.Applications.Application.Id"
                    r_id = subprocess.run([PS, "-NoProfile", "-Command", cmd_app_id], capture_output=True, text=True, timeout=5)
                    app_id = r_id.stdout.strip()
                    if app_id:
                        full_id = f"{package_family}!{app_id}"
                        subprocess.Popen([PS, "-NoProfile", "-WindowStyle", "Hidden", "-Command", f"Start-Process 'shell:AppsFolder\\{full_id}'"], 
                                         creationflags=subprocess.CREATE_NO_WINDOW)
                        return f"Of course, Boss. Opening {app_name} for you right now... ❤️"
            except Exception as e3:
                print("UWP lookup method failed...", e3)
            
            return f"I'm so sorry, Boss. I'm having a little trouble opening {app_name}. Is there something else I can do for you? ❤️"

# ✅ NEW FUNCTION: Play specific media on YouTube or Spotify
def play_media(query: str, platform: str = "youtube") -> str:
    if platform == "youtube":
        try:
            # playonyt dynamically automatically plays the most relevant video and opens it.
            pywhatkit.playonyt(query)
            return f"Playing {query} on YouTube right now, Boss... Enjoy. ❤️"
        except Exception as e:
            # Fallback
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            webbrowser.open(url)
            return f"Opening search results for {query} on YouTube, Boss... ❤️"
    elif platform == "spotify":
        # Launching Spotify search URI directly
        url = f"spotify:search:{urllib.parse.quote(query)}"
        try:
            os.system(f"start {url}")
        except Exception:
            # Fallback to web browser if desktop URI fails
            webbrowser.open(f"https://open.spotify.com/search/{urllib.parse.quote(query)}")
        return f"Searching for {query} on Spotify, Boss... ❤️"

# ✅ NEW FUNCTION: Send a WhatsApp Message
def send_whatsapp_message(message: str) -> str:
    # This will open WhatsApp desktop with the message pre-typed. 
    # The user just selects the contact and presses Enter.
    url = f"whatsapp://send?text={urllib.parse.quote(message)}"
    webbrowser.open(url)
    return "I have prepared the message, Boss. Just click on a contact to send it! ❤️"

if __name__ == "__main__":
    # Test cases
    print(open_app("notepad"))
    print(open_app("whatsapp"))
    print(open_app("youtube"))

# ── NEW ADVANCED LAPTOP CONTROL FUNCTIONS ─────────────────────────────────

def resolve_path(location_hint: str) -> str:
    """Helper to convert spoken language paths into actual file paths."""
    location_hint = location_hint.lower().strip()
    if location_hint in ["downloads", "download folder", "download"]:
        return os.path.join(os.path.expanduser("~"), "Downloads")
    elif location_hint in ["desktop", "desktop folder"]:
        return os.path.join(os.path.expanduser("~"), "Desktop")
    elif location_hint in ["documents", "document", "document folder"]:
        return os.path.join(os.path.expanduser("~"), "Documents")
    elif "c folder" in location_hint or "c drive" in location_hint or "c:" in location_hint:
        return "C:\\"
    elif "d folder" in location_hint or "d drive" in location_hint or "d:" in location_hint:
        return "D:\\"
    
    if os.path.exists(location_hint):
        return location_hint

    return os.path.expanduser("~")

def create_file(location_hint: str, filename: str, content: str = "") -> str:
    try:
        base_path = resolve_path(location_hint)
        full_path = os.path.join(base_path, filename)
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Created file at: {full_path}")
        return f"File '{filename}' has been created successfully at {base_path}, Boss! ❤️"
    except Exception as e:
        print(f"Error creating file: {e}")
        return f"I'm terribly sorry Boss, I couldn't create the file. I encountered an error. ❤️"

def create_folder(location_hint: str, foldername: str) -> str:
    try:
        base_path = resolve_path(location_hint)
        full_path = os.path.join(base_path, foldername)
        os.makedirs(full_path, exist_ok=True)
        
        print(f"Created folder at: {full_path}")
        return f"Folder '{foldername}' has been created successfully at {base_path}, Boss! ❤️"
    except Exception as e:
        print(f"Error creating folder: {e}")
        return f"I'm terribly sorry Boss, I couldn't create the folder. I encountered an error. ❤️"

def images_to_pdf(location_hint: str, output_pdf_name: str) -> str:
    try:
        base_path = resolve_path(location_hint)
        
        valid_extensions = ["*.png", "*.jpg", "*.jpeg", "*.webp", "*.bmp", "*.JPG", "*.PNG", "*.JPEG"]
        image_files = []
        for ext in valid_extensions:
            image_files.extend(glob(os.path.join(base_path, ext)))
            
        image_files = list(set(image_files))
        
        if not image_files:
            return f"I couldn't find any images in {base_path}, Boss. Are you sure they are there? ❤️"
        
        image_files.sort(key=os.path.getctime)
        
        from PIL import Image
        
        images = []
        first_image = None
        
        for img_path in image_files:
            try:
                img = Image.open(img_path).convert('RGB')
                if first_image is None:
                    first_image = img
                else:
                    images.append(img)
            except Exception as e:
                print(f"Failed to process {img_path}: {e}")
                
        if not first_image:
            return "I couldn't process the images into a PDF, Boss."
            
        if not output_pdf_name.lower().endswith(".pdf"):
            output_pdf_name += ".pdf"
            
        output_path = os.path.join(base_path, output_pdf_name)
        
        if images:
            first_image.save(output_path, save_all=True, append_images=images)
        else:
            first_image.save(output_path)
            
        print(f"Generated PDF at: {output_path}")
        return f"I've magically combined your images into '{output_pdf_name}' and saved it to {base_path}, Boss! ❤️"
    except ImportError:
        return "Boss, I need the 'Pillow' library to do this. Please install it first using 'pip install pillow'."
    except Exception as e:
        print(f"Error making PDF: {e}")
        return f"I ran into a problem making the PDF, Boss. Are the images corrupted? ❤️"