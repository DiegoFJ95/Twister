from serial import Serial
import struct
import time


class SerialCom:
    def __init__(self, port, callback, baudrate=115200) -> None:
        self.ser = Serial( port, baudrate=baudrate, timeout=0.005 )
        self.tasks = []
        self.bussy = False
        self.position = 0
        self.callback = callback
        self._iter = self.loop()

    def next(self):
        return next( self._iter )

    def cs( msg ):
        cs = 0
        for c in msg: cs = ( cs + c ) & 0xFFFF
        return msg + b"*" + cs.to_bytes(2,"little")

    def m0( steps ):
        msg = str.encode( "M0 ", "ascii" ) #paso a la derecha
        msg = msg + steps.to_bytes(2,"little")
        return SerialCom.cs(msg)

    def m1( steps ):
        msg = str.encode( "M1 ", "ascii" ) #paso a la izquierda
        msg = msg + steps.to_bytes(2,"little")
        return SerialCom.cs(msg)

    def p0():
        msg = str.encode( "P0 ", "ascii" ) #setea en 0 la var de posicion
        return SerialCom.cs(msg)

    def p1():
        msg = str.encode( "P1 ", "ascii" ) # regresa la posición
        return SerialCom.cs(msg)

    def move(self, steps : int):
        if steps > 0:
            msg = SerialCom.m0(abs(steps))
        else:
            msg = SerialCom.m1(abs(steps))
        flag = False
        for _ in range(5):
            self.ser.write( msg )
            res = self.ser.readline()
            if res == b"OK\n": flag = True; break
        return flag
    
    def zero(self):
        msg = SerialCom.p0()
        flag = False
        for _ in range(5):
            self.ser.write( msg )
            res = self.ser.readline()
            if res == b"OK\n": flag = True; break
        return flag
    
    def pos(self):
        msg = SerialCom.p1()
        flag = False
        for _ in range(5):
            self.ser.write( msg )
            m = self.ser.read(4)
            if len( m ) == 4:
                position = struct.unpack( "<i", m )
            res = self.ser.readline()
            if res == b"OK\n": flag = True; break
        self.position = position[0]
        self.callback( self.position )
        return flag
        
    def schedule(self,task):
        if task[0] in ["M", "Z", "P"]:
            self.tasks.append( task )

    def loop(self):
        while True:
            if not self.bussy:
                if len( self.tasks ):
                    args = self.tasks.pop(0)
                    for _ in range( 3 ):
                        if args[0] == "M": res = self.move(args[1])
                        if args[0] == "Z": res = self.zero()
                        if args[0] == "P": res = self.pos()
                        if res: self.bussy = True; yield; break
                        else: yield
                else:
                    yield
            else:
                res = self.ser.readline()
                if res == b"DONE\n":
                    self.bussy = False
                yield

    # Cosecha propia    
    def close(self):
        self.ser.close()  

# ser = SerialCom( "COM4", print )
# ser.schedule( ("M",100) )
# ser.schedule( ("M",-50) )
# ser.schedule( ("P",) )
# ser.schedule( ("Z",) )
# ser.schedule( ("P",) )
# ser.schedule( ("M",25) )
# ser.schedule( ("P",) )

#for i in range(100):
#    ser.next()
#    time.sleep(0.16)

