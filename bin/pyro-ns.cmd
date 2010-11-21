@echo off
python -O -tt -c "import Pyro.naming,sys; Pyro.naming.main(sys.argv[1:])" %*
