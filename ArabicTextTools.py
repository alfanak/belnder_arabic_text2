import bpy
import os


text_buffer = []

current_char_index = 0


# Arabic letters list

arabic_chars = ['ا', 'أ', 'إ', 'آ', 'ء', 'ب', 'ت', 'ث', 'ج',
                'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص',
                'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل',
                'م', 'ن', 'ه', 'ة', 'و', 'ؤ', 'ي', 'ى', 'ئ', 'ـ']


# Arabic letters that need to be connected to the letter preceding them

right_connectable_chars = ['ا', 'أ', 'إ', 'آ', 'ب', 'ت', 'ث', 'ج', 'ح',
                           'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض',
                           'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م',
                           'ن', 'ه', 'ة', 'و', 'ؤ', 'ي', 'ى', 'ئ', 'ـ']


# Arabic letters that need to be connected to the letter next to them

left_connectable_chars = ['ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'س', 'ش', 'ص',
                          'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل',
                          'م', 'ن', 'ه', 'ي', 'ى', 'ئ', 'ـ']


# Locations (unicode) of Arabic letters shapes (when they are connected to other letters)

#                          ا       أ       إ       آ       ء       ب       ت       ث       ج
chars_variants_bases = [0xFE8D, 0xFE83, 0xFE87, 0xFE81, 0xFE80, 0xFE8F, 0xFE95, 0xFE99, 0xFE9D,
#                          ح       خ       د       ذ       ر       ز       س       ش       ص
                        0xFEA1, 0xFEA5, 0xFEA9, 0xFEAB, 0xFEAD, 0xFEAF, 0xFEB1, 0xFEB5, 0xFEB9,
#                          ض       ط       ظ       ع       غ       ف       ق       ك       ل
                        0xFEBD, 0xFEC1, 0xFEC1, 0xFEC9, 0xFECD, 0xFED1, 0xFED5, 0xFED9, 0xFEDD,
#                          م       ن       ه       ة       و       ؤ       ي       ى       ئ
                        0xFEE1, 0xFEE5, 0xFEE9, 0xFE93, 0xFEED, 0xFE85, 0xFEF1, 0xFEEF, 0xFE89]

chars_arabic_symbols = ['ـ', '،', '؟', '×', '÷']
chars_common = [' ', '.', ',', ':', '|', '(', ')', '[', ']', '{', '}', '!', '+', '-', '*', '/', '\\', '%', '"', '\'', '>', '<', '=', '~', '_']
chars_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# Check if a letter should be connected to the letter preceding it

def is_right_connectable(c):

    if c in right_connectable_chars:

        return True

    return False


# Check if a letter should be connected to the letter next to it

def is_left_connectable(c):

    if c in left_connectable_chars:

        return True

    return False


# Index of an Arabic letter in the list above

def get_char_index(c):

    if c not in arabic_chars:   # not an arabic char

        return -1

    return arabic_chars.index(c)


# Get the location (unicode id) of an Arabic letter shapes (when connected)

def get_char_variants_base(c):

    char_index = get_char_index(c)

    if char_index == -1:   # It's not an arabic char

        return -1

    return chars_variants_bases[char_index]


#

def is_arabic_char(c):

    if c in arabic_chars:

        return True

    return False


# Arabic char variants are located at 0xFE70 to  0xFEFE on unicode fonts.

def is_arabic_char_variant(c):

    if ord(c) >= 0xFE70 and ord(c) <= 0xFEFE:
        return True

    return False


# Get the previous character from a buffer or text array

def get_previous_alphabet(index, text):

    index -= 1

    while index > 0 and (text[index] in chars_common or text[index] in chars_digits or text[index] in chars_arabic_symbols):
        index -= 1

    if index >= 0:
        return text[index]
    else:
        return None


# Get the next character from a buffer or text array

def get_next_alphabet(index, text):

    index += 1

    while index < len(text) and (text[index] in chars_common or text[index] in chars_digits or text[index] in chars_arabic_symbols):
        index += 1

    if index < len(text):
        return text[index]
    else:
        return None


