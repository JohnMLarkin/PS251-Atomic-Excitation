import time

class Keithley6485:
    def __init__(self, resource_manager, visa_addr):
        # Connect to instrument
        self.instr = resource_manager.open_resource(visa_addr)

        # Verify that this is a Keithley 6485 picoammeter
        id_string = self.instr.query('*IDN?')
        if ('KEITHLEY' in id_string) and ('MODEL 6485' in id_string):
            print("Connection to Keithley 6485 successful")
        else:
            self.instr.close()
            raise Exception("Failed to connect to a Keithley 6485")
    
    def __del__(self):
        self.close()

    def close(self):
        self.zcheck_on()
        self.instr.close()

    def print_mode(self):
        result = self.instr.query('CONFIGURE?')
        print(result)

    def zcheck_on(self):
        self.instr.write('SYSTEM:ZCH ON')
    
    def zcheck_off(self):
        self.instr.write('SYSTEM:ZCH OFF')

    def configure_oneshot(self):
        self.instr.write('CONFIGURE:CURRENT')
    
    def get_current(self):
        raw_result = self.instr.query('READ?')
        # raw_result has format
        # (reading)(units),(timestamp),(status)\n
        # reading, timestamp, and status in exponential notation
        result = raw_result.split(",")
        current = result[0][:-1] # drop the unit
        status = int(float(result[2][:-2]))
        if (status & 1):
            raise Exception("Current is over range")
        if (status & 128):
            raise Exception("Voltage is over range")
        if (status & 512):
            raise Exception("Zero check is enabled")
        return float(current)
    