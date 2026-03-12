async function send() {
    const input = document.getElementById('userInput').value;
    const outputText = document.getElementById('output-text');
    const mermaidDiv = document.getElementById('mermaid-graph');

    if (!input) return alert("内容を入力してください");

    outputText.innerText = "生成中...";
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

        const match = content.match(/```mermaid([\s\S]*?)```/);
        const mermaidCode = match ? match[1].trim() : (content.includes("sequenceDiagram") ? content.substring(content.indexOf("sequenceDiagram")).split("```")[0].trim() : null);

        if (mermaidCode) {
            const pre = document.createElement("pre");
            pre.className = "mermaid";
            pre.textContent = mermaidCode;
            mermaidDiv.appendChild(pre);
            try {
                await mermaid.run({ nodes: [pre] });
            } catch (e) {
                mermaidDiv.innerHTML = `<p style="color:red;">コードエラー: ${e.message}</p><pre>${mermaidCode}</pre>`;
            }
        }
    } catch (err) {
        outputText.innerText = "エラー: " + err.message;
    }
}