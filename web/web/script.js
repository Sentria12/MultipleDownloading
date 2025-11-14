const SERVER_URL = 'http://127.0.0.1:5000'; 

// Lấy các phần tử DOM
const progressList = document.getElementById('progress-list');
const historyArea = document.getElementById('history-area');
const clearHistoryButton = document.getElementById('clear-history-button');
const refreshFilesButton = document.getElementById('refresh-files-button');
const downloadSelectedButton = document.getElementById('download-selected-button');
const deleteSelectedButton = document.getElementById('delete-selected-button');
const serverFileList = document.getElementById('server-file-list');

// Hàm hiện thông báo
function addNotification(message) {
    console.log('Thông báo:', message);
    if (historyArea.textContent.includes('Chưa có thông báo')) {
        historyArea.innerHTML = '';
    }
    const notif = document.createElement('div');
    notif.textContent = message;
    historyArea.prepend(notif);
}

// Tải danh sách file
async function loadFilesFromServer() {
    console.log('Đang tải danh sách file...');
    serverFileList.innerHTML = '<i>Đang tải...</i>';
    
    try {
        const response = await fetch(`${SERVER_URL}/files`);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`Server lỗi: ${response.status}`);
        }
        
        const files = await response.json();
        console.log('Files nhận được:', files);
        
        serverFileList.innerHTML = '';
        
        if (files.length === 0) {
            serverFileList.innerHTML = '<i>Chưa có tệp nào trên server.</i>';
            return;
        }
        
        // Hiển thị danh sách file đơn giản
        files.forEach(fileName => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'file-list-item';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = fileName;
            
            const label = document.createElement('label');
            label.textContent = fileName;
            label.style.marginLeft = '8px';
            
            itemDiv.appendChild(checkbox);
            itemDiv.appendChild(label);
            serverFileList.appendChild(itemDiv);
        });
        
        addNotification(`Đã tải ${files.length} file`);
        
    } catch (error) {
        console.error('Lỗi tải file:', error);
        serverFileList.innerHTML = `<i style="color: red;">Lỗi: ${error.message}</i>`;
        addNotification(`Lỗi: ${error.message}`);
    }
}

// Tải file đơn giản
function downloadSingleFile(filename) {
    console.log('Đang tải file:', filename);
    addNotification(`Đang tải: ${filename}`);
    
    // Tạo link tải trực tiếp
    const downloadUrl = `${SERVER_URL}/download/${filename}`;
    console.log('Download URL:', downloadUrl);
    
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    addNotification(`Đã tải: ${filename}`);
}

// Lấy file được chọn
function getSelectedFiles() {
    const checkboxes = serverFileList.querySelectorAll('input[type="checkbox"]:checked');
    const selected = [];
    checkboxes.forEach(cb => {
        selected.push(cb.value);
    });
    return selected;
}

// Sự kiện nút
refreshFilesButton.addEventListener('click', loadFilesFromServer);

downloadSelectedButton.addEventListener('click', () => {
    const selectedFiles = getSelectedFiles();
    console.log('Files được chọn:', selectedFiles);
    
    if (selectedFiles.length === 0) {
        alert('Vui lòng chọn ít nhất một tệp');
        return;
    }
    
    // Tải từng file một
    selectedFiles.forEach(file => {
        downloadSingleFile(file);
    });
});

deleteSelectedButton.addEventListener('click', async () => {
    const selectedFiles = getSelectedFiles();
    
    if (selectedFiles.length === 0) {
        alert('Vui lòng chọn file để xóa');
        return;
    }
    
    if (!confirm(`Xóa ${selectedFiles.length} file?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${SERVER_URL}/delete`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ files: selectedFiles })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            addNotification(`Đã xóa ${selectedFiles.length} file`);
            loadFilesFromServer();
        } else {
            addNotification(`Lỗi xóa: ${result.error}`);
        }
    } catch (error) {
        addNotification(`Lỗi: ${error.message}`);
    }
});

clearHistoryButton.addEventListener('click', () => {
    historyArea.innerHTML = '<div>Chưa có thông báo nào.</div>';
});

// Chạy khi khởi động
loadFilesFromServer();
