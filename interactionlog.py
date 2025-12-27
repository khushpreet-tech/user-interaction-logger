from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import threading
import pyautogui
import imageio
import numpy as np
import time

def screen_rec():

    # Output file
    output_file = "screen_record.mp4"

    # Frames per second
    fps = 10  # 10 frames per second

    # Initialize writer
    writer = imageio.get_writer(output_file, fps=fps)

    print("Recording started.")

    try:
        while True:
            # Take a screenshot
            screenshot = pyautogui.screenshot()

            # Convert to array
            frame = np.array(screenshot)

            # Append frame to video
            writer.append_data(frame)

            # Delay to match FPS
            time.sleep(1 / fps)

    except KeyboardInterrupt:
        print("Recording stopped.")
        writer.close()

def write_to_file(key):
    letter = str(key)
    letter = letter.replace("'", "")

    if letter == 'Key.space':
        letter = ' '
    if letter == 'Key.shift_r':
        letter = ''
    if letter == "Key.ctrl_l":
        letter = ""
    if letter == "Key.enter":
        letter = "\n"

    with open("log.txt", 'a') as f:
        f.write(letter)

def mouse_demo():
    m = Controller()
    print("Mouse demo: current position:", m.position)
    # Move to (10, 20)
    m.position = (10, 20)
    print("Moved mouse to:", m.position)
    # Move relative
    m.move(5, -5)
    print("Moved mouse relatively by (5, -5); now at:", m.position)
    # Click and scroll (demonstration)
    m.press(Button.left)
    m.release(Button.left)
    m.click(Button.left, 2)
    m.scroll(0, 2)
    print("Mouse demo finished.\n")

def on_move(x, y):
    # print a concise message (position only)
    print(f"Mouse moved to ({x:.0f}, {y:.0f})")

def on_click(x, y, button, pressed):
    action = "Pressed" if pressed else "Released"
    print(f"{action} {button} at ({x:.0f}, {y:.0f})")

def on_scroll(x, y, dx, dy):
    direction = "up" if dy > 0 else "down"
    print(f"Scrolled {direction} at ({x:.0f}, {y:.0f})")

def start_listeners(on_key_press=None):
    global keyboard_listener, mouse_listener
    keyboard_listener = keyboard.Listener(on_press=write_to_file)
    mouse_listener = mouse.Listener(on_move=on_move,
                                    on_click=on_click,
                                    on_scroll=on_scroll)

    # start both in non-blocking mode
    keyboard_listener.start()
    mouse_listener.start()

    # wait for both to finish (they stop when Esc pressed)
    keyboard_listener.join()
    mouse_listener.join()

if __name__ == "__main__":
    # Run a quick mouse controller demo in a thread so it doesn't block listeners
    demo_thread = threading.Thread(target=mouse_demo, daemon=True)
    demo_thread.start()
    demo_thread2 = threading.Thread(target=write_to_file , daemon = True)
    demo_thread2.start()
    screen_rec()

    print("Starting listeners. Press Esc to stop.")
    start_listeners()

    # Give a moment for demo thread to finish printing if needed
    time.sleep(0.2)
    print("Program exited.")
