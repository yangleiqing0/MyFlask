import requests


class MethodRequest:

    def __init__(self):
        pass

    @staticmethod
    def request_value(method, url, data, headers):
        print('请求方法: ', method, url, data, headers)
        try:
            if method.upper() == 'GET':
                if 'https' in url:
                    result = requests.get(url, headers=headers, verify=False).text
                else:
                    result = requests.get(url, headers=headers).text
            elif method.upper() == 'POST':
                if 'https' in url:
                    result = requests.post(url, data=data, headers=headers, verify=False).text
                else:
                    result = requests.get(url, data=data, headers=headers).text
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
            result = "解析请求结果失败 : %s" %e

        return result
