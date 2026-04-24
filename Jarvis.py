import tkinter as tk
import os
import subprocess
import webbrowser
import urllib.parse
import urllib.request
import json
import threading
import tempfile
import sys

# Version information
CURRENT_VERSION = "1.0.0"
UPDATE_URL = "https://raw.githubusercontent.com/yourusername/jarvis/main/version.json"  # Replace with your actual update URL
UPDATE_DOWNLOAD_URL = "https://github.com/yourusername/jarvis/releases/latest/download/JarvisInstaller.exe"  # Replace with your actual download URL

def launch_program(program):
    program = program.strip().lower()
    if not program:
        return "Please say a program to open, like 'open notepad'."

    if program == "youtube":
        os.system("start https://youtube.com")
        return "Yes sir, opening YouTube. What are you in the mood to watch?"

    if program == "steam":
        steam_path = r"C:\Program Files (x86)\Steam\Steam.exe"
        if os.path.exists(steam_path):
            subprocess.Popen([steam_path])
            return "Yes sir, opening Steam. Have fun gaming!"
        return "Steam was not found in the default location. Make sure Steam is installed."

    if program == "spotify":
        spotify_path = r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe"
        spotify_path = os.path.expandvars(spotify_path)
        if os.path.exists(spotify_path):
            subprocess.Popen([spotify_path])
            return "Opening Spotify"
        return "Spotify was not found in the default location. Make sure Spotify is installed."

    if program == "discord":
        discord_path = r"C:\Users\%USERNAME%\AppData\Local\Discord\Update.exe"
        discord_path = os.path.expandvars(discord_path)
        if os.path.exists(discord_path):
            subprocess.Popen([discord_path, "--processStart", "Discord.exe"])
            return "Opening Discord"
        return "Discord was not found in the default location. Make sure Discord is installed."

    try:
        subprocess.Popen([program])
        return f"Opening {program.title()}"
    except FileNotFoundError:
        if os.path.exists(program):
            try:
                os.startfile(program)
                return f"Opening {program}"
            except OSError:
                return f"Found '{program}', but could not open it."
        return f"Could not find a program named '{program}'. Try 'open notepad', 'open calculator', 'open Steam', 'open Spotify', or 'open Discord'."


def normalize_text(text):
    return ''.join(ch for ch in text.lower() if ch.isalnum())


def get_steam_executable():
    steam_exe = r"C:\Program Files (x86)\Steam\Steam.exe"
    if os.path.exists(steam_exe):
        return steam_exe
    steam_exe = os.path.expanduser(r"~\AppData\Roaming\Steam\Steam.exe")
    if os.path.exists(steam_exe):
        return steam_exe
    return None


def get_steam_library_folders():
    steam_exe = get_steam_executable()
    if not steam_exe:
        return []

    steamapps = os.path.join(os.path.dirname(steam_exe), "steamapps")
    folders = [steamapps]
    library_file = os.path.join(steamapps, "libraryfolders.vdf")
    if os.path.exists(library_file):
        with open(library_file, encoding="utf-8", errors="ignore") as file:
            for line in file:
                parts = line.strip().split('"')
                if len(parts) >= 4 and parts[1].isdigit():
                    folder = parts[3]
                    if os.path.isdir(os.path.join(folder, "steamapps")):
                        folders.append(os.path.join(folder, "steamapps"))
    return folders


def find_steam_game_appid(game_name):
    target_norm = normalize_text(game_name)
    best_match = None
    for steamapps in get_steam_library_folders():
        if not os.path.isdir(steamapps):
            continue
        for file_name in os.listdir(steamapps):
            if not (file_name.startswith("appmanifest_") and file_name.endswith(".acf")):
                continue
            manifest_path = os.path.join(steamapps, file_name)
            appid = None
            name = None
            with open(manifest_path, encoding="utf-8", errors="ignore") as manifest:
                for line in manifest:
                    if '"appid"' in line:
                        appid = line.split('"')[3].strip()
                    elif '"name"' in line:
                        name = line.split('"')[3].strip()
                    if appid and name:
                        break
            if appid and name:
                name_norm = normalize_text(name)
                if name_norm == target_norm:
                    return appid, name
                if target_norm in name_norm or name_norm in target_norm:
                    best_match = (appid, name)
    return best_match


def run_steam_game(game_name):
    app = find_steam_game_appid(game_name)
    if not app:
        return None
    appid, name = app
    steam_exe = get_steam_executable()
    if not steam_exe:
        return "Steam executable was not found. Please install Steam."
    try:
        subprocess.Popen([steam_exe, "-applaunch", appid])
        return f"Launching Steam game '{name}'"
    except Exception as err:
        return f"Failed to launch Steam game '{name}': {err}"


def parse_timer_duration(text):
    import re
    text = text.strip().lower()
    match = re.match(r'^(\d+(?:\.\d+)?)\s*(seconds|second|minutes|minute|hours|hour)$', text)
    if not match:
        return None
    value = float(match.group(1))
    unit = match.group(2)
    if unit.startswith('second'):
        return value
    if unit.startswith('minute'):
        return value * 60
    if unit.startswith('hour'):
        return value * 3600
    return None


def format_duration(seconds):
    if seconds < 60:
        return f"{int(seconds)} seconds"
    if seconds < 3600:
        minutes = seconds / 60
        return f"{int(minutes)} minutes"
    hours = seconds / 3600
    return f"{hours:.1f} hours"


