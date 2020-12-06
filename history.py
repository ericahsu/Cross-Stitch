# Erica Hsu, 12/4/2020

# Creates the outline of the history.csv file that will hold the patterns that 
# have already been created.

import pandas as pd

OriginalImage = []
PixelatedImage = []
Full = []
Center = []
Favorites = []

df = pd.DataFrame(list(zip(OriginalImage, PixelatedImage, Full, Center, Favorites)),\
    columns = ['Original Image', 'Pixelated Image', 'Full Photo', 'Centered', 'Favorites'])

df.to_csv('history.csv')
