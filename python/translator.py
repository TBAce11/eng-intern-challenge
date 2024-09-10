import sys

braille_to_english = {
    'O.....': 'a', 'O.O...': 'b', 'OO....': 'c', 'OO.O..': 'd', 'O..O..': 'e',
    'OOO...': 'f', 'OOOO..': 'g', 'O.OO..': 'h', '.OO...': 'i', '.OOO..': 'j',
    'O...O.': 'k', 'O.O.O.': 'l', 'OO..O.': 'm', 'OO.OO.': 'n', 'O..OO.': 'o',
    'OOO.O.': 'p', 'OOOOO.': 'q', 'O.OOO.': 'r', '.OO.O.': 's', '.OOOO.': 't',
    'O...OO': 'u', 'O.O.OO': 'v', '.OOO.O': 'w', 'OO..OO': 'x', 'OO.OOO': 'y',
    'O..OOO': 'z', '......': ' ', '.....O': 'capital_follows', '.O...O': 'decimal_follows', '.O.OOO': 'number_follows',
    '..OO.O': '.', '..O...': ',', '..O.OO': '?', '..OOO.': '!', '..OO..': ':',
    'OO.O.O':';', '....OO':'-', '.O..O.':'/', '.OO..O':'<', 'OOO.OO':'>',  # Corrected '<' and '>' since they were overlapping with other characters
    'O.O..O':'(', '.O.OO.':')'
}

english_to_braille = {v: k for k, v in braille_to_english.items()}

numbers = {
    'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5',
    'f': '6', 'g': '7', 'h': '8', 'i': '9', 'j': '0'
}

def braille_to_text(braille):
    result = []
    i = 0
    capitalize_next = False
    number_mode = False

    while i < len(braille):
        char = braille[i:i+6]
        if char == '.....O':
            capitalize_next = True
        elif char == '.O.OOO':
            number_mode = True
        elif char == '.O...O' and number_mode:
            result.append('.') 
        elif char in braille_to_english:
            letter = braille_to_english[char]
            if letter in ['capital_follows', 'number_follows', 'decimal_follows']:
                pass  
            elif number_mode and letter in numbers:
                result.append(numbers[letter])
            else:
                if capitalize_next:
                    letter = letter.upper()
                    capitalize_next = False
                result.append(letter)
                number_mode = False

        i += 6 

    return ''.join(result)

def text_to_braille(text):
    result = []
    number_mode = False

    for char in text:
        if char.isdigit():
            if not number_mode:
                result.append(english_to_braille['number_follows'])
                number_mode = True
            result.append(english_to_braille[list(numbers.keys())[list(numbers.values()).index(char)]])
        elif char == '.' and number_mode:
            result.append(english_to_braille['decimal_follows'])
        else:
            if number_mode:
                number_mode = False
            if char.isupper():
                result.append(english_to_braille['capital_follows'])
                char = char.lower()
            result.append(english_to_braille.get(char.lower(), ''))

    return ''.join(result)

def translate(input_string):
    if set(input_string).issubset({'O', '.'}):
        return braille_to_text(input_string)
    else:
        return text_to_braille(input_string)

if __name__ == "__main__":
    input_string = ' '.join(sys.argv[1:])
    print(translate(input_string))
