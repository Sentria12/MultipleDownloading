// --- 0. CÀI ĐẶT SERVER ---
const SERVER_URL = 'http://127.0.0.1:5000'; 

// --- 1. LẤY CÁC PHẦN TỬ DOM ---
const progressList = document.getElementById('progress-list');
const historyArea = document.getElementById('history-area');
const clearHistoryButton = document.getElementById('clear-history-button');
const tabLinks = document.querySelectorAll('.tab-link');
const tabContents = document.querySelectorAll('.tab-content');

// Download (Tab 1)
const refreshFilesButton = document.getElementById('refresh-files-button');
const downloadSelectedButton = document.getElementById('download-selected-button');
const deleteSelectedButton = document.getElementById('delete-selected-button'); // Nút mới
const serverFileList = document.getElementById('server-file-list');

// --- 2. LOGIC CHUYỂN TAB ---
tabLinks.forEach(link => {
    link.addEventListener('click', () => {
        const tabId = link.getAttribute('data-tab');
        tabLinks.forEach(item => item.classList.remove('active'));
        tabContents.forEach(item => item.classList.remove('active'));
        link.classList.add('active');
        document.getElementById(tabId).classList.add('active');
        if (tabId === 'download-tab') {
            loadFilesFromServer();
        }
    });
});

// --- 3. LOGIC TẢI XUỐNG (DOWNLOAD) ---

refreshFilesButton.addEventListener('click', loadFilesFromServer);

// HÀM: Lấy danh sách các file đang được chọn
function getSelectedFiles() {
    const selectedFiles = [];
    const checkboxes = serverFileList.querySelectorAll('input[type="checkbox"]:checked');
    checkboxes.forEach(cb => {
        selectedFiles.push(cb.value);
    });
    return selectedFiles;
}

// SỰ KIỆN NÚT TẢI VỀ (Đã Cập Nhật)
downloadSelectedButton.addEventListener('click', () => {
    const selectedFiles = getSelectedFiles();

    if (selectedFiles.length === 0) {
        alert('Vui lòng chọn ít nhất một tệp để tải.');
        return;
    }

    // Logic: 1 file thì tải thẳng, 2+ file thì tải ZIP
    if (selectedFiles.length === 1) {
        startSingleDownload(selectedFiles[0]);
    } else {
        startMultipleDownload(selectedFiles);
    }
});

// HÀM: Tải 1 file (giữ nguyên đuôi)
async function startSingleDownload(filename) {
    const fileId = 'file-' + Date.now();
    addFileToUI(filename, null, 'download', fileId); 
    
    const progressBar = document.getElementById(`progress-${fileId}`);
    const statusLabel = document.getElementById(`status-${fileId}`);

    try {
        // Gọi Endpoint 3: GET /download/{filename}
        const response = await fetch(`${SERVER_URL}/download/${filename}`);
        if (!response.ok) {
            throw new Error('Server báo lỗi: ' + response.statusText);
        }

        const contentLength = response.headers.get('Content-Length');
        const totalSize = parseInt(contentLength, 10) || 1; 
        let loaded = 0;
        const reader = response.body.getReader();
        let chunks = []; 

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
            loaded += value.length;
            
            if (contentLength) { 
                const progress = Math.round((loaded / totalSize) * 100);
                progressBar.value = progress;
                statusLabel.textContent = `${progress}%`;
            } else {
                statusLabel.textContent = 'Đang tải...';
            }
        }

        // Lưu file (giữ nguyên tên)
        const blob = new Blob(chunks);
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename; // Giữ tên file gốc
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        statusLabel.textContent = 'Xong!';
        statusLabel.style.color = 'green';
        addNotification(`Tải xuống hoàn thành: ${filename}`);

    } catch (error) {
        statusLabel.textContent = 'Lỗi!';
        statusLabel.style.color = 'red';
        addNotification(`Tải xuống thất bại: ${filename}. ${error.message}`);
    }
}

