
# coding: utf-8

# In[2]:


#Appel de la dll, importation, et ouverture de la communication
from ctypes import cdll, c_char_p, c_wchar_p, create_string_buffer,addressof,c_byte
import time

wdll=cdll.LoadLibrary("ODevice.dll")

#Ouverture de la communication
wdll.odev_open()

#Information
def status():
    buffer = create_string_buffer(256)
    wdll.odev_ask(b"INFO?",buffer)

    if len(buffer.value) == 0:
        raise UserWarning('Monochromator is offline')
    
    return buffer.value


#Open the shutter
def shutteropen():
    status()
    buffer = create_string_buffer(256)
    wdll.odev_ask(b"SHUTTER O",buffer)
    wdll.odev_ask(b'SHUTTER?\n',buffer)

    if not buffer.value ==b"SHUTTER O":
        raise UserWarning('shutter is not in required position')
        
    return buffer.value

#Close the shutter
def shutterclose():
    status()
    buffer = create_string_buffer(256)
    
    wdll.odev_ask(b"SHUTTER C",buffer)
    wdll.odev_ask(b'SHUTTER?\n',buffer)

    if not buffer.value ==b"SHUTTER C":
        raise UserWarning('shutter is not in required position')
        
    return buffer.value

#Ask for the shutter (Open or Close)
def getshutter():
    status()
    buffer = create_string_buffer(256)
    wdll.odev_ask(b'SHUTTER?\n',buffer)

    return buffer.value
    

#Choose the grating
def setgrating(gratingId):
    status()
    buffer = create_string_buffer(256)
    gratingId = int(gratingId)
    buffer = create_string_buffer(256)
    
    if not 1<=gratingId<=3:
        raise ValueError('try 1 for the grating 1,2 for grating 2 or 3 for grating 3')
        
    wdll.odev_write(b'GRAT %.1f\n'%i)
    wdll.odev_ask(b'GRAT?\n',buffer)

    return buffer.value

#To know which grating is using
def getgrating():
    status()
    buffer = create_string_buffer(256)

    wdll.odev_ask(b'GRAT?\n',buffer)

    return buffer.value

#Choose the outport
"""
For Axial OUTPORT = 1
For Lateral OUTPORT = 2
"""
def setoutport(outportId):
    status()
    buffer = create_string_buffer(256)
    outportId = int(outportId)
    
    if not 1<=outportId<=2:
        raise ValueError('try 1 for the axial outport or 2 for the lateral outport')

    wdll.odev_write(b'OUTPORT %.1f \n'%i)
    wdll.odev_ask(b'OUTPORT?\n',buffer)

    return buffer.value

#To know which grating is using
def getoutport():
    status()
    buffer = create_string_buffer(256)
    if len(buffer.value)== 0 :
        raise TypeError('Monochromator is offline')
    wdll.odev_ask(b'OUTPORT?\n',buffer)
    
    return buffer.value
    
#Send a wavelength
def setwave(wave):
    status()
    buffer = create_string_buffer(256)

    if not 300<=wave<=1200:
        raise ValueError('a must be within 300 - 1200')
        
    wdll.odev_write(b'GOWAVE %.3f\n'%i)
    wdll.odev_ask(b'WAVE?\n',buffer)

    return buffer.value

#To knos which wavelength is being sent
def getwave():
    status()
    buffer = create_string_buffer(256)
    
    if len(buffer.value)== 0 :
        raise TypeError('Monochromator is offline')
        
    wdll.odev_ask(b'WAVE?\n',buffer)

    return buffer.value

