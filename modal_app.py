import modal

app = modal.App("ncat-gpu-app")

image = (
    modal.Image.debian_slim()
    .apt_install("fontconfig")  # For fc-list and font discovery
    .pip_install(
        "Flask",
        "Werkzeug",
        "requests",
        "ffmpeg-python",
        "openai-whisper",
        "gunicorn",
        "APScheduler",
        "srt",
        "numpy",
        "torch",
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client",
        "google-cloud-storage",
        "psutil",
        "boto3",
        "Pillow",
        "matplotlib",
        "yt-dlp",
        "jsonschema",
        # "playwright",  # Uncomment only if you want screenshot endpoints
    )
    .run_commands(
        "mkdir -p /usr/share/fonts/custom"
    )
    .env(
        {
            "S3_BUCKET_NAME": "lumeora",
            "S3_ENDPOINT_URL": "https://047a93543c3c69fc1cb880a69f9938a1.r2.cloudflarestorage.com",
            "S3_REGION": "auto",
        }
    )
    .add_local_dir(".", "/root")
)

@app.function(
    image=image,
    gpu="A10G",
    max_containers=1,
    secrets=[modal.Secret.from_name("ncat-secret")]
)
@modal.web_server(port=8080)
def run_ncat_api():
    import os
    print("DEBUG: CWD:", os.getcwd())
    print("DEBUG: Files in CWD:", os.listdir("."))
    import subprocess
    subprocess.run(["gunicorn", "--bind", "0.0.0.0:8080", "app:app"])
