import modal

app = modal.App("ncat-gpu-app")

image = (
    modal.Image.debian_slim()
    .apt_install("fontconfig")
    .pip_install("Flask")
    .add_local_dir(".", "/root")
)

@app.function(image=image, max_containers=1)
@modal.web_server(port=8080)
def run():
    import subprocess
    subprocess.run(["python", "app.py"])
