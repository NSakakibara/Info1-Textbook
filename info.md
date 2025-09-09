はい、承知いたしました。
WCAG 2.0のコントラスト比計算式に基づいたWebアプリケーションを作成します。

以下のHTMLコードをコピーして、`index.html`のようなファイル名で保存し、Webブラウザで開くとシミュレーターとして動作します。

-----

### 完成コード

```html
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WCAG 2.0 コントラスト比チェッカー</title>
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 600px;
        margin: 20px auto;
        padding: 0 15px;
        background-color: #f8f9fa;
    }
    h1 {
        text-align: center;
        color: #000;
    }
    .controls, .result {
        background-color: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .color-picker-group {
        display: flex;
        justify-content: space-around;
        align-items: center;
    }
    .color-picker-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    label {
        margin-bottom: 10px;
        font-weight: bold;
    }
    input[type="color"] {
        width: 80px;
        height: 40px;
        border: 1px solid #ccc;
        border-radius: 4px;
        cursor: pointer;
        padding: 0;
        background: none;
    }
    #preview {
        margin-top: 20px;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 16px;
        text-align: center;
        transition: background-color 0.3s, color 0.3s;
    }
    #preview p {
        font-weight: bold;
        font-size: 1.2em;
    }
    .result h2 {
        margin-top: 0;
        text-align: center;
    }
    #contrast-ratio {
        font-size: 2em;
        font-weight: bold;
        text-align: center;
        margin: 0;
    }
    #wcag-level {
        text-align: center;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 10px;
    }
</style>
</head>
<body>

    <h1>WCAG 2.0 コントラスト比チェッカー</h1>

    <div class="controls">
        <div class="color-picker-group">
            <div class="color-picker-item">
                <label for="bgColorPicker">背景色</label>
                <input type="color" id="bgColorPicker" value="#FFFFFF">
            </div>
            <div class="color-picker-item">
                <label for="textColorPicker">文字色</label>
                <input type="color" id="textColorPicker" value="#000000">
            </div>
        </div>
        <div id="preview">
            <p>ここにサンプルテキストが表示されます。</p>
            The quick brown fox jumps over the lazy dog.
        </div>
    </div>

    <div class="result">
        <h2>コントラスト比</h2>
        <p id="contrast-ratio">21.00</p>
        <p id="wcag-level"></p>
    </div>

<script>
    // DOM要素の取得
    const bgColorPicker = document.getElementById('bgColorPicker');
    const textColorPicker = document.getElementById('textColorPicker');
    const preview = document.getElementById('preview');
    const contrastRatioEl = document.getElementById('contrast-ratio');
    const wcagLevelEl = document.getElementById('wcag-level');

    // HEXからRGBへ変換する関数
    function hexToRgb(hex) {
        const bigint = parseInt(hex.slice(1), 16);
        const r = (bigint >> 16) & 255;
        const g = (bigint >> 8) & 255;
        const b = bigint & 255;
        return [r, g, b];
    }

    // 相対輝度を計算する関数
    function getLuminance(rgb) {
        const [r, g, b] = rgb.map(v => {
            v /= 255;
            return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }
    
    // WCAGレベルを判定する関数
    function getWcagLevel(ratio) {
        if (ratio >= 7) {
            return '<span style="color: green;">AAA (適合)</span>';
        }
        if (ratio >= 4.5) {
            return '<span style="color: #6a8f00;">AA (適合)</span>';
        }
        if (ratio >= 3) {
            return '<span style="color: orange;">AA (大きい文字)</span>';
        }
        return '<span style="color: red;">不適合</span>';
    }


    // メインの計算と表示更新を行う関数
    function updateContrast() {
        // 1. カラーピッカーから色を取得
        const bgColor = bgColorPicker.value;
        const textColor = textColorPicker.value;

        // 2. プレビューに色を適用
        preview.style.backgroundColor = bgColor;
        preview.style.color = textColor;

        // 3. コントラスト比を計算
        const bgRgb = hexToRgb(bgColor);
        const textRgb = hexToRgb(textColor);

        const lum1 = getLuminance(bgRgb);
        const lum2 = getLuminance(textRgb);

        const lighter = Math.max(lum1, lum2);
        const darker = Math.min(lum1, lum2);
        
        const contrastRatio = (lighter + 0.05) / (darker + 0.05);

        // 4. 結果を表示
        contrastRatioEl.textContent = contrastRatio.toFixed(2);
        wcagLevelEl.innerHTML = `判定: ${getWcagLevel(contrastRatio)}`;
    }

    // イベントリスナーを設定
    bgColorPicker.addEventListener('input', updateContrast);
    textColorPicker.addEventListener('input', updateContrast);

    // 初期読み込み時に一度実行
    window.addEventListener('load', updateContrast);

</script>

</body>
</html>
```

-----

### アプリケーションの機能説明

1.  **カラーピッカー**:

      * 画面上部に「背景色」と「文字色」を選択するためのカラーピッカーが2つ設置されています。
      * これをクリックすると、OS標準の色選択ダイアログが開き、直感的に色を選ぶことができます。

2.  **サンプル表示**:

      * カラーピッカーのすぐ下に、サンプル表示エリアがあります。
      * ピッカーで色を変更すると、その色がリアルタイムでこのエリアの背景色と文字色に適用され、実際の見た目を確認できます。

3.  **コントラスト比の計算と表示**:

      * サンプル表示の下に「コントラスト比」が表示されます。
      * この数値は、WCAG 2.0で定義されている計算式に基づいて、選択された2色のコントラスト比を算出したものです。
      * 数値に加えて、コントラスト比がWCAGのどの達成基準（`AAA`, `AA`, `不適合`など）を満たしているかの簡単な判定も表示されます。これにより、アクセシビリティ基準をクリアしているか一目でわかります。

### 技術的な解説

  * **HTML**: アプリケーションの骨格を定義しています。`input type="color"`でカラーピッカーを、`div`でプレビューエリアや結果表示エリアを作成しています。
  * **CSS**: 見た目を整えています。Flexboxを使ってレイアウトを調整し、カード型のデザインで情報を整理しています。
  * **JavaScript**: アプリケーションの全てのロジックを担っています。
      * `addEventListener`: カラーピッカーの値が変更された（`input`）ことを検知し、処理を開始します。
      * **色の取得と適用**: カラーピッカーの`.value`プロパティから16進数カラーコード（例: `#ffffff`）を取得し、プレビュー要素の`style`プロパティを直接変更しています。
      * **コントラスト比の計算**:
        1.  `hexToRgb`: 16進数カラーコードをRGB値（0-255）の配列に変換します。
        2.  `getLuminance`: WCAGの仕様に基づき、RGB値から**相対輝度**を計算します。この計算式は、人間の目の色の感じ方を考慮したものです。
        3.  `updateContrast`: 2つの色の相対輝度を元に、最終的なコントラスト比 `(明るい方の輝度 + 0.05) / (暗い方の輝度 + 0.05)` を計算します。
      * **結果の表示**: 計算したコントラスト比を`.toFixed(2)`で小数点以下2桁に丸めて表示しています。