# Link Arabic letters

def link_text(unlinked_text):

    #

    linked_text = []

    previous_char = ""

    next_char = ""

    char_code = 0

    skip_char = False

    # When the letter "Alef" is connected to the letter "Lem" they become one letter
    # but the buffer still contains the two

    uncounted_chars = 0

    #

    for current_char in unlinked_text:

        #

        if skip_char:
            skip_char = False
            continue

        #

        previous_char = ""
        next_char = ""

        #

        chars_count = len(linked_text) + uncounted_chars

        if chars_count > 0:
            previous_char = unlinked_text[chars_count - 1]

        if chars_count < len(unlinked_text) - 1:
            next_char = unlinked_text[chars_count + 1]

        # Lem-Alef
        # Tehere are four forms of this letter

        if current_char == 'ل':

            if next_char == 'ا':

                char_code = 0xFEFB

            elif next_char == 'أ':

                char_code = 0xFEF7

            elif next_char == 'إ':

                char_code = 0xFEF9

            elif next_char == 'آ':

                char_code = 0xFEF5

            else:

                char_code = 0

            if char_code != 0:

                if is_left_connectable(previous_char):

                    char_code += 1

                linked_text.insert(0, chr(char_code))

                uncounted_chars += 1

                skip_char = True

                continue
        
        #

        if current_char in chars_arabic_symbols:

            linked_text.insert(0, current_char)

            continue

        if current_char == '\n':

            linked_text.insert(0, current_char)

            continue

        # Common characters follows the direction of the previous text (RTL or LTR)

        if current_char in chars_common:
            
            previous_alpha = get_previous_alphabet(chars_count, unlinked_text)
            next_alpha = get_next_alphabet(chars_count, unlinked_text)
            
            char_pos = 0

            if not is_arabic_char(previous_alpha) and not is_arabic_char(next_alpha) and previous_alpha != '\n':
                
                while char_pos < len(linked_text) and not is_arabic_char_variant(linked_text[char_pos]) and linked_text[char_pos] != '\n':
                    char_pos += 1
            
            linked_text.insert(char_pos, current_char)

            continue

        # Other letters

        char_code = get_char_variants_base(current_char)
        
        if char_code == -1:   # = Not an arabic character

            # Do not reverse non-arabic characters

            previous_alpha = get_previous_alphabet(chars_count, unlinked_text)
            next_alpha = get_next_alphabet(chars_count, unlinked_text)

            char_pos = 0

            # Numbers

            if len(linked_text) > 0 and linked_text[0] in chars_digits:

                while char_pos < len(linked_text) and linked_text[char_pos] in chars_digits:
                    char_pos +=1
            
            # Non-Arabic alhpabet

            elif not is_arabic_char(previous_alpha):

                c = chars_count - 1

                while not is_arabic_char(previous_alpha) and char_pos < len(linked_text) and linked_text[char_pos] != '\n':

                    previous_alpha = get_previous_alphabet(c, unlinked_text)
                    char_pos += 1
                    c -= 1

            linked_text.insert(char_pos, current_char)

            continue

        # It's an Arabic alhpabet

        if is_left_connectable(previous_char) and is_right_connectable(current_char):

            if is_left_connectable(current_char) and is_right_connectable(next_char):

                char_code += 3

            else:

                char_code += 1
        else:

            if is_left_connectable(current_char) and is_right_connectable(next_char):

                char_code += 2

        linked_text.insert(0, chr(char_code))

    text = ''.join(linked_text)

    return text


# swap lines

# When we reverse the order of our characters (to show arabic text correctly), we will get our lines of text swaped
# so we have to swap our text lines back to make it shown correctly

def swap_lines(linked_text):

    new_text = []

    current_line_start = 0

    char_counter = 0

    for c in reversed(linked_text):

        if(c == '\n'):

            new_text.append('\n')

            current_line_start = char_counter + 1

            char_counter += 1

            continue

        new_text.insert(current_line_start, c)

        char_counter += 1

    return ''.join(new_text)


