import requests, json
from datetime import datetime
from dateutil import tz
import PySimpleGUI as sg

sg.theme("Black")

layout = [
    [sg.Text("Input currency")],
    [sg.Combo(['CAD', 'USD'], size=(6, None), key='input_currency', default_value='USD', readonly=True), sg.Input('1', key='input', size=(30, 1), focus=True, enable_events=True)],
    [sg.Text("Output currency")],
    [sg.Combo(['CAD', 'USD'], size=(6, None), key='output_currency', default_value='CAD', readonly=True), sg.Input('', key='output', size=(30, 1), readonly=True, disabled_readonly_background_color='black')],
    [sg.Text(key='status_text', size=(35, 2))],
    [sg.Button("Convert", key='convert')]
]

def GetRates(currency: str):
    global window
    global filePath
    window['status_text'].update("Requesting exchange rates...", text_color='white')
    window.refresh()
    try:
        response = requests.get(f'https://open.er-api.com/v6/latest/{currency}').json()

    except requests.ConnectionError:
        raise Exception("Failed to request exchange rates: No internet connection")

    except Exception as exception:
        raise Exception(f"Failed to request exchange rates: {exception}")

    try:
        ratesFile = open(filePath, 'r')
        rates = json.load(ratesFile)

    except:
        rates = {}

    rates[currency] = response
    ratesFile = open(filePath, 'w')
    json.dump(rates, ratesFile, indent=4)
    ratesFile.close()
    return dict(rates[currency])

def Convert(input: float, input_currency: str, output_currency: str):
    global window
    global filePath
    try:
        input_currency = input_currency.upper()
        output_currency = output_currency.upper()
        try:
            with open(filePath, 'r') as ratesFile:
                info = json.load(ratesFile)[input_currency]

            if  datetime.timestamp(datetime.now()) - info['time_last_update_unix'] > 86400:
                raise KeyError

        except (KeyError, FileNotFoundError):
            info = GetRates(input_currency)

        rates = dict(info['rates'])
        currencies = list(rates.keys())
        window['input_currency'].update(input_currency, values=currencies, size=(6, None))
        window['output_currency'].update(output_currency, values=currencies, size=(6, None))
        lastUpdated = datetime.fromtimestamp(info['time_last_update_unix']).replace(tzinfo=tz.tzutc())
        window['status_text'].update(f"Last updated: {lastUpdated.astimezone(tz.tzlocal()).strftime('%Y-%m-%d %H:%M:%S')}", text_color='white')
        return round(float(input) * rates[output_currency], 4)
    
    except Exception as error:
        Error(error)
        return ''

def Error(error):
    global window
    window['status_text'].update(error, text_color='red')

filePath = 'rates.json'
window = sg.Window("Currency Converter", layout)
event, values = window.read(0)
window['output'].update(Convert(values['input'], values['input_currency'], values['output_currency']))
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    elif event == 'input' and values['input'] != '' and values['input'][-1] not in '0123456789.':
        window['input'].update(values['input'][:-1])

    elif event == 'convert':
        if values['input'] == '':
            Error("Please enter an amount")
            window['output'].update('')

        else:
            window['output'].update(Convert(values['input'], values['input_currency'], values['output_currency']))

window.close()