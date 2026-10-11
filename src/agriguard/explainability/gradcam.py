"""Grad-CAM visual explanation engine for CNN vision backbones."""

import base64
import io
from typing import Optional, Tuple
import matplotlib.cm as cm
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torchvision.transforms.functional as TF


class GradCAM:
    def __init__(self, model: nn.Module, target_layer: nn.Module):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output.detach()

        def backward_hook(module, grad_in, grad_out):
            self.gradients = grad_out[0].detach()

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_full_backward_hook(backward_hook)

    def generate_heatmap(
        self,
        input_tensor: torch.Tensor,
        target_class_idx: Optional[int] = None,
    ) -> np.ndarray:
        """Computes 2D normalized Grad-CAM heatmap array in range [0.0, 1.0]."""
        self.model.eval()
        self.model.zero_grad()

        input_tensor = input_tensor.clone().requires_grad_(True)
        outputs = self.model(input_tensor)

        if target_class_idx is None:
            target_class_idx = int(torch.argmax(outputs, dim=1).item())

        score = outputs[0, target_class_idx]
        score.backward()

        if self.gradients is None or self.activations is None:
            # Fallback uniform heatmap if backward hook not reached
            return np.zeros((input_tensor.shape[2], input_tensor.shape[3]), dtype=np.float32)

        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
        activations = self.activations[0]

        for i in range(len(pooled_gradients)):
            activations[i, :, :] *= pooled_gradients[i]

        heatmap = torch.mean(activations, dim=0).cpu().numpy()
        heatmap = np.maximum(heatmap, 0)  # ReLU
        denom = np.max(heatmap)
        if denom > 0:
            heatmap /= denom

        return heatmap

    @staticmethod
    def overlay_heatmap_on_image(
        original_pil: Image.Image,
        heatmap: np.ndarray,
        alpha: float = 0.45,
        colormap: str = "jet",
    ) -> Image.Image:
        """Overlays Grad-CAM heatmap onto the original PIL image."""
        w, h = original_pil.size
        # Resize heatmap to match image dimensions
        heatmap_img = Image.fromarray(np.uint8(255 * heatmap))
        heatmap_resized = np.array(heatmap_img.resize((w, h), Image.Resampling.BILINEAR)) / 255.0

        # Apply colormap
        try:
            import matplotlib as mpl
            cmap = mpl.colormaps[colormap]
        except Exception:
            cmap = cm.get_cmap(colormap)
        colored_heatmap = cmap(heatmap_resized)[:, :, :3]  # drop alpha channel
        colored_heatmap_uint8 = np.uint8(255 * colored_heatmap)
        colored_pil = Image.fromarray(colored_heatmap_uint8).convert("RGBA")

        # Blend with original
        orig_rgba = original_pil.convert("RGBA")
        blended = Image.blend(orig_rgba, colored_pil, alpha=alpha)
        return blended.convert("RGB")

    @staticmethod
    def to_base64_jpeg(img: Image.Image) -> str:
        """Encodes PIL image as Base64 JPEG string."""
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode("utf-8")