# Unlink Arabic text (get the original text before it gets connected)

def unlink_text(linked_text):

    #

    unlinked_text = []

    #

    for c in linked_text:

        if ord(c) in {0xFE8D, 0xFE8E}:

            unlinked_text.insert(0, 'ا')

        elif ord(c) in {0xFE83, 0xFE84}:

            unlinked_text.insert(0, 'أ')

        elif ord(c) in {0xFE87, 0xFE88}:

            unlinked_text.insert(0, 'إ')

        elif ord(c) in {0xFE81, 0xFE82}:

            unlinked_text.insert(0, 'آ')

        elif ord(c) in {0xFE80}:

            unlinked_text.insert(0, 'ء')

        elif ord(c) in {0xFE8F, 0xFE90, 0xFE91, 0xFE92}:

            unlinked_text.insert(0, 'ب')

        elif ord(c) in {0xFE95, 0xFE96, 0xFE97, 0xFE98}:

            unlinked_text.insert(0, 'ت')

        elif ord(c) in {0xFE99, 0xFE9A, 0xFE9B, 0xFE9C}:

            unlinked_text.insert(0, 'ث')

        elif ord(c) in {0xFE9D, 0xFE9E, 0xFE9F, 0xFEA0}:

            unlinked_text.insert(0, 'ج')

        elif ord(c) in {0xFEA1, 0xFEA2, 0xFEA3, 0xFEA4}:

            unlinked_text.insert(0, 'ح')

        elif ord(c) in {0xFEA5, 0xFEA6, 0xFEA7, 0xFEA8}:

            unlinked_text.insert(0, 'خ')

        elif ord(c) in {0xFEA9, 0xFEAA}:

            unlinked_text.insert(0, 'د')

        elif ord(c) in {0xFEAB, 0xFEAC}:

            unlinked_text.insert(0, 'ذ')

        elif ord(c) in {0xFEAD, 0xFEAE}:
            unlinked_text.insert(0, 'ر')

        elif ord(c) in {0xFEAF, 0xFEB0}:

            unlinked_text.insert(0, 'ز')

        elif ord(c) in {0xFEB1, 0xFEB2, 0xFEB3, 0xFEB4}:

            unlinked_text.insert(0, 'س')

        elif ord(c) in {0xFEB5, 0xFEB6, 0xFEB7, 0xFEB8}:

            unlinked_text.insert(0, 'ش')

        elif ord(c) in {0xFEB9, 0xFEBA, 0xFEBB, 0xFEBC}:

            unlinked_text.insert(0, 'ص')

        elif ord(c) in {0xFEBD, 0xFEBE, 0xFEBF, 0xFEC0}:

            unlinked_text.insert(0, 'ض')

        elif ord(c) in {0xFEC1, 0xFEC2, 0xFEC3, 0xFEC4}:

            unlinked_text.insert(0, 'ط')

        elif ord(c) in {0xFEC5, 0xFEC6, 0xFEC7, 0xFEC8}:

            unlinked_text.insert(0, 'ظ')

        elif ord(c) in {0xFEC9, 0xFECA, 0xFECB, 0xFECC}:

            unlinked_text.insert(0, 'ع')

        elif ord(c) in {0xFECD, 0xFECE, 0xFECF, 0xFED0}:

            unlinked_text.insert(0, 'غ')

        elif ord(c) in {0xFED1, 0xFED2, 0xFED3, 0xFED4}:

            unlinked_text.insert(0, 'ف')

        elif ord(c) in {0xFED5, 0xFED6, 0xFED7, 0xFED8}:

            unlinked_text.insert(0, 'ق')

        elif ord(c) in {0xFED9, 0xFEDA, 0xFEDB, 0xFEDC}:

            unlinked_text.insert(0, 'ك')

        elif ord(c) in {0xFEDD, 0xFEDE, 0xFEDF, 0xFEE0}:

            unlinked_text.insert(0, 'ل')

        elif ord(c) in {0xFEE1, 0xFEE2, 0xFEE3, 0xFEE4}:

            unlinked_text.insert(0, 'م')

        elif ord(c) in {0xFEE5, 0xFEE6, 0xFEE7, 0xFEE8}:

            unlinked_text.insert(0, 'ن')

        elif ord(c) in {0xFEE9, 0xFEEA, 0xFEEB, 0xFEEC}:

            unlinked_text.insert(0, 'ه')

        elif ord(c) in {0xFE93, 0xFE94}:

            unlinked_text.insert(0, 'ة')

        elif ord(c) in {0xFEED, 0xFEEE}:

            unlinked_text.insert(0, 'و')

        elif ord(c) in {0xFE85, 0xFE86}:

            unlinked_text.insert(0, 'ؤ')

        elif ord(c) in {0xFEF1, 0xFEF2, 0xFEF3, 0xFEF4}:

            unlinked_text.insert(0, 'ي')

        elif ord(c) in {0xFEEF, 0xFEF0}:

            unlinked_text.insert(0, 'ى')

        elif ord(c) in {0xFE89, 0xFE8A, 0xFE8B, 0xFE8C}:

            unlinked_text.insert(0, 'ئ')

        elif ord(c) in {0xFEFB, 0xFEFC}:

            unlinked_text.insert(0, 'ا')
            unlinked_text.insert(0, 'ل')

        elif ord(c) in {0xFEF7, 0xFEF8}:

            unlinked_text.insert(0, 'أ')
            unlinked_text.insert(0, 'ل')

        elif ord(c) in {0xFEF9, 0xFEFA}:

            unlinked_text.insert(0, 'إ')
            unlinked_text.insert(0, 'ل')

        elif ord(c) in {0xFEF5, 0xFEF6}:

            unlinked_text.insert(0, 'آ')
            unlinked_text.insert(0, 'ل')

        # Other characters

        else:

            unlinked_text.insert(0, c)

    return unlinked_text


