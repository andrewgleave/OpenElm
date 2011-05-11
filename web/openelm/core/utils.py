import Image


__copyright__ = "Copyright 2011 Red Robot Studios Ltd."
__license__ = "GPL v3.0 http://www.gnu.org/licenses/gpl.html"


def crop_image_to_dimensions(original_image, dimensions):
    """Crops an image to the specified dimensions
    
    Scale image so that both dimensions are big enough to fill the frame
    then crop extra width or height."""
    
    image = original_image.copy()
    scale_factor_x = dimensions[0] / float(image.size[0])
    scale_factor_y = dimensions[1] / float(image.size[1])
    scale_factor = max(scale_factor_x, scale_factor_y)
    image = image.resize((int(image.size[0] * scale_factor),
                        int(image.size[1] * scale_factor)),
                        Image.ANTIALIAS)
    offset_left = (image.size[0] - dimensions[0]) // 2
    offset_top = (image.size[1] - dimensions[1]) // 2
    box = (offset_left, offset_top,
            offset_left + dimensions[0],
            offset_top + dimensions[1])
    return image.crop(box)
