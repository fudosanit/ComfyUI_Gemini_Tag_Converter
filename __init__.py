# __init__.py

from google import genai
import os # 環境変数からキーを取得する場合などのために

class JapaneseToDanbooruTags:
    """
    Gemini APIを使用して、任意の言語のテキストを英語のDanbooruタグ形式に変換するComfyUIカスタムノード。
    APIキーやシステムプロンプトはノードUIから入力できます。
    """
    
    def __init__(self):
        pass

    @classmethod
    def IS_CHANGED(s, *args, **kwargs):
        # 常に最新の結果を得るため、変更チェックは常にTrueの動作とする
        return ""

    @classmethod
    def INPUT_TYPES(s):
        """ノードの入力（UIに表示される必須項目とオプション項目）を定義"""
        return {
            "required": {
                # APIキーの入力フィールド
                "gemini_api_key": ("STRING", {"multiline": False, "default": "", "placeholder": "Your Gemini API Key"}),
                
                # 任意の言語のテキストを受け入れる入力フィールド
                "input_text": ("STRING", {"multiline": True, "default": "A beautiful girl under a cherry tree.", "placeholder": "説明テキストを入力 (日本語、英語など)"}),
                
                # 言語選択のドロップダウン
                "input_language": (["Japanese", "English", "Chinese", "Korean", "Auto Detect"], {"default": "Auto Detect"}),
                
                # 使用するモデル名
                "model_name": ("STRING", {"default": "gemini-2.5-flash"}),
            },
            "optional": {
                # オプションのシステムプロンプト入力フィールド
                "system_prompt_override": ("STRING", {"multiline": True, "default": "", "placeholder": "カスタムシステムプロンプト (任意)"}),
            }
        }

    # ノードの表示名とカテゴリ
    FUNCTION = "execute"
    CATEGORY = "AI/Text Converter"
    
    # ノードの出力の型と名前
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("danbooru_tags",)

    # system_prompt_override をオプション引数として受け取る
    def execute(self, gemini_api_key, input_text, input_language, model_name, system_prompt_override=""):
        """ノードのメイン処理"""
        
        if not gemini_api_key:
            raise ValueError("Gemini API Keyが入力されていません。ノードの入力フィールドを確認してください。")

        # =======================================================
        # 1. system_prompt の決定ロジック
        # =======================================================
        if system_prompt_override.strip():
            # ユーザーがカスタムプロンプトを設定した場合、それを使用
            final_system_prompt = system_prompt_override.strip()
            print("[GeminiTagNode] Custom System Promptを使用します。")
        else:
            # カスタムプロンプトがない場合、従来のデフォルトプロンプトを動的に生成
            if input_language == "Auto Detect":
                final_system_prompt = (
                    "あなたは、画像生成AIのためのプロンプトを生成するエキスパートです。"
                    "与えられた文章を、カンマ区切りの英語のdanbooruタグ形式のプロンプトに変換してください。"
                    "元の文章の言語を自動で検出し、正確に英語タグに変換してください。"
                    "出力はタグのみとし、それ以外の説明や前置き、後書きは一切含めないでください。"
                )
            else:
                final_system_prompt = (
                    f"あなたは、{input_language}で書かれた文章を画像生成AIのためのプロンプトに変換するエキスパートです。"
                    "与えられた文章を、カンマ区切りの英語のdanbooruタグ形式のプロンプトに変換してください。"
                    "出力はタグのみとし、それ以外の説明や前置き、後書きは一切含めないでください。"
                )
            print(f"[GeminiTagNode] Default System Prompt (言語: {input_language}) を使用します。")


        try:
            # 2. Gemini Clientの初期化
            client = genai.Client(api_key=gemini_api_key) 
            
            # 3. API呼び出しの実行
            response = client.models.generate_content(
                model=model_name,
                contents=input_text,
                # 決定された final_system_prompt を使用
                config={"system_instruction": final_system_prompt}
            )
            
            # 4. 結果の整形と返却
            tags = response.text.strip()
            
            print(f"[GeminiTagNode] 変換結果: {tags}")
            
            # ComfyUIのノードは結果をタプルで返します
            return (tags,)

        except Exception as e:
            # APIエラーや接続エラーが発生した場合
            error_message = f"[GeminiTagNode ERROR]: API呼び出し中にエラーが発生しました: {e}"
            print(error_message)
            # エラーを発生させてノード実行を中断
            raise RuntimeError(error_message)


# ノード情報をComfyUIに登録するための辞書
NODE_CLASS_MAPPINGS = {
    "JapaneseToDanbooruTags": JapaneseToDanbooruTags
}
# ノードの表示名を登録するための辞書
NODE_DISPLAY_NAME_MAPPINGS = {
    "JapaneseToDanbooruTags": "Gemini多言語→Danbooruタグ"
}