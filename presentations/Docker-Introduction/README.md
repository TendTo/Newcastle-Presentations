# Introduction to Docker

<!-- New section -->

## Why do we need virtualization?

Applications in general need to interact with the operating system, the hardware, and other applications.

If even an element of the system changes, the application may not work as expected.

<!-- .element: class="fragment" -->

<a target="_blank" href="https://www.redbubble.com/i/magnet/Shrug-It-Works-On-My-Machine-Funny-Programmer-Excuse-programming-meme-by-ProgrammingMeme/65289679.TBCTK">
    <img src="https://ih1.redbubble.net/image.1939881725.9679/st,small,845x845-pad,1000x1000,f8f8f8.u2.jpg" width="300px" /></img>
</a>

<!-- .element: class="fragment" -->

<!-- New subsection -->

### Virtual machines

<div class="cols">

<a target="_blank" href="https://www.docker.com/resources/what-container/">
    <img src="https://www.docker.com/wp-content/uploads/2021/11/container-vm-whatcontainer_2.png" width="500px" /></img>
</a>

<div>

**Virtual Machines** (VMs) are a great way to improve reproducibility.

They use a very complex software, the **hypervisor**, to emulate the hardware and the operating system.
They are (mostly) completely independent from the host system.

<!-- .element: class="fragment" -->

</div>

</div>

<!-- New subsection -->

### Containers

<div class="cols">

<a target="_blank" href="https://www.docker.com/resources/what-container/">
    <img src="https://www.docker.com/wp-content/uploads/2021/11/docker-containerized-appliction-blue-border_2.png" width="500px" /></img>
</a>

<div>

**Containers** are a lightweight alternative to VMs.

They use some features of the Linux kernel, namely **namespaces** and **cgroups**, to completely isolate a process from the rest of the system.
They can't emulate different kernel or hardware.

<!-- .element: class="fragment" -->

</div>

</div>

<!-- New section -->

## Docker

<div class="cols">

<a target="_blank" href="https://www.docker.com">
    <img src="./img/docker-logo.svg" width="100px" /></img>
</a>

