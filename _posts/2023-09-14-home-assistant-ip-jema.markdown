---
layout: post
title:  "IP/JEM-A変換アダプターとHome Assistantでスマートロック"
date:   2023-09-14 22:00:00 +0900
categories: smarthome
---
## はじめに

パナソニックさんから[IP/JEM-A変換アダプター](https://av.jpn.support.panasonic.com/support/hnavi/product/ja2/index.html)という製品が発売されています。
これは電気錠やシャッター等のJEM-Aで制御する住宅設備をECHONET Lite対応コントローラーで制御するためのものです。

我が家は新築の時に[Aiseg2](https://www2.panasonic.biz/jp/densetsu/aiseg/)とこちらの変換アダプターと電気錠を設置していたので、すでにAiseg2やスマホアプリから電気錠が操作できるようになっていました。
しかしAiseg2とその周辺のスマホアプリではできることが制限されています。

|| Aiseg2本体 | ドアホン本体 | スマートHEMSアプリ | ドアホンコネクトアプリ |
|-|-|-|-|-|
|宅内から施錠|○|○|○|○|
|宅内から開錠|○|○|✖️|△(着信中のみ可)|
|外出先から施錠|-|-|○|○|
|外出先から開錠|-|-|✖️|△(着信中のみ可)|

アプリの動作も遅く使い勝手がイマイチなので、Home Assistantを使って改善してみます。

### Home Assistant

我が家では[Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)に[Home Assistant OSをインストール](https://www.home-assistant.io/installation/raspberrypi#install-home-assistant-operating-system)して運用しています。

非公式の[echonet lite インテグレーション](https://github.com/scottyphillips/echonetlite_homeassistant)を使えばechonet lite経由で操作できるのですが、我が家のアダプターは操作できないようになっていました。
ハウスメーカーがセットアップの段階でアダプターを1:1通信モードに設定していたのが原因のようです。

## 実装

LANで誰でも鍵を開錠できてしまうのはセキュアではないので、今回は1:1通信モードを解除するのではなく、アダプタの管理画面をHTTP越しに操作することにしました。

### ブラウザで操作してみる

ブラウザで次のURLにアクセスするとIP/JEM-A変換アダプターの管理画面にログインできます。

```
http://[IP/JEM-A変換アダプターのIPアドレス]:8080/
```

![認証画面](/assets/posts/home-assistant-ip-jema/auth.png){: width="300"}

認証が設定されており、次の情報が必要です。

```
ユーザー名: admin
パスワード: 設定したパスワード(デフォルト値は本体裏側に記載)
```

認証に成功すると管理画面が表示されます。
開け閉めするためのボタンと、現在の状態が表示されています。

![管理画面](/assets/posts/home-assistant-ip-jema/admin.png){: width="300"}


### Pythonで操作してみる

ブラウザから操作した時に発生するリクエストを真似て、Pythonから操作してみます。

ダイジェスト認証を通してGETメソッド(!?)でアクセスするだけで全ての操作が行えます。

[jema.py](/assets/posts/home-assistant-ip-jema/jema.py)

こんな感じで実行できます。

```bash
JEMA_BASE_URL=http://[IP/JEM-A変換アダプターのIPアドレス]:8080/ \
JEMA_PASSWORD=[パスワード] \
python3 jema.py 
```

### Home Assistantから操作

以上を踏まえてHome Assistantのカスタムコンポーネントを実装すると、こんな感じでWebやアプリから操作できるようになりました。

![Home Assistant](/assets/posts/home-assistant-ip-jema/home_assistant.png){: width="300"}

導入方法等はリポジトリを参照してください。

[jema_lock](https://github.com/sato4390/jema_lock)

## おわりに

宅内/外出先問わずHome Assistantから鍵の開け閉めができるようになりました。

[Home Assitantのコンパニオンアプリ](https://apps.apple.com/jp/app/home-assistant/id1099568401)は大変便利で、iOSのウィジェットにも対応しています。
今回の機能と組み合わせてロック画面にアクションを登録しておくと、迅速に鍵の開け閉めができるようになります。
