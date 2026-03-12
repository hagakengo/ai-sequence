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
        
        // --- 修正箇所: AIの回答を強引にMermaid形式に整形 ---
        let rawContent = data.content;
        // ```mermaid を除去
        let cleanCode = rawContent.replace(/```mermaid/g, '').replace(/```/g, '').trim();
        // 文法キーワードの前に強制的に改行を入れる
        cleanCode = cleanCode
            .replace(/participant/g, '\nparticipant')
            .replace(/Note/g, '\nNote')
            .replace(/->>/g, '\n->>')
            .replace(/sequenceDiagram/g, 'sequenceDiagram\n');
        // ---------------------------------------------

        renderMermaid(cleanCode);
        loadHistory();
    } catch (err) {
        mermaidDiv.innerHTML = "エラー: " + err.message;
    }
}

function renderMermaid(code) {
    const mermaidDiv = document.getElementById('mermaid-graph');
    // <pre class="mermaid"> に入れることで、ライブラリが自動検知します
    mermaidDiv.innerHTML = `<pre class="mermaid">${code}</pre>`;
    mermaid.run();
}

function changeTheme(theme) {
    mermaid.initialize({ startOnLoad: false, theme: theme });
    mermaid.run();
}

// 履歴とダウンロードはそのまま
async function loadHistory() {
    const res = await fetch('/api/history');
    const history = await res.json();
    document.getElementById('history-list').innerHTML = history.map(h => `<li>${h.input}</li>`).join('');
}