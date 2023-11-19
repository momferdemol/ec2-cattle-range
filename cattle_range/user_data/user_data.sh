#!/bin/bash
sudo apt update
sudo apt install -y python3-pip
sudo git clone https://github.com/momferdemol/url-shortener-api.git
cd url-shortener-api
pip -q install -r requirements.txt
export PATH=$PATH:/home/ssm-user/.local/bin
sudo chmod a+rwx ./app
uvicorn app.main:app --host 0.0.0.0 --port 80