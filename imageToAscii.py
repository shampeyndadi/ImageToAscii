import PIL.Image
import shutil
from PIL import ImageEnhance, ImageFilter

# Reference(s): https://www.youtube.com/watch?v=v_raWlX7tZY

ASCII_CHARACTER = ["@", "*", "+", "#", "&", "%", "_", ":", "0", "/", "X"]

def resizeImage(image, new_width=100):
    width, height = image.size
    ratio = height / width
    newHeight = int(new_width * ratio * 0.55)
    resizedImage = image.resize((new_width, newHeight))
    return resizedImage

def grayifyImage(image):
    grayImage = image.convert("L")
    return(grayImage)

def applyContrast(image, factor=1.5):
    """Increase the contrast of the image by a given factor."""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def applyBlur(image, radius=2):
    """Apply a blur filter to reduce noise in the image."""
    return image.filter(ImageFilter.GaussianBlur(radius))

def pixelToAscii(image):
    pixels = image.getdata()
    characters = ""
    
    for pixel in pixels:
        if pixel < 25: 
            characters += " " 
        elif pixel < 50:
            characters += ASCII_CHARACTER[0]
        elif pixel < 75:
            characters += ASCII_CHARACTER[1]
        elif pixel < 100:
            characters += ASCII_CHARACTER[2]
        elif pixel < 125:
            characters += ASCII_CHARACTER[3]
        elif pixel < 150:
            characters += ASCII_CHARACTER[4]
        elif pixel < 175:
            characters += ASCII_CHARACTER[5]
        elif pixel < 200:
            characters += ASCII_CHARACTER[6]
        elif pixel < 225:
            characters += ASCII_CHARACTER[7]
        else:
            characters += ASCII_CHARACTER[8]

    return characters

def getTerminalWidth(defaultWidth = 100):
    try:
        columns, _ = shutil.get_terminal_size(fallback=(defaultWidth, 24))
        return columns
    except Exception as e:
        return defaultWidth


def main():
    path = input("Enter image path: ")

    try:
        image = PIL.Image.open(path)
    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
        return  
    except Exception as e:
        print(f"Error: {e}")
        return  

    image = applyContrast(image, factor=1.5) 
    image = applyBlur(image, radius=2) 

    terminalWidth = getTerminalWidth()

    newWidth = min(terminalWidth, 100)
    resizedImage = resizeImage(image, newWidth)
    
    grayImage = grayifyImage(resizedImage)
    asciiStr = pixelToAscii(grayImage)

    pixelCount = len(asciiStr)
    generateAscii = "\n".join(asciiStr[i:(i+newWidth)] for i in range(0, pixelCount, newWidth))
    
    print(generateAscii)

if __name__ == '__main__':
    main()

