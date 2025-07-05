import modal

app = modal.App("ncat-gpu-app")

image = (
    modal.Image.debian_slim()
    .pip_install("torch", "openai-whisper", "ffmpeg-python", "flask", "gunicorn", "other-ncat-deps")
    .env(
        {
            "S3_BUCKET_NAME": "lumeora",
            "S3_ENDPOINT_URL": "https://047a93543c3c69fc1cb880a69f9938a1.r2.cloudflarestorage.com",
            "S3_REGION": "auto",
        }
    )
)
@app.function(
    image=image,
    gpu="A10G",
    concurrency_limit=1,
    secrets=[modal.Secret.from_name("ncat-secret")],
)

@modal.web_server(port=8080)
def run_ncat_api():
    import subprocess
    subprocess.run(["gunicorn", "--bind", "0.0.0.0:8080", "app:app"])
