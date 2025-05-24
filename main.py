import time
import keyboard
import win32clipboard
import win32con
from tendo import singleton
me = singleton.SingleInstance()

eng_to_rus = {
    'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ',
    'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', '\'': 'э',
    'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '/': '.',
    '`': 'ё',
    '@': '"', '#': '№', '$': ';', '^': ':', '&': '?'
}

rus_to_eng = {v: k for k, v in eng_to_rus.items()}

def convert_layout(text):
    result = []
    for ch in text:
        lower = ch.lower()
        if lower in eng_to_rus:
            converted = eng_to_rus[lower]
        elif lower in rus_to_eng:
            converted = rus_to_eng[lower]
        else:
            converted = ch

        if ch.isupper():
            converted = converted.upper()
        result.append(converted)
    return ''.join(result)

def get_clipboard_text():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
    except TypeError:
        data = ''
    win32clipboard.CloseClipboard()
    return data

def set_clipboard_text(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
    win32clipboard.CloseClipboard()

def simulate_ctrl_c():
    keyboard.press_and_release('ctrl+c')

def simulate_ctrl_v():
    keyboard.press_and_release('ctrl+v')

def on_hotkey():
    oldtext = get_clipboard_text()
    simulate_ctrl_c()
    time.sleep(0.1)

    text = get_clipboard_text()
    if not text or text == oldtext:
        return

    converted = convert_layout(text)
    if converted == text:
        return

    set_clipboard_text(converted)
    time.sleep(0.05)
    simulate_ctrl_v()

def main():
    keyboard.add_hotkey('ctrl+\'', on_hotkey)
    keyboard.wait()

if __name__ == '__main__':
    main()
