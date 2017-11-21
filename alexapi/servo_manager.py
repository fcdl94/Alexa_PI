#in questo file verrà creata una classe che si occupa di gestire il movimento attraverso una classe wrapper
#la libreria che verrà usata è adafruit pca9685
import Adafruit_PCA9685 as pca

class servomanager():
    #funzione esempio
    def movto(self,position):
        #viene passata la possizione in cui il servo deve ruotare
        #nella funzione init verra specificato quanti punti cardinali tenere in considerazino
    def __init__(self):
        #questa funzione avrà lo scopo di inizializzare il driver per il servo
        pwm=pca.PCA9685(address=0x54,busnum=1)