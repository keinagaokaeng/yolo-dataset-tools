import os
import glob
import shutil

def rename_dataset():
    # 入力元（元のデータセット）
    images_dir = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/dataset/images'
    labels_dir = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/dataset/labels'
    
    prefix = 'Chauliodus-'
    class_name = prefix.rstrip('-') # ハイフンを取り除いてフォルダ名（クラス名）にする
    
    # 出力先のベースディレクトリ
    out_base_dir = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/rename/dataset'
    
    # クラス名のフォルダを間に挟んで images と labels を出力
    out_images_dir = os.path.join(out_base_dir, class_name, 'images')
    out_labels_dir = os.path.join(out_base_dir, class_name, 'labels')

    # 出力先ディレクトリを作成
    os.makedirs(out_images_dir, exist_ok=True)
    os.makedirs(out_labels_dir, exist_ok=True)

    # 画像ファイルのリストを取得（サブディレクトリも含む）
    image_paths = glob.glob(os.path.join(images_dir, '**', '*.jpg'), recursive=True) + \
                  glob.glob(os.path.join(images_dir, '**', '*.png'), recursive=True)
    image_paths.sort()
    
    if not image_paths:
        print("画像が見つかりません。パスを確認してください。")
        return

    print(f"合計 {len(image_paths)} 枚の画像と、対応するラベルのコピー＆リネームを開始します...")

    for i, img_path in enumerate(image_paths, 1):
        # 元のファイル情報
        rel_path = os.path.relpath(img_path, images_dir)
        rel_dir = os.path.dirname(rel_path)
        old_name_no_ext = os.path.splitext(os.path.basename(img_path))[0]
        ext = os.path.splitext(img_path)[1]
        
        # 対応する元のラベルパス
        label_path = os.path.join(labels_dir, rel_dir, old_name_no_ext + '.txt')
        
        # 新しい連番のファイル名
        new_name_no_ext = f"{prefix}{i}"
        
        # 出力先のパス (サブフォルダを削除し、直下にフラットに出力)
        new_img_path = os.path.join(out_images_dir, new_name_no_ext + ext)
        new_label_path = os.path.join(out_labels_dir, new_name_no_ext + '.txt')
        
        # 画像をコピー
        shutil.copy2(img_path, new_img_path)
        
        # ラベルをコピー (存在する場合のみ)
        if os.path.exists(label_path):
            shutil.copy2(label_path, new_label_path)

    print("コピーとフラット化リネームが完了しました！")
    print(f"出力先:\n  {out_images_dir}\n  {out_labels_dir}")
    print(f"「{prefix}1」から「{prefix}{len(image_paths)}」までの連番で出力しました。")

if __name__ == '__main__':
    rename_dataset()
