// Custom Binary Studio — Core Logic

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const symZeroInput = document.getElementById('symZero');
    const symOneInput = document.getElementById('symOne');
    const bitSeparatorSelect = document.getElementById('bitSeparator');
    const presetButtons = document.querySelectorAll('.btn-preset');
    
    const previewZero = document.getElementById('previewZero');
    const previewOne = document.getElementById('previewOne');

    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    const textInput = document.getElementById('textInput');
    const textOutput = document.getElementById('textOutput');
    const btnCopyText = document.getElementById('btnCopyText');

    const encodedInput = document.getElementById('encodedInput');
    const btnDecode = document.getElementById('btnDecode');
    const decodedOutput = document.getElementById('decodedOutput');

    const numDecimalInput = document.getElementById('numDecimal');
    const stdBinaryNum = document.getElementById('stdBinaryNum');
    const customBinaryNum = document.getElementById('customBinaryNum');

    const canvas = document.getElementById('signalCanvas');
    const ctx = canvas.getContext('2d');
    const btnAnimateSignal = document.getElementById('btnAnimateSignal');

    const gateSelect = document.getElementById('gateSelect');
    const btnInputA = document.getElementById('btnInputA');
    const btnInputB = document.getElementById('btnInputB');
    const groupInputB = document.getElementById('groupInputB');
    const logicResultBit = document.getElementById('logicResultBit');
    const logicResultSym = document.getElementById('logicResultSym');
    const truthTableBody = document.querySelector('#truthTable tbody');

    const asciiTableBody = document.querySelector('#asciiTable tbody');

    let animationId = null;
    let animProgress = 0;

    // --- 1. Symbol Configuration & Presets ---

    function getSymbols() {
        return {
            zero: symZeroInput.value || '0',
            one: symOneInput.value || '1',
            sep: bitSeparatorSelect.value
        };
    }

    function updatePreviewPills() {
        const { zero, one } = getSymbols();
        previewZero.textContent = `0 = ${zero}`;
        previewOne.textContent = `1 = ${one}`;
        
        // Refresh all translations & components
        updateTextTranslation();
        updateNumberTranslation();
        updateLogicGate();
        renderAsciiTable();
        drawSignalWave();
        renderBitButtons();
        updateImageBinaryOutputs();
    }

    // Preset button handlers
    presetButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            presetButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            symZeroInput.value = btn.dataset.zero;
            symOneInput.value = btn.dataset.one;
            updatePreviewPills();
        });
    });

    symZeroInput.addEventListener('input', () => {
        presetButtons.forEach(b => b.classList.remove('active'));
        updatePreviewPills();
    });

    symOneInput.addEventListener('input', () => {
        presetButtons.forEach(b => b.classList.remove('active'));
        updatePreviewPills();
    });

    bitSeparatorSelect.addEventListener('change', updatePreviewPills);

    // --- 2. Translation Logic ---

    function charTo8BitBinary(char) {
        const code = char.charCodeAt(0);
        return code.toString(2).padStart(8, '0');
    }

    function textToStandardBinary(text) {
        return text.split('').map(charTo8BitBinary);
    }

    function standardToCustomBinary(stdBinArray, zeroSym, oneSym, sep) {
        return stdBinArray.map(byte => {
            return byte.split('').map(bit => (bit === '0' ? zeroSym : oneSym)).join(sep);
        }).join('   '); // Space between bytes
    }

    function updateTextTranslation() {
        const text = textInput.value;
        if (!text) {
            textOutput.value = '';
            return;
        }

        const { zero, one, sep } = getSymbols();
        const stdBytes = textToStandardBinary(text);
        const customBin = standardToCustomBinary(stdBytes, zero, one, sep);
        textOutput.value = customBin;

        drawSignalWave();
    }

    textInput.addEventListener('input', updateTextTranslation);

    // Copy to clipboard
    btnCopyText.addEventListener('click', () => {
        if (!textOutput.value) return;
        navigator.clipboard.writeText(textOutput.value).then(() => {
            const originalText = btnCopyText.textContent;
            btnCopyText.textContent = '✅ Copiado!';
            setTimeout(() => btnCopyText.textContent = originalText, 1500);
        });
    });

    // Decoding custom binary back to text
    btnDecode.addEventListener('click', () => {
        const encoded = encodedInput.value.trim();
        if (!encoded) {
            decodedOutput.value = '';
            return;
        }

        const { zero, one } = getSymbols();

        // Escape symbols for regex safely
        const escapeRegExp = (str) => str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        
        let cleaned = encoded;
        // Replace custom one with '1' first, zero with '0'
        const regexOne = new RegExp(escapeRegExp(one), 'g');
        const regexZero = new RegExp(escapeRegExp(zero), 'g');

        cleaned = cleaned.replace(regexOne, '1').replace(regexZero, '0');
        // Filter out any non-0/1 characters
        cleaned = cleaned.replace(/[^01]/g, '');

        // Chunk into 8-bit blocks
        let resultText = '';
        for (let i = 0; i < cleaned.length; i += 8) {
            const byteStr = cleaned.substr(i, 8);
            if (byteStr.length === 8) {
                const charCode = parseInt(byteStr, 2);
                resultText += String.fromCharCode(charCode);
            }
        }

        decodedOutput.value = resultText || '(Formato não reconhecido)';
    });

    // Number Translation
    function updateNumberTranslation() {
        const val = parseInt(numDecimalInput.value, 10);
        if (isNaN(val) || val < 0) {
            stdBinaryNum.textContent = '0';
            customBinaryNum.textContent = getSymbols().zero;
            return;
        }

        const { zero, one, sep } = getSymbols();
        const stdBin = val.toString(2);
        stdBinaryNum.textContent = stdBin;

        const customBin = stdBin.split('').map(bit => bit === '0' ? zero : one).join(sep);
        customBinaryNum.textContent = customBin;
    }

    numDecimalInput.addEventListener('input', updateNumberTranslation);

    // Tabs navigation
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });

    // --- 3. Digital Signal Oscilloscope (Canvas) ---

    function getBitSequenceFromText() {
        const text = textInput.value || 'Ola';
        const stdBytes = textToStandardBinary(text);
        // Take up to first 32 bits for clean visualization
        return stdBytes.join('').slice(0, 32);
    }

    function drawSignalWave(progressRatio = 1.0) {
        const width = canvas.width;
        const height = canvas.height;
        ctx.clearRect(0, 0, width, height);

        const bits = getBitSequenceFromText();
        if (bits.length === 0) return;

        const { zero, one } = getSymbols();

        const paddingX = 40;
        const paddingY = 30;
        const waveWidth = width - (paddingX * 2);
        const bitWidth = waveWidth / bits.length;

        const yHigh = paddingY + 20;
        const yLow = height - paddingY - 20;

        // Grid lines
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(paddingX, yHigh);
        ctx.lineTo(width - paddingX, yHigh);
        ctx.moveTo(paddingX, yLow);
        ctx.lineTo(width - paddingX, yLow);
        ctx.stroke();

        // Voltage Labels
        ctx.fillStyle = '#9ca3af';
        ctx.font = '11px JetBrains Mono';
        ctx.textAlign = 'right';
        ctx.fillText(`HIGH (${one})`, paddingX - 8, yHigh + 4);
        ctx.fillText(`LOW (${zero})`, paddingX - 8, yLow + 4);

        // Waveform Path
        ctx.strokeStyle = '#00f2fe';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#00f2fe';
        ctx.shadowBlur = 10;

        ctx.beginPath();
        let prevY = bits[0] === '1' ? yHigh : yLow;
        let currentX = paddingX;

        ctx.moveTo(currentX, prevY);

        const maxVisibleBits = Math.floor(bits.length * progressRatio);

        for (let i = 0; i < maxVisibleBits; i++) {
            const nextY = bits[i] === '1' ? yHigh : yLow;
            const nextX = currentX + bitWidth;

            // Vertical line if state changed
            if (nextY !== prevY) {
                ctx.lineTo(currentX, nextY);
            }
            // Horizontal line across bit width
            ctx.lineTo(nextX, nextY);

            // Draw Bit Symbol text above/below line
            ctx.shadowBlur = 0;
            ctx.fillStyle = bits[i] === '1' ? '#10b981' : '#ef4444';
            ctx.font = 'bold 11px JetBrains Mono';
            ctx.textAlign = 'center';
            const labelY = bits[i] === '1' ? yHigh - 10 : yLow + 16;
            const labelSym = bits[i] === '1' ? one : zero;
            ctx.fillText(labelSym.length > 3 ? labelSym.slice(0, 3) : labelSym, currentX + (bitWidth / 2), labelY);

            ctx.shadowColor = '#00f2fe';
            ctx.shadowBlur = 10;

            prevY = nextY;
            currentX = nextX;
        }

        ctx.stroke();
        ctx.shadowBlur = 0; // Reset shadow

        // Scan Line Effect if animating
        if (progressRatio < 1.0) {
            ctx.strokeStyle = '#ec4899';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(currentX, 10);
            ctx.lineTo(currentX, height - 10);
            ctx.stroke();
        }
    }

    btnAnimateSignal.addEventListener('click', () => {
        if (animationId) cancelAnimationFrame(animationId);
        animProgress = 0;
        
        function animate() {
            animProgress += 0.02;
            if (animProgress > 1.0) {
                animProgress = 1.0;
                drawSignalWave(1.0);
                return;
            }
            drawSignalWave(animProgress);
            animationId = requestAnimationFrame(animate);
        }
        animate();
    });

    // --- 4. Logic Gates Simulator ---

    function evaluateGate(gate, a, b) {
        switch (gate) {
            case 'AND': return a & b;
            case 'OR':  return a | b;
            case 'XOR': return a ^ b;
            case 'NAND': return (a & b) ? 0 : 1;
            case 'NOR':  return (a | b) ? 0 : 1;
            case 'NOT':  return a ? 0 : 1;
            default: return 0;
        }
    }

    function toggleBitButton(btn) {
        const current = btn.dataset.bit === '1' ? '0' : '1';
        btn.dataset.bit = current;
        btn.textContent = current === '1' ? getSymbols().one : getSymbols().zero;
        updateLogicGate();
    }

    btnInputA.addEventListener('click', () => toggleBitButton(btnInputA));
    btnInputB.addEventListener('click', () => toggleBitButton(btnInputB));

    gateSelect.addEventListener('change', () => {
        if (gateSelect.value === 'NOT') {
            groupInputB.style.display = 'none';
        } else {
            groupInputB.style.display = 'flex';
        }
        updateLogicGate();
    });

    function updateLogicGate() {
        const { zero, one } = getSymbols();

        // Update button text to show custom symbols
        btnInputA.textContent = btnInputA.dataset.bit === '1' ? one : zero;
        btnInputB.textContent = btnInputB.dataset.bit === '1' ? one : zero;

        const gate = gateSelect.value;
        const bitA = parseInt(btnInputA.dataset.bit, 10);
        const bitB = parseInt(btnInputB.dataset.bit, 10);

        const resBit = evaluateGate(gate, bitA, bitB);
        const resSym = resBit === 1 ? one : zero;

        logicResultBit.textContent = resBit;
        logicResultSym.textContent = `(${resSym})`;

        // Render Truth Table
        truthTableBody.innerHTML = '';
        const combinations = gate === 'NOT' ? [[0], [1]] : [[0,0], [0,1], [1,0], [1,1]];

        combinations.forEach(([a, b]) => {
            const outBit = evaluateGate(gate, a, b ?? 0);
            const outSym = outBit === 1 ? one : zero;

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${a === 1 ? one : zero} (${a})</td>
                <td>${gate === 'NOT' ? '-' : (b === 1 ? one : zero) + ' (' + b + ')'}</td>
                <td><strong>${outBit}</strong></td>
                <td style="color: ${outBit === 1 ? '#10b981' : '#ef4444'}; font-weight: bold;">${outSym}</td>
            `;
            truthTableBody.appendChild(tr);
        });
    }

    // --- 5. Real-Time ASCII Map Table ---

    function renderAsciiTable() {
        const { zero, one, sep } = getSymbols();
        asciiTableBody.innerHTML = '';

        const sampleChars = ['A', 'B', 'C', 'X', 'Y', 'Z', 'a', 'b', 'c', '0', '1', '2', '!', '@', '#'];

        sampleChars.forEach(char => {
            const dec = char.charCodeAt(0);
            const stdBin = charTo8BitBinary(char);
            const customBin = stdBin.split('').map(b => b === '0' ? zero : one).join(sep);

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${char}</strong></td>
                <td>${dec}</td>
                <td><code>${stdBin}</code></td>
                <td><code style="color: var(--primary);">${customBin}</code></td>
            `;
            asciiTableBody.appendChild(tr);
        });
    }

    // Initial Setup
    initInteractiveBitManipulator();
    initPixelImageStudio();
    updatePreviewPills();
});

