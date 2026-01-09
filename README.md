# Docker Container Workshop: Reproducible Python Environments

This workshop demonstrates how to move from local Python environments (e.g., Conda) to **Docker-based system-level reproducibility**.

The goal is to freeze the **environment**, not the workflow.

---

## Prerequisites

- Docker Desktop installed and running  
- A terminal  
  - PowerShell on Windows  
  - Terminal on macOS / Linux  
- (Optional) Conda for local environment comparison

Verify Docker is working before starting:

```bash
docker run hello-world
```

You should see outputs saying your docker was installed correctly.

---

## Part 1: Environment Management with Conda

This section is **optional** and included to illustrate environment-level control.

```bash
conda create -n reproduce python=3.10
conda activate reproduce
conda list
```

Create a `requirements.txt` file:

```text
numpy==1.26.4
pandas==2.2.2
jupyterlab==4.2.5
```

Install dependencies locally:

```bash
pip install -r requirements.txt
```


> Conda controls the Python environment.  
> Docker will extend this to control the system environment.

---

## Part 2: Build the Docker Image

### Project structure

```text
.
├── Dockerfile
├── analysis.py
├── requirements.txt
└── analysis.ipynb   # optional
```

### Build the image

```bash
docker build -t reproducible-python .
```

Verify the image was created:

```bash
docker images
```

---

## Part 3: Run the Analysis Script (Frozen Environment)

Run the container using only what is inside the image:

```bash
docker run --rm reproducible-python
```

This executes the `analysis.py` file that was copied into the image at build time.

---

## Part 4: Iterate with Local Code (Volume Mount)

Modify `analysis.py` locally (for example, add a new print statement, e.g. you can use co-Pilot to help you with that!).

Run again **with a volume mount**, so the container uses your local files.

### Windows (PowerShell)

```powershell
docker run --rm -v ${PWD}:/app reproducible-python
```

### macOS / Linux

```bash
docker run --rm -v "$PWD":/app reproducible-python
```

> The image does not change.  
> Your local folder is mounted into the container at runtime.

---

## Part 5 (Optional): Run a Jupyter Notebook from the Same Image

This demonstrates using the **same image** with a different interface.

### Start JupyterLab in the container

#### Windows (PowerShell)

```powershell
docker run --rm -it `
  -p 8888:8888 `
  -v ${PWD}:/app `
  reproducible-python `
  jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

#### macOS / Linux

```bash
docker run --rm -it \
  -p 8888:8888 \
  -v "$PWD":/app \
  reproducible-python \
  jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

Open the URL printed in the terminal (token included) to access JupyterLab.

> Same image.  
> Same environment.  
> Different execution interface.

---

## Key Takeaways

- Conda controls **Python-level assumptions**
- Docker controls **system-level assumptions**
- Volume mounts enable fast iteration without rebuilding images
- Containers are disposable; images are reusable
- Reproducibility is about controlling assumptions, not tools

---

## Cleanup

Containers are removed automatically when using `--rm`.

To remove the image:

```bash
docker rmi reproducible-python
```

---

## Notes
- For conda env, alternatively, start from 

```bash
conda env create -f env.yml
```
to directly build conda env
- Docker Desktop must be running before executing Docker commands
- Jupyter uses a token for authentication by default
- Do not expose unauthenticated Jupyter servers publicly

## Command Explanations (Quick Reference)

### Conda-related commands

**`conda create -n reproduce python=3.10`**  
Creates a new Conda environment named `reproduce` with Python version 3.10.

**`conda activate reproduce`**  
Activates the `reproduce` environment so that installed packages and Python are isolated from other environments.

**`conda list`**  
Lists all packages installed in the currently active Conda environment.

**`conda install <package>`**  
Installs a package into the active Conda environment, resolving Python and system-level dependencies when possible.

---

### pip-related commands

**`pip install -r requirements.txt`**  
Installs Python packages listed in `requirements.txt` into the currently active environment (Conda or system Python).

**`pip install <package>`**  
Installs a Python package from PyPI into the active environment.

> Note: `pip` manages Python packages only.  
> It does not manage system libraries or the operating system.

---

### Docker-related commands

**`docker build -t reproducible-python .`**  
Builds a Docker image named `reproducible-python` using the `Dockerfile` in the current directory.

**`docker images`**  
Lists Docker images available on the local machine.

**`docker run <image>`**  
Creates and starts a new container from the specified image.

**`docker run --rm <image>`**  
Runs a container and automatically removes it after it exits.

**`-v <local_path>:<container_path>`**  
Mounts a local directory into the container at runtime, allowing the container to read and write local files.

**`-p <host_port>:<container_port>`**  
Maps a port from the container to the host machine (used for Jupyter and other services).

---

### Jupyter-related commands

**`jupyter lab`**  
Starts a JupyterLab server, allowing interactive notebooks to run in a web browser.

**`--ip=0.0.0.0`**  
Allows Jupyter to accept connections from outside the container.

**`--port=8888`**  
Specifies the port Jupyter listens on inside the container.

**`--no-browser`**  
Prevents Jupyter from attempting to open a browser inside the container.

**`--allow-root`**  
Allows Jupyter to run as the root user (required in many container environments).

---

## Summary

- **Conda** manages Python environments and dependencies  
- **pip** installs Python packages within an environment  
- **Docker** encapsulates the entire system environment  
- **Jupyter** provides an interactive interface on top of the same environment

Each tool controls a different layer of assumptions.