# Prepare our text (3D text, text_buffer)

def init():

    global current_char_index
    global text_buffer

    if bpy.context.object is None or bpy.context.object.type != 'FONT' or bpy.context.object.mode != 'EDIT':

        return
    
    text_buffer = swap_lines(bpy.context.object.data.body)
    text_buffer = unlink_text(text_buffer)
    
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    new_font = os.path.join(addon_dir, "bmonofont-i18n.ttf")
    
    if os.path.exists(new_font):
        bpy.context.object.data.font = bpy.data.fonts.load(new_font, check_existing=True)    

    bpy.context.object.data.align_x = 'RIGHT'
    
    current_char_index = 0
    
    update_visual_cursor_position()


#

def update_text():
    
    global text_buffer
    global current_char_index
    
    linked_text = link_text(text_buffer)
    linked_text = swap_lines(linked_text)
    
    bpy.ops.font.select_all()
    bpy.ops.font.delete()
    bpy.ops.font.text_insert(text=linked_text)
    
    update_visual_cursor_position()
    

# Add a new character

def insert_text(char):
    
    global text_buffer
    global current_char_index
    
    text_buffer.insert(current_char_index, char)
    
    current_char_index += 1
    
    update_text()
    

# Move the cursor (well, our pointer) to the previous char/position

def move_previous():
    
    global current_char_index
    
    if current_char_index > 0:

        current_char_index -= 1
    
        # update_text()
    
    update_visual_cursor_position()


# Move the cursor/pointer to the next char/position

def move_next():
    
    global text_buffer
    global current_char_index
    
    if current_char_index < len(text_buffer):
        
        current_char_index += 1
        
        # update_text()
        
    update_visual_cursor_position()


# Move the cursor/pointer to the start of the current line

