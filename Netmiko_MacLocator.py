from netmiko import ConnectHandler

SWITCH_ACTUAL = {"device_type": "cisco_ios","host": "192.168.1.1","username": "cisco","password": "cisco"}
               #b05c.da22.8039

#el switch local o en switch's vecinos, de no encontrarlo termina el programa.
#Retorna un puerto de forma abreviada.
def show_mac_address_table(conexion, mac):
    connection = ConnectHandler(**conexion)
    salida = connection.send_command("show mac address-table")
    hostname = connection.send_command("show running-config | include hostname")

    buscar = salida.find(mac) #.find devuelve un -1 si no encuentra el string
    
    if buscar != -1:
        puerto = salida.split(mac)[1].split()[1]
        if puerto == "FastEthernet1/0/48" or puerto == "FastEthernet1/0/48":
            print("Buscando...")
        else: 
            print("\nLa MAC:",mac, "se encuentra en el puerto", puerto, "del dispositivo", hostname[9::])
        return puerto
    else:
        print (f"\n Imposible Encontrar la mac. Pruebe Otra vez")
        return buscar

# Envia un show interface para obtener la interfaz completa donde se 
#ubica la dirección MAC
def show_interface(conexion, port):
    connection = ConnectHandler(**conexion)
    comando = "show interface " + port
    salida = connection.send_command(comando)

    interface = salida.split()[0]
    return interface
# Muestra la salida de show cdp neighbors detail, recorre la salida
#en busca de la interfaz donde se encontró la MAC, si se hace match regresa
#la IP de conexión hacia el dispositivo vecino. En caso de no hacer match, 
#regresa un -1 significando que no hay un vecino CDP en esa interfaz.
def cdp_neighbor_details(conexion, interface):
    connection = ConnectHandler(**conexion)
    salida = connection.send_command("show cdp neighbors detail")

    texto = "Interface: " + interface
    dispositivos = salida.split("-------------------------")
    
    for i in dispositivos:
        if texto in i:
              filtro = i.split("Platform")[0]
              segundofiltro = filtro.split("IP address: ")[1]
              print("Vecino encontrado en ", texto)
              return segundofiltro.strip()
    return -1

def nueva_conexion(IP):
    #print("\nConectando a ", IP) 
    SWITCH_VECINO = {"device_type": "cisco_ios","host": IP,"username": "cisco","password": "cisco",}
    return SWITCH_VECINO

mac_buscada = input('introduce la mac buscada en este formato "FFFF.FFFFF.FFFF": )')

while True: 
    PORT = show_mac_address_table(SWITCH_ACTUAL, mac_buscada)
    if PORT == -1:
        break
    INTERFACE = show_interface(SWITCH_ACTUAL, PORT)
    IP = cdp_neighbor_details(SWITCH_ACTUAL, INTERFACE)
    if IP == -1:
        break
    SWITCH_ACTUAL = nueva_conexion(IP)