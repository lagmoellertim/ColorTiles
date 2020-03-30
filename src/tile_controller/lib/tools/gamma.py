import math


def correct_gamma(r, g, b, gamma):
    gamma_correction = 1 / gamma
    r_corrected = 255 * math.pow(r / 255, gamma_correction)
    g_corrected = 255 * math.pow(g / 255, gamma_correction)
    b_corrected = 255 * math.pow(b / 255, gamma_correction)

    return (r_corrected, g_corrected, b_corrected)
