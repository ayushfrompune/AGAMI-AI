import keyboard
import subprocess

def execute_function():
    subprocess.run(["python", "/Users/macbookpro/PycharmProjects/OPENAi_TRIAL1/Siri_Animation.py"])

# Define the shortcut
shortcut = "space+A"  # Change this to your preferred key combination

#print(f"Listening for the shortcut: {shortcut}")
# Add a listener for the shortcut
keyboard.add_hotkey(shortcut, execute_function)

# Keep the script running
keyboard.wait()  # This will keep the program alive until you stop it manually
