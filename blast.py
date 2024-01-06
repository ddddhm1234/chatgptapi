"""
填入FOFA_KEY，调用blast方法即可自动寻找可用的chatgpt api
"""

FOFA_KEY = {
    "email": "",
    "key": ""
}

import requests
import json
import base64
import chatgpt

def get_result(query="", size=2000, fields="host,ip,port,country_name,region,city,lastupdatetime,banner,as_organization"):
    def list2dict(keys, values):
        return [dict(zip(keys, value)) for value in values]

    results = []
    url = "https://fofa.info/api/v1/search/all?email=your_email&key=your_key&qbase64=your_base64&size=your_size" \
          "&fields=your_fields"
    m_url = url.replace("your_email", FOFA_KEY["email"])
    m_url = m_url.replace("your_key", FOFA_KEY["key"])
    m_url = m_url.replace("your_base64", base64.encodebytes(query.encode()).decode())
    m_url = m_url.replace("your_fields", fields)
    m_url = m_url.replace("your_size", str(size))
    result = json.loads(requests.get(m_url).content.decode("utf8"))
    columns = fields.split(",")
    results += list2dict(columns, result["results"])
    while (len(results) < result["size"]):
        result = json.loads(requests.get(m_url + "&page=" + str(int(result["page"]) + 1)).content.decode("utf8"))
        if result["error"]:
            break
        results += list2dict(columns, result["results"])
    return results

def blast():
    result = get_result('title="chatgpt api demo"')
    for item in result:
        host = item["host"]
        if not host.startswith("http"):
            host = "http://" + host
        api = host + "/api/generate"
        gpt = chatgpt.ChatGPT(api)
        if gpt.is_ok():
            print("[√]", api)
        else:
            print("[x]", api)

blast()
