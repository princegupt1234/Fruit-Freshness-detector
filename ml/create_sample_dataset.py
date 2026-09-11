from pathlib import Path
from PIL import Image, ImageDraw

root = Path('dataset')
for split in ['train', 'validation', 'test']:
    for cls in ['apple', 'banana']:
        d = root / split / cls
        d.mkdir(parents=True, exist_ok=True)
        for i in range(2):
            color = (255, 0, 0) if cls == 'apple' else (255, 255, 0)
            img = Image.new('RGB', (224, 224), color=color)
            draw = ImageDraw.Draw(img)
            draw.rectangle((40, 40, 180, 180), fill=(0, 0, 0))
            img.save(d / f'{cls}_{i}.jpg')

print('Sample dataset created in dataset/')
