# Guide 02: Ubuntu Setup for AI

> **Series:** Gaming PC → AI Agent Setup | West AI Labs Community
> **Level:** Beginner — never used Linux before? Perfect. We start from zero.

---

## Before We Start

This guide assumes:
- You have (or are installing) Ubuntu 22.04 or 24.04
- You have an NVIDIA GPU (check [Guide 01](./guide-01-is-my-gpu-ready.md) if unsure)
- You're comfortable typing commands — you don't need to understand them all, just type them carefully

> **Why Ubuntu?** It's the most widely supported Linux distro for AI work. NVIDIA's drivers, CUDA, and most AI tooling is tested on Ubuntu first. If something breaks, there's a 99% chance someone on the internet has already fixed it.

---

## Part 1: Getting Ubuntu Running

### Option A: Ubuntu is Already Installed
Skip to Part 2. You're ahead of the curve.

### Option B: Dual Boot (Keep Windows + Add Ubuntu)

This is the recommended path if you game on Windows and want AI on the side.

1. **Back up your stuff first.** Seriously.
2. Download Ubuntu 22.04 LTS from [ubuntu.com](https://ubuntu.com/download/desktop)
3. Flash it to a USB drive using [Rufus](https://rufus.ie/) (Windows app, free)
4. Boot from USB (restart, press F2/F8/F11/Del during boot — depends on your motherboard)
5. Choose "Install Ubuntu alongside Windows"
6. Give Ubuntu at least **50GB** of disk space (more if you're storing models — they're big)
7. Finish the installer, reboot

On boot you'll see a menu asking which OS to load. Pick Ubuntu for this guide.

### Option C: Replace Windows Entirely
Only do this if you're committed. Same process as above, but choose "Erase disk and install Ubuntu" instead.

---

## Part 2: First Boot — Get Comfortable

When Ubuntu boots, you'll see a desktop. Open the **Terminal** — it's your new best friend.

Find it by:
- Pressing `Ctrl + Alt + T`
- Or searching "Terminal" in the app launcher (the grid icon bottom-left)

The terminal looks intimidating. It isn't. It's just a very direct way to talk to your computer. Commands follow this pattern:
```
do-this to-this --with-these-options
```

Let's start with a simple update:
```bash
sudo apt update && sudo apt upgrade -y
```

> 💡 **`sudo`** = "superuser do" — it runs the command with admin privileges. Linux will ask for your password the first time per session. It won't show the password as you type — that's normal.

Let this finish. It might take a few minutes.

---

## Part 3: NVIDIA Drivers

This is the step people mess up the most. Ubuntu comes with a generic graphics driver — we need the real NVIDIA one.

### The Easy Way (Recommended)

Ubuntu has a built-in tool for this:

1. Open the app launcher and search for **"Software & Updates"**
2. Click the **"Additional Drivers"** tab
3. Ubuntu will detect your GPU and show available NVIDIA drivers
4. Select the one labeled **"proprietary, tested"** (usually the highest version number)
5. Click **"Apply Changes"**
6. Reboot

### Verify It Worked
After rebooting, open terminal and run:
```bash
nvidia-smi
```

You should see something like:
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.xxx    Driver Version: 535.xxx    CUDA Version: 12.x        |
+-----------------------------------------------------------------------------+
| GPU  Name        Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|   0  NVIDIA GeForce RTX 3080  |  ...                 |
```

If you see your GPU name, **you're done with drivers.** If you get "command not found" or errors, the driver install didn't take — try the terminal method below.

### Terminal Method (If the GUI Didn't Work)
```bash
# Remove any broken NVIDIA packages
sudo apt purge nvidia-* -y
sudo apt autoremove -y

# Install the recommended driver
sudo ubuntu-drivers install

# Reboot
sudo reboot
```

---

## Part 4: CUDA

**CUDA** is NVIDIA's toolkit that lets software talk to your GPU for computation (not just graphics). Most AI software needs it.

> 💡 When you ran `nvidia-smi` above, it showed "CUDA Version: X.X" — that's the *maximum* CUDA version your driver supports. We now install the actual CUDA toolkit.

```bash
# Add NVIDIA's package repository
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb

# Update and install CUDA toolkit
sudo apt update
sudo apt install -y cuda-toolkit-12-3

# Add CUDA to your PATH so programs can find it
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

Verify:
```bash
nvcc --version
```
You should see a version number. If you do, CUDA is ready.

> 📝 **Note for Ubuntu 24.04 users:** Replace `ubuntu2204` with `ubuntu2404` in the wget URL above.

---

## Part 5: Docker with GPU Passthrough

**Docker** is a way to run software in isolated containers — like a virtual machine but lighter and faster. Most AI tooling ships as Docker containers. We need Docker to be able to see your GPU.

### Install Docker

```bash
# Install prerequisites
sudo apt install -y ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add yourself to the docker group (so you don't need sudo every time)
sudo usermod -aG docker $USER

# Start Docker on boot
sudo systemctl enable docker
sudo systemctl start docker
```

**Log out and back in** for the group change to take effect, then verify:
```bash
docker run hello-world
```
You should see "Hello from Docker!" — that means Docker is working.

### Install NVIDIA Container Toolkit (GPU Passthrough)

This is the piece that lets Docker containers use your GPU:

```bash
# Add NVIDIA Container Toolkit repo
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install it
sudo apt update
sudo apt install -y nvidia-container-toolkit

# Configure Docker to use it
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Verify GPU passthrough works:
```bash
docker run --rm --gpus all nvidia/cuda:12.3.0-base-ubuntu22.04 nvidia-smi
```

You should see your GPU details printed from inside a container. **If you see this, your system is fully ready for AI.**

---

## Part 6: Install Ollama

**Ollama** is the easiest way to run AI models locally. It handles downloading models, loading them on your GPU, and serving them via an API.

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

That's literally it. Ollama installs itself, sets up a systemd service (so it starts automatically), and configures GPU support automatically.

Verify:
```bash
ollama --version
```

Test with your first model:
```bash
ollama run llama3.2
```

This downloads the Llama 3.2 3B model (~2GB) and starts a chat. Type something. It'll respond. Your GPU is doing AI inference.

To exit the chat: type `/bye` or press `Ctrl+D`.

### See Available Models
```bash
ollama list
```

### Pull More Models
```bash
# 7B — good for most things
ollama pull llama3.1

# Faster, smarter small model
ollama pull qwen2.5:7b

# 14B if you have 10GB+ VRAM
ollama pull qwen2.5:14b
```

---

## What You've Built

Here's what's now running on your machine:

```
Your Gaming PC
├── Ubuntu 22.04/24.04
├── NVIDIA Driver (GPU ↔ OS)
├── CUDA Toolkit (GPU ↔ software)
├── Docker + NVIDIA Container Toolkit (GPU ↔ containers)
└── Ollama (runs AI models on your GPU)
```

This is the exact stack that powers Jr.'s agent Hohenheim — the D&D Dungeon Master that never forgets a plot thread or character backstory.

---

## Troubleshooting

**`nvidia-smi` shows "No devices were found"**
→ Driver didn't install. Try: `sudo ubuntu-drivers install && sudo reboot`

**Docker GPU test fails with "unknown runtime: nvidia"**
→ Forgot to restart Docker: `sudo systemctl restart docker`

**Ollama is slow / not using GPU**
→ Check: `ollama ps` — if the GPU column is empty, your CUDA might not be linked properly. Run `nvidia-smi` while a model is loaded — GPU utilization should be non-zero.

---

## Next Step

**→ [Guide 03: Ollama + OpenClaw Quickstart](./guide-03-ollama-openclaw-quickstart.md)**

Ollama is running. Now let's install OpenClaw and connect your AI to Discord so it can actually talk to people.

---

*West AI Labs Community Guide Series | Updated Feb 2026*
