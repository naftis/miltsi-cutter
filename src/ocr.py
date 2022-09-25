from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import webcolors
import math
import os
import re
import json

rgb_code_dictionary = {
    (240, 167, 0): "orange",
    (0, 58, 140): "blue",
    (112, 208, 0): "green"
}

tolerance = 3000  # if different frames


def distance(c1, c2):
    (r1, g1, b1) = c1
    (r2, g2, b2) = c2

    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def get_closest_color(point):
    colors = list(rgb_code_dictionary.keys())
    closest_colors = sorted(colors, key=lambda color: distance(color, point))
    closest_color = closest_colors[0]
    code = rgb_code_dictionary[closest_color]
    return code


def find_dominant_color(image):
    pixels = image.getcolors(image.size[0] * image.size[1])
    sorted_pixels = sorted(pixels, key=lambda t: t[0])
    dominant_color = sorted_pixels[-1][1]
    return get_closest_color(dominant_color)


def resize_to_half(image):
    w, h = image.size
    resized = image.resize((round(w), round(h)))
    return resized


def parse_integer_from_string(my_string):
    return int(''.join(filter(str.isdigit, my_string)))


def is_a_question(sentence):
    has_spaces = " " in sentence
    is_not_spam = sentence.count("\n") < 3
    is_lengthy = len(sentence) > 10

    is_preliminary_question = has_spaces and len(
        sentence) > 20 and is_not_spam
    is_question = "?" in sentence and has_spaces and len(
        sentence) > 10 and is_not_spam

    return is_preliminary_question or is_question


def is_normal_question(question):
    return "?" in question


def parse_question_text(text):
    return re.sub(r"\?([\s\S]+)", "?", text)


def clearify_image(image):
    grayscale = image.convert("L")
    blackandwhite = grayscale.point(lambda x: 0 if x < 200 else 255, '1')
    return blackandwhite


def parse_frames(input):
    is_active_call_a_friend = False
    interesting_frames = []

    for filename in sorted(os.listdir(input), key=parse_integer_from_string):
        print(filename)
        if not filename.endswith(".png"):
            continue

        image = Image.open(input + filename)
        w, h = image.size

        question = resize_to_half(image.crop(
            (332, 692, w - 332, h - 110 - 170)))
        question = clearify_image(question)

        call_a_friend = resize_to_half(
            image.crop((1155, 100, 1155 + 410, 100 + 50)))
        call_a_friend = clearify_image(call_a_friend)

        question_text = parse_question_text(
            pytesseract.image_to_string(question, lang="fin"))
        is_question_presented = is_a_question(question_text)

        if is_question_presented:
            a = resize_to_half(image.crop((384, 818, 384 + 521, 818 + 66)))
            b = resize_to_half(image.crop((1061, 818, 1061 + 521, 818 + 66)))
            c = resize_to_half(image.crop((384, 904, 384 + 521, 904 + 66)))
            d = resize_to_half(image.crop((1061, 904, 1061 + 521, 904 + 66)))
            (a, b, c, d) = map(lambda option: clearify_image(option), (a, b, c, d))
            (a_text, b_text, c_text, d_text) = map(
                lambda image: pytesseract.image_to_string(image, lang="fin"), (a, b, c, d))
            (a_color, b_color, c_color, d_color) = map(
                lambda image: find_dominant_color(image), (a, b, c, d))

        call_a_friend = pytesseract.image_to_string(call_a_friend, lang="fin")
        if call_a_friend == "Kilauta kaverille":
            is_active_call_a_friend = True

        if is_question_presented and [a_color, b_color, c_color, d_color].count("blue") < 4:
            is_active_call_a_friend = False

        is_recordable_tick = is_active_call_a_friend or is_question_presented
        interesting_frames.append({
            "filename": filename,
            "is_recordable_tick": is_recordable_tick,
            "is_normal_question": is_normal_question(question_text)
        })

    interesting_frames.sort(
        key=lambda i: parse_integer_from_string(i["filename"]))

    with open('output.txt', 'w') as f:
        f.write("%s\n" % json.dumps(interesting_frames))
