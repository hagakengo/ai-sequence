async function send() {
    const input = document.getElementById('userInput').value;
    const outputText = document.getElementById('output-text');
    const mermaidDiv = document.getElementById('mermaid-graph');

    if (!input) {
        alert("入力欄にテキストを入力してください！");
        return;
    }

    outputText.innerText = "AIが図解を設計中...";
    mermaidDiv.innerHTML = "";

    try {
        // Vercel上のFlask API (/api) にリクエストを送信
        const res = await fetch('/api', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                input: input + "。必ずmermaid形式のsequenceDiagramコードを含めて回答してください。"
            })
        });

        if (!res.ok) throw new Error("サーバーからの応答がありません。");

        const data = await res.json();
        const content = data.content;

        // 1. 全文をテキストエリアに表示
        outputText.innerText = content;

        // 2. Mermaidコードの抽出（Markdownのバッククォート囲みを探す）
        let mermaidCode = "";
        const match = content.match(/```mermaid([\s\S]*?)```/);
        
        if (match) {
            mermaidCode = match[1].trim();
        } else if (content.includes("sequenceDiagram")) {
            // もし囲みがない場合でも、キーワードから抽出を試みる
            const start = content.indexOf("sequenceDiagram");
            mermaidCode = content.substring(start).split("```")[0].trim();
        }

        // 3. 描画処理
        if (mermaidCode) {
            mermaidDiv.innerHTML = `<pre class="mermaid">${mermaidCode}</pre>`;
            // Mermaidライブラリを使って図を描画
            await mermaid.run({ nodes: [mermaidDiv] });
        } else {
            mermaidDiv.innerHTML = "図のデータが見つかりませんでした。テキストを確認してください。";
        }
    } catch (err) {
        console.error("エラー:", err);
        outputText.innerText = "エラーが発生しました: " + err.message;
    }
}