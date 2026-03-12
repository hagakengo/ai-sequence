async function send() {
    const input = document.getElementById('userInput').value;
    const outputText = document.getElementById('output-text');
    const mermaidDiv = document.getElementById('mermaid-graph');

    if (!input) return alert("内容を入力してください");

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

        if (mermaidCode) {
            // 描画用の要素を作成
            const pre = document.createElement("pre");
            pre.className = "mermaid";
            pre.textContent = mermaidCode;
            mermaidDiv.appendChild(pre);
            
            // Mermaidレンダリング実行
            await mermaid.run({ nodes: [pre] });
        } else {
            mermaidDiv.innerHTML = "<p style='color:red;'>図のコードが見つかりませんでした。</p>";
        }

    } catch (err) {
        console.error("Error:", err);
        outputText.innerText = "エラー: " + err.message;
    }
}