def move_line_start():
    
    global text_buffer
    global current_char_index
    
    while current_char_index > 0:
        
        current_char_index -= 1
        
        if text_buffer[current_char_index] == '\n':
            
            current_char_index += 1

            break
        
    update_visual_cursor_position()


# Move the cursor/pointer to the end of the current line

def move_line_end():
    
    global text_buffer
    global current_char_index
    
    while current_char_index < len(text_buffer):
        
        if text_buffer[current_char_index] == '\n':
            
            break
        
        current_char_index += 1
        
    update_visual_cursor_position()


# Move the cursor/pointer to the previous line

def move_up():
    
    global text_buffer
    global current_char_index
    
    line_start = get_line_start()
    line_offset = current_char_index - line_start
    
    previous_line_end = line_start - 2
    
    previous_line_start = get_line_start(previous_line_end)
    
    previous_line_size = previous_line_end - previous_line_start
    
    new_index = previous_line_start + min(line_offset, previous_line_size + 1)
    
    if is_valid_char_index(new_index):
        
        current_char_index = new_index
        update_visual_cursor_position()


# Move the cursor/pointer to the next line

def move_down():
    
    global text_buffer
    global current_char_index
    
    new_line_size = 0
    
    line_start = get_line_start()
    line_offset = current_char_index - line_start
    
    new_index = get_next_line_start()
    
    if new_index == -1:
    
        return
    
    for i in range(line_offset):
        
        if not is_valid_char_index(new_index):
        
            break
        
        if text_buffer[new_index] == '\n':
        
            break
        
        new_index += 1
        
    if is_valid_char_index(new_index) or new_index == len(text_buffer):
        
        current_char_index = new_index
        update_visual_cursor_position()


# Delete the previous character

def delete_previous():
    
    global current_char_index
    
    if current_char_index > 0:
        
        text_buffer.pop(current_char_index - 1)
        
        current_char_index -= 1
        
        update_text()


# Delete the next character

def delete_next():
    
    global text_buffer
    global current_char_index
    
    if is_valid_char_index(current_char_index):
        
        del(text_buffer[current_char_index])
        
        update_text()


#

def get_line_start(index=-1):
    
    global text_buffer
    global current_char_index
    
    line_start = current_char_index if index == - 1 else index
    
    while line_start > 0:
        
        line_start -= 1
        
        if text_buffer[line_start] == '\n':

            line_start += 1
            
            break
        
    return line_start


#

def get_next_line_start():
    
    global text_buffer
    global current_char_index
    
    next_line_start = current_char_index
    
    while next_line_start < len(text_buffer):
        
        if text_buffer[next_line_start] == '\n':

            next_line_start += 1
            
            break
        
        next_line_start += 1
        
        if next_line_start == len(text_buffer):
        
            return -1
        
    return next_line_start


#


def is_valid_char_index(index):
    
    if len(text_buffer) > 0 and index >= 0 and index < len(text_buffer):
    
        return True
    
    return False


# Make the visual cursor follow our pointer

def update_visual_cursor_position():
    
    global text_buffer
    global current_char_index

    # Move visual cursor to the begining of the text
    
    for i in range(len(text_buffer)):
    
        bpy.ops.font.move(type='PREVIOUS_CHARACTER')
    
    #
    
    current_line_start = get_line_start()
    
    for i in range(current_line_start):

        if text_buffer[i] == '\n':
        
            bpy.ops.font.move(type='NEXT_LINE')
    
    # NOTE: we can do this in another way, without moving the cursor to the and of the line and then bring it back
    # we can just count the length of the current line and move the cursor forward:
    # (line_length - current_line_offset(= current_char_index - line_start)) times
    
    bpy.ops.font.move(type='LINE_END')
    
    for i in range(current_line_start, current_char_index):
        
        # Do not count "Lem-Alef" as two letters
        
        if text_buffer[i] in {'ا', 'أ', 'إ', 'آ'}:
            
            if i > 0 and text_buffer[i - 1] == 'ل':
                
                continue
            
        bpy.ops.font.move(type='PREVIOUS_CHARACTER')

