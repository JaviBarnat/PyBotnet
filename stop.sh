kill $(pgrep -f './server/grpcserver.py')
kill $(pgrep -f './flaskapp/pybotnet.py')
echo PyBotnet se ha detenido correctamente