import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "Custom.AutoDownload",
    async setup() {
        api.addEventListener("auto_download_direct", (event) => {
            const { data, filename } = event.detail;
            const blob = base64ToBlob(data, "image/png");
            const url = window.URL.createObjectURL(blob);
            
            const link = document.createElement("a");
            link.href = url;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            const nodes = app.graph.findNodesByType("AutoDownloadNode");
            if (nodes && nodes.length > 0) {
                const node = nodes.find(n => n.widgets_values?.[0] === filename.split('_')[0]) || nodes[nodes.length - 1];
                if (node) {
                    node.imgs = [new Image()];
                    node.imgs[0].src = url;
                    node.setDirtyCanvas(true);
                }
            }
        });
    }
});

function base64ToBlob(base64, type) {
    const binStr = atob(base64);
    const len = binStr.length;
    const arr = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        arr[i] = binStr.charCodeAt(i);
    }
    return new Blob([arr], { type: type });
}
