import argparse
from pathlib import Path
from tqdm import tqdm
import torch
from dalle_pytorch import DiscreteVAE, DALLE
from dalle_pytorch.simple_tokenizer import tokenize


def generate_img(dalle_path: str,
                 text: str,
                 num_images: int = 30,
                 batch_size: int = 4,
                 top_k: float = 0.9,
                 device: str = "cpu"):
    # Check the DALLE path
    dalle_path = Path(dalle_path)
    assert dalle_path.exists(), 'Trained DALL-E must exist'

    load_obj = torch.load(str(dalle_path), map_location=torch.device(device))
    dalle_params, vae_params, \
        weights = load_obj.pop('hparams'), load_obj.pop('vae_params'), load_obj.pop('weights')

    dalle_params.pop('vae', None)  # cleanup later
    vae = DiscreteVAE(**vae_params)

    dalle = DALLE(vae=vae, **dalle_params).to(device)
    dalle.load_state_dict(weights)

    # Generate images
    text = tokenize([text], dalle.text_seq_len).to(device)
    text = text.repeat(num_images, 1)
    outputs = []

    for text_chunk in tqdm(text.split(batch_size), desc='generating images'):
        output = dalle.generate_images(text_chunk, filter_thres=top_k)
        outputs.append(output)

    outputs = torch.cat(outputs)

    return torch.transpose(outputs, 1, 3)
