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
        
        // AIの回答からmermaidコードを抽出
        let code = data.content;
        const match = code.match(/```mermaid([\s\S]*?)```/);
        if (match) {
            code = match[1].trim();
        }
        
        // 図を描画
        renderMermaid(code);
        loadHistory();
    } catch (err) {
        mermaidDiv.innerHTML = "エラー: " + err.message;
    }
}

function renderMermaid(code) {
    const mermaidDiv = document.getElementById('mermaid-graph');
    // 一旦プレーンテキストとしてpreタグに入れ、mermaid.runで変換させる
    mermaidDiv.innerHTML = `<pre class="mermaid">${code}</pre>`;
    mermaid.run();
}

function changeTheme(theme) {
    mermaid.initialize({ startOnLoad: false, theme: theme });
    mermaid.run();
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
        canvas.width = img.width; canvas.height = img.height;
        canvas.getContext("2d").drawImage(img, 0, 0);
        const a = document.createElement("a");
        a.href = canvas.toDataURL("image/png");
        a.download = "diagram.png";
        a.click();
    };
}

async function loadHistory() {
    const res = await fetch('/api/history');
    const history = await res.json();
    document.getElementById('history-list').innerHTML = history.map(h => `<li>${h.input}</li>`).join('');
}