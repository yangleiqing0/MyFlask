import requests
import time

class MethodRequest:

    def __init__(self):
        pass

    def request_value(self, method, url, data, headers):
        headers.update({'Connection': 'close'})
        print('请求方法: ', method, url, data, headers, type(url))
        requests.adapters.DEFAULT_RETRIES = 51
        requests.session().keep_alive = False
        try:
            if method.upper() == 'GET':
                if 'https' in url:
                    print('True')
                    result = requests.get(url, headers=headers, verify=False).text
                else:
                    result = requests.get(url, headers=headers).text
            elif method.upper() == 'POST':
                if 'https' in url:
                    result = requests.post(url, data=data, headers=headers, verify=False).text
                else:
                    result = requests.post(url, data=data, headers=headers).text
            elif method.upper() == 'PUT':
                if 'https' in url:
                    result = requests.put(url, data=data, headers=headers, verify=False).text
                else:
                    result = requests.put(url, data=data, headers=headers).text
            elif method.upper() == 'DELETE':
                if 'https' in url:
                    result = requests.delete(url, data=data, headers=headers, verify=False).text
                else:
                    result = requests.delete(url, data=data, headers=headers).text
            else:
                result = "请求方法不正确"
        except Exception as e:
            print(e)
            time.sleep(0.5)
            result = "解析请求结果失败 : %s" %e

        return result
