import os 
## Direcorio de instalación del API de python de freeling
directoriofreeling= (os.environ ['FREELING_PYTHON'] )
directorio = directoriofreeling +"/APIs/python"
import sys
sys.path.append( directorio  )
import freeling
import subprocess
import simplejson as json

def obtenersentidos(linea):
  #print ("respuesta: "+ respuesta);
  #print("entro")
  inisen =respuesta.find('-')-8;
  if( respuesta.find(':') >=0):
    sentidos = respuesta[inisen:];
    print ("sentidosproducto: "+ sentidos);
    sentidos=sentidos.split(':0/');
    #print("HOLA")
  else:
    sentidos=""

  return sentidos

def freelingsentidos(frase):
  command= "echo \"" + frase+ "\" | analyzer_client localhost:50006 "
  #print("command " +command)
  respuesta = subprocess.check_output(command, shell=True)
  r= str(respuesta)
  respuesta=respuesta.decode("utf-8")
  respuesta=respuesta.split('\n')
  respuesta=respuesta[0]
  return respuesta

def freelingsentidosFrase(frase):
  command= "echo \"" + frase+ "\" | analyzer_client localhost:50006 "
  #print("command " +command)
  respuesta = subprocess.check_output(command, shell=True)
  r= str(respuesta)
  respuesta=respuesta.decode("utf-8")
  respuesta=respuesta.split('\n')
  respuesta=respuesta[3]
  return respuesta


DATA = directoriofreeling +"/data";
LANG="/es";
freeling.util_init_locale("default");
#Semantic Database Module
semantic = freeling.semanticDB (DATA + LANG +"/semdb.dat");

#Conjunto de ACCIONES
#acciones = ['consultar', 'realizar', 'ayuda', 'devolver', 'pagar', 'modificar' ]
#acciones_sinonimos = ['consultar','ejecutar','realizar','causar','crear','hacer','realizar','organizar','realizar','efectuar','cumplir',' modificar','alterar','cambiar','','alterar','arreglar','pagar','avalar','subvencionar','abonar','liquidar','costear','dar','devengar','rendir','compensar','enmendarse',
#'expiar','ayudar','auxiliar','asistir','devolver','reponer','llevar_de_regreso','regresar','traer_de_regreso','reembolsar','volver_a_pagar','reembolsar']

#Conjunto de PRODUCTOS
#productos = ['transferencia', 'tarjeta', 'movimiento' , 'recibo' , 'contraseña', 'seguro']
productos_sinonimos = ['transferencia', 'tarjeta', 'movimiento' , 'recibo' , 'contraseña' ,'transferir','transportar','trasladar','transferir','transportar','trasladar','transferir','transferir','pasar','transferir','pasar','transferir','transmitir','transferir','transmitir','entregar','presentar','transferir','traspasar','transferir'];
acciones_transferencia= ['transferir','transportar','trasladar','transferir','transportar','trasladar','transferir','transferir','pasar','transferir','pasar','transferir','transmitir','transferir','transmitir','entregar','presentar','transferir','traspasar','transferir'];


productos=['agenda de contacto', 'foto', 'etf', 'carteras gestionadas', 'warrants', 'claves', 'alertas y notificaciones', 'pias', 'área personal', 'ote', 'configuración personalizada', 'depósitos', 'carteras asesoradas', 'colabor@', 'correspondencia virtual', 'impuestos', 'sicavs', 'oasys', 'moneda extranjera', 'talonarios', 'extacto mensual', 'cajero/oficina', 'remesas', 'otros dispositivos', 'cuentas', 'transferencias', 'recibos / adeudos', 'carteras', 'traspasos', 'fondo de inversión', 'reembolso', 'seguros', 'recibos no domiciliado', 'transferencias/traspasos', 'comisiones', 'valores', 'cheques', 'traspasos a tarjeta', 'europlazo', 'movimientos', 'movimiento', 'tarjeta', 'divisas', 'préstamos', 'efectivo móvil', 'fondos de inversión / planes de pensiones', 'alias', 'recarga de móvil', 'iban',  'datos personales', 'ppa', 'alta', 'alertas', 'operaciones ágiles', 'hipoteca', 'plan de pensiones', 'posición global', 'gráficos']
acciones=['movimientos', 'registrado', 'usuario', 'anular', 'hipoteca', 'modificar', 'seguros', 'cliente', 'opv', 'asesoramiento', 'extracto mensual', 'operaciones', 'seguridad', 'depósitos', 'planes', 'simular', 'consulta','consulta', 'realizar', 'cuentas', 'tarjetas', 'fondos', 'consulta de mercado', 'operar', 'gestionar', 'alertas', 'transferencias', 'área_personal', 'valores', 'contratar']

