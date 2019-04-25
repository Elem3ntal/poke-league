# CONFIGURACIONES ESTATICAS
# ==================================================================================================
VIRTUAL_ENV = .env
RUNTIME_VERSION = 3.7

# CONFIGURACIONES DE COLORES
# ==================================================================================================
HEADER = '\033[96m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# COMANDOS POR DEFECTO
# ==================================================================================================
install: install_requirements_system virtual install_requirements_python

clean:
	@+echo $(HEADER)"Desinstalando paquetes y entorno virtual"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@rm -rf ./$(VIRTUAL_ENV)
	@+echo $(OKGREEN)"[OK] Entorno virtual desinstalado"$(END)
	@+echo ""

virtual:
	@+echo  $(HEADER)"Instalando y activando entorno virtual"
	@+echo "---------------------------------------------"$(END)
	@+echo $(WARNING)""
	@if test ! -d "$(VIRTUAL_ENV)"; then \
		pip install virtualenv; \
		virtualenv -p python$(RUNTIME_VERSION) $(VIRTUAL_ENV); \
	fi
	@+echo ""$(END)

install_requirements_system:
	@+echo $(HEADER)"Instalando paqueteria del sistema"
	@+echo "---------------------------------------------"$(END)
	@+echo $(HEADER)""
	sudo apt-get install -y python3 python3-pip virtualenvwrapper
	if ! dpkg -l | grep redis-server -c >>/dev/null; then sudo apt-get install -y redis-server; fi
	@+echo $(OKGREEN)"[OK] Redis"$(END)
	@+echo $(HEADER)""
	if ! dpkg -l | grep mongodb-server -c >>/dev/null; then sudo apt-get install -y mongodb; fi
	@+echo $(OKGREEN)"[OK] Mongodb"$(END)
	@+echo $(OKGREEN)"[OK] Paqueteria lista"$(END)
	@+echo ""


install_requirements_python:
	@+echo $(HEADER)"Instalando paquetes requeridos por el entorno"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(WARNING)""
	@ $(VIRTUAL_ENV)/bin/pip --no-cache-dir install -Ur Setup/requirements.txt
	@ touch $(VIRTUAL_ENV)/bin/activate
	@+echo $(OKGREEN)"[OK] Paquetes instalados"$(END)
	@+echo ""

run:
	@+echo $(HEADER)"PENDIENTE"$(END)
	@+echo ""