import torch
print(torch.cuda.is_available())  # should print true
print(torch.cuda.get_device_name(0))  # should print gpu name