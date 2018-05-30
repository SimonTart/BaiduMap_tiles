import requests
import logging

def getProxy():
    proxy = requests.get('http://127.0.0.1:5010/get').text
    return proxy

def deleteProxy(proxy):
    requests.get('http://127.0.0.1:5010/delete?proxy={}'.format(proxy))

def getProxyStatus():
    return requests.get('http://127.0.0.1:5010/get_status').content


def request(method, url, **kwargs):
    proxyCount = 20
    proxy = getProxy()
    while True:
        proxy = getProxy()
        try:
            res = requests.request(method, url, timeout = 3, proxies={'http': 'http://{}'.format(proxy)}, **kwargs)
            if res.status_code == 200:
                return res
        except Exception as e:
            logging.error('IP  Not Availble')
            deleteProxy(proxy)
            

    logging.error('Proxy Not Availble', extra = getProxyStatus())
    logging.info('Proxy Not Availble, Using Local Network')
    ravenClient.captureMessage('Proxy Not Availble, Using Local Network')
    return requests.request(method, url, **kwargs)

def get(url, **kwargs):
    return request('get', url, **kwargs)