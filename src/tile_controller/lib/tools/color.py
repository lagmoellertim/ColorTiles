np = None


def hsv_to_rgb(h, s, v):
    rgb_color = np.HSBtoRGB(h*360, s, v)
    return (
        (rgb_color & 0xff0000) >> 16,
        (rgb_color & 0x00ff00) >> 8,
        rgb_color & 0x0000ff
    )


def rgb_to_hsv(r, g, b):
    rgb_color = (r << 16) + (g << 8) + b
    hsv_color = np.RGBtoHSB(rgb_color)
    return (hsv_color[0]/360, hsv_color[1], hsv_color[2])
