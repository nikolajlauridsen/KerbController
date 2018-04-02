"""
Various helper functions to make life a bit easier.
"""
import math


def mapvalue(value, leftMin, leftMax, rightMin, rightMax):
    """Maps one range to another.
    Code taken from:
    http://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another"""
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def frexp10(x):
    """
    Return mantissa and exponent (base 10), similar to base-2 frexp()
    :param x: floating point number
    :return: tuple (mantissa, exponent)

    Taken from: http://exality.com/convert-floats-to-engineering-notation/
    """
    exp = math.floor(math.log10(x))
    return x/10**exp, exp


def eng_notate(x, d=3, suff=True, neg_ok=False):
    """
    Convert a float to a string in engineering units, with specified
    significant digits
    :param x: float to convert
    :param d: number of significant digits
    :param suff: True:  use suffix unit letter
                 False: return scientific notation
    :param neg_ok: True if negative values are ok, False otherwise
    :return: string conversion of x, either scientific notation
             or with suffix

    Taken from: http://exality.com/convert-floats-to-engineering-notation/
    """
    # Practical component suffixes
    _SUFFIX = ["p", "n", "u", "m", "", "k", "M", "G"]
    # Offset to unit multiplier (no suffix)

    _UNIT_OFFSET = 4

    sign = ""
    if neg_ok and x < 0.0:
        sign = "-"
        x = -x
    if x < 0.0 or not math.isfinite(x):
        return "RangeErr"
    if x == 0:
        return "0.0"
    # Normalize the number and round to get d significant digits
    mant, exp = frexp10(x)
    r = round(mant,d-1)
    # Convert back to original scale
    x = r * math.pow(10.0, exp)
    # Get integer exponent to group by factors of 1000
    p = int(math.floor(math.log10(x)))
    p3 = p // 3
    # Get root value string
    value = x / math.pow(10.0, 3*p3)
    numStr = "{:f}".format(value)
    # Slice to length, avoid trailing "."
    if numStr[d] != ".":
        numStr = numStr[0:d+1]
    else:
        numStr = numStr[0:d]
    # Prepend '-' if necessary
    numStr = sign + numStr
    if suff:
        # Append units suffix
        p3i = p3 + _UNIT_OFFSET
        if p3i < 0:
            # Smaller than lowest unit
            return "<1{}".format(_SUFFIX[0])
        if p3i > len(_SUFFIX)-1:
            # Larger than largest unit
            return ">999{}".format(_SUFFIX[-1])
        else:
            s = _SUFFIX[p3i]
            return "{}{}".format(numStr, s)
    else:
        # No suffix, return floating point string
        if p3 != 0:
            return "{}e{:d}".format(numStr, 3*p3)
        else:
            return "{}".format(numStr)
