// 関数は全てトップレベルで定義する
async function send() {
    const input = document.getElementById('userInput').value;
    const mermaidDiv = document.getElementById('mermaid-graph');
    if (!input) return alert("入力してください");

    mermaidDiv.innerHTML = "生成中...";

    try {
        const res = await fetch('/api', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: input })
        });
        const data = await res.json();
        
        // AIの回答からコードを抽出
        let code = data.content;
        const match = code.match(/```mermaid([\s\S]*?)```/);
        if (match) {
            code = match[1].trim();
        }
        
        renderMermaid(code);
        loadHistory();
    } catch (err) {
        mermaidDiv.innerHTML = "エラー: " + err.message;
    }
}

function renderMermaid(code) {
    const mermaidDiv = document.getElementById('mermaid-graph');
    // mermaidオブジェクトが定義されているか確認
    if (typeof mermaid === 'undefined') {
        mermaidDiv.innerHTML = "エラー: mermaidが読み込まれていません";
        return;
    }
    
    // 描画実行
    mermaidDiv.innerHTML = `<pre class="mermaid">${code}</pre>`;
    mermaid.run();
}

function changeTheme(theme) {
    if (typeof mermaid === 'undefined') return;
    mermaid.initialize({ startOnLoad: false, theme: theme });
    mermaid.run();
}

async function loadHistory() {
    try {
        const res = await fetch('/api/history');
        const history = await res.json();
        document.getElementById('history-list').innerHTML = 
            history.map(h => `<li>${h.input}</li>`).join('');
    } catch (err) {
        console.error("履歴の取得に失敗しました:", err);
    }
}

async function downloadPNG() {
    const svg = document.querySelector('svg');
    if (!svg) return alert("図が生成されていません");
    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svg);
    const canvas = document.createElement("canvas");
    const img = new Image();
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(source)));
    img.onload = () => {
        canvas.width = img.width; 
        canvas.height = img.height;
        canvas.getContext("2d").drawImage(img, 0, 0);
        const a = document.createElement("a");
        a.href = canvas.toDataURL("image/png");
        a.download = "diagram.png";
        a.click();
    };
}