def schedule_timer(duration_seconds, label=None):
    if duration_seconds is None or duration_seconds <= 0:
        return "Please specify a timer length like '5 seconds' or '25 minutes'."
    if duration_seconds > 86400:
        return "Timer is too long. Please set one for 24 hours or less."
    timer_label = label or format_duration(duration_seconds)

    search_query = urllib.parse.quote_plus(f"{timer_label} timer")
    webbrowser.open(f"https://www.google.com/search?q={search_query}")

    def timer_finished():
        display_message("Jarvis", f"Timer finished: {timer_label}")

    root.after(int(duration_seconds * 1000), timer_finished)
    return f"Timer set for {timer_label} and opened in your browser."

def check_for_updates():
    """Check if there's a newer version available."""
    try:
        with urllib.request.urlopen(UPDATE_URL, timeout=10) as response:
            data = json.loads(response.read().decode())
            latest_version = data.get('version', CURRENT_VERSION)
            
            if latest_version > CURRENT_VERSION:
                return True, latest_version, data.get('changelog', 'No changelog available')
            else:
                return False, CURRENT_VERSION, None
    except Exception as e:
        return False, CURRENT_VERSION, f"Error checking for updates: {str(e)}"

def download_update():
    """Download the latest installer."""
    try:
        display_message("Jarvis", "Downloading update...")
        
        with urllib.request.urlopen(UPDATE_DOWNLOAD_URL, timeout=30) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            
            # Create temporary file
            temp_dir = tempfile.gettempdir()
            installer_path = os.path.join(temp_dir, "Jarvis_Update.exe")
            
            with open(installer_path, 'wb') as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        progress = int((downloaded / total_size) * 100)
                        display_message("Jarvis", f"Download progress: {progress}%")
        
        return installer_path
    except Exception as e:
        display_message("Jarvis", f"Error downloading update: {str(e)}")
        return None

def install_update(installer_path):
    """Install the downloaded update."""
    try:
        display_message("Jarvis", "Installing update... Please wait.")
        
        # Run the installer silently
        subprocess.Popen([installer_path, '/SILENT', '/NORESTART'], 
                        creationflags=subprocess.CREATE_NO_WINDOW)
        
        display_message("Jarvis", "Update installed successfully! Please restart Jarvis to use the new version.")
        return True
    except Exception as e:
        display_message("Jarvis", f"Error installing update: {str(e)}")
        return False

def perform_update():
    """Complete update process."""
    def update_thread():
        try:
            # Check for updates
            has_update, latest_version, changelog = check_for_updates()
            
            if not has_update:
                display_message("Jarvis", f"You are already running the latest version ({CURRENT_VERSION}).")
                return
            
            display_message("Jarvis", f"New version available: {latest_version}")
            if changelog:
                display_message("Jarvis", f"Changelog: {changelog}")
            
            # Download update
            installer_path = download_update()
            if not installer_path:
                return
            
            # Install update
            if install_update(installer_path):
                display_message("Jarvis", "Update completed! The application will now close.")
                root.after(3000, root.quit)  # Close after 3 seconds
                
        except Exception as e:
            display_message("Jarvis", f"Update failed: {str(e)}")
    
    # Run update in background thread
    threading.Thread(target=update_thread, daemon=True).start()

# Create Window
root = tk.Tk()
root.title("Jarvis")
root.geometry("400x300")

# Chat Display
chat_log = tk.Text(root, state='disabled')
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_log.configure(takefocus=0)

# Input Box
entry = tk.Entry(root)
entry.pack(padx=10, pady=10, fill=tk.X)

def set_focus():
    entry.focus_set()
    entry.icursor(tk.END)

root.after(200, set_focus)

entry.bind("<Button-1>", lambda e: entry.focus_set())

# Function to display messages
def display_message(sender, message):
    chat_log.config(state='normal')
    chat_log.insert(tk.END, f"{sender}: {message}\n")
    chat_log.config(state='disabled')
    chat_log.see(tk.END)

# Basic Command Handler
def handle_command(command):
    command = command.lower()

    if command.startswith("create a timer for "):
        duration_text = command.split("create a timer for ", 1)[1]
        duration_seconds = parse_timer_duration(duration_text)
        return schedule_timer(duration_seconds, label=duration_text)

    if command.startswith("run "):
        target = command.split(" ", 1)[1]
        steam_result = run_steam_game(target)
        if steam_result is not None:
            return steam_result
        return launch_program(target)

    if command.startswith("open "):
        target = command.split(" ", 1)[1]
        return launch_program(target)

    if command in ["update", "update jarvis", "check for updates"]:
        perform_update()
        return "Checking for updates..."

    if command in ["version", "what version", "current version"]:
        return f"Current version: {CURRENT_VERSION}"

    return "I do not recognize that command. Try 'create a timer for 5 seconds', 'open notepad', 'open calculator', 'update', or 'version'."

# When user presses Enter
def on_enter(event):
    user_input = entry.get()
    entry.delete(0, tk.END)

    display_message("You", user_input)
    response = handle_command(user_input)
    display_message("Jarvis", response)
    entry.focus_set()

entry.bind("<Return>", on_enter)

# Check for updates on startup (in background)
def startup_update_check():
    def check_thread():
        try:
            has_update, latest_version, _ = check_for_updates()
            if has_update:
                display_message("Jarvis", f"Update available! Say 'update' to install version {latest_version}.")
        except:
            pass  # Silently fail on startup check
    
    threading.Thread(target=check_thread, daemon=True).start()

# Start update check after GUI is ready
root.after(2000, startup_update_check)  # Check 2 seconds after startup

root.mainloop()