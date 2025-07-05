import modal

app = modal.App("ncat-gpu-app")

image = (
    modal.Image.debian_slim()
    .apt_install("fontconfig")
    .pip_install("Flask", "gunicorn")
    .add_local_dir(".", "/root")
)

@app.function(
    image=image,
    gpu="A10G",
    max_containers=1,
)
@modal.web_server(port=8080)
def run_ncat_api():
    import subprocess
    subprocess.run(["gunicorn", "--bind", "0.0.0.0:8080", "app:app"])
