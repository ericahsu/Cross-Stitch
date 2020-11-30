from PIL import Image

# Open Paddington
img = Image.open("testImage2.gif")

# Resize smoothly down to 16x16 pixels
imgSmall = img.resize((100, 100),resample=Image.BILINEAR)

# Scale back up using NEAREST to original size
result = imgSmall.resize(img.size,Image.NEAREST)

# Save
result.save('result.png')