# Andy Warhol-Style Collage Creator

This Python program creates an Andy Warhol-style collage from a single input image.

## Author

Rodolfo Lopez

## Date

Fall 2019

## Features

- Applies various filters to the input image
- Creates a 3x2 collage of filtered images
- Supports custom output size

## Usage

1. Ensure you have Python installed on your system.

2. Install the pillow dependency:

   ```
   pip install pillow
   ```

3. Ensure the `comp110_image.py` module and the .jpg input image are in the same directory as `collage_creator.py`

4. Run the script:

   ```
   python collage_creator.py
   ```

5. Follow the prompts:

   - Enter the input image filename (eg. cute-cat.jpg)
   - Specify the output collage filename
   - Set the maximum width and height for the collage

6. The program will generate and display the collage, then save it to the specified file.

## Filters Applied

- Posterize
- Sunset
- Negative
- Blur
- Edge detection
- Grayscale

## Acknowledgements

Dr. Sat Garcia wrote the module `comp110_image.py` and I wrote the module `collage_creator.py`
