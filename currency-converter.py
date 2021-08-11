import requests
import json
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


def get_rates(currency: str):
    global window
    global filepath
    window['status_text'].update("Requesting exchange rates...", text_color='white')
    window.refresh()
    try:
        response = requests.get(f'https://open.er-api.com/v6/latest/{currency}').json()
    except requests.ConnectionError:
        raise Exception("Failed to request exchange rates: No internet connection")
    except Exception as exception:
        raise Exception(f"Failed to request exchange rates: {exception}")
    try:
        file = open(filepath, 'r')
        rates = json.load(file)
    except OSError:
        rates = {}
    rates[currency] = response
    file = open(filepath, 'w')
    json.dump(rates, file, indent=4)
    file.close()
    return dict(rates[currency])


def convert(input: float, input_currency: str, output_currency: str):
    global window
    global filepath
    try:
        input_currency = input_currency.upper()
        output_currency = output_currency.upper()
        try:
            with open(filepath, 'r') as file:
                info = json.load(file)[input_currency]
            if datetime.timestamp(datetime.now()) - info['time_last_update_unix'] > 86400:
                raise KeyError
        except (KeyError, FileNotFoundError):
            info = get_rates(input_currency)
        rates = dict(info['rates'])
        currencies = list(rates.keys())
        window['input_currency'].update(input_currency, values=currencies, size=(6, None))
        window['output_currency'].update(output_currency, values=currencies, size=(6, None))
        last_updated = datetime.fromtimestamp(info['time_last_update_unix']).replace(tzinfo=tz.tzutc())
        window['status_text'].update(f"Last updated: {last_updated.astimezone(tz.tzlocal()).strftime('%Y-%m-%d %H:%M:%S')}", text_color='white')
        return round(float(input) * rates[output_currency], 4)
    except Exception as error:
        show_error(error)
        return ''


def show_error(error):
    global window
    window['status_text'].update(error, text_color='red')


filepath = 'rates.json'
window = sg.Window("Currency Converter", layout)
event, values = window.read(0)
window['output'].update(convert(values['input'], values['input_currency'], values['output_currency']))
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'input' and values['input'] != '' and values['input'][-1] not in '0123456789.':
        window['input'].update(values['input'][:-1])
    elif event == 'convert':
        if values['input'] == '':
            show_error("Please enter an amount")
            window['output'].update('')
        else:
            window['output'].update(convert(values['input'], values['input_currency'], values['output_currency']))
window.close()
