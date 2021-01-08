"""
# File: writer.py
# Project: tp2
# File Created: Monday, 4th January 2021 9:31:55 am
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Friday, 8th January 2021 1:55:42 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2021 MIT, Institue de neurosciences de la Timone
"""

import png
import logging

logging.basicConfig(level=logging.DEBUG)


def MsgToBinary(msg):
    """
    Convert string to binary

    Args:
        msg ([str]): [str to convert]

    Returns:
        [binary]: [str converted]
    """

    res = "".join(format(ord(i), "08b") for i in msg)

    return res


def encryptPicture(imgToPx, textBin):
    """
    Hide the text in the image using lsb technique

    Args:
        imgToPx ([array]): [array of pixels]
        textBin ([binary]): [message to hide in binary form]

    Returns:
        [type]: [array of pixels]
    """

    logging.info("  TRYING TO ENCRYPT YOUR MESSAGE")
    for i in range(0, len(textBin)):
        listPixel = list(imgToPx[i])
        del listPixel[-1]
        listPixel.insert(len(listPixel), textBin[i])
        pixel = "".join(listPixel)
        imgToPx[i] = pixel

    logging.info("  ENCRYPTION DONE")
    return imgToPx


def writeToOutputFile(imgToPx, width, height, info):
    """
    Write image on the output file using pypng built-in 
    function :
    https://pypng.readthedocs.io/en/latest/png.html?highlight=array_scanlines#png.Writer.array_scanlines

    Args:
        imgToPx ([type]): [array of pixels]
        width ([type]): [Width of array]
        height ([type]): [height of array]
        info ([type]): [description]
    """

    writer = png.Writer(width, height, **info)
    output_file = open("output/output.png", "wb")
    logging.info("  TRYING TO WRITE TO OUTPUT FILE")
    output = \
        writer.array_scanlines([int(binary_px, 2) for binary_px in imgToPx])
    writer.write(output_file, output)
    logging.info("  MESSAGE ENCRYPTED")


def sanityCheck(msg_Bin, imgToPx):
    """
    Check is the message is not to long

    Args:
        msg_Bin ([binary]): [msg in binary form]
        imgToPx ([type]): [array of pixels]
    """
    if len(msg_Bin) > len(imgToPx):
        logging.warning("   MESSAGE TOO LONG")


def writeFunction(textToWrite, input):
    """
    write the message in input file
    https://pypng.readthedocs.io/en/latest/ex.html#a-little-message

    Args:
        textToWrite ([str]): [text to hide]
        input ([type]): [description]
    """

    textBin = MsgToBinary(textToWrite)
    file = png.Reader(filename=input)
    width, height, pixels, info = file.asRGBA8()
    imgToPx = [f"{px:08b}" for row in pixels for px in row]
    if "palette" in info:
        del info["palette"]
    sanityCheck(textBin, imgToPx)

    imgToPx = encryptPicture(imgToPx, textBin)

    writeToOutputFile(imgToPx, width, height, info)


def decryptMessage(arrayPixelized):
    """
    Find the  message in the array of pixels

    Args:
        arrayPixelized ([array]): [image transformed to array of pixels]

    Returns:
        [str]: [message found]
    """

    text = ""
    bytes = []

    logging.info("  TRYING TO DECRYPT YOUR IMAGE")

    def _split8(text):
        logging.info("  SPLITING TO 8")
        for _ in range(0, len(text), 8):
            bytes.append(text[_:_ + 8])
        return bytes

    def _getTextInArray(arrayPixelized, text):
        logging.info("  GETTING LSB")
        for byte in arrayPixelized:
            text += byte[-1]
        return text

    def _getTextFromByte(arrayPixelized):
        logging.info("  GETTING TEXT FROM BYTES")
        msgOutput = ""
        tmp = ""
        for char in all_bytes:
            tmp = chr(int(char, 2))
            if not tmp.isprintable():
                break

            msgOutput += tmp
        return msgOutput

    text = _getTextInArray(arrayPixelized, text)
    all_bytes = _split8(text)
    msg = _getTextFromByte(arrayPixelized)

    return msg


def readFunction():


    file = png.Reader(filename="output/output.png")
    width, height, pixels, info = file.asRGBA8()
    arrayPixelized = [f"{px:08b}" for row in pixels for px in row]

    return decryptMessage(arrayPixelized)
