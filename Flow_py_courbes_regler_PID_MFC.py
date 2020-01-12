from tkinter import*
from recherche_creation_ports import*
from trames_fonctions import*

numeroDeSerie=''

class instrument:
    def __init__(self):
        self.nom="INSTRUMENT"

    def liste_port(self):
        port_disponible=listing_ports()
        return(port_disponible)

    def cree_port(self):
        monPort=cree_port_unique()
        return(monPort)

    def Initreset(self,monPort,initReset):
        Initreset_7('E',initReset,monPort)

    def Control_mode(self,monPort,modeControle):
        Control_mode_12('E',modeControle,monPort)

    def modelType(self,monPort):
        modele=BHT_Model_number_91('L',0,monPort)
        return(modele)

    def numeroSerie(self,monPort):
        numeroDeSerie=Serial_number_92('L',0,monPort)
        return(numeroDeSerie)

    def fluideNom(self,monPort):
        fluide=Fluid_name_25('L',0,monPort)
        return(fluide)

    def capaciteUnit(self,monPort):
        uniteCapacite=Capacity_unit_129('L',0,monPort)
        return(uniteCapacite)

    def laCapacite(self,monPort):
        capacite=Capacity_21('L',0,monPort)
        return(capacite)

    def PID_Kp(self,monPort):
        valeur_Kp=PID_Kp_167('L',0,monPort)
        return(valeur_Kp)

    def PID_Ti(self,monPort):
        valeur_Ti=PID_Ti_168('L',0,monPort)
        return(valeur_Ti)

    def PID_Td(self,monPort):
        valeur_Td=PID_Td_169('L',0,monPort)
        return(valeur_Td)

    def PID_Kp_E(self,monPort,val_Kp):
        PID_Kp_167('E',val_Kp,monPort)

    def PID_Ti_E(self,monPort,val_Ti):
        PID_Ti_168('E',val_Ti,monPort)

    def PID_Td_E(self,monPort,val_Td):
        PID_Td_169('E',val_Td,monPort)

    def laMesure(self,monPort):
        maMesure=fMeasure_205('L',0,monPort)
        return(maMesure)

    def laConsigne(self,monPort,consigne):
        fSetpoint_206('E',consigne,monPort)

    def laConsigneLue(self,monPort):
        maConsigne=fSetpoint_206('L',0,monPort)
        return(maConsigne)

canal1=instrument()
portDisponible=canal1.liste_port()
nbrePort=len(portDisponible)
monPort=canal1.cree_port()

lesCOMs=[""]*20
for bla in range(0,nbrePort):
    lesCOMs[bla]=str(portDisponible[bla])

if monPort=="":
    port_actif="Pas d'instrument en ligne"
    instruction="Pour sortir fermer cette fenêtre"
else:
    port_actif="Un instrument en ligne"
    instruction="Pour poursuivre : fermer cette fenêtre"

fenCom=Tk()
fenCom.geometry("400x400+150+50")
fenCom.title("CONFIGURATION")
fenCom['bg']='white'

etiquette_port_actif=Label(fenCom,text=port_actif,bg='white',font="ARIAL 15",fg='red')
etiquette_port_actif.pack()
for bla in range(0,nbrePort):
    etiquette_port_present=Label(fenCom,text=lesCOMs[bla],bg='white',font="ARIAL 12",fg='blue')
    etiquette_port_present.pack()
etiquette_instruction=Label(fenCom,text=instruction,bg='white',font="ARIAL 15",fg='red')
etiquette_instruction.pack()
fenCom.mainloop()

