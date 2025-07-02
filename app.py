<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDFレジュメ評価プロンプト生成ツール</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #ff6b6b, #feca57);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .main-content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 40px;
            padding: 25px;
            border-radius: 15px;
            background: linear-gradient(145deg, #ffffff, #f8f9fa);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        .section-title {
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: #2c3e50;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .section-title::before {
            content: '';
            width: 4px;
            height: 25px;
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            border-radius: 2px;
        }
        
        .upload-area {
            border: 3px dashed #3498db;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            background: linear-gradient(145deg, #f8f9ff, #ffffff);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .upload-area:hover {
            border-color: #2980b9;
            background: linear-gradient(145deg, #f0f7ff, #f8f9ff);
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(52, 152, 219, 0.15);
        }
        
        .upload-area.dragover {
            border-color: #27ae60;
            background: linear-gradient(145deg, #f0fff4, #f8fff8);
        }
        
        .upload-icon {
            font-size: 3rem;
            color: #3498db;
            margin-bottom: 15px;
        }
        
        .upload-text {
            font-size: 1.1rem;
            color: #34495e;
            font-weight: 500;
        }
        
        .upload-subtext {
            font-size: 0.9rem;
            color: #7f8c8d;
            margin-top: 8px;
        }
        
        .pdf-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 30px;
        }
        
        .pdf-section {
            border-radius: 12px;
            overflow: hidden;
        }
        
        .rejected-section {
            background: linear-gradient(145deg, #fff5f5, #ffffff);
            border: 2px solid #ff6b6b;
        }
        
        .accepted-section {
            background: linear-gradient(145deg, #f0fff4, #ffffff);
            border: 2px solid #27ae60;
        }
        
        .pdf-header {
            padding: 20px;
            color: white;
            font-weight: 600;
            text-align: center;
            font-size: 1.2rem;
        }
        
        .rejected-section .pdf-header {
            background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        }
        
        .accepted-section .pdf-header {
            background: linear-gradient(135deg, #27ae60, #2ecc71);
        }
        
        .file-list {
            padding: 20px;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .file-item {
            display: flex;
            align-items: center;
            justify-content: between;
            padding: 12px 15px;
            margin-bottom: 10px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease;
        }
        
        .file-item:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .file-name {
            flex: 1;
            font-weight: 500;
            color: #2c3e50;
        }
        
        .file-size {
            font-size: 0.8rem;
            color: #7f8c8d;
            margin-left: 10px;
        }
        
        .remove-btn {
            background: #e74c3c;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.8rem;
            margin-left: 10px;
            transition: background 0.2s ease;
        }
        
        .remove-btn:hover {
            background: #c0392b;
        }
        
        .generate-btn {
            display: block;
            width: 100%;
            max-width: 400px;
            margin: 40px auto;
            padding: 20px 40px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 50px;
            font-size: 1.3rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .generate-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        }
        
        .generate-btn:active {
            transform: translateY(-1px);
        }
        
        .generate-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result-section {
            display: none;
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(145deg, #f8f9fa, #ffffff);
            border-radius: 15px;
            border: 2px solid #27ae60;
        }
        
        .result-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #27ae60;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .result-content {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.05);
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            white-space: pre-wrap;
            max-height: 400px;
            overflow-y: auto;
            line-height: 1.6;
        }
        
        .download-btn {
            margin-top: 15px;
            padding: 12px 25px;
            background: #27ae60;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: background 0.2s ease;
        }
        
        .download-btn:hover {
            background: #219a52;
        }
        
        .status-message {
            margin-top: 15px;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: 500;
        }
        
        .status-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        input[type="file"] {
            display: none;
        }
        
        .instruction-upload {
            margin-bottom: 30px;
        }
        
        .instruction-content {
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            white-space: pre-wrap;
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #ddd;
        }
        
        @media (max-width: 768px) {
            .pdf-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .main-content {
                padding: 20px;
            }
            
            .section {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 PDFレジュメ評価プロンプト生成ツール</h1>
            <p>合格・不合格データからAI評価用プロンプトを自動生成</p>
        </div>
        
        <div class="main-content">
            <!-- 既存指示文アップロード -->
            <div class="section instruction-upload">
                <div class="section-title">📋 既存の指示文・評価基準をアップロード</div>
                <div class="upload-area" onclick="document.getElementById('instructionFile').click()">
                    <div class="upload-icon">📄</div>
                    <div class="upload-text">クリックして指示文ファイルを選択</div>
                    <div class="upload-subtext">.txt または .json ファイル</div>
                </div>
                <input type="file" id="instructionFile" accept=".txt,.json" onchange="handleInstructionUpload(event)">
                <div id="instructionContent" class="instruction-content" style="display: none;"></div>
            </div>
            
            <!-- PDFアップロード -->
            <div class="section">
                <div class="section-title">📚 PDFレジュメアップロード</div>
                <div class="pdf-grid">
                    <!-- 不合格者セクション -->
                    <div class="pdf-section rejected-section">
                        <div class="pdf-header">❌ 不合格者のレジュメ</div>
                        <div class="upload-area" onclick="document.getElementById('rejectedFiles').click()">
                            <div class="upload-icon">📄</div>
                            <div class="upload-text">不合格レジュメをアップロード</div>
                            <div class="upload-subtext">複数選択可能</div>
                        </div>
                        <input type="file" id="rejectedFiles" multiple accept=".pdf" onchange="handlePDFUpload(event, 'rejected')">
                        <div id="rejectedList" class="file-list"></div>
                    </div>
                    
                    <!-- 合格者セクション -->
                    <div class="pdf-section accepted-section">
                        <div class="pdf-header">✅ 合格者のレジュメ</div>
                        <div class="upload-area" onclick="document.getElementById('acceptedFiles').click()">
                            <div class="upload-icon">📄</div>
                            <div class="upload-text">合格レジュメをアップロード</div>
                            <div class="upload-subtext">複数選択可能</div>
                        </div>
                        <input type="file" id="acceptedFiles" multiple accept=".pdf" onchange="handlePDFUpload(event, 'accepted')">
                        <div id="acceptedList" class="file-list"></div>
                    </div>
                </div>
            </div>
            
            <!-- 生成ボタン -->
            <button class="generate-btn" id="generateBtn" onclick="generatePrompt()">
                🚀 指示文のプロンプトを生成
            </button>
            
            <!-- ローディング -->
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AIがレジュメを分析してプロンプトを生成しています...</p>
            </div>
            
            <!-- 結果表示 -->
            <div class="result-section" id="resultSection">
                <div class="result-title">✨ 生成されたプロンプト</div>
                <div class="result-content" id="resultContent"></div>
                <button class="download-btn" onclick="downloadResult()">📥 プロンプトをダウンロード</button>
            </div>
            
            <!-- ステータスメッセージ -->
            <div id="statusMessage"></div>
        </div>
    </div>

    <script>
        // データ格納用オブジェクト
        const appData = {
            instruction: '',
            rejectedResumes: [],
            acceptedResumes: [],
            generatedPrompt: ''
        };

        // 既存指示文のアップロード処理
        function handleInstructionUpload(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                appData.instruction = e.target.result;
                const contentDiv = document.getElementById('instructionContent');
                contentDiv.textContent = appData.instruction;
                contentDiv.style.display = 'block';
                showStatus('既存の指示文を読み込みました', 'success');
            };
            reader.readAsText(file);
        }

        // PDFアップロード処理
        async function handlePDFUpload(event, type) {
            const files = Array.from(event.target.files);
            const listElement = document.getElementById(type + 'List');
            
            for (const file of files) {
                try {
                    const text = await extractTextFromPDF(file);
                    const resumeData = {
                        name: file.name,
                        size: formatFileSize(file.size),
                        content: text,
                        id: Date.now() + Math.random()
                    };
                    
                    if (type === 'rejected') {
                        appData.rejectedResumes.push(resumeData);
                    } else {
                        appData.acceptedResumes.push(resumeData);
                    }
                    
                    addFileToList(listElement, resumeData, type);
                } catch (error) {
                    showStatus(`PDFの読み込みに失敗しました: ${file.name}`, 'error');
                }
            }
            
            updateGenerateButton();
        }

        // PDFからテキストを抽出
        async function extractTextFromPDF(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = async function(e) {
                    try {
                        const typedarray = new Uint8Array(e.target.result);
                        const pdf = await pdfjsLib.getDocument(typedarray).promise;
                        let text = '';
                        
                        for (let i = 1; i <= pdf.numPages; i++) {
                            const page = await pdf.getPage(i);
                            const textContent = await page.getTextContent();
                            const pageText = textContent.items.map(item => item.str).join(' ');
                            text += pageText + '\n';
                        }
                        
                        resolve(text);
                    } catch (error) {
                        reject(error);
                    }
                };
                reader.readAsArrayBuffer(file);
            });
        }

        // ファイルリストに追加
        function addFileToList(listElement, resumeData, type) {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <span class="file-name">${resumeData.name}</span>
                <span class="file-size">${resumeData.size}</span>
                <button class="remove-btn" onclick="removeFile('${resumeData.id}', '${type}')">削除</button>
            `;
            listElement.appendChild(fileItem);
        }

        // ファイル削除
        function removeFile(id, type) {
            if (type === 'rejected') {
                appData.rejectedResumes = appData.rejectedResumes.filter(item => item.id !== parseFloat(id));
                document.getElementById('rejectedList').innerHTML = '';
                appData.rejectedResumes.forEach(resume => {
                    addFileToList(document.getElementById('rejectedList'), resume, 'rejected');
                });
            } else {
                appData.acceptedResumes = appData.acceptedResumes.filter(item => item.id !== parseFloat(id));
                document.getElementById('acceptedList').innerHTML = '';
                appData.acceptedResumes.forEach(resume => {
                    addFileToList(document.getElementById('acceptedList'), resume, 'accepted');
                });
            }
            updateGenerateButton();
        }

        // ファイルサイズフォーマット
        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        // 生成ボタンの状態更新
        function updateGenerateButton() {
            const btn = document.getElementById('generateBtn');
            const hasData = appData.rejectedResumes.length > 0 || appData.acceptedResumes.length > 0;
            btn.disabled = !hasData;
        }

        // プロンプト生成（モックアップ版）
        async function generatePrompt() {
            const btn = document.getElementById('generateBtn');
            const loading = document.getElementById('loading');
            const resultSection = document.getElementById('resultSection');
            
            btn.disabled = true;
            loading.style.display = 'block';
            resultSection.style.display = 'none';
            
            // 実際のAI処理の代わりにモックアップ処理
            await new Promise(resolve => setTimeout(resolve, 3000));
            
            const prompt = generateMockPrompt();
            appData.generatedPrompt = prompt;
            
            document.getElementById('resultContent').textContent = prompt;
            resultSection.style.display = 'block';
            loading.style.display = 'none';
            btn.disabled = false;
            
            showStatus('プロンプトの生成が完了しました！', 'success');
        }

        // モックプロンプト生成
        function generateMockPrompt() {
            const rejectedCount = appData.rejectedResumes.length;
            const acceptedCount = appData.acceptedResumes.length;
            const totalCount = rejectedCount + acceptedCount;
            
            return `# 履歴書評価システム - 自動生成プロンプト

## 分析データ概要
- 合格者レジュメ: ${acceptedCount}件
- 不合格者レジュメ: ${rejectedCount}件
- 総分析件数: ${totalCount}件

## 評価基準 (自動抽出)

### 必須項目 (MUST)
1. **技術的スキル**: 募集職種に関連する技術スキルの明確な記載
2. **実務経験**: 3年以上の関連業務経験
3. **学習意欲**: 継続的な学習・成長への意欲の表現
4. **コミュニケーション能力**: チームワークや協調性に関する記述

### 推奨項目 (WANT)
1. **プロジェクト実績**: 具体的な成果物や達成した成果
2. **リーダーシップ経験**: チームを率いた経験や後輩指導経験
3. **資格・認定**: 業界関連の資格や認定の取得
4. **多様性**: 異なる業界や職種での経験

### 減点項目 (NG)
1. **転職頻度**: 2年未満での転職が3回以上
2. **説明不足**: 業務内容や成果の具体性に欠ける記述
3. **ネガティブ表現**: 前職や組織に対する批判的な記述
4. **基本情報不備**: 連絡先や基本的な情報の不備

## スコアリング構造
- MUST項目: 各25点 (最大100点)
- WANT項目: 各15点 (最大60点)
- NG項目: 各-20点
- 合格基準: 120点以上

## 判定指針
${appData.instruction ? `
### 既存指示文との整合性チェック
以下の既存指示文と整合性を保ちながら評価を行う：
"${appData.instruction.substring(0, 200)}..."
` : ''}

### 最終判定
1. 定量スコアが120点以上の場合は合格候補
2. 110-119点の場合は要検討（面接での確認推奨）
3. 110点未満の場合は不合格

## 注意事項
- この評価基準は過去データに基づく自動生成です
- 最終判定は人事担当者の総合判断を優先してください
- 定期的な基準見直しを推奨します

生成日時: ${new Date().toLocaleString('ja-JP')}`;
        }

        // 結果ダウンロード
        function downloadResult() {
            const blob = new Blob([appData.generatedPrompt], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `evaluation_prompt_${new Date().toISOString().split('T')[0]}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }

        // ステータスメッセージ表示
        function showStatus(message, type) {
            const statusDiv = document.getElementById('statusMessage');
            statusDiv.textContent = message;
            statusDiv.className = `status-message status-${type}`;
            setTimeout(() => {
                statusDiv.textContent = '';
                statusDiv.className = '';
            }, 3000);
        }

        // ドラッグ&ドロップ対応
        document.addEventListener('DOMContentLoaded', function() {
            const uploadAreas = document.querySelectorAll('.upload-area');
            
            uploadAreas.forEach(area => {
                area.addEventListener('dragover', function(e) {
                    e.preventDefault();
                    this.classList.add('dragover');
                });
                
                area.addEventListener('dragleave', function(e) {
                    e.preventDefault();
                    this.classList.remove('dragover');
                });
                
                area.addEventListener('drop', function(e) {
                    e.preventDefault();
                    this.classList.remove('dragover');
                    
                    if (this.onclick.toString().includes('instructionFile')) {
                        document.getElementById('instructionFile').files = e.dataTransfer.files;
                        handleInstructionUpload({target: {files: e.dataTransfer.files}});
                    } else if (this.onclick.toString().includes('rejectedFiles')) {
                        document.getElementById('rejectedFiles').files = e.dataTransfer.files;
                        handlePDFUpload({target: {files: e.dataTransfer.files}}, 'rejected');
                    } else if (this.onclick.toString().includes('acceptedFiles')) {
                        document.getElementById('acceptedFiles').files = e.dataTransfer.files;
                        handlePDFUpload({target: {files: e.dataTransfer.files}}, 'accepted');
                    }
                });
            });
        });

        // 初期化
        updateGenerateButton();
    </script>
</body>
</html>