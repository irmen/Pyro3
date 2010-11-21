@echo off
python -O -tt -c "from Pyro.ext.NS_NtService import PyroNS_NTService; import sys; sys.argv[0]='nssvc.bat'; PyroNS_NTService.HandleCommandLine()" %*
