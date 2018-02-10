#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
from bs4 import BeautifulSoup
import requests
import codecs

class Auvasa():

    #paradas = "http://www.auvasa.es/dataapp/Paradas.xml"
    #parada = "http://www.auvasa.es/rssparada.asp?codigo=%codigoParada%"
    #lineas = "http://www.auvasa.es/dataapp/Lineas.xml"
    #linea = "http://www.auvasa.es/rsstrayectos.asp?codigo=%linea%"
    #horarios = "http://www.auvasa.es/dataapp/Horarios.xml"
    #tarjeta = "http://2.139.171.116:3506/rsstarjeta.asp?codigo=%tarjeta%"
    #noticias = "http://www.auvasa.es/rss.asp"

    def novedades(self):
        urlNovedades = 'http://www.auvasa.es/rss.asp'
        s = ''
        req = requests.get(urlNovedades)
        req.encoding = 'utf-8'
        status_code = req.status_code
        if status_code == 200:
            xml = BeautifulSoup(req.text, "xml")

            description = xml.find('description')
            description = str(description).replace('<description>', '')
            description = description.replace('</description>', '')
            s += '🆕 '+description+' 🆕'+'\n\n'

            title = xml.find_all('title')
            description = xml.find_all('description')

            for i in range(1, 4):
                s += '🔴 '+(title[i].get_text()).encode('utf-8')+'\n\n'
                desc = (description[i].get_text()).encode('utf-8')
                desc = desc.replace('<BR>', '\n')
                s += desc
                s += '\n\n'

            return s

    def tarjetaNum(self,codigoTarjeta):
        codigo1 = base64.b64encode(codigoTarjeta)
        codigo2 = base64.b64encode(codigo1)
        urlTarjeta = 'http://2.139.171.116:3506/rsstarjeta.asp?codigo='+codigo2
        s = ''
        req = requests.get(urlTarjeta)
        status_code = req.status_code
        if status_code == 200:
            xml = BeautifulSoup(req.text, "xml")

            titles = xml.find('title')
            titles = str(titles).replace('<title>', '')
            titles = titles.replace('</title>', '')
            s += titles+'\n'

            description = xml.find('description')
            description = str(description).replace('<description>', '')
            description = description.replace('</description>', '')
            s += description+'\n'

            s += 'ID de la tarjeta: '+codigoTarjeta+'\n'

            saldo = xml.find('saldomonedero')
            saldo = str(saldo).replace('<saldomonedero>', '')
            saldo = saldo.replace('</saldomonedero>', '')
            s += 'El saldo actual de la tarjeta es de: '+saldo+' 💶 euros.'+'\n'

            if(description == 'NODATA'):
                s = '❌ El número de la tarjeta introducido es incorrecto.'

            return s

    def numLinea(self, codigoLinea):
        urlLinea = 'http://www.auvasa.es/rsstrayectos.asp?codigo='+codigoLinea
        r = ''

        req = requests.get(urlLinea)
        req.encoding = 'utf-8'
        status_code = req.status_code
        if status_code == 200:
            xml = BeautifulSoup(req.text, "xml")

            linea = xml.find('Línea')
            linea = str(linea).replace('<Línea>', '')
            linea = linea.replace('</Línea>', '')
            r += '🚌'+linea+'\n'

            items = xml.find_all('OrdenTrayecto')
            ordenes = xml.find_all('OrdenParada')
            paradas = xml.find_all('Parada')
            codigos = xml.find_all('Codigo')

            resultado1 = 'TRAYECTO 1 ➡️\n'
            resultado2 = 'TRAYECTO 2 ⬅️\n'

            if(linea == 'U8' or linea == 'U1' or linea == 'C1' or linea == 'C2'):
                resultado1 = 'TRAYECTO ÚNICO ➡️\n'
            if(linea == 'M1' or linea == 'M2' or linea == 'M3' or linea == 'M4' or linea == 'M5' or linea == 'M6' or linea == 'M7'):
                resultado1 = 'TRAYECTO ÚNICO ➡️\n'
            if(linea == 'P1' or linea == 'P2' or linea == 'P3' or linea == 'P6' or linea == 'P7' or linea == 'P13' or linea == 'PSC1' or linea == 'PSC2' or linea == 'PSC3'):
                resultado1 = 'TRAYECTO ÚNICO ➡️\n'

            for i in range(0, len(items)):

                if((items[i].get_text()).encode('utf-8') == '1'):
                    resultado1 += '🚏'+(ordenes[i].get_text()).encode('utf-8')+' '
                    resultado1 += 'Parada: '+(paradas[i].get_text()).encode('utf-8')+'\n'
                    resultado1 += '🔢Código de la parada: '+(codigos[i].get_text()).encode('utf-8')
                    resultado1 += '\n'

                if((items[i].get_text()).encode('utf-8') == '2'):
                    resultado2 += '🚏'+(ordenes[i].get_text()).encode('utf-8')+' '
                    resultado2 += 'Parada: '+(paradas[i].get_text()).encode('utf-8')+'\n'
                    resultado2 += '🔢Código de la parada: '+(codigos[i].get_text()).encode('utf-8')
                    resultado2 += '\n'

            if(linea == 'U8' or linea == 'U1' or linea == 'C1' or linea == 'C2'):
                resultado2 = ''
            if(linea == 'M1' or linea == 'M2' or linea == 'M3' or linea == 'M4' or linea == 'M5' or linea == 'M6' or linea == 'M7'):
                resultado2 = ''
            if(linea == 'P1' or linea == 'P2' or linea == 'P3' or linea == 'P6' or linea == 'P7' or linea == 'P13' or linea == 'PSC1' or linea == 'PSC2' or linea == 'PSC3'):
                resultado2 = ''

            if(linea == 'None'):
                error = 1
            else:
                error = 0

            return r, resultado1, resultado2, error

    def search(self,myDict, lookup):
        for key, value in myDict.items():

            value = (value).lower()

            lookup = lookup.lower()

            if lookup in value:

                return key
        else:
            return None

    def paradaNum(self, codigoParada):
        if not codigoParada.isdigit():
            d = {}
            with codecs.open("paradas.txt", "r", "utf-8") as f:
                for line in f:
                    (key, val) = line.split(':')
                    d[int(key)] = val

            codigoParada = str(self.search(d,codigoParada))

        if codigoParada != None:

            codigo1 = base64.b64encode(codigoParada)
            codigo2 = base64.b64encode(codigo1)
            urlParada = 'http://www.auvasa.es/rssparada.asp?codigo='+codigo2
            r = ' '
            req = requests.get(urlParada)
            req.encoding = 'utf-8'
            status_code = req.status_code
            if status_code == 200:
                xml = BeautifulSoup(req.text, "xml")

                titles = xml.find('title')
                titles = str(titles).replace('<title>', '')
                titles = titles.replace('</title>', '')
                r += titles+'\n'

                nombreParada = xml.find('nombreparada')
                nombreParada = str(nombreParada).replace('<nombreparada>', '')
                nombreParada = nombreParada.replace('</nombreparada>', '')
                r += '🚏Nombre de la parada: '+nombreParada+'\n'

                codigoParada = xml.find('codigoparada')
                codigoParada = str(codigoParada).replace('<codigoparada>', '')
                codigoParada = codigoParada.replace('</codigoparada>', '')
                r += '🔢Código de parada: '+codigoParada+'\n'

                lon = xml.find('ccX')
                lon = str(lon).replace('<ccX>', '')
                lon = lon.replace('</ccX>', '')

                lat = xml.find('ccY')
                lat = str(lat).replace('<ccY>', '')
                lat = lat.replace('</ccY>', '')

                correspondencias = xml.find('correspondenciasparada')
                correspondencias = str(correspondencias).replace('<correspondenciasparada>', '')
                correspondencias = correspondencias.replace('</correspondenciasparada>', '')
                r += 'Correspondencias: '+correspondencias+'\n'

                r += '\n'

                description = xml.find('description')
                description = str(description).replace('<description>', '')
                description = description.replace('</description>', '')
                if description!= "NODATA":
                    r += description+'\n'
                else:
                    r+= "❌🚌 No se esperan autobuses en los próximos minutos"
                items = xml.find_all('item')
                lineas = xml.find_all('linea')
                trayectos = xml.find_all('trayecto')
                tiempos = xml.find_all('tiempo')

                for i in range(0, len(items)):

                    r += '🚌Línea '+(lineas[i].get_text()).encode('utf-8')
                    r += ' Trayecto: '+(trayectos[i].get_text()).encode('utf-8')+'\n'
                    r += '🕓Tiempo de espera: '+(tiempos[i].get_text()).encode('utf-8')+' minutos'
                    r += '\n\n'

                return r, (lat, lon)
