import os
import re
import shutil
import pandas as pd
import requests
import lxml
import glob
import tarfile
from bs4 import BeautifulSoup

url_base = 'https://arxiv.org/e-print/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
}
DOWNLOAD_DIR = 'Downloads/'

def download_tar(file_name, dir):
    
    url = url_base + file_name
    file_name += '.tar.gz'
    file_path = os.path.join(dir, file_name)
    if os.path.exists(file_path):
        print("File {} Already Exisist".format(file_name))
        return file_path
    else:
        req = requests.get(url,headers=headers)
        if req.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(req.content)
            print('Finish Download: {}'.format(file_name))
            return file_path
        else:
            print('Download {} Failed.'.format(file_name))
            return None

def un_tar(file):
    tar = tarfile.open(file)
    names = tar.getnames()
    if os.path.isdir(file + '_files'):
        pass
    else:
        os.mkdir(file + '_files')
        for name in names:
            tar.extract(name, file + '_files')
    return file + '_files'

def find_texs(untar_file):
    texs = glob.glob('{}/*.tex'.format(untar_file))
    return texs

def parse_tex(file):
    rule = re.compile(r'\\begin{equation}(.*?)\\end{equation}',re.S)
    with open(file, 'rb') as f:
        content = f.read().decode('utf-8')
        content = content.replace('\n','')
        results = rule.findall(content)
    return results

def parse_texs(files):
    results = []
    rule = re.compile(r'\\begin{equation}(.*?)\\end{equation}',re.S)
    for file in files:
        with open(file, 'rb') as f:
            content = f.read().decode('utf-8')
            content = content.replace('\n','')
            result = rule.findall(content)
        results += result
    return {index:value for index, value in enumerate(results)}

def clean_files(tar_file, folder):
    shutil.rmtree(folder)
    os.remove(tar_file)

