# potatoe-disease-

Potatoe Disease — Potato leaf disease classifier

This repository contains a Cloud Function that serves a TFLite model to classify potato leaf images.

Quick overview
- Function entrypoint: `gcp/main.py` (handler `predict`).
- Models are stored in a GCS bucket; configure the bucket via the `MODEL_BUCKET` environment variable.
- Recommended runtime: Python 3.10. Key deps live in `gcp/requirements.txt`.

Deploy (example)
1. Upload your TFLite model to GCS:
	gsutil cp path/to/1.tflite gs://<BUCKET>/models/potato-model.tflite
2. Deploy the function (from `gcp` folder):
	gcloud functions deploy predict --runtime python310 --trigger-http --region us-central1 --set-env-vars MODEL_BUCKET=<BUCKET> --source="C:\Code\Potatoe-Disease\gcp"

Testing
- Use `curl` to POST an image as `file` form-data to the function URL.

Notes
- Large binaries and nested repos are excluded via `.gitignore`.
- If you need to keep large files, use Git LFS.

Contact
- Repo pushed to: https://github.com/nkemuduku/potatoe-disease-.git

Changed Instruction (#8)
 - Updated repository structure and added placeholders for large model files. See `saved_models/README.md` for guidance.