import torch

def get_position_embedding(max_seq_len, dim):
    assert dim % 2 == 0
    position = torch.arange(max_seq_len)
    freqs = torch.pow(10000, torch.arange(0, dim, 2) / -dim)
    # angles = torch.einsum('i, j -> i j', position, freqs)
    # angles = torch.unsqueeze(position, dim=1) * torch.unsqueeze(freqs, dim=0)
    angles = position[:, None] * freqs[None, :]
    sin_values = torch.sin(angles)
    cos_values = torch.cos(angles)
    return torch.stack((sin_values, cos_values), dim=-1).view(max_seq_len, dim)


def get_position_embedding2(max_seq_len, dim):
    assert dim % 2 == 0
    position = torch.arange(max_seq_len).unsqueeze(1)
    div_term = torch.exp(torch.arange(0, dim, 2).float() * (-torch.log(torch.tensor(10000.0)) / dim))
    angles = position * div_term.unsqueeze(0)
    position_embedding = torch.zeros((max_seq_len, dim))
    position_embedding[:, 0::2] = torch.sin(angles)
    position_embedding[:, 1::2] = torch.cos(angles)
    return position_embedding


print(get_position_embedding(1024, 128).shape)
print(get_position_embedding(1024, 128) - get_position_embedding2(1024, 128) < 1e-4)
