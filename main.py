import os
import json
import base64
import requests
from datetime import datetime

def Get_language(section_name, language):
    try:
        with open(os.path.join(os.path.dirname(__file__), "language" ,f"{language}.json"), "r", encoding="utf-8") as language_file:
            language_temp = json.load(language_file)
            language = language_temp[section_name]
            return language
    except FileNotFoundError:
        print("找不到语言文件\ncan't find language file")
        return None
    except KeyError:
        if language == "zh_cn":
            print(f"错误:语言文件中缺少'{section_name}'部分,请检查语言文件是否完整。")
        else:
            print(f"Error: The '{section_name}' section is missing in the language file, please check if the language file is complete.")
        return None

def Get_data(username, usernameurl, outtime, steve, alex, language):
    language = Get_language("Get_data", language)
    if language is None:
        return None
    try:
        return_data = requests.get(usernameurl , timeout=outtime)
    except requests.RequestException as e:
        print(language.get("getError").format(e=e))
        return None
    if return_data.status_code == 200:
        usernamedata = return_data.json()
        uuid = usernamedata.get("id")
        uuidurl = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        username = usernamedata.get("name")
        try:
            return_data = requests.get(uuidurl, timeout=outtime)
        except requests.RequestException as e:
            print(language.get("getError").format(e=e))
            return None
        if return_data.status_code == 200:
            uuiddata = return_data.json()
            properties = uuiddata.get("properties", [])
            if not properties:
                print(language.get("outUserNotSKIN").format(username=username, uuid=uuid))
                return None
            value = properties[0].get("value")
            system_time = datetime.now()
            value_b64 = base64.b64decode(value)
            value_b64_json = value_b64.decode('utf-8')
            value_json = json.loads(value_b64_json)
            value_timestamp = value_json.get("timestamp" , 0)
            value_timestamp_datetime = datetime.fromtimestamp(value_timestamp / 1000)
            value_SKIN_url = value_json.get("textures", {}).get("SKIN", {}).get("url" , "")
            value_SKIN_model = value_json.get("textures", {}).get("SKIN", {}).get("metadata", {}).get("model" , "classic")
            value_CAPE_url = value_json.get("textures", {}).get("CAPE", {}).get("url", None)
            the_other_model = f"[{value_SKIN_model}({language.get('unknown')})]"
            if value_SKIN_model == "classic":
                value_SKIN_model_name = f"classic{steve}"
            elif value_SKIN_model == "slim":
                value_SKIN_model_name = f"slim{alex}"
            else:
                value_SKIN_model_name = f"unknown{the_other_model}"
            if value_json.get("profileId") == uuid and value_json.get("profileName") == username:
                return username, uuid, value_SKIN_url, value_SKIN_model ,value_SKIN_model_name, value_timestamp_datetime, value_CAPE_url, system_time
            else:
                print(language.get("systemError"))
                return None
        else:
            print(language.get("errorUUIDNotSKIN"))
            return None
    elif return_data.status_code == 404:
        print(language.get("error404"))
        return None
    elif return_data.status_code == 429:
        print(language.get("error429"))
        return None
    elif return_data.status_code == 500:
        print(language.get("error500"))
        return None
    elif return_data.status_code == 503:
        print(language.get("error503"))
        return None
    else:
        print(language.get("errorUnknown").format(status_code=return_data.status_code))
        return None

def Download_SKIN(value_SKIN_url, value_SKIN_model, username , outtime, language):
    language = Get_language("Download_SKIN", language)
    if language is None:
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
        print(language.get("success").format(SKIN_path=SKIN_path))
        return True
    except requests.RequestException as e:
        print(language.get("getError").format(e=e))
        return False

def Download_CAPE(value_CAPE_url, username , outtime, language):
    language = Get_language("Download_CAPE", language)
    if language is None:
        return False
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
        print(language.get("success").format(CAPE_path=CAPE_path))
        return True
    except requests.RequestException as e:
        print(language.get("getError").format(e=e))
        return False

def main():
    while True:
        choice_language_num = input("选择语言\nSelect language\n\n1.中文(简体)\n2.English\n")
        if choice_language_num == "1":
            choice_language = "zh_cn"
            break
        elif choice_language_num == "2":
#            choice_language = "en_us"
            print("错误：该功能暂未完成\nError: This feature is not yet completed")
            choice_language = "zh_cn"
            break
        else:
            print("错误：输入错误\nError: Invalid input")
    language = Get_language("main", choice_language)
    if language is None:
        return
    outtime = 10
    alex = language.get("alex")
    steve = language.get("steve")
    username = input(language.get("qUsername")).strip()
    usernameurl = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    return_data = Get_data(username , usernameurl , outtime , steve , alex, choice_language)
    if return_data is None:
        return 
    username, uuid, value_SKIN_url, value_SKIN_model, value_SKIN_model_name, value_timestamp_datetime, value_CAPE_url, system_time = return_data
    print(language.get("outData").format(username=username, uuid=uuid, value_SKIN_url=value_SKIN_url, value_SKIN_model_name=value_SKIN_model_name))
    if value_CAPE_url:
        print(language.get("outDataCAPE").format(value_CAPE_url=value_CAPE_url))
    print(language.get("outTime").format(value_timestamp_datetime=value_timestamp_datetime, system_time=system_time))
    DownloadSKIN = input(language.get("qDownloadSKIN")).strip().lower()
    while DownloadSKIN not in ["y", "n"]:
        print(language.get("inputError"))
        DownloadSKIN = input(language.get("qDownloadSKIN")).strip().lower()
    if DownloadSKIN == "y":
        FDownloadSKIN = Download_SKIN(value_SKIN_url, value_SKIN_model, username, outtime, choice_language)
        if FDownloadSKIN is False:
            print(language.get("errorDownloadSKIN"))
            FDownloadSKIN = Download_SKIN(value_SKIN_url, value_SKIN_model, username, outtime, choice_language)
            if FDownloadSKIN is False:
                print(language.get("getError"))
    if value_CAPE_url:
        DownloadCAPE = input(language.get("qDownloadCAPE")).strip().lower()
        while DownloadCAPE not in ["y", "n"]:
            print(language.get("inputError"))
            DownloadCAPE = input(language.get("qDownloadCAPE")).strip().lower()
        if DownloadCAPE == "y":
            FDownloadCAPE = Download_CAPE(value_CAPE_url, username , outtime, choice_language)
            if FDownloadCAPE is False:
                print(language.get("errorDownloadCAPE"))
                FDownloadCAPE = Download_CAPE(value_CAPE_url, username , outtime, choice_language)
                if FDownloadCAPE is False:
                    print(language.get("getError"))  

if __name__ == "__main__":
    main()