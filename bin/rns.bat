@echo off
:RESTART
echo Starting Pyro Name Server
python -O -tt -c "import Pyro.naming,sys; Pyro.naming.main(sys.argv[1:])" %*
echo.
echo ---- Name server stopped! Restarting! (press ctrl-break now to abort) ----
echo. 
sleep 2
goto RESTART
