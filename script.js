async function send() {
    const input = document.getElementById('userInput').value;
    const outputText = document.getElementById('output-text');
    const mermaidDiv = document.getElementById('mermaid-graph');

    if (!input) {
        alert("テキストを入力してください");
        return;
    }

    outputText.innerText = "AIが図解を設計中...";
    mermaidDiv.innerHTML = "";

    try {
        const res = await fetch('/api', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: input })
        });

        const data = await res.json();
        const content = data.content;
        outputText.innerText = content;

        // Mermaidコードの抽出
        let mermaidCode = "";
        const match = content.match(/```mermaid([\s\S]*?)```/);
        if (match) {
            mermaidCode = match[1].trim();
        } else if (content.includes("sequenceDiagram")) {
            const start = content.indexOf("sequenceDiagram");
            mermaidCode = content.substring(start).split("```")[0].trim();
        }

        // 描画
        if (mermaidCode) {
            // IDを付けて、古い形式の初期化を呼び出す
            mermaidDiv.innerHTML = `<div class="mermaid-container">${mermaidCode}</div>`;
            const container = document.querySelector(".mermaid-container");
            
            // Mermaidレンダリングを実行
            await mermaid.run({
                nodes: [container]
            });
        } else {
            mermaidDiv.innerHTML = "図のデータが見つかりませんでした。";
        }

    } catch (err) {
        console.error("Error:", err);
        outputText.innerText = "エラー: " + err.message;
    }
}