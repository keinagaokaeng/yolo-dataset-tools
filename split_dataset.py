import os
import glob
import shutil
import random
import yaml

def main():
    # 再現性のためシードを固定
    random.seed(42)
    
    dataset_base = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/dataset'
    output_base  = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/dataset_split'
    
    # 対象のクラスとクラスIDの定義（dataset.yaml生成用）
    target_classes = {
        'Chauliodus': 0,
        'Avocettina': 1,
        'Trichiurus lepturus': 2
    }
    
    # プレフィックスの定義
    prefixes = {
        'Chauliodus': 'Chauliodus',
        'Avocettina': 'Avocettina',
        'Trichiurus lepturus': 'Trichiurus_lepturus'
    }
    
    splits = ['train', 'val', 'test']
    
    print("データスプリット（8:1:1）を開始します...")
    print(f"入力元: {dataset_base}")
    print(f"出力先: {output_base}")
    print("-" * 40)
    
    # 出力ディレクトリ構造の作成
    for s in splits:
        os.makedirs(os.path.join(output_base, 'images', s), exist_ok=True)
        os.makedirs(os.path.join(output_base, 'labels', s), exist_ok=True)
        
    total_train = 0
    total_val = 0
    total_test = 0
    
    for class_name, prefix in prefixes.items():
        class_dir = os.path.join(dataset_base, class_name)
        
        # すべての画像を取得
        all_image_paths = glob.glob(os.path.join(class_dir, '**', '*.jpg'), recursive=True) + \
                          glob.glob(os.path.join(class_dir, '**', '*.png'), recursive=True)
                          
        # プレフィックスで絞り込み
        images = [p for p in all_image_paths if os.path.basename(p).startswith(prefix + '-')]
        
        if not images:
            print(f"[{class_name}] 警告: 画像が見つかりませんでした。スキップします。")
            continue
            
        # シャッフル
        random.shuffle(images)
        
        total_images = len(images)
        train_end = int(total_images * 0.8)
        val_end = int(total_images * 0.9)
        
        train_imgs = images[:train_end]
        val_imgs = images[train_end:val_end]
        test_imgs = images[val_end:]
        
        print(f"[{class_name}] 計 {total_images} 枚 -> train: {len(train_imgs)}, val: {len(val_imgs)}, test: {len(test_imgs)}")
        
        total_train += len(train_imgs)
        total_val += len(val_imgs)
        total_test += len(test_imgs)
        
        # ファイルのコピーを行う内部関数
        def copy_data(img_list, split_name):
            img_out_dir = os.path.join(output_base, 'images', split_name)
            lbl_out_dir = os.path.join(output_base, 'labels', split_name)
            
            for img_path in img_list:
                basename = os.path.basename(img_path)
                # 画像のコピー
                shutil.copy2(img_path, os.path.join(img_out_dir, basename))
                
                # ラベルのコピー
                label_path = img_path.replace('/images', '/labels').rsplit('.', 1)[0] + '.txt'
                if os.path.exists(label_path):
                    shutil.copy2(label_path, os.path.join(lbl_out_dir, os.path.basename(label_path)))
                    
        # 各スプリットへコピー
        copy_data(train_imgs, 'train')
        copy_data(val_imgs, 'val')
        copy_data(test_imgs, 'test')

    print("-" * 40)
    print("データコピー完了！")
    print(f"最終枚数 -> train: {total_train}, val: {total_val}, test: {total_test}")
    
    # dataset.yaml の生成
    yaml_path = os.path.join(output_base, 'dataset.yaml')
    yaml_content = {
        'path': output_base,
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'names': {id: name for name, id in target_classes.items()}
    }
    
    with open(yaml_path, 'w', encoding='utf-8') as f:
        # YAMLの順番を綺麗にするための手動書き出し
        f.write(f"path: {yaml_content['path']}\n")
        f.write(f"train: {yaml_content['train']}\n")
        f.write(f"val: {yaml_content['val']}\n")
        f.write(f"test: {yaml_content['test']}\n\n")
        f.write("names:\n")
        for name, cls_id in target_classes.items():
            f.write(f"  {cls_id}: {name}\n")
            
    print(f"YOLO設定ファイル {yaml_path} を作成しました。")

if __name__ == '__main__':
    main()
