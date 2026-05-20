# YOLO Dataset Tools
[English follows Japanese]
---
## 🇯🇵 日本語 (Japanese)
画像とCSVデータから、AI学習用の「YOLOフォーマット」のデータセットを自動構築し、バウンディングボックスの描画・プレビューを行うためのPythonスクリプト群です。
### ファイル構成
* **`Folder_Images_to_yaml_labels.py`**
  CSVデータ（座標情報など）と元画像群を読み込み、YOLO学習に必要なフォルダ構成（`images/` と `labels/`）および設定ファイル（`dataset.yaml`）を自動生成するスクリプトです。
* **`preview_yolo_labels.py`**
  生成されたYOLOフォーマットのデータセットを読み込み、画像上にバウンディングボックスとクラス名を描画して順番にプレビュー表示する確認用スクリプトです。
### 動作環境 (必要なライブラリ)
スクリプトを実行するには以下のPythonライブラリが必要です。
bash
pip install pandas opencv-python numpy


使い方
### 1. データセットの構築 (`python3 Folder_Images_to_yaml_labels.py`)
Folder_Images_to_yaml_labels.py をエディタで開き、スクリプト下部にある以下のパスをご自身の環境に合わせて変更してください。

path_archive: 座標情報などが入ったCSVファイルのパス
dir_images: 元画像が入っているフォルダのパス
dir_save_base: データセットを出力するフォルダのパス
設定後、以下のコマンドを実行します。

bash
python3 Folder_Images_to_yaml_labels.py
実行が完了すると、出力先フォルダに images フォルダ、labels フォルダ、および dataset.yaml が作成されます。

### 2. データセットのプレビュー・確認（｀preview_yolo_labels.py｀）
データセットが正しく作成されているかを確認するため、preview_yolo_labels.py を実行します。 （※こちらもスクリプト内の読み込み先パスを、ご自身の環境に合わせて変更してください）

bash
python3 preview_yolo_labels.py
プレビュー画面の操作方法

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
  ```bash
  python3 filter_small_bboxes.py


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

bash
python3 Folder_Images_to_yaml_labels.py
Once execution is complete, the images folder, labels folder, and dataset.yaml will be created in the output directory.

2. Previewing and Verifying the Dataset
Run preview_yolo_labels.py to check if the dataset has been created correctly. (Please also change the read paths in this script to match your environment.)

bash
python3 preview_yolo_labels.py
Preview Controls

3. Filtering and Evacuating Small Bounding Boxes (filter_small_bboxes.py)
A script to detect and safely exclude (evacuate) bounding boxes that are too small (e.g., noise or extremely difficult to detect) from the YOLO dataset.

Key Features:
Calculates the area ratio (width * height) of the labels and excludes boxes smaller than the specified threshold (MIN_AREA_RATIO) from the text files.
If all boxes in an image are excluded, the image and its label are automatically moved to an evacuated/ folder. This ensures safety as the data is not permanently deleted.
After processing, it automatically counts and displays the total number of remaining and evacuated datasets in the terminal.
Usage: Adjust the MIN_AREA_RATIO value in the script (currently set to 0.0023, which evacuates about half of the dataset) and run the following command:
bash
python3 filter_small_bboxes.py

f key: Next image
d key: Previous image
q or ESC key: Exit preview
