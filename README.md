# YOLO Dataset Tools
[English follows Japanese]
---
## 🇯🇵 日本語 (Japanese)
画像とCSVデータから、AI学習用の「YOLOフォーマット」のデータセットを自動構築するためのPythonスクリプト群です。

## 動作環境 (必要なライブラリ)
スクリプトを実行するには以下のPythonライブラリが必要です。
```bash
pip install pandas opencv-python numpy
```

使い方
### 1. データセットの構築 (`python3 Folder_Images_to_yaml_labels.py`)
Folder_Images_to_yaml_labels.py をエディタで開き、スクリプト下部にある以下のパスをご自身の環境に合わせて変更してください。

path_archive: 座標情報などが入ったCSVファイルのパス
dir_images: 元画像が入っているフォルダのパス
dir_save_base: データセットを出力するフォルダのパス

実行が完了すると、出力先フォルダに images フォルダ、labels フォルダ、および dataset.yaml が作成されます。

### 2. データセットのプレビュー・確認（｀preview_yolo_labels.py｀）
データセットが正しく作成されているかを確認するため、preview_yolo_labels.py を実行します。 （※こちらもスクリプト内の読み込み先パスを、ご自身の環境に合わせて変更してください）

*プレビュー画面の操作方法
f キー: 次の画像へ進む
d キー: 前の画像へ戻る
q または ESC キー: プレビューを終了する

### 3. 小さなバウンディングボックスのフィルタリング・退避 (`filter_small_bboxes.py`)
YOLOラベルデータから、面積が小さすぎる（ノイズや検出が極めて困難な）バウンディングボックスを検出し、データセットから安全に除外（退避）するスクリプトです。
* **主な機能**:
  * ラベルの `width * height` (面積比) を計算し、指定した閾値（`MIN_AREA_RATIO`）未満のボックスをテキストから除外します。
  * 画像内のすべてのボックスが除外された場合、その画像とラベルファイルは自動的に `evacuated/`（退避フォルダ）に移動します。データを完全に削除するわけではないため安全です。
  * 処理完了後に、残存データセットと退避データの総数を自動カウントしてターミナルに分かりやすく表示します。
* **使い方**:
* 閾値は、面積比 0.001（0.1%、4K画像で約90x90ピクセル相当）を初期値として推奨
* スクリプト内の `MIN_AREA_RATIO` の数値を調整し（現状はデータの半数が退避される `0.0023` に設定されています）、以下のコマンドを実行します。

### 4.リネーム（rename_dataset.py ）
YOLOフォーマットで構成された大量のデータセットから、特定のクラス（特定の魚など）を含む画像のみを抽出し、綺麗に連番でリネームしながら別のフォルダへ整理・コピーするためのPythonスクリプトです。設定完了後、以下のコマンドで実行します。

### 5. データ分割（split_dataset.py）
すべての画像データをランダムにシャッフルし、80% を train（学習用）、10% を val（検証用）、10% を test（テスト用） に分割して新しいフォルダ（dataset_split）へコピーするスクリプトを新しく作成しました。

入力: dataset ディレクトリ（各クラスの画像）
出力: dataset_split/images/train, val, test （および対応する labels フォルダ）
dataset.yaml も同時に自動生成されるため、このフォルダをそのまま YOLO の学習コマンドに渡せます。

### 6.データ拡張(augment_dataset.py)
YOLOデータセットにおけるクラス間のデータ数不均衡を解消するデータ拡張スクリプトです。少数クラスの画像（反転、色調補正、ノイズ追加など）を自動で拡張し、多数クラスの枚数と完全に一致するまで量産します。

🇬🇧 English
A set of Python scripts to automatically build a "YOLO format" dataset for AI training from images and CSV data, and to preview the generated bounding boxes.

File Structure
Folder_Images_to_yaml_labels.py Reads CSV data (coordinates, etc.) and source images to automatically generate the folder structure (images/ and labels/) and the configuration file (dataset.yaml) required for YOLO training.
preview_yolo_labels.py A script to verify the generated YOLO format dataset. It reads the dataset, draws bounding boxes and class names on the images, and displays them sequentially for preview.
Requirements
The following Python libraries are required to run the scripts:

bash
pip install pandas opencv-python numpy
Usage
1. Building the Dataset
Open Folder_Images_to_yaml_labels.py in an editor and change the following paths at the bottom of the script to match your environment:

path_archive: Path to the CSV file containing coordinate information.
dir_images: Path to the folder containing the source images.
dir_save_base: Path to the output folder for the dataset.
After configuration, run the following command:

Once execution is complete, the images folder, labels folder, and dataset.yaml will be created in the output directory.

2. Previewing and Verifying the Dataset
Run preview_yolo_labels.py to check if the dataset has been created correctly. (Please also change the read paths in this script to match your environment.)

Preview Controls
f key: Next image
d key: Previous image
q or ESC key: Exit preview


3. Filtering and Evacuating Small Bounding Boxes (filter_small_bboxes.py)
A script to detect and safely exclude (evacuate) bounding boxes that are too small (e.g., noise or extremely difficult to detect) from the YOLO dataset.

Key Features:
Calculates the area ratio (width * height) of the labels and excludes boxes smaller than the specified threshold (MIN_AREA_RATIO) from the text files.
If all boxes in an image are excluded, the image and its label are automatically moved to an evacuated/ folder. This ensures safety as the data is not permanently deleted.
After processing, it automatically counts and displays the total number of remaining and evacuated datasets in the terminal.
Usage: Adjust the MIN_AREA_RATIO value in the script (currently set to 0.0023, which evacuates about half of the dataset) and run the following command:

4.Rename（rename_dataset.py ）
rename_dataset.py is a Python script designed to extract specific classes (e.g., a specific fish species) from a large YOLO-formatted dataset, and seamlessly copy them to a new folder while renaming them sequentially.

5.Split(split_dataset.py)
A script that automatically splits and organizes your image and label data into YOLO's standard format: train, val, and test.

Key Features
Class-Balanced Splitting: Splits data at an 8:1:1 ratio for each class individually, preventing class distribution bias in your training or test sets.
Reproducibility: Uses a fixed random seed (random.seed), ensuring you get the exact same split results every time you run it.
Auto-generates YAML: Automatically creates the dataset.yaml configuration file required for YOLO training.

6. Augmentation (augment_dataset.py)
A data augmentation script to resolve class imbalance in YOLO datasets. It automatically augments minority class images (using flips, color adjustments, and noise) to perfectly match the image count of the majority class.

Key Features
Prevents Data Leakage: Targets only the train directory, keeping val and test data completely clean.
Dynamic Target Calculation: Automatically counts the majority class images and matches minority classes to that number.
Auto Bounding Box Recalculation: YOLO label coordinates are accurately recalculated when images are flipped.
Lightweight: Runs entirely on cv2 (OpenCV) and numpy without external augmentation libraries.