// --- 6. Pixel Image Binary Studio (8x8 Grid) ---
let pixelGridState = [
    0,1,1,0,0,1,1,0,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    0,1,1,1,1,1,1,0,
    0,0,1,1,1,1,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0
]; // Default Heart

const PRESET_HEART = [
    0,1,1,0,0,1,1,0,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    0,1,1,1,1,1,1,0,
    0,0,1,1,1,1,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0
];

const PRESET_SMILEY = [
    0,0,1,1,1,1,0,0,
    0,1,0,0,0,0,1,0,
    1,0,1,0,0,1,0,1,
    1,0,0,0,0,0,0,1,
    1,0,1,0,0,1,0,1,
    1,0,0,1,1,0,0,1,
    0,1,0,0,0,0,1,0,
    0,0,1,1,1,1,0,0
];

const PRESET_INVADER = [
    0,0,0,1,1,0,0,0,
    0,0,1,1,1,1,0,0,
    0,1,1,1,1,1,1,0,
    1,1,0,1,1,0,1,1,
    1,1,1,1,1,1,1,1,
    0,0,1,0,0,1,0,0,
    0,1,0,1,1,0,1,0,
    1,0,1,0,0,1,0,1
];

function initPixelImageStudio() {
    const matrixElem = document.getElementById('pixelMatrix');
    if (!matrixElem) return;

    // Build 64 pixel cells
    renderPixelMatrixDOM();

    // Setup Presets
    document.getElementById('btnPresetHeart')?.addEventListener('click', () => loadPixelPreset(PRESET_HEART, 'btnPresetHeart'));
    document.getElementById('btnPresetSmiley')?.addEventListener('click', () => loadPixelPreset(PRESET_SMILEY, 'btnPresetSmiley'));
    document.getElementById('btnPresetInvader')?.addEventListener('click', () => loadPixelPreset(PRESET_INVADER, 'btnPresetInvader'));
    document.getElementById('btnPresetClear')?.addEventListener('click', () => loadPixelPreset(new Array(64).fill(0), 'btnPresetClear'));

    // Copy image bits button
    document.getElementById('btnCopyImgBin')?.addEventListener('click', () => {
        const out = document.getElementById('imgBinaryOutput');
        if (!out || !out.value) return;
        navigator.clipboard.writeText(out.value).then(() => {
            const btn = document.getElementById('btnCopyImgBin');
            btn.textContent = '✅ Copiado!';
            setTimeout(() => btn.textContent = '📋 Copiar Bits', 1500);
        });
    });

    // Render from custom 64-bit input
    document.getElementById('btnRenderFromBin')?.addEventListener('click', () => {
        const inputElem = document.getElementById('imgBinaryInput');
        if (!inputElem) return;
        const val = inputElem.value.replace(/[^01]/g, '');
        if (val.length < 64) {
            alert('Por favor, insira pelo menos 64 bits (0s e 1s) para renderizar a matriz de pixels 8x8.');
            return;
        }
        pixelGridState = val.slice(0, 64).split('').map(b => parseInt(b, 10));
        renderPixelMatrixDOM();
        updateImageBinaryOutputs();
    });
}