[Docker](https://www.docker.com) is the most popular containerization software.  
Some alternatives are [Podman](https://podman.io/) or [LXC](https://linuxcontainers.org/).

</div>

It also provides a [registry](https://hub.docker.com/) where you can find pre-built images.

<!-- .element: class="fragment" -->

<!-- New subsection -->

### Installation

Since Docker is specifically built with the Linux kernel in mind, it is not natively supported on Windows and macOS.
It needs to spin up a virtual machine to run Linux.

[Docker Desktop](https://www.docker.com/products/docker-desktop) handles everything for you.

<!-- .element: class="fragment" -->

- [Windows](https://docs.docker.com/docker-for-windows/install/)
- [Mac](https://docs.docker.com/docker-for-mac/install/)
- [Linux](https://docs.docker.com/engine/install/)
  - Docker Desktop ([will use a VM](https://docs.docker.com/desktop/faqs/linuxfaqs/))
  - Docker Engine

<!-- .element: class="fragment" -->

<!-- New subsection -->

### Images

<div class="cols">

<a target="_blank" href="https://hub.docker.com/layers/library/python/latest/images/sha256-5a2936b50ea64ce3e090c862d2482d5d90ed19ee2ceba5cf96ea171bd1dcba67?context=explore">
    <img src="./img/layers.png" width="500px" /></img>
</a>

<div>

An **image** is a read-only template with instructions for creating a Docker container.

They are made up of **layers** that are stacked on top of each other, like git commits.

<!-- .element: class="fragment" -->

Only the top layer is writable.

<!-- .element: class="fragment" -->

</div>

</div>

<!-- New subsection -->

### Dockerfile

Dockerfiles are the instructions to build an image.

```dockerfile
FROM python:3.9.7-slim-buster # Base image

WORKDIR /app # Working directory (creates it if it does not exist)

COPY requirements.txt requirements.txt # Copy files from host to container

RUN pip install -r requirements.txt # Run a command in the container

COPY . . # Copy files from host to container

ENTRYPOINT ["python", "main.py"] # Run a command as soon as the container starts
```

<!-- New subsection -->

### Build an image

```bash
# Build an image from the Dockerfile in the current directory
# docker build -t <image-name>:<tag> <context>
# -t: tag the image with a name
# .: use the current directory as context
docker build -t my-image:latest .
```

<!-- New subsection -->

### Images commands

```bash
# List all images
docker images
# Remove an image
docker rmi <image-name>:<tag>
# Remove all images
docker rmi $(docker images -q)
# Remove all dangling images
docker image prune
```

<!-- New subsection -->

### Run a container

```bash
# Run a container from an image
# docker run <image-name>:<tag>
# -d: run the container in detached mode
# -p: publish a container's port(s) to the host
# --name: name the container
# --rm: remove the container when it exits
docker run -d -p 5000:5000 --name my-container --rm my-image:latest
```

<!-- New subsection -->

### Storage

<div class="cols">

<a target="_blank" href="https://docs.docker.com/storage/">
    <img src="./img/volumes.webp" width="500px" /></img>
</a>

<div>

Storage inside a container is ephemeral and is destroyed when the container is removed.

**Volumes** and **bind mounts** are used to persist data.

<!-- .element: class="fragment" -->

</div>

<!-- New subsection -->

#### Transferring files into containers

- Copy them directly into the image.
  The files become part of the image and are independent from the host.

```dockerfile
# COPY <src> <dest>
# ADD has the same syntax, src can be a URL or a tar file
COPY requirements.txt requirements.txt
COPY . .
```

- Use a bind mount.
  In this case, the connection is bidirectional and continuous.

<!-- .element: class="fragment" data-fragment-index="1" -->

```bash
# docker run -v <host-path>:<container-path>
docker run -v $(pwd):/app
```

<!-- .element: class="fragment" data-fragment-index="1" -->

<!-- New section -->

## Examples

Three examples of how to use Docker in your workflow.

- [Distributing a Haskell script](#distributing-a-haskell-script)
- [Running Qiskit in a Jupyter Notebook](#running-Qiskit-in-a-jupyter-notebook)
- [Web architecture with php and mysql](#web-architecture-with-php-and-mysql)

<!-- New subsection -->

<!-- .slide: id="distributing-a-haskell-script" -->

### Distributing a Haskell script

Let's say you have a Haskell script that you want to distribute to other people.
They may not have the whole Haskell toolchain installed, so you can use Docker to create a container that runs the script.

```dockerfile
FROM haskell:slim       # Official base image (https://hub.docker.com/_/haskell)
COPY main.hs .          # Copy the script into the container
RUN ghc -o main main.hs # Compile the script 
ENTRYPOINT ["./main"]   # Run the script as soon as the container starts
```

<!-- .element: class="fragment" -->

```bash
docker build -t my-haskell-script .   # Build the image
docker run -it --rm my-haskell-script # Create and run the container
```

<!-- .element: class="fragment" -->

<!-- New subsection -->

### Running Qiskit in a notebook

<!-- .slide: id="running-Qiskit-in-a-jupyter-notebook" -->

<!-- New subsection -->

### Web architecture with php and mysql

<!-- .slide: id="web-architecture-with-php-and-mysql" -->

<!-- New section -->

## References

- [Docker](https://www.docker.com/)
- [Docker Hub](https://hub.docker.com/)

<!-- New subsection -->

## Images

- [It works on my machine!](https://www.redbubble.com/i/magnet/Shrug-It-Works-On-My-Machine-Funny-Programmer-Excuse-programming-meme-by-ProgrammingMeme/65289679.TBCTK)
- [VM vs Container](https://www.docker.com/resources/what-container/)
