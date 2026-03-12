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
    // mermaidオブジェクトの存在確認
    if (typeof mermaid === 'undefined') {
        mermaidDiv.innerHTML = "エラー: mermaidが読み込まれていません";
        return;
    }
    
    // mermaid.run を使用して動的に描画
    mermaidDiv.innerHTML = `<pre class="mermaid">${code}</pre>`;
    mermaid.run();
}

function changeTheme(theme) {
    if (typeof mermaid === 'undefined') return;
    mermaid.initialize({ startOnLoad: false, theme: theme });
    mermaid.run();
}

// 他の関数(downloadPNG, loadHistory)はそのまま維持