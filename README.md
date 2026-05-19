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
1. データセットの構築
Folder_Images_to_yaml_labels.py をエディタで開き、スクリプト下部にある以下のパスをご自身の環境に合わせて変更してください。

path_archive: 座標情報などが入ったCSVファイルのパス
dir_images: 元画像が入っているフォルダのパス
dir_save_base: データセットを出力するフォルダのパス
設定後、以下のコマンドを実行します。

bash
python3 Folder_Images_to_yaml_labels.py
実行が完了すると、出力先フォルダに images フォルダ、labels フォルダ、および dataset.yaml が作成されます。

2. データセットのプレビュー・確認
データセットが正しく作成されているかを確認するため、preview_yolo_labels.py を実行します。 （※こちらもスクリプト内の読み込み先パスを、ご自身の環境に合わせて変更してください）

bash
python3 preview_yolo_labels.py
プレビュー画面の操作方法

f キー: 次の画像へ進む
d キー: 前の画像へ戻る
q または ESC キー: プレビューを終了する


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

f key: Next image
d key: Previous image
q or ESC key: Exit preview
