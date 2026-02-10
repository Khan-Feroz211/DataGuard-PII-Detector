import os
from huggingface_hub import snapshot_download

def download_weights():
    # Define the repository and local path
    repo_id = "theinvinciblehasnainali/DataGuard-Weights" 
    local_dir = "models"
    
    print(f"🚀 Starting download from Hugging Face: {repo_id}")
    print(f"📂 Destination: {os.path.abspath(local_dir)}")

    try:
        # This downloads the entire folder structure (base, small, tiny)
        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            repo_type="model"
        )
        print("\n✅ Success! Models are downloaded and ready for inference.")
    except Exception as e:
        print(f"\n❌ Error downloading models: {e}")
        print("Make sure the repository is public or you are logged in.")

if __name__ == "__main__":
    download_weights()