function loadPixelPreset(presetArray, activeBtnId) {
    pixelGridState = [...presetArray];
    
    document.querySelectorAll('.pixel-controls-bar .btn-preset').forEach(b => b.classList.remove('active'));
    document.getElementById(activeBtnId)?.classList.add('active');

    renderPixelMatrixDOM();
    updateImageBinaryOutputs();
}

function renderPixelMatrixDOM() {
    const matrixElem = document.getElementById('pixelMatrix');
    if (!matrixElem) return;

    matrixElem.innerHTML = '';

    pixelGridState.forEach((state, idx) => {
        const cell = document.createElement('div');
        cell.className = `pixel-cell ${state === 1 ? 'active' : ''}`;
        cell.title = `Pixel ${idx + 1} (Bit: ${state})`;

        cell.addEventListener('click', () => {
            pixelGridState[idx] = pixelGridState[idx] === 1 ? 0 : 1;
            cell.classList.toggle('active', pixelGridState[idx] === 1);
            updateImageBinaryOutputs();
        });

        matrixElem.appendChild(cell);
    });

    updateImageBinaryOutputs();
}

function updateImageBinaryOutputs() {
    const stdOut = document.getElementById('imgBinaryOutput');
    const customOut = document.getElementById('imgCustomOutput');
    if (!stdOut || !customOut) return;

    // Standard binary string (rows of 8 bits)
    let stdRows = [];
    for (let r = 0; r < 8; r++) {
        stdRows.push(pixelGridState.slice(r * 8, (r + 1) * 8).join(''));
    }
    stdOut.value = stdRows.join('\n');

    // Custom Symbol visual representation
    const symZero = document.getElementById('symZero')?.value || '0';
    const symOne = document.getElementById('symOne')?.value || '1';
    const sep = document.getElementById('bitSeparator')?.value || '';

    let customRows = [];
    for (let r = 0; r < 8; r++) {
        const rowBits = pixelGridState.slice(r * 8, (r + 1) * 8);
        const rowCustom = rowBits.map(b => b === 1 ? symOne : symZero).join(sep);
        customRows.push(rowCustom);
    }
    customOut.value = customRows.join('\n');
}


