document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".main-content pre code").forEach(code => {
        const pre = code.closest("pre");
        const block = document.createElement("div");
        block.className = "command-block";
        const bar = document.createElement("div");
        bar.className = "command-bar";
        const label = document.createElement("span");
        label.textContent = "Terminal";
        const button = document.createElement("button");
        button.type = "button";
        button.className = "command-copy";
        button.textContent = "Copy";
        button.setAttribute("aria-label", "Copy terminal command");
        const status = document.createElement("span");
        status.setAttribute("role", "status");
        bar.append(label, status, button);
        pre.before(block);
        block.append(bar, pre);
        button.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(code.textContent.replace(/\n$/, ""));
                status.textContent = "Copied";
                setTimeout(() => { status.textContent = ""; }, 2000);
            } catch {
                const range = document.createRange();
                range.selectNodeContents(code);
                const selection = window.getSelection();
                selection.removeAllRanges();
                selection.addRange(range);
                status.textContent = "Selected — press Ctrl+C or ⌘C";
            }
        });
    });
});