// HÀM: Tải nhiều file (ZIP)
async function startMultipleDownload(filenames) {
    const zipName = "download.zip";
    const fileId = 'file-' + Date.now();
    addFileToUI(zipName, null, 'download', fileId); 
    
    const progressBar = document.getElementById(`progress-${fileId}`);
    const statusLabel = document.getElementById(`status-${fileId}`);

    try {
        // Gọi Endpoint 4: POST /download-multiple
        const response = await fetch(`${SERVER_URL}/download-multiple`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ files: filenames })
        });
        
        if (!response.ok) throw new Error('Server báo lỗi: ' + response.statusText);

        const contentLength = response.headers.get('Content-Length');
        const totalSize = parseInt(contentLength, 10) || 1; 
        let loaded = 0;
        const reader = response.body.getReader();
        let chunks = []; 

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
            loaded += value.length;
            
            if (contentLength) { 
                const progress = Math.round((loaded / totalSize) * 100);
                progressBar.value = progress;
                statusLabel.textContent = `${progress}%`;
            } else {
                statusLabel.textContent = 'Đang tải...';
            }
        }

        // Lưu file ZIP
        const blob = new Blob(chunks, { type: 'application/zip' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = zipName; 
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        statusLabel.textContent = 'Xong!';
        statusLabel.style.color = 'green';
        addNotification(`Tải ZIP hoàn thành: ${zipName}`);

    } catch (error) {
        statusLabel.textContent = 'Lỗi!';
        statusLabel.style.color = 'red';
        addNotification(`Tải ZIP thất bại. ${error.message}`);
    }
}

// HÀM: Tải danh sách tệp (hiển thị checkbox)
async function loadFilesFromServer() {
    serverFileList.innerHTML = '<i>Đang tải...</i>';
    try {
        const response = await fetch(`${SERVER_URL}/files`); 
        if (!response.ok) throw new Error('Không thể kết nối server.');
        const files = await response.json();
        serverFileList.innerHTML = ''; 
        if (files.length === 0) {
            serverFileList.innerHTML = '<i>Chưa có tệp nào trên server.</i>';
            return;
        }
        files.forEach(fileName => {
            const fileId = 'cb-' + fileName.replace(/[^a-zA-Z0-9]/g, '');
            const itemDiv = document.createElement('div');
            itemDiv.className = 'file-list-item';
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = fileId;
            checkbox.value = fileName;
            const label = document.createElement('label');
            label.htmlFor = fileId;
            label.textContent = fileName;
            itemDiv.appendChild(checkbox);
            itemDiv.appendChild(label);
            serverFileList.appendChild(itemDiv);
        });
    } catch (error) {
        serverFileList.innerHTML = `<i>Lỗi: ${error.message}</i>`;
    }
}

// --- 6. HÀM XỬ LÝ CHUNG (Cốt lõi) ---
function addFileToUI(fileName, sizeInBytes, taskType, fileId) {
    let sizeText = sizeInBytes ? `(${(sizeInBytes / (1024 * 1024)).toFixed(2)} MB)` : '';
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    fileItem.id = fileId;
    fileItem.setAttribute('data-type', taskType);
    const taskName = taskType === 'download' ? 'Tải xuống' : 'Tải lên';
    fileItem.innerHTML = `
        <span class="file-name" title="${fileName}">
            <b>[${taskName}]</b> ${fileName} ${sizeText}
        </span>
        <progress class="file-progress" id="progress-${fileId}" max="100" value="0"></progress>
        <span class="file-status" id="status-${fileId}">0%</span>
    `;
    progressList.appendChild(fileItem);
}

// --- 7. HÀM QUẢN LÝ LỊCH SỬ (CSDL Local) ---
function addNotification(message) {
    if (historyArea.textContent.includes('Chưa có thông báo')) {
        historyArea.innerHTML = '';
    }
    const notif = document.createElement('div');
    const timestamp = `[${new Date().toLocaleTimeString()}]`;
    notif.textContent = `${timestamp} ${message}`;
    historyArea.prepend(notif);
    saveHistory();
}
function saveHistory() { localStorage.setItem('downloadHistory', historyArea.innerHTML); }
function loadHistory() {
    const savedHistory = localStorage.getItem('downloadHistory');
    if (savedHistory) {
        historyArea.innerHTML = savedHistory;
    }
}
clearHistoryButton.addEventListener('click', () => {
    historyArea.innerHTML = '<div>Chưa có thông báo nào.</div>';
    localStorage.removeItem('downloadHistory');
});

// --- CHẠY KHI TẢI TRANG ---
loadHistory();
loadFilesFromServer();