// --- Interactive 8-Bit Manipulator ---
const currentBitArray = [0, 1, 0, 0, 0, 0, 0, 1]; // Default 'A' (65)

function initInteractiveBitManipulator() {
    const container = document.getElementById('interactiveBitRow');
    if (!container) return;

    renderBitButtons();
}

function renderBitButtons() {
    const container = document.getElementById('interactiveBitRow');
    if (!container) return;

    const symZero = document.getElementById('symZero').value || '0';
    const symOne = document.getElementById('symOne').value || '1';

    container.innerHTML = '';

    currentBitArray.forEach((bitVal, idx) => {
        const btn = document.createElement('button');
        btn.className = `interactive-bit-btn ${bitVal === 1 ? 'active' : ''}`;
        
        const sym = bitVal === 1 ? symOne : symZero;
        
        btn.innerHTML = `
            <span class="bit-val">${bitVal}</span>
            <span class="bit-sym-sub">${sym.length > 4 ? sym.slice(0, 4) + '..' : sym}</span>
        `;

        btn.addEventListener('click', () => {
            currentBitArray[idx] = currentBitArray[idx] === 1 ? 0 : 1;
            renderBitButtons();
            updateBitMatrixStats();
        });

        container.appendChild(btn);
    });

    updateBitMatrixStats();
}

function updateBitMatrixStats() {
    const decElem = document.getElementById('bitMatrixDecimal');
    const charElem = document.getElementById('bitMatrixChar');
    const customElem = document.getElementById('bitMatrixCustom');
    if (!decElem || !charElem || !customElem) return;

    const stdBinStr = currentBitArray.join('');
    const decVal = parseInt(stdBinStr, 2);

    decElem.textContent = decVal;

    // ASCII Representation
    if (decVal >= 32 && decVal <= 126) {
        charElem.textContent = `'${String.fromCharCode(decVal)}'`;
    } else {
        charElem.textContent = `(Controle / 0x${decVal.toString(16).toUpperCase()})`;
    }

    // Custom Symbol String
    const symZero = document.getElementById('symZero').value || '0';
    const symOne = document.getElementById('symOne').value || '1';
    const sep = document.getElementById('bitSeparator').value;

    const customStr = currentBitArray.map(b => b === 1 ? symOne : symZero).join(sep);
    customElem.textContent = customStr;
}

