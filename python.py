# Install required libraries
!pip install qrcode[pil] Pillow

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Function to generate QR code
def generate_qr_code(url, qr_size):
    qr = qrcode.QRCode(
        version=None,  # Automatically adjusts the size
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((qr_size, qr_size), Image.ANTIALIAS)
    return qr_img

# Function to create a coupon with QR code and coupon code text
def create_coupon(coupon_code, coupon_url, template_path, output_path, qr_position, qr_size, text_position, font_path):
    # Open the coupon template
    template = Image.open(template_path).convert('RGB')

    # Generate the QR code image
    qr_img = generate_qr_code(coupon_url, qr_size)

    # Paste the QR code onto the template
    template.paste(qr_img, qr_position)

    # (Optional) Add the coupon code text below the QR code
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype(font_path, size=16)  # Ensure the font file is accessible
    draw.text(text_position, f"Coupon Code: {coupon_code}", fill="white", font=font)

    # Save the final coupon image
    output_file = os.path.join(output_path, f"{coupon_code}_coupon.png")
    template.save(output_file)
    print(f"Saved {output_file}")

# Example usage
if __name__ == "__main__":
    # Paths and parameters (Change these according to your setup)
    template_path = "/content/coupon_template.png"  # **Change this to your coupon template file path**
    output_folder = "/content/drive/My Drive/created_coupons"  # **Change this to the folder in your Google Drive where you want to save the coupons**
    coupon_base_url = "https://gigisalon.github.io/coupon/coupon.html"  # **Change this to your base coupon URL**
    qr_position = (938, 124)               # **Change x, y coordinates for the QR code position on your template**
    qr_size = 140                          # **Change this to the size (width and height) of the QR code in pixels**
    text_position = (912, 273)             # **Change x, y coordinates for the coupon code text position**
    font_path = "/content/Times New Roman.ttf"  # **Change this to your desired font path**

    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate 160 coupons
    for i in range(1, 161):
        coupon_code = f"COUPON{i:03}"
        coupon_url = f"{coupon_base_url}?id={coupon_code}"

        create_coupon(
            coupon_code=coupon_code,
            coupon_url=coupon_url,
            template_path=template_path,
            output_path=output_folder,
            qr_position=qr_position,
            qr_size=qr_size,
            text_position=text_position,
            font_path=font_path
        )
