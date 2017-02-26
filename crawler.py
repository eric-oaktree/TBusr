#!/usr/bin/python3
##T-Tracker
#<agency tag="mbta" title="MBTA" regionTitle="Massachusetts"/>
#<route tag="501" title="501"/>
#501outbound <stop tag="914" title="Washington St opp Montfern Ave" lat="42.3499599" lon="-71.1648699" stopId="00914"/>
#501inbound <stop tag="977" title="Washington St @ Montfern Ave" lat="42.3498999" lon="-71.16452" stopId="00977"/>

#<route tag="503" title="503"/>
#503outbound <stop tag="914" title="Washington St opp Montfern Ave" lat="42.3499599" lon="-71.1648699" stopId="00914"/>
#503inbound <stop tag="977" title="Washington St @ Montfern Ave" lat="42.3498999" lon="-71.16452" stopId="00977"/>

#<route tag="57" title="57"/>
#57outbound <stop tag="977" title="Washington St @ Montfern Ave" lat="42.3499" lon="-71.16452" stopId="00977"/>
#57inbound <stop tag="914" title="Washington St opp Montfern Ave" lat="42.3499599" lon="-71.1648699" stopId="00914"/>


#http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=mbta&stopId=00977


import datetime, requests, re, os
import bs4

cwd = os.getcwd()
routeReg = re.compile(r'routeTitle="(\d+)"')

def grabber(stop):
    feed = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=mbta&stopId=' + stop)
    if feed.status_code == requests.codes.ok:
        xml = open('bus.xml', 'w')
        xml.write(feed.text)
        xml.close()
    else:
        print('API Error')

def active_routes():
    routes = {}
    xmlf = open('bus.xml', 'r')
    xml = xmlf.read()
    soup = bs4.BeautifulSoup(xml, 'xml')
    preds = soup.find_all('predictions')
    for pred in preds:
        pred_attr = dict(pred.attrs)
        route = pred_attr['routeTitle']
        active = pred_attr.get('dirTitleBecauseNoPredictions', 'Active')
        if active != 'Active':
            active = 'Inactive'
        routes[route] = active
    return routes

def next_bus():
    routeDict = {}
    xmlf = open('bus.xml', 'r')
    xml = xmlf.read()
    soup = bs4.BeautifulSoup(xml, 'xml')
    preds = soup.find_all('predictions')
    for pred in preds:
        busDict = {}
        pred_attr = dict(pred.attrs)
        route = pred_attr['routeTitle']
        active = pred_attr.get('dirTitleBecauseNoPredictions', 'Active')
        if active != 'Active':
            active = 'Inactive'
        if active == 'Active':
            busList = pred.find_all('prediction')
            bus1Dict = dict(busList[0].attrs)
            bus2Dict = dict(busList[1].attrs)
            busDict['next'] = bus1Dict['seconds']
            busDict['after'] = bus2Dict['seconds']
            routeDict[route] = busDict
        else:
            routeDict[route] = 'Inactive'
    return routeDict
