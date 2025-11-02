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

## ⚙️ システムプロンプトの上書き (上級者向けオプション)

このノードでは、Geminiモデルへの指示内容であるシステムプロンプトをカスタマイズできます。これにより、Danbooruタグ以外の出力形式を試したり、特定のタグ付けの傾向（例: より詳細な背景、特定のカメラアングルを優先するなど）をモデルに強制したりすることが可能です。

### 📌 パラメータ

| パラメータ名 | 必須/任意 | 説明 |
| :--- | :--- | :--- |
| **`system_prompt_override`** | 任意 | **このフィールドにテキストを入力すると、デフォルトのプロンプト（言語検出/Danbooruタグ変換の指示）は無視され、入力した内容がそのままGeminiモデルへのシステム指示として使用されます。** |

### 💡 デフォルトの動作

`system_prompt_override` フィールドが空の場合、ノードは自動的に以下の指示をモデルに送ります（`input_language`に応じて動的に生成されます）。

> *「あなたは、画像生成AIのためのプロンプトを生成するエキスパートです。与えられた文章を、カンマ区切りの英語のdanbooruタグ形式のプロンプトに変換してください。元の文章の言語を自動で検出し、正確に英語タグに変換してください。出力はタグのみとし、それ以外の説明や前置き、後書きは一切含めないでください。」*
