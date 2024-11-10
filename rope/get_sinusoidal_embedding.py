import torch

def get_sinusoidal_embedding(dim, max_seq_len, device):
    """
    获取Sinusoidal编码 的 PyTorch 实现。

    参数：
    - dim: 单个位置编码的维度，应为偶数。
    - max_seq_len: 可以支持的最大序列长度。
    - device: 位置编码应放置的设备（CPU或GPU）。

    返回：
    - pos_emb: 维度为 (max_seq_len, dim) 的旋转式位置编码矩阵（的 PyTorch tensor）。
    """
    # 验证dim是否为偶数
    assert dim % 2 == 0, "Embedding dimension should be an even number."

    # 生成位置索引向量
    position = torch.arange(max_seq_len, dtype=torch.float32, device=device)

    # 根据位置生成频率
    freqs = torch.pow(10000, -1 * torch.arange(0, dim, 2, device=device) / dim)

    # 计算旋转式位置编码（rotary position encoding）
    angles = position[:, None] * freqs[None, :]

    sin = torch.sin(angles)
    cos = torch.cos(angles)

    # 组合奇偶位置编码成完整的RoPE矩阵
    pos_emb = torch.stack((sin, cos), dim=1).reshape(max_seq_len, dim)
    return pos_emb

# 示例用法：
dim = 64  # 嵌入维度
max_seq_len = 128  # 最大序列长度
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

rotary_emb = get_sinusoidal_embedding(dim, max_seq_len, device)
print(rotary_emb.shape)  # 输出: torch.Size([128, 64])
