# for glitch
pip3 install -r requirements.txt --user
python3 server.py
# For production use: 
# gunicorn server:app -w 1 --log-file -
