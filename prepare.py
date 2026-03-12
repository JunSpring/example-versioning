import os
import random
import shutil
from pathlib import Path

# 설정
RAW_DATA_DIR = Path("raw_data")
PROCESSED_DATA_DIR = Path("data")
TRAIN_RATIO = 0.8
SEED = 42 # 재현성을 위해 시드 고정

def prepare_data():
    # 1. 기존 결과물 삭제 (새로운 셔플을 위해)
    if PROCESSED_DATA_DIR.exists():
        shutil.rmtree(PROCESSED_DATA_DIR)
    
    # 클래스 정의 (cats, dogs)
    classes = ["cats", "dogs"]
    
    for cls in classes:
        # 2. 모든 날짜 폴더에서 해당 클래스의 이미지 수집
        all_images = []
        # data/raw/*/cats/*.jpg 패턴으로 찾기
        for img_path in RAW_DATA_DIR.glob(f"**/{cls}/*"):
            if img_path.is_file():
                all_images.append(img_path)
        
        # 3. 셔플
        random.seed(SEED)
        random.shuffle(all_images)
        
        # 4. 분할 지점 계산
        split_idx = int(len(all_images) * TRAIN_RATIO)
        train_images = all_images[:split_idx]
        val_images = all_images[split_idx:]
        
        # 5. 폴더 생성 및 하드링크 연결
        for dataset_type, images in [("train", train_images), ("validation", val_images)]:
            target_dir = PROCESSED_DATA_DIR / dataset_type / cls
            target_dir.mkdir(parents=True, exist_ok=True)
            
            for img in images:
                target_path = target_dir / img.name
                try:
                    # os.link는 파일을 복사하지 않고 주소값만 연결함 (용량 0 소모)
                    os.link(img, target_path)
                except FileExistsError:
                    pass

    print(f"✅ 데이터 준비 완료!")
    print(f"전체 이미지 수: {len(all_images) * 2} (클래스당 {len(all_images)}개)")
    print(f"결과 경로: {PROCESSED_DATA_DIR}")

if __name__ == "__main__":
    prepare_data()