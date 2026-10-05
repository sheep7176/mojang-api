import os
import json
import base64
import requests
from datetime import datetime

def Get_data(username, usernameurl, outtime, steve, alex):
    try:
        return_data = requests.get(usernameurl , timeout=outtime)
    except requests.RequestException as e:
        print(f"错误:请求失败 {e}")
        return None
    if return_data.status_code == 200:
        usernamedata = return_data.json()
        uuid = usernamedata.get("id")
        uuidurl = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        username = usernamedata.get("name")
        try:
            return_data = requests.get(uuidurl, timeout=outtime)
        except requests.RequestException as e:
            print(f"错误:请求失败 {e}")
            return None
        if return_data.status_code == 200:
            uuiddata = return_data.json()
            properties = uuiddata.get("properties", [])
            if not properties:
                print(f"用户名:{username}\nUUID:{uuid}\n错误:该玩家没有设置皮肤。")
                return None
            value = properties[0].get("value")   # ← 复用 properties，不重复请求
            system_time = datetime.now()
            value_b64 = base64.b64decode(value)
            value_b64_json = value_b64.decode('utf-8')
            value_json = json.loads(value_b64_json)
            value_timestamp = value_json.get("timestamp" , 0)
            value_timestamp_datetime = datetime.fromtimestamp(value_timestamp / 1000)
            value_SKIN_url = value_json.get("textures", {}).get("SKIN", {}).get("url" , "")
            value_SKIN_model = value_json.get("textures", {}).get("SKIN", {}).get("metadata", {}).get("model" , "classic")
            value_CAPE_url = value_json.get("textures", {}).get("CAPE", {}).get("url", None)
            the_other_model = f"[{value_SKIN_model}(未知)]"
            if value_SKIN_model == "classic":
                value_SKIN_model_name = f"classic{steve}"
            elif value_SKIN_model == "slim":
                value_SKIN_model_name = f"slim{alex}"
            else:
                value_SKIN_model_name = f"unknown{the_other_model}"
            if value_json.get("profileId") == uuid and value_json.get("profileName") == username:
                return username, uuid, value_SKIN_url, value_SKIN_model ,value_SKIN_model_name, value_timestamp_datetime, value_CAPE_url, system_time
            else:
                print("错误:请重试")
                return None
        else:
            print("错误:无法获取皮肤数据,请检查UUID是否正确。")
            return None
    elif return_data.status_code == 404:
        print("错误:用户名不存在,请检查用户名是否正确。")
        return None
    elif return_data.status_code == 429:
        print("错误:请求过于频繁,请稍后再试。")
        return None
    elif return_data.status_code == 500:
        print("错误:请重试")
        return None
    elif return_data.status_code == 503:
        print("错误:服务器维护中,请稍后再试。")
        return None
    else:
        print(f"错误:未知错误,状态码:{return_data.status_code}")
        return None

def Download_SKIN(value_SKIN_url, value_SKIN_model, username , outtime):
    if not value_SKIN_url:
        print("错误:无法下载皮肤图片,请检查皮肤链接是否正确。")
        return False
    try:
        return_data = requests.get(value_SKIN_url, timeout=outtime)
        return_data.raise_for_status()
        SKIN_data = return_data.content
        if SKIN_data[:4] == b"\x89PNG":
            ext = "png"
        elif SKIN_data[:4] == b"GIF8":
            ext = "gif"
        elif SKIN_data[:3] == b"\xff\xd8\xff":
            ext = "jpg"
        else:
            ext = "png"
        SKIN_name = f"{username}_{value_SKIN_model}.{ext}"
        SKIN_folder = os.path.dirname(os.path.abspath(__file__))
        SKIN_path = os.path.join(SKIN_folder, SKIN_name)
        with open(SKIN_path, "wb") as f:
            f.write(SKIN_data)
        print(f"成功:皮肤图片已下载到: {SKIN_path}\n")
        return True
    except requests.RequestException as e:
        print(f"错误:请求失败 {e}")
        return False

def Download_CAPE(value_CAPE_url, username , outtime):
    try:
        return_data = requests.get(value_CAPE_url, timeout=outtime)
        return_data.raise_for_status()
        CAPE_data = return_data.content
        if CAPE_data[:4] == b"\x89PNG":
            ext = "png"
        elif CAPE_data[:4] == b"GIF8":
            ext = "gif"
        elif CAPE_data[:3] == b"\xff\xd8\xff":
            ext = "jpg"
        else:
            ext = "png"
        CAPE_name = f"{username}_cape.{ext}"
        CAPE_folder = os.path.dirname(os.path.abspath(__file__))
        CAPE_path = os.path.join(CAPE_folder, CAPE_name)
        with open(CAPE_path, "wb") as f:
            f.write(CAPE_data)
        print(f"成功:披风文件已下载到: {CAPE_path}\n")
        return True
    except requests.RequestException as e:
        print(f"错误:请求失败 {e}")
        return False

def main():
    outtime = 10
    alex = "[alex(纤细)]"
    steve = "[steve(标准)]"
    username = input("输入用户名: \n").strip()
    usernameurl = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    return_data = Get_data(username , usernameurl , outtime , steve , alex)
    if return_data is None:
        return 
    username, uuid, value_SKIN_url, value_SKIN_model, value_SKIN_model_name, value_timestamp_datetime, value_CAPE_url, system_time = return_data
    print(f"\n用户名:{username}\nUUID:{uuid}\n皮肤文件链接:{value_SKIN_url}\n皮肤类型:{value_SKIN_model_name}")
    if value_CAPE_url:
        print(f"披风文件链接:{value_CAPE_url}")
    print(f"时间戳:{value_timestamp_datetime}\n本地时间:{system_time}\n")
    DownloadSKIN = input("是否下载皮肤图片?(Y/N): \n").strip().lower()
    while DownloadSKIN not in ["y", "n"]:
        print("错误:请输入Y或N")
        DownloadSKIN = input("是否下载皮肤图片?(Y/N): \n").strip().lower()
    if DownloadSKIN == "y":
        Download_SKIN(value_SKIN_url, value_SKIN_model, username, outtime)
    if value_CAPE_url:
        DownloadCAPE = input("是否下载披风文件?(Y/N): \n").strip().lower()
        while DownloadCAPE not in ["y", "n"]:
            print("错误:请输入Y或N")
            DownloadCAPE = input("是否下载披风文件?(Y/N): \n").strip().lower()
        if DownloadCAPE == "y":
            Download_CAPE(value_CAPE_url, username , outtime)

if __name__ == "__main__":
    main()