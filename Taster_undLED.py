import RPi.GPIO as GPIO
import time
import sqlite3
            

class sql_setup:
    def __init__(self, pfad=str):
        pfad = "{0}/datenbank.db".format(pfad)
        file = open(pfad,"a+")
        self.verbindung = sqlite3.connect(pfad)
        self.zeiger = self.verbindung.cursor()

    def create_table(self, name=str,spalte=str,typ=str,spalte2=str,typ2=str):
        create_table = 'CREATE TABLE IF NOT EXISTS "{0}" ("id" INTEGER PRIMARY KEY AUTOINCREMENT,"{1}" {2},"{3}" {4});'.format(name,spalte,typ,spalte2,typ2)
        self.zeiger.execute(create_table)
        self.verbindung.commit()

    def neue_spalte(self,tableName, spalte=str ,typ=str):
        spalte= "ALTER TABLE {0} ADD COLUMN {1} {2};".format(tableName,spalte,typ)
        self.zeiger.execute(spalte)
        self.verbindung.commit()
    def daten_einfügen(self,tablename=str,data1=str,data2=str):
        insert = 'INSERT INTO {0} VALUES (NULL,"{1}", "{2}")'.format(tablename,data1,data2)
        self.zeiger.execute(insert)
        self.verbindung.commit()

class led:
    def __init__ (self,pin,pfad):
        self.pin = pin
        self.zustand = False
        self.objekt2 = sql_setup(pfad)
        self.objekt2.create_table("LEDundTASTER","zustand","TEXT","datum","TEXT")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        

    def get_time(self):
        return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    def get_zustand(self):
        return self.zustand

    def toggel(self,zustand_neu=bool):
        if zustand_neu == True:
            self.zustand = True
            GPIO.output(self.pin, GPIO.HIGH)
            self.objekt2.daten_einfügen("LEDundTASTER",str(self.get_zustand()),str(self.get_time()))
            print("led an")
        elif zustand_neu == False:
            self.zustand = False
            GPIO.output(self.pin, GPIO.LOW)
            self.objekt2.daten_einfügen("LEDundTASTER",str(self.get_zustand()),str(self.get_time()))
            print("led aus")

class Taster:
    def __init__(self, pin2,ledpin,pfad):
        self.pin2 = pin2
        self.ledpin = ledpin
        self.obejekt = led(self.ledpin,pfad)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin2,GPIO.IN)

    def gedruekt(self):
        if (GPIO.input(self.pin2)==True):
            if self.obejekt.get_zustand()==True:
              self.obejekt.toggel(False)
            elif self.obejekt.get_zustand() == False:
                self.obejekt.toggel(True)
            print(self.obejekt.get_zustand())
            time.sleep(0.1)

try:

    if __name__ == "__main__":
        GPIO.setwarnings(False)
        GPIO.cleanup()
        a = Taster(10,24,"/home/pi/Desktop")
        while True:
            a.gedruekt()
            time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    
        
                