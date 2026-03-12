async function send() {
    const input = document.getElementById('userInput').value;
    const outputText = document.getElementById('output-text');
    const mermaidDiv = document.getElementById('mermaid-graph');

    if (!input) {
        alert("テキストを入力してください");
        return;
    }

    outputText.innerText = "AIが思考中... データベースに保存を準備しています...";
    mermaidDiv.innerHTML = "";

    try {
        const res = await fetch('/api', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: input })
        });

        if (!res.ok) throw new Error(`サーバーエラー: ${res.status}`);

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

        // 描画処理
        if (mermaidCode) {
            const pre = document.createElement("pre");
            pre.className = "mermaid";
            pre.textContent = mermaidCode;
            mermaidDiv.appendChild(pre);
            
            // Mermaidレンダリングを実行
            await mermaid.run({ nodes: [pre] });
        } else {
            mermaidDiv.innerHTML = "<p style='color:orange;'>図のコードが生成されませんでした。文章を確認してください。</p>";
        }

    } catch (err) {
        console.error("Error:", err);
        outputText.innerText = "エラーが発生しました: " + err.message;
    }
}