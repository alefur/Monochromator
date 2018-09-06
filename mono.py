# coding: utf-8

# In[2]:


import time
# Appel de la dll, importation, et ouverture de la communication
from ctypes import cdll, c_char_p, c_wchar_p, create_string_buffer, addressof, c_byte

wdll = cdll.LoadLibrary('ODevice.dll')

# Ouverture de la communication
wdll.odev_open()


def status():
    """Information"""
    buffer = create_string_buffer(256)
    wdll.odev_ask(b'INFO?', buffer)

    if len(buffer.value) == 0:
        raise UserWarning('Monochromator is offline')

    return buffer.value


def getshutter(getStatus=True):
    """Ask for the shutter position(Open or Close)"""
    if getStatus:
        status()

    buffer = create_string_buffer(256)
    wdll.odev_ask(b'SHUTTER?\n', buffer)

    return buffer.value


def shutteropen():
    """Open the shutter"""
    status()

    wdll.odev_write(b'SHUTTER O')
    shutter = getshutter(getStatus=False)

    if shutter != b'SHUTTER O':
        raise UserWarning('shutter is not in required position')

    return shutter


def shutterclose():
    """Close the shutter"""
    status()

    wdll.odev_write(b'SHUTTER C')
    shutter = getshutter(getStatus=False)

    if shutter != b'SHUTTER C':
        raise UserWarning('shutter is not in required position')

    return shutter


def getgrating(getStatus=True):
    """To know which grating is currently used"""
    if getStatus:
        status()

    buffer = create_string_buffer(256)
    wdll.odev_ask(b'GRAT?\n', buffer)

    return buffer.value


def setgrating(gratingId):
    """Choose the grating (1,2,3)"""
    status()

    gratingId = int(gratingId)

    if not 1 <= gratingId <= 3:
        raise ValueError('try 1 for the grating 1,2 for grating 2 or 3 for grating 3')

    wdll.odev_write(b'GRAT %d\n' % gratingId)

    return getgrating(getStatus=False)


def getoutport(getStatus=True):
    """To know which grating is currently used """
    if getStatus:
        status()

    buffer = create_string_buffer(256)
    wdll.odev_ask(b'OUTPORT?\n', buffer)

    return buffer.value


def setoutport(outportId):
    """Choose the outport : For Axial OUTPORT = 1 , For Lateral OUTPORT = 2"""
    status()

    outportId = int(outportId)

    if not 1 <= outportId <= 2:
        raise ValueError('try 1 for the axial outport or 2 for the lateral outport')

    wdll.odev_write(b'OUTPORT %d\n' % outportId)

    return getoutport(getStatus=False)


def getwave(getStatus=True):
    """To know which wavelength is being sent"""

    if getStatus:
        status()

    buffer = create_string_buffer(256)
    wdll.odev_ask(b'WAVE?\n', buffer)

    return buffer.value


def setwave(wave):
    """Send a wavelength"""
    status()
    wave = float(wave)

    if not 300 <= wave <= 1200:
        raise ValueError('a must be within 300 - 1200')

    wdll.odev_write(b'GOWAVE %.3f\n' % wave)

    return getwave(getStatus=False)
