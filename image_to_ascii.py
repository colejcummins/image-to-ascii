from PIL import Image
from sys import argv


def main():
  if len(argv) < 2:
    print('usage: image_to_ascii.py <input_image> [<compression>] [<-s> <-l>]')

  input_image = Image.open(argv[1])
  compression = int(argv[2]) if len(argv) > 2 else 12

  output = get_output_chars(input_image, compression, argv[1:])

  with open("out.txt", "w") as f:
    f.write(output)


#
# Image, Int -> Str
#
# Returns a string of output characters corresponding to the given input image and level of compression
#
def get_output_chars(input_image, compression, args):
  pixel_array = input_image.load()
  output = ''

  with open("./resources/char_set.txt", "r") as char_file:
    char_list = char_file.read().split('\n')

  for i in range(0, input_image.size[1], compression):
    for j in range(0, input_image.size[0], int(compression/2)):
      if '-s' in args:
        block_sum = compress_block(i, j, compression, input_image.size, pixel_array)
      else:
        block_sum = int(pixel_sum(pixel_array[j, i]) / 3)
      print(pixel_array[j, i])
      print(block_sum)
      output += char_list[(-1 if '-l' in args else 1) * block_sum]

    output += '\n'

  return output


#
# Int, Int, Int, (Int, Int), PixelAccess -> Int
#
# Compresses a single block of pixels to one pixel value
#
def compress_block(i, j, compression, size, pixel_array):
  block_sum = 0

  for k in range(i, i + compression):
    for l in range(j, j + compression):
      if k < size[1] and l < size[0]:
        block_sum += pixel_sum(pixel_array[l, k])
      else:
        block_sum += pixel_sum(pixel_array[j, i])

  return int(block_sum / (compression * compression * 3))


#
# (Int, Int, Int, [Int]) -> Float
#
# Sums up a single pixel's RGB values
#
def pixel_sum(pixel):
  return (pixel[0] + pixel[1] + pixel[2]) * ((pixel[3]/255) if len(pixel) > 3 else 1)


if __name__ == "__main__":
  main()
