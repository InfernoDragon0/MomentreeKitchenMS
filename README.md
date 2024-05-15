# Momentree Kitchen (Maplestory)
Automatically complete the Momentree Kitchen PvP minigame in Maplestory! A GPU with CUDA compatiblity is necessary for high performance detection. If you are running it via a CPU, it will be much slower.

### Installation
- Tested on Python 3.11
- Install the requirements.txt
- (Optional, Recommended) If running on a GPU, go to https://pytorch.org/ and select your configuration to install.
- If you already had the CPU version of pyTorch and want to convert to GPU, you should `pip uninstall torch, torchaudio and torchvision` first to avoid conflicts

### Configuration
- Set your `npc` button accordingly
- Increase or Decrease `confidence` if you encounter false positives or negatives accordingly
- Increase `sleepAfterSuccess` to determine how much combo you want to earn

### Model
- A simple model `noisyArrow.pt` based on the `yolov8m.pt` model is trained to detect the success box and the V droplet. When using this mode, it will check if the V droplet is between the success zone and presses a button. The success zone is anywhere in the yellow or pink region.
- An alternate model is provided `noisyOnly.pt`, if you are using this, then you will need to change the logic by commenting lines 111 to 130 and uncommenting lines 133 to 157. This is for those who are running CPU
