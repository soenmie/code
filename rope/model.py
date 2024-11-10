import torch

from torch import nn
from einops import rearrange

def get_rotary_embedding(dim, max_seq_len, base, device):
    assert dim % 2 == 0
    positions = torch.arange(max_seq_len, device=device)
    freqs = torch.pow(base, torch.arange(0, dim, 2, device=device) / -dim)
    angles = positions[:, None] * freqs[None, :]
    return torch.cat((angles, angles), dim=-1)


def rotate_half(x):
    x = rearrange(x, '... (j d) -> ... j d', j=2)
    x1, x2 = x.unbind(dim=-2)
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_pos_emb(x, emb):
    return x * emb.cos() + rotate_half(x) * emb.sin()


class VectorRopeModel(nn.Module):
    def __init__(self, dim, max_seq_len, base, device):
        super().__init__()
        self.max_seq_len = max_seq_len
        self.dim = dim
        self.base = base
        self.rotary_embedding = get_rotary_embedding(dim, max_seq_len, base, device)
        self.a = nn.Parameter(torch.randn(dim), requires_grad=True)
        self.b = nn.Parameter(torch.randn(dim), requires_grad=True)

    def forward(self, m, n):
        a = apply_rotary_pos_emb(self.a, self.rotary_embedding[m])
        b = apply_rotary_pos_emb(self.b, self.rotary_embedding[n])
        return torch.einsum('bi,bi -> b', a, b)


if __name__ == '__main__':
    # 设置 printoptions，threshold 参数为 float('inf') 以避免任何张量项的省略
    torch.set_printoptions(threshold=float('inf'))
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    torch.manual_seed(123)

    epochs = 400
    dim = 64
    max_seq_len = 314
    base = 200

    model = VectorRopeModel(dim, max_seq_len, base, device)
    model.to(device)

    input_m, input_n = torch.meshgrid(torch.arange(max_seq_len, device=device), torch.arange(max_seq_len, device=device), indexing='ij')
    input_m = input_m.flatten()
    input_n = input_n.flatten()

    optimizer = torch.optim.SGD(params=model.parameters(), lr=0.001)

    for epoch in range(epochs):
        model.train()
        loss = -torch.sum(torch.sigmoid(model(input_m, input_n)))
        if (epoch + 1) % 10 == 0:
            a, b = list(model.parameters())
            B = apply_rotary_pos_emb(b.unsqueeze(0).expand(max_seq_len, -1), model.rotary_embedding)
            cosine_of_angle_0 = torch.dot(a, b) / (torch.norm(a) * torch.norm(b))
            cosine_of_angles = torch.einsum('i,bi -> b', a, B) / (torch.norm(a) * torch.norm(b))
            cosine_of_angle_mean = torch.mean(cosine_of_angles)
            cosine_of_angle_var = torch.var(cosine_of_angles)
            print(f'epoch: {epoch}, loss: {loss}, cosine_of_angle_0: {cosine_of_angle_0}, cosine_of_angle_mean: {cosine_of_angle_mean}, cosine_of_angle_var: {cosine_of_angle_var}')
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    a, b = list(model.parameters())
    print('-' * 8 + 'a, b' + '-' * 8)
    print(a, b, sep='\n')
    print('-' * 8 + 'cosine_of_angle' + '-' * 8)
    print(torch.dot(a, b) / (torch.norm(a) * torch.norm(b)))
    print('-' * 8 + f'cosine_of_angle[0, {max_seq_len})' + '-' * 8)
    B = apply_rotary_pos_emb(b.unsqueeze(0).expand(max_seq_len, -1), model.rotary_embedding)
    print(torch.einsum('i,bi -> b', a, B) / (torch.norm(a) * torch.norm(b)))
    print('-' * 8 + f'dot product[0, {max_seq_len})' + '-' * 8)
    print(torch.einsum('i,bi -> b', a, B))
