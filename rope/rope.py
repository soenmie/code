import torch

from einops import rearrange

torch.manual_seed(123)

BASE = 10000


def get_rotary_embedding(dim, max_seq_len, device):
    assert dim % 2 == 0
    positions = torch.arange(max_seq_len, device=device)
    freqs = torch.pow(BASE, torch.arange(0, dim, 2, device=device) / -dim)
    angles = positions[:, None] * freqs[None, :]
    return torch.cat((angles, angles), dim=-1)


def rotate_half(x):
    x = rearrange(x, '... (j d) -> ... j d', j=2)
    x1, x2 = x.unbind(dim=-2)
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_pos_emb(x, emb):
    return x * emb.cos() + rotate_half(x) * emb.sin()


# 检查CUDA是否可用，并据此设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print('device:', device)

batch_size = 1
seq_len = 2
dim = 128
pos = 1

emb = get_rotary_embedding(dim, seq_len, device)
print(emb.shape)

# 创建在指定设备上的tensor
x = torch.randn(dim, device=device)

rotary_emb = apply_rotary_pos_emb(x, emb[pos])
print(rotary_emb)
