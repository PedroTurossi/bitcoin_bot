import ssl
import json

import bitstamp.client
import websocket

import credenciais

def cliente():
    return bitstamp.client.Trading(username=credenciais.username, key=credenciais.key, secret=credenciais.secret)

def comprar(quantidade):
    cliente = cliente()
    cliente.buy_market_order(quantidade)

def vender(quantidade):
    cliente = cliente()
    cliente.sell_market_order(quantidade)

def ao_abrir(ws):
    print('abriu')

    json_subscribe = """
{
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}
"""

    ws.send(json_subscribe)

def ao_fechar(ws):
    print('fechou')

def ao_receber_mensagem(ws, mensagem):
    mensagem = json.loads(mensagem)
    price = mensagem['data']['price']
    print('USD', price)

    if price > 90000:
        vender()
    elif price < 87000:
        comprar()
    else:
        print('Aguardando')

def erro(ws, erro):
    print('Erro - ', erro)


if __name__ == '__main__':
    ws = websocket.WebSocketApp('wss://ws.bitstamp.net',
                                on_open=ao_abrir,
                                on_close=ao_fechar,
                                on_message=ao_receber_mensagem,
                                on_error=erro)
    ws.run_forever(sslopt={'cert_regs': ssl.CERT_NONE})