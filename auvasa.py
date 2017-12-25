#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
from bs4 import BeautifulSoup
import requests

class Auvasa():

    #paradas = "http://www.auvasa.es/dataapp/Paradas.xml"
    #parada = "http://www.auvasa.es/rssparada.asp?codigo=%codigoParada%"
    #lineas = "http://www.auvasa.es/dataapp/Lineas.xml"
    #linea = "http://www.auvasa.es/rsstrayectos.asp?codigo=%linea%"
    #horarios = "http://www.auvasa.es/dataapp/Horarios.xml"
    #tarjeta = "http://2.139.171.116:3506/rsstarjeta.asp?codigo=%tarjeta%"
    #noticias = "http://www.auvasa.es/rss.asp"

    def paradaNum(codigoParada):
    	codigo1 = base64.b64encode(codigoParada)
    	codigo2 = base64.b64encode(codigo1)
    	urlParada = 'http://www.auvasa.es/rssparada.asp?codigo='+codigo2

        req = requests.get(urlParada)
        status_code = req.status_code
        if status_code == 200:
            xml = BeautifulSoup(req.text, "xml")

            titles = xml.find('title')
            titles = str(titles).replace('<title>', '')
            titles = titles.replace('</title>', '')
            print titles

            nombreParada = (xml.find('nombreparada')).encode("utf-8")
            nombreParada = str(nombreParada).replace('<nombreparada>', '')
            nombreParada = nombreParada.replace('</nombreparada>', '')
            print 'Nombre de la parada: '+nombreParada

            codigoParada = xml.find('codigoparada')
            codigoParada = str(codigoParada).replace('<codigoparada>', '')
            codigoParada = codigoParada.replace('</codigoparada>', '')
            print 'Codigo de parada: '+codigoParada

            coordenadaX = xml.find('ccX')
            coordenadaX = str(coordenadaX).replace('<ccX>', '')
            coordenadaX = coordenadaX.replace('</ccX>', '')
            print 'Coodenada X: '+coordenadaX

            coordenadaY = xml.find('ccY')
            coordenadaY = str(coordenadaY).replace('<ccY>', '')
            coordenadaY = coordenadaY.replace('</ccY>', '')
            print 'Coodenada Y: '+coordenadaY

            correspondencias = xml.find('correspondenciasparada')
            correspondencias = str(correspondencias).replace('<correspondenciasparada>', '')
            correspondencias = correspondencias.replace('</correspondenciasparada>', '')
            print 'Correspondencias: '+correspondencias

            print '\n'

            description = xml.find('description')
            description = str(description).replace('<description>', '')
            description = description.replace('</description>', '')
            print description

            items = xml.find_all('item')
            lineas = xml.find_all('linea')
            trayectos = xml.find_all('trayecto')
            tiempos = xml.find_all('tiempo')
            for i in range(0, len(items)):

                print 'Línea '+(lineas[i].get_text())
                print 'Trayecto: '+(trayectos[i].get_text())
                print 'Tiempo de espera: '+(tiempos[i].get_text())+' minutos'
                print '\n'


    def tarjetaNum(codigoTarjeta):
        codigo1 = base64.b64encode(codigoTarjeta)
        codigo2 = base64.b64encode(codigo1)
        urlTarjeta = 'http://2.139.171.116:3506/rsstarjeta.asp?codigo='+codigo2

        req = requests.get(urlTarjeta)
        status_code = req.status_code
        if status_code == 200:
            xml = BeautifulSoup(req.text, "xml")

            titles = xml.find('title')
            titles = str(titles).replace('<title>', '')
            titles = titles.replace('</title>', '')
            print titles

            description = xml.find('description')
            description = str(description).replace('<description>', '')
            description = description.replace('</description>', '')
            print description

            print 'ID de la tarjeta: '+codigoTarjeta

            saldo = xml.find('saldomonedero')
            saldo = str(saldo).replace('<saldomonedero>', '')
            saldo = saldo.replace('</saldomonedero>', '')
            print 'El saldo actual de la tarjeta es de: '+saldo+' euros.'
