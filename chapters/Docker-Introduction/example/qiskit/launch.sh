docker build -t jupyter-qiskit .
docker run -it --rm -p 8888:8888 -v $(pwd)/volume:/home/jovyan/work/volume jupyter-qiskit
