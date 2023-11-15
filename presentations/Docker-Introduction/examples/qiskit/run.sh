docker build -t jupyter-qiskit-example .
docker run -it --rm -p 8888:8888 -v $(pwd)/notebooks:/home/jovyan/work -e NB_UID=$(id -u) -e NB_GID=$(id -g) -e GRANT_SUDO=yes jupyter-qiskit-example
