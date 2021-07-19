nohup python ./server/grpcserver.py > /dev/null 2>&1 &
nohup python ./flaskapp/pybotnet.py > /dev/null 2>&1 &
echo PyBotnet se ha iniciado correctamente