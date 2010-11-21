@echo off
python -O -tt -c "import Pyro.nsc,sys; Pyro.nsc.main(sys.argv[1:])" %*
