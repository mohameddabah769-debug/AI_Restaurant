"""
QR Code Generator for Mohamed Dabah Portfolio
Generates styled QR codes for Social Channels (WhatsApp, Facebook, LinkedIn, Instagram)
"""

import os
from pathlib import Path
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

from .config import SOCIAL_CHANNELS

def generate_all_qrs(output_dir: Path):
    """
    Generates QR code images for all defined social channels.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Color themes for each platform (RGB)
    color_schemes = {
        "whatsapp": {"edge": (37, 211, 102), "center": (10, 80, 40)},
        "facebook": {"edge": (24, 119, 242), "center": (10, 45, 110)},
        "linkedin": {"edge": (10, 102, 194), "center": (5, 45, 95)},
        "instagram": {"edge": (228, 64, 95), "center": (131, 58, 180)},
    }
    
    generated_files = []
    
    for channel in SOCIAL_CHANNELS:
        qr_filename = channel["qr_file"]
        qr_filepath = output_dir / qr_filename
        url = channel["url"]
        cid = channel["id"]
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        scheme = color_schemes.get(cid, {"edge": (0, 240, 255), "center": (20, 20, 40)})
        
        try:
            # Styled high-end QR with rounded modules and gradient
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=RoundedModuleDrawer(),
                color_mask=RadialGradiantColorMask(
                    back_color=(10, 15, 30),
                    center_color=scheme["center"],
                    edge_color=scheme["edge"]
                )
            )
        except Exception:
            # Fallback to standard clean QR code
            img = qr.make_image(fill_color=scheme["edge"], back_color=(10, 15, 30))
            
        img.save(str(qr_filepath))
        generated_files.append(qr_filepath)
        
    return generated_files

if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    qr_dir = current_dir / "static" / "images" / "qr"
    generate_all_qrs(qr_dir)
    print("All QR codes generated successfully.")
