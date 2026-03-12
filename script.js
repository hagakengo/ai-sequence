async function send() {
    const input = document.getElementById('userInput').value;
    const res = await fetch('/api', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ input }) });
    const data = await res.json();
    renderMermaid(data.content);
    loadHistory();
}

function renderMermaid(content) {
    const match = content.match(/```mermaid([\s\S]*?)```/);
    if (match) {
        const mermaidDiv = document.getElementById('mermaid-graph');
        mermaidDiv.innerHTML = `<div class="mermaid">${match[1]}</div>`;
        mermaid.run();
    }
}

function changeTheme(theme) {
    mermaid.initialize({ startOnLoad: false, theme: theme });
    mermaid.run();
}

async function downloadPNG() {
    const svg = document.querySelector('svg');
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