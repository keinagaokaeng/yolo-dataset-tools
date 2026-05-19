import os
import cv2
import glob

def parse_yaml_names(yaml_path):
    """
    dataset.yamlからクラスIDとクラス名のマッピングを取得します。
    """
    names = {}
    if not os.path.exists(yaml_path):
        print(f"Warning: {yaml_path} が見つかりません。")
        return names
        
    with open(yaml_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    in_names = False
    for line in lines:
        line = line.strip()
        if line.startswith('names:'):
            in_names = True
            continue
            
        if in_names:
            if not line:
                continue
            if ':' in line:
                parts = line.split(':')
                try:
                    idx = int(parts[0].strip())
                    name = parts[1].strip()
                    names[idx] = name
                except ValueError:
                    pass
    return names

def draw_yolo_bbox(image, label_path, names):
    """
    YOLOフォーマットのラベルファイルを読み込み、画像にバウンディングボックスを描画します。
    """
    h, w, _ = image.shape
    if not os.path.exists(label_path):
        # ラベルファイルが存在しない場合はそのまま返す
        return image
        
    with open(label_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 5:
            try:
                class_id = int(float(parts[0]))
                x_center = float(parts[1])
                y_center = float(parts[2])
                box_w = float(parts[3])
                box_h = float(parts[4])
                
                # 正規化された座標からピクセル座標へ変換
                x_c = int(x_center * w)
                y_c = int(y_center * h)
                bw = int(box_w * w)
                bh = int(box_h * h)
                
                # 左上(x1, y1)と右下(x2, y2)の座標を計算
                x1 = int(x_c - bw / 2)
                y1 = int(y_c - bh / 2)
                x2 = int(x_c + bw / 2)
                y2 = int(y_c + bh / 2)
                
                # クラス名の取得
                class_name = names.get(class_id, str(class_id))
                
                # 描画設定
                color = (0, 255, 0) # 緑色
                thickness = max(1, int(min(w, h) / 500)) # 画像サイズに合わせて線の太さを調整
                
                # バウンディングボックスの描画
                cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
                
                # ラベルテキストの描画
                label_text = f"{class_name}"
                font_scale = thickness * 0.4
                (text_w, text_h), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
                
                # テキストの背景を塗りつぶして見やすくする
                cv2.rectangle(image, (x1, max(y1 - text_h - 10, 0)), (x1 + text_w, y1), color, -1)
                cv2.putText(image, label_text, (x1, max(y1 - 5, 0)), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness)
                
            except ValueError:
                pass
                
    return image

def main():
    yaml_path = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/dataset/dataset.yaml'
    images_dir = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/dataset/images'
    labels_dir = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/dataset/labels'

    # クラス名マッピングの取得
    names = parse_yaml_names(yaml_path)
    print(f"クラス情報: {names}")

    # 画像ファイルのリストを取得
    image_paths = glob.glob(os.path.join(images_dir, '*.jpg')) + glob.glob(os.path.join(images_dir, '*.png'))
    image_paths.sort()
    
    if not image_paths:
        print(f"エラー: {images_dir} に画像が見つかりません。")
        return
        
    print(f"合計 {len(image_paths)} 枚の画像が見つかりました。")
    print("操作方法: 何かキーを押すと次の画像へ進みます。'q' または 'ESC' キーで終了します。")

    for img_path in image_paths:
        img_name = os.path.basename(img_path)
        name_no_ext, _ = os.path.splitext(img_name)
        label_path = os.path.join(labels_dir, name_no_ext + '.txt')
        
        # 画像の読み込み
        image = cv2.imread(img_path)
        if image is None:
            print(f"読み込み失敗: {img_path}")
            continue
            
        # バウンディングボックスの描画
        image = draw_yolo_bbox(image, label_path, names)
        
        # 画面に収まるようにリサイズ (最大 1200x800)
        h, w = image.shape[:2]
        max_h, max_w = 800, 1200
        if h > max_h or w > max_w:
            scale = min(max_h/h, max_w/w)
            image = cv2.resize(image, (int(w*scale), int(h*scale)))
        
        # 表示
        window_name = 'YOLO Dataset Preview'
        cv2.imshow(window_name, image)
        
        # キー入力待ち
        key = cv2.waitKey(0) & 0xFF
        
        # 'q' または 'ESC' でループを抜ける
        if key == 27 or key == ord('q'):
            print("プレビューを終了します。")
            break
            
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