fichero = open('../extractorIntencionSuperbuscador/fich.csv')

entrada=fichero.readline();
entrada=entrada.replace(' ','')
#print (" entrada " +entrada)
intencion= entrada.split("|");
#Leo el fichero
while entrada:
  sentidosaccion=""
  sentidosproducto=""
  producto_inferido=""
  accion_inferida=""
  # ANALIZO LA ACCION DE LA INTENCIÓN
  accion= intencion[0].lower().replace(' ','')
  #print("accion " +accion)
  if(accion!=""):
    respuesta=freelingsentidosFrase("Yo voy a " +accion + ".")
    sentidosaccion=obtenersentidos(respuesta)
    sentidosproducto=""
    producto_inferido=""
    accion_inferida=""

  contsen=0
  while accion_inferida=="" and contsen<len(sentidosaccion):
    sen  = sentidosaccion[contsen]
    #print ("Sentido: "+ sen)
    #Obtengo la info del sentido
    senseinfo = semantic.get_sense_info (sen)
    #Obtengo los SINONIMOS
    sinos= senseinfo.words;
    #Miro con cual de las acciones se corresponde la accion extraida
    #Comparo todas las acciones con todos los sinonimos
    contsin=0;
    while accion_inferida=="" and contsin<len(sinos):
      sino=sinos[contsin]
      for a in acciones:
        if a==sino:
          accion_inferida=a
          #print ("Accion inferida: " +accion_inferida)

      #Si no he encontrado una accion asociada, busco en las acciones sinonimos de transferencias
      contactra=0
      if accion_inferida=="":
        while producto_inferido=="" and contactra<len(acciones_transferencia):
          t=acciones_transferencia[contactra]
          if t==sino:
            producto_inferido="transferencia"
            #print ("Producto inferido: " + producto_inferido)
          contactra=contactra+1

      contsin=contsin+1

    contsen=contsen+1


  # ANALIZO EL PRODUCTO DE LA INTENCIÓN
  producto= intencion[1].lower().replace(' ','')
  #print("producto " +producto)

  #Compruebo si es plural
  respuesta=freelingsentidos(producto + ".")
  print("respuestas " +respuesta)
  if(respuesta.find('NCFP000')>=0):
    #print("entro " +producto[:len(producto)-2] )
    respuesta=freelingsentidos( producto[:len(producto)-1] + "." )
    print("respuestas " +respuesta)
    sentidosproducto=obtenersentidos(respuesta)
    if(sentidosproducto==""):
      respuesta=freelingsentidos( producto[:len(producto)-2] + "." )
      sentidosproducto=obtenersentidos(respuesta)
  else:
    sentidosproducto=obtenersentidos(respuesta)

  contsen=0 
  print("n sent " + str(len(sentidosproducto))) 
  while producto_inferido=="" and contsen<len(sentidosproducto) and sentidosproducto!="":
    sen  = sentidosproducto[contsen]
    #print ("Sentido: "+ sen)
    #Obtengo la info del sentido
    senseinfo = semantic.get_sense_info (sen)
    #Obtengo los SINONIMOS
    sinos= senseinfo.words;
    #for sino in sinos:
      #print ("  sinonimo: " + sino)
    #Miro con cual de las acciones se corresponde la accion extraida
    #Comparo todas las acciones con todos los sinonimos
    contsin=0;
    while producto_inferido=="" and contsin<len(sinos):
      sino=sinos[contsin]
      for a in productos:
        if a==sino:
          producto_inferido=a
          #print ("Producto inferido: " + producto_inferido)
      contsin=contsin+1
    contsen=contsen+1
  #Extraigo los parámetros, pero no hago nada con ellos
  parametros=intencion[2].lower().replace(' ' ,'')
  #print("parametros " +parametros)

  resultado = json.dumps({"accions" :accion_inferida, "producto": producto_inferido, "parametro": parametros} );
  print (resultado)


  entrada=fichero.readline();
  #print (" entrada " +entrada)
  intencion= entrada.split("|");

fichero.close()