if monPort !="":
    while numeroDeSerie=='':
        numeroDeSerie=canal1.numeroSerie(monPort)
    canal1.Control_mode(monPort,0)
    modele=canal1.modelType(monPort)
    nom_de_fluide=canal1.fluideNom(monPort)
    unite=canal1.capaciteUnit(monPort)
    pleine_echelle=canal1.laCapacite(monPort)
    mesure=canal1.laMesure(monPort)
    Proportionnelle=canal1.PID_Kp(monPort)
    Integrale=canal1.PID_Ti(monPort)
    Derive=canal1.PID_Td(monPort)

    def admission_Kp(value_Kp):
        value_Kp=float(value_Kp)
        canal1.Initreset(monPort,64)
        canal1.PID_Ti_E(monPort,value_Kp)
        canal1.Initreset(monPort,82)

    def admission_Ti(value_Ti):
        value_Ti=float(value_Ti)
        canal1.Initreset(monPort,64)
        canal1.PID_Ti_E(monPort,value_Ti)
        canal1.Initreset(monPort,82)

    def admission_Td(value_Td):
        value_Td=float(value_Td)
        canal1.Initreset(monPort,64)
        canal1.PID_Td_E(monPort,value_Td)
        canal1.Initreset(monPort,82)

    def admission_consigne(valeur):
        valeur=float(valeur)
        canal1.laConsigne(monPort,valeur)

    counter_consigne=0
    x=0
    y=0
    def inc_label_consigne():
        def count_consigne():
            global counter_consigne
            global x
            global y
            counter_consigne += 1
            w=x+1
            z=canal1.laConsigneLue(monPort)
            z=z/pleine_echelle
            z=585-(580*z)
            ligneCons=feuillet.create_line(x,y,w,z,width=2,fill='red')
            x=w
            y=z
            if x>720:
                feuillet.delete(ALL)
                for bla in range(0,58):
                    for ble in range(0,75):
                        posx=str(60*bla)
                        posy=str(30*ble)
                        feuillet.create_line(posx,"0",posx,"600",width=1,fill="blue")
                        feuillet.create_line("0",posy,"750",posy,width=1,fill="blue")
                feuillet.place(x='0',y='40')
                x=0
            feuillet.after(100,count_consigne)
        count_consigne()
    
    counter_mesure=0
    t=0
    u=0
    def inc_label_mesure():
        def count_mesure():
            global counter_mesure
            global t
            global u
            counter_mesure += 1
            s=t+1
            v=canal1.laMesure(monPort)
            v=v/pleine_echelle
            v=585-(580*v)
            ligneMesure=feuillet.create_line(t,u,s,v,width=2,fill='green')
            t=s
            u=v
            if t>720:
                feuillet.delete(ALL)
                for bla in range(0,58):
                    for ble in range(0,75):
                        posx=str(60*bla)
                        posy=str(30*ble)
                        feuillet.create_line(posx,"0",posx,"600",width=1,fill="blue")
                        feuillet.create_line("0",posy,"750",posy,width=1,fill="blue")
                feuillet.place(x='0',y='40')
                t=0
            feuillet.after(100,count_mesure)
        count_mesure()

    fen=Tk()
    fen.title("Courbe du flux")
    fen.geometry("1000x650+10+10")
    fen['bg']="AliceBlue"

    label_modele=Label(fen,text=modele,bg="Azure",fg="blue",font="ARIAL 16")
    label_modele.place(x='1',y='1')
    label_numero_de_serie=Label(fen,text=numeroDeSerie,bg="Azure",fg="blue",font="ARIAL 18")
    label_numero_de_serie.place(x='250',y='1')
    label_nom_de_fluide=Label(fen,text=nom_de_fluide,bg="Azure",fg="blue",font="ARIAL 18")
    label_nom_de_fluide.place(x='420',y='1')
    label_capacite=Label(fen,text=str(pleine_echelle)+" "+unite,bg="Azure",fg="blue",font="ARIAL 18")
    label_capacite.place(x='590',y='1')
    label_Kp=Label(fen,text="Kp",bg="Azure",fg="red",font="ARIAL 18")
    label_Kp.place(x='830',y='1')
    label_Ti=Label(fen,text="Ti",bg="Azure",fg="red",font="ARIAL 18")
    label_Ti.place(x='880',y='1')
    label_Td=Label(fen,text="Td",bg="Azure",fg="red",font="ARIAL 18")
    label_Td.place(x='930',y='1')    

    consigne=DoubleVar()
    valeur_pleine_echelle=pleine_echelle
    resolution_echelle=valeur_pleine_echelle/100
    rouleur=Scale(fen,variable=consigne,bg="white",troughcolor="red",from_=valeur_pleine_echelle, to =0,orient=VERTICAL,width=30,length=590,resolution=resolution_echelle,command=admission_consigne)
    rouleur.place(x='750',y='40')

    Kp=DoubleVar()
    rouleur_Kp=Scale(fen,variable=Kp,bg="white",troughcolor="Azure",from_=0, to=100,orient=VERTICAL,resolution=0.1,width=20,length=590,command=admission_Kp)
    rouleur_Kp.place(x='800',y='40')
    rouleur_Kp.set(Proportionnelle)

    Ti=DoubleVar()
    rouleur_Ti=Scale(fen,variable=Ti,bg="white",troughcolor="Azure",from_=0, to=10,orient=VERTICAL,resolution=0.01,width=20,length=590,command=admission_Ti)
    rouleur_Ti.place(x='850',y='40')
    rouleur_Ti.set(Integrale)

    Td=DoubleVar()
    rouleur_Td=Scale(fen,variable=Td,bg="white",troughcolor="Azure",from_=0, to=10,orient=VERTICAL,resolution=0.01,width=20,length=590,command=admission_Td)
    rouleur_Td.place(x='900',y='40')
    rouleur_Td.set(Derive)

    feuillet=Canvas(fen,width=750,height=680,bg="white")
    for bla in range(0,58):
        for ble in range(0,75):
            posx=str(60*bla)
            posy=str(30*ble)
            feuillet.create_line(posx,"0",posx,"600",width=1,fill="blue")
            feuillet.create_line("0",posy,"750",posy,width=1,fill="blue")
    feuillet.place(x='0',y='40')
    inc_label_consigne()
    inc_label_mesure()
    fen.mainloop()
