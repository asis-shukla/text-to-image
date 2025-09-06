const form = document.getElementById('textForm');
const textInput = document.getElementById('textInput');
const resultSection = document.getElementById('resultSection');
const generatedText = document.getElementById('generatedText');
const generatedImage = document.getElementById('generatedImage');
const errorMsg = document.getElementById('errorMsg');
const downloadBtn = document.getElementById('downloadBtn');
const clearBtn = document.getElementById('clearBtn');
let lastImageUrl = null;

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorMsg.textContent = '';
    resultSection.style.display = 'none';
    const text = textInput.value.trim();
    if (!text) {
        errorMsg.textContent = 'Please enter some text.';
        return;
    }
    try {
        const response = await fetch('/api/text-to-image-v2', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        if (!response.ok) {
            const err = await response.json();
            errorMsg.textContent = err.detail || 'Error generating image.';
            return;
        }
        const data = await response.json();
        generatedText.textContent = data.text;
        generatedImage.src = data.image_url;
        generatedImage.alt = data.text;
        lastImageUrl = data.image_url;
        resultSection.style.display = 'block';
    } catch (err) {
        errorMsg.textContent = 'Network error. Please try again.';
    }
});

downloadBtn.addEventListener('click', () => {
    if (generatedImage.src) {
        const link = document.createElement('a');
        link.href = generatedImage.src;
        link.download = generatedImage.src.split('/').pop();
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
});

clearBtn.addEventListener('click', async () => {
    if (!lastImageUrl) return;
    try {
        const filename = lastImageUrl.split('/').pop();
        const response = await fetch('/api/clear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename })
        });
        if (!response.ok) {
            const err = await response.json();
            errorMsg.textContent = err.detail || 'Error clearing image.';
            return;
        }
        // Clear UI
        generatedText.textContent = '';
        generatedImage.src = '';
        generatedImage.alt = '';
        resultSection.style.display = 'none';
        textInput.value = '';
        lastImageUrl = null;
    } catch (err) {
        errorMsg.textContent = 'Network error. Please try again.';
    }
});

// Auto-expand textarea from 3 to 10 rows, then show scrollbar
const textarea = document.getElementById('textInput');
const minRows = 3;
const maxRows = 10;
textarea.addEventListener('input', function () {
    this.rows = minRows;
    const lineCount = this.value.split('\n').length;
    const scrollRows = Math.floor(this.scrollHeight / 24); // 24px is approx line height
    let newRows = Math.max(lineCount, scrollRows, minRows);
    if (newRows > maxRows) {
        newRows = maxRows;
        this.style.overflowY = 'auto';
    } else {
        this.style.overflowY = 'hidden';
    }
    this.rows = newRows;
});