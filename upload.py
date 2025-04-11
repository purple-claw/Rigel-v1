from huggingface_hub import HfApi, HfFolder, Repository, create_repo, upload_folder


username = "nitinsri"  
model_name = "Rigel_ClauseNet"
repo_id = f"{username}/{model_name}"

# Step 3: Upload the local model folder
upload_folder(
    folder_path="/home/dev/Desktop/rigel-v1",   
    repo_id=repo_id,
    path_in_repo=".", 
    commit_message="Initial upload of fine-tuned Rigel clause classifier"
)
