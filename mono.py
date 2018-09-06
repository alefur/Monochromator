import time
# Appel de la dll, importation, et ouverture de la communication
from ctypes import cdll, c_char_p, c_wchar_p, create_string_buffer, addressof, c_byte


class Monochromator:
    wdll = cdll.LoadLibrary('ODevice.dll')
    wdll.odev_open()

    errorCodes = {0: 'Command not understood',
                  1: 'System error (miscellaneous)',
                  2: 'Bad parameter used in Command',
                  3: 'Destination position for wavelength motion not allowed',
                  6: 'Accessory not present (usually filter wheel)',
                  7: 'Accessory already in specified position',
                  8: 'Could not home wavelength drive',
                  9: 'Label too long',
                  }

    def __init__(self, remote=False):
        if not remote:
            self.status()
            self.init()

    def init(self):
        self.wdll.odev_write(b'HANDSHAKE 1\n')

    def sendCommand(self, cmdStr, error='20\r\n'):
        """send command to monochromator"""
        buffer = create_string_buffer(256)
        self.wdll.odev_ask(b'%s\n' % cmdStr, buffer)

        if len(buffer.value) == 0:
            raise UserWarning('Monochromator is offline')

        ret = buffer.value.decode('utf8')
        if error in ret:
            raise UserWarning(self.getError())

        return ret.split('\r\n', 1)

    def getError(self):
        buffer = create_string_buffer(256)
        self.wdll.odev_ask(b'ERROR?\n' % cmdStr, buffer)
        errorCode = buffer.value.decode('utf8').split('\r\n')[0]

        return self.errorCodes[int(errorCode)]

    def status(self):
        """Information"""
        return self.sendCommand('INFO?')

    def getshutter(self):
        """Ask for the shutter position(Open or Close)"""
        return self.sendCommand('SHUTTER?')

    def getgrating(self):
        """To know which grating is currently used"""
        return self.sendCommand('GRAT?')

    def getoutport(self):
        """To know which grating is currently used """
        return self.sendCommand('OUTPORT?')

    def getwave(self):
        """To know which wavelength is being sent"""
        return self.sendCommand('WAVE?')

    def __setshutter(self, state):
        """Open the shutter"""
        self.sendCommand('SHUTTER %s' % state)

        return self.getshutter()

    def shutteropen(self):
        """Close the shutter"""
        return self.__setshutter(state='O')

    def shutterclose(self):
        """Close the shutter"""
        return self.__setshutter(state='C')

    def setgrating(self, gratingId):
        """Choose the grating (1,2,3)"""

        gratingId = int(gratingId)

        if not 1 <= gratingId <= 3:
            raise ValueError('try 1 for the grating 1,2 for grating 2 or 3 for grating 3')

        self.sendCommand('GRAT %d' % gratingId)

        return self.getgrating()

    def setoutport(self, outportId):
        """Choose the outport : For Axial OUTPORT = 1 , For Lateral OUTPORT = 2"""

        outportId = int(outportId)

        if not 1 <= outportId <= 2:
            raise ValueError('try 1 for the axial outport or 2 for the lateral outport')

        self.sendCommand('OUTPORT %d' % outportId)

        return self.getoutport()

    def setwave(self, wave):
        """Send a wavelength"""

        wave = float(wave)

        if not 300 <= wave <= 1200:
            raise ValueError('a must be within 300 - 1200')

        self.sendCommand('GOWAVE %.3f' % wave)

        return self.getwave()
