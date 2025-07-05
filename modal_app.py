import modal

app = modal.App("ncat-gpu-app")

image = (
    modal.Image.debian_slim()
    # ... your .apt_install(), .pip_install(), .env(), .add_local_dir() ...
)

@app.function(image=image, gpu="A10G", max_containers=1)
@modal.web_server(port=8080)
def run():
    import subprocess
    subprocess.run(["python", "app.py"])
