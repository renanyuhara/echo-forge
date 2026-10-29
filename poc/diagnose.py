"""Inspect the local Python, CUDA, and GPU environment before downloading a model."""
import json
import platform
import sys


def main() -> None:
    info = {"python": sys.version.split()[0], "platform": platform.platform()}
    try:
        import torch
        info["torch"] = torch.__version__
        info["torch_cuda_runtime"] = torch.version.cuda
        info["cuda_available"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            info["gpu_name"] = torch.cuda.get_device_name(0)
            props = torch.cuda.get_device_properties(0)
            info["gpu_memory_gib"] = round(props.total_memory / (1024**3), 2)
            info["compute_capability"] = list(torch.cuda.get_device_capability(0))
    except ImportError:
        info["error"] = "PyTorch is not installed"
    print(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
