# Build in model
import os
from pathlib import Path
import io
import base64
# For website
from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
)
from flask_mail import (
    Mail,
    Message,
)
# For loading dot file
from dotenv import load_dotenv
# DL package
import torch
import torchvision.transforms as transforms
# Model to use
from dalle_pytorch import DiscreteVAE, VQGanVAE1024, DALLE
from dalle_pytorch.tokenizer import tokenizer
# Time bar
from tqdm import tqdm
# Tensor operation
from einops import repeat

# Load env file
load_dotenv()

# Set up the flask email from dot file
app = Flask(__name__)
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PROT=465,
    MAIL_USE_SSL=True,
    MAIL_DEFAULT_SENDER=("Text to image", os.environ.get("MAIL_USERNAME")),
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
)
mail = Mail(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = ("png", "jpg", "jpeg", "gif")

# Model Hyperparameters
REAL_DALLE_PATH = Path("weight/real-image.pt")
ICON_DALLE_PATH = Path("weight/icon.pt")
NUM_IMAGES = 24
BATCH_SIZE = 4
TOP_K = 0.9
device = "cuda" if torch.cuda.is_available() else "cpu"


def load_model(path, taming=False):
    """Load in the pretrained model"""
    load_obj = torch.load(str(path),
                          map_location=torch.device(device))

    dalle_params, vae_params, weights = \
        load_obj.pop("hparams"), load_obj.pop("vae_params"), load_obj.pop("weights")

    dalle_params.pop("vae", None)

    if taming:
        vae = VQGanVAE1024()
    else:
        vae = DiscreteVAE(**vae_params)

    dalle = DALLE(vae=vae,
                  **dalle_params).to(device)
    dalle.load_state_dict(weights)

    return dalle


# Build the model
real_dalle = load_model(REAL_DALLE_PATH,
                        taming=True)
icon_dalle = load_model(ICON_DALLE_PATH)


@app.route("/")
def index():
    return render_template("index.html",
                           show_gallery="none",
                           images="none",
                           display_success="none")


@app.route("/icon")
def icon_index():
    return render_template("icon.html",
                           show_gallery="none",
                           images="none",
                           display_success="none")


def allowed_file(filename):
    return filename.endswith(ALLOWED_EXTENSIONS)


@app.route("/send", methods=["POST"])
def send_message():
    msg_title = "Feed back for text to Image"
    msg_body = "From " + request.form.get("email") + "<br>" + request.form.get("message")

    msg = Message(subject=msg_title,
                  recipients=[app.config.get("MAIL_USERNAME")],
                  html=msg_body)

    mail.send(msg)

    return render_template("index.html",
                           show_gallery="none",
                           images="none",
                           display_success="block")


@app.route("/upload/<filename>")
def send_image(filename):
    return send_from_directory("images", filename)


def make_images(category, text):
    # Using to inverse the normalization of the image
    def norm_ip(img, low, high):
        img.clamp_(min=low, max=high)
        img.sub_(low).div_(max(high - low, 1e-5))

    def norm_range(t):
        norm_ip(t, float(t.min()), float(t.max()))

    if category == "icon":
        dalle_model = icon_dalle
    else:
        dalle_model = real_dalle

    # Generate images
    text = tokenizer.tokenize([text], dalle_model.text_seq_len).to(device)
    text = repeat(text, "() n -> b n",
                  b=NUM_IMAGES)

    # Generate images
    outputs = []

    for text_chunk in tqdm(text.split(BATCH_SIZE),
                           desc=f"generating images for - {text}"):
        output = dalle_model.generate_images(text_chunk,
                                             filter_thres=TOP_K)
        outputs.append(output)

    outputs = torch.cat(outputs)

    to_pil = transforms.ToPILImage()
    html_images = []

    count = 0
    for output in outputs:
        output = output.clone()
        norm_range(output)

        # Convert to pillow
        pil_image = to_pil(output).convert("RGB")

        # Encode to base64 for demonstrating in HTML
        output_buffer = io.BytesIO()
        pil_image.save(output_buffer, format="PNG")
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode("ascii")
        html_images.append(base64_str)
        count += 1

    return html_images


@app.route("/generate-icon", methods=["GET", "POST"])
def generate_icon():
    show_gallery = "block"

    # Get in the text
    text = str(request.values.get("text"))

    # Generate images
    html_images = make_images("icon", text)

    return render_template("icon.html",
                           images=html_images,
                           show_gallery=show_gallery,
                           display_success="none")


@app.route("/generate", methods=["GET", "POST"])
def generate():
    show_gallery = "block"

    # Get in the text
    text = str(request.values.get("text"))

    # Generate images
    html_images = make_images("real", text)

    return render_template("index.html",
                           images=html_images,
                           show_gallery=show_gallery,
                           display_success="none")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
