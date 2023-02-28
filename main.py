#!/usr/bin/env python

import datetime
import sys
from crontab import CronTab
import os
import subprocess



def horaDeUsoDeAplicacion(programa):
    os.system(f"echo $(ps ax -o start,comm | grep {programa}) > /home/usuario/Escritorio/proyecto/horas.txt")
    file = open('/home/usuario/Escritorio/proyecto/horas.txt','r')
    linea = file.readline()
    if linea == '\n': #el programa no está abierto
        pass
    else: #el programa está abierto
        lineaHora = linea.split()[0]
        horasInicio = lineaHora.split(':')[0]
        minutosInicio= lineaHora.split(':')[1]
        tiempoInicio = float(horasInicio) + float(minutosInicio) / 60
        #obtengo la hora actual
        os.system("echo $(date) > /home/usuario/Escritorio/proyecto/tiempoActual.txt")
        archivoTiempoActual = open('/home/usuario/Escritorio/proyecto/tiempoActual.txt', 'r')
        linea = archivoTiempoActual.readline()
        hora = linea.split()[4]
        horasFinal = hora.split(':')[0]
        minutosFinal = hora.split(':')[1]
        tiempoFinal = float(horasFinal) + float(minutosFinal) / 60
        #calculo el tiempo usado
        tiempoUsado = tiempoFinal - tiempoInicio
        #obtengo el registro de tiempo usado semanal
        archivoRegistroTiempoUsado =  open('/home/usuario/Escritorio/proyecto/registroTiempoUsadoSpotify.txt')
        lineaRegistro = archivoRegistroTiempoUsado.readline()
        registroHora = float(lineaRegistro)
        #le sumo el tiempo usado actual
        tiempoUsadoTotal = registroHora + tiempoUsado
        os.system(f"echo {tiempoUsadoTotal} > /home/usuario/Escritorio/proyecto/registroTiempoUsadoSpotify.txt")
        limiteSemanal = float(sys.argv[2])
        #me fijo si se ha superado el limite
        if (tiempoUsadoTotal > limiteSemanal):
            os.system(f"DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus /usr/bin/notify-send 'Limite semanal superado' 'Has superado tu limite semanal para {programa}'")
            archivoContadorNotis = open('/home/usuario/Escritorio/proyecto/contadorNotisLimite.txt', 'r')
            lineaContador = archivoContadorNotis.readline()
            contadorNotis = int(lineaContador)
            contadorNotis += 1
            os.system(f"echo {contadorNotis} > /home/usuario/Escritorio/proyecto/contadorNotisLimite.txt")
            #si el limite se ha superado, me fijo cuantos veces se le avisó al usuario y si son mas de 2, se procede a cerrar el programa.
            if contadorNotis > 2:
                os.system(f"killall {programa}")


horaDeUsoDeAplicacion(sys.argv[1])
