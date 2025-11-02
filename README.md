# ComfyUI Gemini Tag Converter (多言語対応)

Gemini APIを利用して、任意の言語で書かれたテキストを、画像生成AIのための英語のDanbooru形式のタグに変換するComfyUIカスタムノードです。

## ✨ 機能

* 日本語、英語、中国語など、任意の言語のテキストを入力可能。
* 入力言語をドロップダウンから指定できるため、Geminiモデルの変換精度を向上。
* APIキーはノードのUIから直接入力でき、設定ファイルを探す必要なし。
* 出力はカンマ区切りのDanbooruタグ（文字列）。

## 📦 インストール方法

1.  このリポジトリのフォルダ (`ComfyUI_Gemini_Tag_Converter`) を、ComfyUIのカスタムノードディレクトリにクローンまたは配置します。
    ```bash
    cd ComfyUI/custom_nodes/
    git clone https://github.com/fudosanit/ComfyUI_Gemini_Tag_Converter.git
    cd ComfyUI_Gemini_Tag_Converter
    pip install -r requirements.txt
    ```
2.  ComfyUIを再起動します。
3.  起動時に、`requirements.txt`に基づいて必要な依存ライブラリ（`google-genai`）が自動的にインストールされます。

## 🔑 使用方法

1.  ComfyUIのワークフローで、**Add Node** -> **AI/Text Converter** -> **Gemini多言語→Danbooruタグ** を選択し、ノードを追加します。
2.  **`gemini_api_key`** フィールドに、あなたの**Gemini API Key**を入力します。
3.  **`input_text`** フィールドに、画像にしたいシーンを任意の言語で記述します。
4.  **`input_language`** ドロップダウンで、入力したテキストの言語を選択するか、「Auto Detect」を選択します。
5.  ノードの出力（`danbooru_tags`）を、CLIP Text Encodeノードなどに接続して使用します。

---

この3つのファイルを`ComfyUI_Gemini_Tag_Converter`フォルダに配置し、Git管理下（GitHub）に置くことで、完全なカスタムノードとして公開できます。
