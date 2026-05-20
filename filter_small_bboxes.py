import os
import glob
import shutil

def filter_small_bboxes():
    # 対象ディレクトリの設定
    dataset_base = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/rename/dataset/Chauliodus'
    images_dir = os.path.join(dataset_base, 'images')
    labels_dir = os.path.join(dataset_base, 'labels')
    
    # 退避フォルダ（小さすぎるデータを一時的に移す場所）の設定
    evacuated_base = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/rename/dataset/evacuated'
    evacuated_images_dir = os.path.join(evacuated_base, 'images')
    evacuated_labels_dir = os.path.join(evacuated_base, 'labels')
    
    # 【設定】バウンディングボックスの最小面積（幅 × 高さ）の閾値
    # 0.0023 に設定すると、現状の2682枚のデータのうち約半分が退避されます
    MIN_AREA_RATIO = 0.0023
    
    # 退避フォルダの作成
    os.makedirs(evacuated_images_dir, exist_ok=True)
    os.makedirs(evacuated_labels_dir, exist_ok=True)

    # 処理対象のラベルファイルをすべて取得
    label_paths = glob.glob(os.path.join(labels_dir, '*.txt'))
    
    if not label_paths:
        print("ラベルファイルが見つかりません。パスを確認してください。")
        return

    print(f"合計 {len(label_paths)} 個のラベルファイルのチェックを開始します...")
    print(f"閾値: 面積比 < {MIN_AREA_RATIO}")

    evacuated_bboxes_count = 0
    evacuated_images_count = 0

    for label_path in label_paths:
        with open(label_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        valid_lines = []
        is_modified = False
        
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                try:
                    w = float(parts[3])
                    h = float(parts[4])
                    area = w * h
                    
                    if area >= MIN_AREA_RATIO:
                        valid_lines.append(line)
                    else:
                        is_modified = True
                        evacuated_bboxes_count += 1
                except ValueError:
                    # 数値に変換できない不正な行は無視する（そのまま残す）
                    valid_lines.append(line)
                    
        # 変更があった場合の処理
        if is_modified:
            label_name = os.path.basename(label_path)
            name_no_ext, _ = os.path.splitext(label_name)
            
            # 対応する画像ファイルを探す（.jpg または .png）
            img_path_jpg = os.path.join(images_dir, name_no_ext + '.jpg')
            img_path_png = os.path.join(images_dir, name_no_ext + '.png')
            img_path = img_path_jpg if os.path.exists(img_path_jpg) else img_path_png
            
            if len(valid_lines) == 0:
                # この画像の有効なバウンディングボックスが0個になった場合
                # ラベルと画像を退避フォルダに移動する
                evacuated_images_count += 1
                
                dest_label_path = os.path.join(evacuated_labels_dir, label_name)
                shutil.move(label_path, dest_label_path)
                
                if os.path.exists(img_path):
                    img_name = os.path.basename(img_path)
                    dest_img_path = os.path.join(evacuated_images_dir, img_name)
                    shutil.move(img_path, dest_img_path)
            else:
                # 有効なバウンディングボックスが残っている場合は、ファイルを上書き更新する
                with open(label_path, 'w', encoding='utf-8') as f:
                    for valid_line in valid_lines:
                        f.write(valid_line)

    # 最終的なデータ数のカウント
    remaining_images = len(glob.glob(os.path.join(images_dir, '*.*')))
    remaining_labels = len(glob.glob(os.path.join(labels_dir, '*.txt')))
    evacuated_images = len(glob.glob(os.path.join(evacuated_images_dir, '*.*')))
    evacuated_labels = len(glob.glob(os.path.join(evacuated_labels_dir, '*.txt')))

    print("-" * 30)
    print("フィルタリングと退避処理が完了しました！")
    print(f"• 小さすぎてデータセットから除外（退避）されたバウンディングボックスの数 : {evacuated_bboxes_count} 個")
    print(f"• 有効なボックスがなくなり、丸ごと退避された画像ファイルの数: {evacuated_images_count} 枚")
    print("-" * 30)
    print("[ 処理後のデータ数 ]")
    print(f"✅ 残存データセット (Chauliodus)")
    print(f"   画像データ数 : {remaining_images} 枚")
    print(f"   ラベルデータ数: {remaining_labels} 個")
    print(f"📦 退避フォルダ (evacuated)")
    print(f"   画像データ数 : {evacuated_images} 枚")
    print(f"   ラベルデータ数: {evacuated_labels} 個")
    print("-" * 30)

if __name__ == '__main__':
    filter_small_bboxes()
