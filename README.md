# SimilarFaceRecognition
Similar Face Recognition System

## Necessary File
```bash
API
┝ subject.jpg       camera.html -> estimate.phpで保存される被験者画像
┝ face.jpg          predict.pyで抽出される顔画像
┗ list.csv          クラスラベルと芸能人名のリスト
```

list.csv
```csv
0,John
1,Marry
2,Ann
…………
```

```bash
Learning
┝ cnn_model.json            CNNモデルの構造を記述したJSON
┝ cnn_model.yaml            CNNモデルの構造を記述したYAML
┗ cnn_model_weight.hdf5     CNNモデルの重みを保存したファイル
```
## Required Settings
### Setting HostName

In `API/predict.py`  
Please change your hostname

```py
Host_name = "172.21.39.178"
```

## How to use

First, Put this repository in your web public directory.

### Run API
Go `API` Directory and Run below

```bash
python3 predict.py
```

### Access System
http:// `Hostname`/SimilarFaceRecognition

You can access the system.
