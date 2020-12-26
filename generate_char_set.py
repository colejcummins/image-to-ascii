from PIL import Image, ImageDraw, ImageFont
from os import system
from sys import argv

def main():
  if len(argv) > 2:
    print("usage: generate_char_set.py <-a>")

  char_arr = create_font_mappings(argv[1:])
  write_char_set(char_arr)


#
# List[Str] -> List[(Str, Float)]
#
# Creates a list of ascii characters in a specified set ordered based on their apparent brightness
#
def create_font_mappings(args):
  fnt = ImageFont.truetype('./resources/CONSOLA.TTF', 28)

  char_arr = []
  for i in range(32, 127):
    if '-a' not in args and chr(i).isalnum():
      continue
    create_font_image(i, fnt)
    char_arr.append(read_font_image(i))

  char_arr.sort(key=lambda v: v[1])
  system('rm font.png')

  return char_arr


#
# Int, FreeTypeFont -> None
#
# Creates an image containing a single character corresponding to the ascii value in the given font
#
def create_font_image(ascii_val, font):
  img = Image.new('RGB', (30, 30), color=(0, 0, 0))

  d = ImageDraw.Draw(img)
  d.text((2, 2), chr(ascii_val), font=font, fill=(255, 255, 255))

  img.save('font.png')


#
# Int -> (Str, Float)
#
# Reads in an image containing a single character of the given ascii value, outputs a tuple with the corresponding
# character and apparent brightness
#
def read_font_image(ascii_val):
  img = Image.open('font.png')

  pixel_array = img.load()

  total_val = 0
  for i in range(img.size[0]):
    for j in range(img.size[1]):
      total_val += sum(pixel_array[i, j])

  return (chr(ascii_val), round((total_val/(img.size[0] * img.size[1]))/3, 3))


#
# List[(Str, Float)] -> None
#
# Writes a set of 255 characters to a text file corresponding to all possible intensity values, ordered by apparent
# brightness
#
def write_char_set(char_arr):
  mod = 255/char_arr[-1][1]

  output = []
  for i in range(0, 256):
    output.append(closest_char(char_arr, i/mod))

  with open('./resources/char_set.txt', 'w') as out_file:
    out_file.write('\n'.join(output))


#
# List[(Str, Float)], Int -> Str
#
# Finds the closest character in the given character set to the given intensity
#
def closest_char(chars, intensity):
  saved = chars[-1]
  for char in chars:
    if abs(intensity - char[1]) < abs(intensity - saved[1]):
      saved = char
  return saved[0]

if __name__ == '__main__':
  main()
