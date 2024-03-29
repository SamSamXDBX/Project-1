from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from jnius import autoclass

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')

#Connexion HC-06:
def get_socket_stream(name):
    paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    socket = None
    for device in paired_devices:
        if device.getName() == name:
            socket = device.createRfcommSocketToServiceRecord(
                UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
            recv_stream = socket.getInputStream()
            send_stream = socket.getOutputStream()
            break
    socket.connect()
    return recv_stream, send_stream
 
class Application(App):
    def build(self):
        #Pour la connexion EDR :
        self.recv_stream, self.send_stream=None,None
        #Interface graphique :
        Layout=BoxLayout(orientation='vertical',spacing=20,padding=(0,20))
        self.Haut_Layout=GridLayout(cols=1,size_hint=(0.80,0.7),pos_hint={'x':.1, 'y':.1})
        self.orientation='vertical' #Nombre maximum de colonnes
        
        #On l'ajoute a la fenetre principal:
        Layout.add_widget(self.Haut_Layout)
        
        self.BoutonConnect=Button(text='Connect')
        self.BoutonConnect.bind(on_press=self.connect)
        #On ajoute le bouton dans l'affichage:
        self.Haut_Layout.add_widget(self.BoutonConnect)
        
        
        self.Bas_Layout=GridLayout(cols=3,size_hint=(0.80,0.7),pos_hint={'x':.1, 'y':.1},spacing=20)
        self.orientation='horizontal' #Nombre maximum de colonnes
        self.spacing=8 #Espace entre les objets contenus
        self.padding=30 #Marges interieures du Layout
        
        #On l'ajoute a la fenetre principal:
        Layout.add_widget(self.Bas_Layout)
        
        #On cree un bouton:
        self.Bouton1=Button()
        #On lui donne des proprietes:
        #Une taille en pourcentages:
        self.Bouton1.size_hint=(0.5,0.5)
        #Une position:
        self.Bouton1.pos_hint={0.5: 0.5}
        #Une couleur de fond:
        self.Bouton1.background_normal="image1.png"
        self.Bouton1.bind(on_press=self.send)
        self.Bouton1.id='1'
        #On l'ajoute au layout principal:
        self.Bas_Layout.add_widget(self.Bouton1)
        
        #On cree un bouton:
        self.Bouton2=Button()
        #On lui donne des proprietes:
        #Une taille en pourcentages:
        self.Bouton2.size_hint=(0.5,0.5)
        #Une position:
        self.Bouton2.pos_hint={0.6: 0.6}
        #Une couleur de fond:
        self.Bouton2.background_normal="image2.png"
        self.Bouton2.bind(on_press=self.send)
        self.Bouton2.id='2'
        #On l'ajoute au layout principal:
        self.Bas_Layout.add_widget(self.Bouton2)
        
         #On cree un bouton:
        self.Bouton3=Button()
        #On lui donne des proprietes:
        #Une taille en pourcentages:
        self.Bouton3.size_hint=(0.5,0.5)
        #Une position:
        self.Bouton3.pos_hint={0.9: 0.9}
        #Une couleur de fond:
        self.Bouton3.background_normal="image3.png"
        self.Bouton3.bind(on_press=self.send)
        self.Bouton3.id='3'
        #On l'ajoute au layout principal:
        self.Bas_Layout.add_widget(self.Bouton3)
        
        
        return Layout
 
    def connect(self,instance):
        try:
            self.recv_stream, self.send_stream = get_socket_stream('HC-06')
        except:
            instance.background_color=[1,0,0,1]
        if self.send_stream!=None:
            instance.background_color=[0,1,0,1]
            instance.text="connected"
 
    def send(self, instance):
        if self.send_stream!=None:
            self.send_stream.write(int(instance.id))
            self.send_stream.flush()
 
if __name__ == '__main__':
    Application().run()