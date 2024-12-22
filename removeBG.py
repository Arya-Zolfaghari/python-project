from rembg import remove
from PIL import Image


input_path = "C:/Users/Arya/OneDrive/Dokumente/python/image/1000011800.jpg"
output_path = "father.png"


input = Image.open(input_path)
output = remove(input)
output.save(output_path)



