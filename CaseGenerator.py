from glob import glob
import os
import random
import unicodedata
import xml.etree.ElementTree as ET

COLORS = {"red" : "#FF0000", "green" : "#00FF00", "blue" : "#0000FF", "yellow" : "#FFFF00", "cyan" : "#00FFFF", "magenta" : "#FF00FF", "white" : "#FFFFFF", "black" : "#000000"}
ET.register_namespace("", "http://www.w3.org/2000/svg")

def get_existing_colors(original: str) -> tuple[set, ET.Element]:
  '''
  Lists all the colors set in the `fill` attribute of the input SVG code as a set together with the root element of the SVG.
  '''
  S = set()

  root = ET.fromstring(original)
  assert root.tag[-3:] == "svg"
  for e in root.iter():
    if "fill" in e.attrib:
      S.add(e.attrib["fill"])
  return S, root

def output_to_file(n: str, output_folder: str, original: str, query: str, answer: str):
  '''
  Outputs the prompt and the answer image to the appropriate path.
  '''
  os.makedirs(f"{output_folder}/query/", exist_ok=True)
  os.makedirs(f"{output_folder}/answer/", exist_ok=True)
  with open(f"{output_folder}/query/{n}.txt", "w") as q:
    q.write(query + "\n\n```svg\n" + original + "\n```\n\nPlease respond in the following format. Only return the SVG code. \n\n```svg\n<svg>...</svg>\n```")
  with open(f"{output_folder}/answer/{n}.svg", "w") as a:
    a.write(answer)

def change_color(original: str, n: str, name: str):
  '''
  Generates cases for the Change Color task.
  '''
  S, _ = get_existing_colors(original)
  color_from = random.choice(list(S))
  color_to = random.choice(list(COLORS))

  output_to_file(n, "cases/1_ChangeColor", original, f"The following code is the SVG code for the emoji '{name.lower()}'. Please generate an SVG code that changes the part of the emoji with a {color_from} color to {color_to}.", original_content.replace(color_from, color_to))

def set_contour(original: str, n: str, name: str, width: int):
  '''
  Generates cases for the Set Contour task.
  '''
  S, root = get_existing_colors(original)
  area_color = random.choice(list(S))

  for e in root.iter():
    if "fill" in e.attrib and e.attrib["fill"] == area_color:
      e.attrib["stroke"] = "black"
      e.attrib["stroke-width"] = str(width)
  output_to_file(n, "cases/2_SetContour", original, f"The following code is the SVG code for the emoji '{name.lower()}'. Please generate an SVG code that draws a black line around the part of the emoji with a {area_color} color.", ET.tostring(root, encoding='unicode'))

def compression(original: str, n: str, name: str):
  '''
  Generates cases for the Compression task. Note that the answer image is the same as the original.
  '''
  output_to_file(n, "cases/3_Compression", original, f"The following code is the SVG code for the emoji '{name.lower()}'. Please generate a more compact SVG code that represents the same emoji.", original)

def up_side_down(original: str, n: str, name: str):
  '''
  Generates cases for the Upside-Down task.
  '''
  _, root = get_existing_colors(original)

  assert root.attrib["viewBox"] == "0 0 36 36"
  
  root.attrib["transform"] = "translate(0,36) scale(1,-1)"
  output_to_file(n, "cases/4_UpSideDown", original, f"The following code is the SVG code for the emoji '{name.lower()}'. Please flip this emoji upside down.", ET.tostring(root, encoding='unicode'))

def transparency(original: str, n: str, name: str):
  '''
  Generates cases for the Transparency task.
  '''
  _, root = get_existing_colors(original)

  root.attrib["opacity"] = "0.5"
  output_to_file(n, "cases/5_Transparency", original, f"The following code is the SVG code for the emoji '{name.lower()}'. Please make this emoji transparent by half.", ET.tostring(root, encoding='unicode'))

def crop_to_half(original: str, n: str, name: str):
  '''
  Generates cases for the Crop to Half task.
  '''
  _, root = get_existing_colors(original)

  assert root.attrib["viewBox"] == "0 0 36 36"
  root.attrib["viewBox"] = "0 0 18 36"
  output_to_file(n, "cases/6_CropToHalf", original, f"The following code is the SVG code for the emoji '{name.lower()}'. Please trim the right half and keep the left half.", ET.tostring(root, encoding='unicode'))

l = glob("twemoji/assets/svg/*.svg")
random.shuffle(l)
count = 0
os.makedirs("cases",exist_ok=True)

for f in l:
  n = os.path.basename(f).split(".")[0]
  if "-" in n:
    continue # Skip zwj sequences
  c = int(n, 16)
  if 0x1f1e6 <= c <= 0x1f1ff:
    continue # Skip regional indicator symbols
  try:
    name = unicodedata.name(chr(c))
  except ValueError:
    continue # Skip unnamed characters

  count += 1

  with open(f) as original:
    original_content = original.read()

  change_color(original_content, n, name)
  set_contour(original_content, n, name, 1)
  compression(original_content, n, name)
  up_side_down(original_content, n, name)
  transparency(original_content, n, name)
  crop_to_half(original_content, n, name)

  if count >= 100:
    break