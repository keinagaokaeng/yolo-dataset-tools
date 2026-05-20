import os
import glob
import cv2
import numpy as np
import random

def augment_data(image, label_lines):
    # ランダムに適用する拡張フラグ
    flip_h = random.choice([True, False])
    flip_v = random.choice([True, False])
    change_color = random.choice([True, False])
    add_noise = random.choice([True, False])
    
    # 最低1つは変換が適用されるようにする（全部Falseなら水平反転をTrueにする）
    if not any([flip_h, flip_v, change_color, add_noise]):
        flip_h = True
        
    new_image = image.copy()
    
    # 画像の変換
    if flip_h:
        new_image = cv2.flip(new_image, 1)
    if flip_v:
        new_image = cv2.flip(new_image, 0)
        
    if change_color:
        alpha = random.uniform(0.7, 1.3) # コントラスト (0.7 ~ 1.3倍)
        beta = random.randint(-30, 30)   # 明るさ (-30 ~ +30)
        new_image = cv2.convertScaleAbs(new_image, alpha=alpha, beta=beta)
        
    if add_noise:
        # ランダムなガウシアンノイズ
        noise = np.random.normal(0, 10, new_image.shape).astype(np.float32)
        new_image = cv2.add(new_image.astype(np.float32), noise)
        new_image = np.clip(new_image, 0, 255).astype(np.uint8)
        
    # バウンディングボックスの座標変換
    new_label_lines = []
    for line in label_lines:
        parts = line.strip().split()
        if len(parts) >= 5:
            class_id = parts[0]
            x_c, y_c, bw, bh = map(float, parts[1:5])
            
            # 反転した場合の中心座標の再計算
            if flip_h:
                x_c = 1.0 - x_c
            if flip_v:
                y_c = 1.0 - y_c
                
            new_label_lines.append(f"{class_id} {x_c:.6f} {y_c:.6f} {bw:.6f} {bh:.6f}\n")
            
    return new_image, new_label_lines

def main():
    # 今回は dataset_split/images/train を入力および出力先とする
    train_images_dir = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/dataset_split/images/train'
    train_labels_dir = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/dataset_split/labels/train'
    
    # 対象のクラスとファイルのプレフィックス
    target_classes = {
        'Chauliodus': 'Chauliodus',
        'Avocettina': 'Avocettina',
        'Trichiurus lepturus': 'Trichiurus_lepturus'
    }
    
    # 基準となる Chauliodus の画像枚数（trainに割り当てられた数）をカウントし、TARGET_COUNTとする
    chauliodus_images = glob.glob(os.path.join(train_images_dir, 'Chauliodus-*.jpg')) + \
                        glob.glob(os.path.join(train_images_dir, 'Chauliodus-*.png'))
    TARGET_COUNT = len(chauliodus_images)
    
    if TARGET_COUNT == 0:
        print("エラー: trainフォルダ内にChauliodusの画像が見つかりません。先に split_dataset.py を実行してください。")
        return
        
    print(f"データ拡張を開始します... (目標枚数: 各クラス {TARGET_COUNT} 枚)")
    print(f"対象ディレクトリ: {train_images_dir}")
    print("-" * 40)
    
    for class_folder, prefix in target_classes.items():
        
        # 既存の画像をすべて取得
        all_image_paths = glob.glob(os.path.join(train_images_dir, '*.jpg')) + \
                          glob.glob(os.path.join(train_images_dir, '*.png'))
                          
        # 対象プレフィックス（例: Avocettina-1.jpg）で絞り込み
        current_images = [p for p in all_image_paths if os.path.basename(p).startswith(prefix + '-')]
        
        if not current_images:
            print(f"[{class_folder}] エラー: trainフォルダ内に元の画像が見つかりません。")
            print("データ拡張処理が失敗しました")
            import sys
            sys.exit(1)
            
        current_count = len(current_images)
        print(f"[{class_folder}] 現在の枚数: {current_count} 枚")
        
        shortage = TARGET_COUNT - current_count
        if shortage <= 0:
            print(f"[{class_folder}] 既に目標枚数({TARGET_COUNT}枚)に達しているため、拡張不要です。")
            print("-" * 40)
            continue
            
        print(f"[{class_folder}] 不足している {shortage} 枚の画像を拡張生成します...")
        generated_count = 0
        while generated_count < shortage:
            # 元画像からランダムに1つ選ぶ
            src_img_path = random.choice(current_images)
            basename_no_ext = os.path.splitext(os.path.basename(src_img_path))[0]
            src_label_path = os.path.join(train_labels_dir, basename_no_ext + '.txt')
            
            # 画像とラベルの読み込み
            image = cv2.imread(src_img_path)
            if image is None:
                continue
                
            label_lines = []
            if os.path.exists(src_label_path):
                with open(src_label_path, 'r', encoding='utf-8') as f:
                    label_lines = f.readlines()
                    
            # 拡張処理を適用
            aug_image, aug_label_lines = augment_data(image, label_lines)
            
            # 保存
            generated_count += 1
            new_basename = f"{prefix}_aug_{generated_count}"
            
            new_img_path = os.path.join(train_images_dir, new_basename + '.jpg')
            new_label_path = os.path.join(train_labels_dir, new_basename + '.txt')
            
            cv2.imwrite(new_img_path, aug_image)
            
            with open(new_label_path, 'w', encoding='utf-8') as f:
                f.writelines(aug_label_lines)
                
            if generated_count % 200 == 0:
                print(f"  ... {generated_count} 枚 生成完了")
                
        print(f"[{class_folder}] 拡張完了！合計 {TARGET_COUNT} 枚になりました。")
        print("-" * 40)
        
    print("すべてのデータ拡張処理が完了しました！")

if __name__ == '__main__':
    main()
