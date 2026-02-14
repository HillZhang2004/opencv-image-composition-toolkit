# Note: you should not need to add any more libraries to complete
# this assignment. If you think you need another library, please
# check with your instructor first.
import cv2
import numpy as np

# Note: this function is provided for you, and it may be useful.
# You should understand how it works.
def load_img(impath):
    """
    Loads an image from a specified location and returns it in RGB format.
    Input:
    - impath: a string specifying the target image location.
    Returns an RGB image.
    """
    img = cv2.imread(impath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

# Note: this function is provided for you, and it may be useful.
# You should understand how it works.
def load_alpha(impath):
    """
    Loads an image with a transparency channel and returns an RGB image and a transparency channel as two separate objects.
    Input:
    - impath: a string specifying the target image location. This image should have a transparency channel.
    Returns:
    - content: an RGB image containing the input image content.
    - alpha: a single channel image containing the input's transparency map
    """

    img_raw = cv2.imread(impath, cv2.IMREAD_UNCHANGED)
    img = img_raw.copy()
    img[:,:,0] = img_raw[:,:,2]
    img[:,:,2] = img_raw[:,:,0]

    content = img[:,:,0:3]
    alpha = img[:,:,3]

    return content, alpha

#TODO: Complete this function
def place_object(bkg_img, element, elmask, location, height):
    """
    Places an element into a specified location of background image at a specified scale.
    Parameters:
    - bkg_img: an RGB image into which the element should be inserted
    - element: an RGB image containing the object be inserted
    - elmask: a transparency mask that corresponds to the element being inserted
    - location: a tuple in (x,y) format which specifies the horizontal and vertical position, respectively, in normalized image scale coordinates to which the centroid of the minimal bounding box of the element should be inserted
    - height: specifies the height of the minimal bounding box for the element in normalized image scale. The element's width should be scaled accordingly to maintain its aspect ratio

    Returns an RGB image containing the composite output. This should *not* modify the input images, but should instead create a new image, and
    should be in 8-bit integer format.
    """

    img_out = bkg_img.copy().astype(np.float32)
    H, W = bkg_img.shape[0], bkg_img.shape[1]

    ys, xs = np.where(elmask > 0)
    if ys.size == 0 or xs.size == 0:
        return img_out.astype('uint8')

    y0, y1 = int(ys.min()), int(ys.max()) + 1
    x0, x1 = int(xs.min()), int(xs.max()) + 1

    el = element[y0:y1, x0:x1, :]
    mk = elmask[y0:y1, x0:x1]
    h0, w0 = mk.shape[0], mk.shape[1]

    new_h = int(round(height * H))
    if new_h <= 0:
        return img_out.astype('uint8')

    new_w = int(round(new_h * (w0 / h0)))
    if new_w <= 0:
        return img_out.astype('uint8')

    interp = cv2.INTER_AREA if new_h < h0 else cv2.INTER_LINEAR
    el = cv2.resize(el, (new_w, new_h), interpolation=interp)
    mk = cv2.resize(mk, (new_w, new_h), interpolation=interp)

    x_norm, y_norm = location
    cx = int(round(x_norm * (W - 1)))
    cy = int(round(y_norm * (H - 1)))

    tlx = cx - new_w // 2
    tly = cy - new_h // 2

    bx0, by0 = max(0, tlx), max(0, tly)
    bx1, by1 = min(W, tlx + new_w), min(H, tly + new_h)

    if bx0 >= bx1 or by0 >= by1:
        return img_out.astype('uint8')

    ex0, ey0 = bx0 - tlx, by0 - tly
    ex1, ey1 = ex0 + (bx1 - bx0), ey0 + (by1 - by0)

    patch = el[ey0:ey1, ex0:ex1, :].astype(np.float32)
    alpha = mk[ey0:ey1, ex0:ex1].astype(np.float32) / 255.0
    alpha = np.clip(alpha, 0.0, 1.0)
    alpha = alpha[:, :, None]

    bg = img_out[by0:by1, bx0:bx1, :]
    img_out[by0:by1, bx0:bx1, :] = alpha * patch + (1.0 - alpha) * bg

    img_out = np.clip(img_out, 0, 255)
    return img_out.astype('uint8')
