
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
    a_test = create_string_buffer(256)
    if len(a_test.value) == 0:
        raise UserWarning('Monochromator is offline')
    wdll.odev_ask(b"INFO?",a_test)
    print(a_test.value)
    return a_test.value


#Open the shutter
def shutteropen():
    b_test = create_string_buffer(256)
    if len(b_test.value)== 0 :
        raise TypeError('Monochromator is offline')
    wdll.odev_ask(b"SHUTTER O",b_test)
    wdll.odev_write(b'SHUTTER?\n')
    wdll.odev_read(b_test)
    print(b_test.value)
    if not b_test.value ==a:
        raise UserWarning('shutter is not in required position')
    return b_test.value

#Close the shutter
def shutterclose():
    j_test = create_string_buffer(256)
    if len(j_test.value)==0 :
        raise TypeError('Monochromator is offline')
    wdll.odev_ask(b"SHUTTER C",j_test)
    wdll.odev_write(b'SHUTTER?\n')
    wdll.odev_read(j_test)
    print(j_test.value)
    if not j_test.value ==a:
        raise UserWarning('shutter is not in required position')
    return j_test.value

#Ask for the shutter (Open or Close)
def getshutter():
    f_test = create_string_buffer(256)
    if len(f_test.value)== 0 :
        raise TypeError('Monochromator is offline')
    wdll.odev_write(b'SHUTTER?\n')
    wdll.odev_read(f_test)
    print(f_test.value)
    return f_test.value
    

#Choose the grating
def grat(i):
    c_test = create_string_buffer(256)
    if not 1<=i<=3:
        raise ValueError('try 1 for the grating 1,2 for grating 2 or 3 for grating 3')
    if len(c_test.value)== 0 :
        raise TypeError('Monochromator is offline')
    wdll.odev_write(b'GRAT %.1f\n'%i)
    wdll.odev_write(b'GRAT?\n')
    wdll.odev_read(c_test)
    print(c_test.value)
    return c_test.value

#To know which grating is using
def getgrat():
    g_test = create_string_buffer(256)
    if len(g_test.value)== 0 :
        raise TypeError('Monochromator is offline')
    wdll.odev_write(b'GRAT?\n')
    wdll.odev_read(g_test)
    print(g_test.value)
    return g_test.value

#Choose the outport
"""
For Axial OUTPORT = 1
For Lateral OUTPORT = 2
"""
def outport(i):
    d_test = create_string_buffer(256)
    if not 1<=i<=2:
        raise ValueError('try 1 for the axial outport or 2 for the lateral outport')
    if len(d_test.value)== 0 :
        raise TypeError('Monochromator is offline')
    wdll.odev_write(b'OUTPORT %.1f \n'%i)
    wdll.odev_write(b'OUTPORT?\n')
    wdll.odev_read(d_test)
    print(d_test.value)
    return d_test.value

#To know which grating is using
def getoutport():
    h_test = create_string_buffer(256)
    if len(h_test.value)== 0 :
        raise TypeError('Monochromator is offline')
    wdll.odev_write(b'OUTPORT?\n')
    wdll.odev_read(h_test)
    print(h_test.value)
    return h_test.value
    
#Send a wavelength
def gowave(i):
    e_test = create_string_buffer(256)
    if len(e_test.value)== 0 :
        raise TypeError('Monochromator is offline')
    if not 300<=i<=1200:
        raise ValueError('a must be within 300 - 1200')
    wdll.odev_write(b'GOWAVE %.1f\n'%i)
    wdll.odev_write(b'WAVE?\n')
    wdll.odev_read(e_test)
    print(e_test.value)
    return e_test.value

#To knos which wavelength is being sent
def getwave():
    i_test = create_string_buffer(256)
    if len(i_test.value)== 0 :
        raise TypeError('Monochromator is offline')
    wdll.odev_write(b'WAVE?\n')
    wdll.odev_read(i_test)
    print(i_test.value)
    return i_test.value

