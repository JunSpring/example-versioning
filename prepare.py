import os
import random
import shutil
from pathlib import Path

# 설정
RAW_DATA_DIR = Path("raw_data")
PROCESSED_DATA_DIR = Path("data")
VAL_COUNT_PER_CLASS = 400  # 클래스당 400장 (총 800장)
SEED = 42

def prepare_data():
    if PROCESSED_DATA_DIR.exists():
        shutil.rmtree(PROCESSED_DATA_DIR)
    
    classes = ["cats", "dogs"]
    
    for cls in classes:
        # 1. 모든 날짜 폴더에서 이미지 수집
        all_images = []
        for img_path in RAW_DATA_DIR.glob(f"**/{cls}/*"):
            if img_path.is_file():
                all_images.append(img_path)
        
        # 2. 셔플
        random.seed(SEED)
        random.shuffle(all_images)
        
        # 3. 개수 기반 분할 (800장을 맞추기 위해 클래스당 400장 할당)
        if len(all_images) < VAL_COUNT_PER_CLASS:
            print(f"⚠️ 경고: {cls} 이미지가 {VAL_COUNT_PER_CLASS}장보다 적습니다!")
            val_idx = len(all_images)
        else:
            val_idx = VAL_COUNT_PER_CLASS
            
        val_images = all_images[:val_idx]
        train_images = all_images[val_idx:]
        
        # 4. 하드링크 생성
        for dataset_type, images in [("train", train_images), ("validation", val_images)]:
            target_dir = PROCESSED_DATA_DIR / dataset_type / cls
            target_dir.mkdir(parents=True, exist_ok=True)
            
            for img in images:
                target_path = target_dir / img.name
                try:
                    os.link(img, target_path)
                except FileExistsError:
                    pass

    print(f"✅ 데이터 준비 완료! (Validation: 클래스당 {VAL_COUNT_PER_CLASS}장 고정)")

if __name__ == "__main__":
    prepare_data() 