document.addEventListener('DOMContentLoaded', () => {
    // 初始化元素引用
    const loader = document.getElementById('loader');
    const forestAnimation = document.getElementById('forest-animation');
    const mainSection = document.getElementById('main-section');
    const forestVideo = document.getElementById('forest-video');
    const skipBtn = document.querySelector('.skip-animation');
    const dialogueText = document.querySelector('.dialogue-text');
    const quizSection = document.getElementById('quiz-section');
    const teacherK = document.querySelector('.character-img');
    const teacherIntroSection = document.getElementById('teacher-intro-section');
    const backToIndexBtn = document.getElementById('back-to-index-btn');
    const bgMusic = document.getElementById('bg-music');
    const audioPrompt = document.getElementById('audio-prompt');
    const typeSound = document.getElementById('type-sound');

    // 狀態變量
    let typeWriterTimeout = null;
    let isTyping = false;

    // 初始化頁面
    setTimeout(() => {
        loader.style.display = 'none';
        initVideo();
    }, 1000);

    // 初始化影片
    function initVideo() {
        if (!forestVideo) return;

        // 確保影片靜音以符合瀏覽器自動播放政策
        forestVideo.muted = true;
        
        forestVideo.addEventListener('loadeddata', () => {
            forestVideo.play().catch(handleVideoError);
        });
        
        forestVideo.addEventListener('ended', handleAnimationEnd);
        forestVideo.addEventListener('error', handleVideoError);
        
        if (skipBtn) {
            skipBtn.addEventListener('click', handleAnimationEnd);
        }
    }

    function handleVideoError(error) {
        console.error('影片處理錯誤:', error);
        handleAnimationEnd();
    }

    function handleAnimationEnd() {
        if (!forestAnimation || !mainSection) return;

        forestAnimation.style.opacity = '0';
        setTimeout(() => {
            forestAnimation.style.display = 'none';
            mainSection.style.display = 'flex';
            void mainSection.offsetHeight; // 強制重繪
            mainSection.classList.add('active');
            
            // 只有當不在介紹頁面時才啟動對話
            if (!teacherIntroSection || teacherIntroSection.style.display !== 'flex') {
                startDialogue();
            }
        }, 800);
    }

    // 打字機效果（優化版）
    function startDialogue() {
        if (!dialogueText || isTyping) return;

        const textLines = [
            "歡迎來到潛意識財富森林！",
            "我是潛意識無限學院的院長",
            "～大K老師～",
            "準備好探索你的金錢動物了嗎？"
        ];

        dialogueText.textContent = '';
        isTyping = true;
        let lineIndex = 0;
        let charIndex = 0;

        const typeWriter = () => {
            if (lineIndex < textLines.length) {
                if (charIndex < textLines[lineIndex].length) {
                    // 逐字顯示
                    dialogueText.textContent += textLines[lineIndex][charIndex];
                    charIndex++;
                    
                    // 播放打字音效
                    playTypeSound();
                    
                    typeWriterTimeout = setTimeout(typeWriter, 100);
                } else {
                    // 換行（最後一行不加換行）
                    if (lineIndex < textLines.length - 1) {
                        dialogueText.appendChild(document.createElement('br'));
                    }
                    lineIndex++;
                    charIndex = 0;
                    typeWriterTimeout = setTimeout(typeWriter, 500);
                }
            } else {
                // 打字完成
                isTyping = false;
                if (quizSection) {
                    quizSection.style.display = 'flex';
                }
            }
        };

        // 清除之前的計時器
        if (typeWriterTimeout) {
            clearTimeout(typeWriterTimeout);
        }
        typeWriter();
    }

    function playTypeSound() {
        if (!typeSound) return;
        typeSound.currentTime = 0;
        typeSound.play().catch(e => console.error('打字音效播放失敗:', e));
    }

    // 大K老師介紹功能
    if (teacherK) {
        teacherK.addEventListener('click', () => {
            if (!teacherIntroSection || !mainSection) return;
            
            // 停止當前打字效果
            if (typeWriterTimeout) {
                clearTimeout(typeWriterTimeout);
                isTyping = false;
            }
            
            mainSection.style.display = 'none';
            teacherIntroSection.style.display = 'flex';
            
            // 添加歷史記錄以便瀏覽器返回按鈕工作
            window.history.pushState({ page: 'teacher' }, '', '#teacher');
        });
    }

    if (backToIndexBtn) {
        backToIndexBtn.addEventListener('click', () => {
            if (!teacherIntroSection || !mainSection) return;
            
            teacherIntroSection.style.display = 'none';
            mainSection.style.display = 'flex';
            
            // 如果不是從動畫過來，重新開始對話
            if (forestAnimation.style.display === 'none') {
                startDialogue();
            }
            
            window.history.pushState({ page: 'main' }, '', '#main');
        });
    }

    // 處理瀏覽器返回按鈕
    window.addEventListener('popstate', () => {
        if (teacherIntroSection && teacherIntroSection.style.display === 'flex') {
            backToIndexBtn.click();
        }
    });

    // 音效處理
    function initAudio() {
        if (!bgMusic) return;
        
        bgMusic.volume = 0.6;
        bgMusic.play().catch(e => {
            console.log('音效需要用戶交互後才能播放');
            if (audioPrompt) {
                audioPrompt.style.display = 'block';
            }
        });
    }

    // 點擊頁面啟用音效
    document.body.addEventListener('click', () => {
        if (bgMusic && bgMusic.paused) {
            bgMusic.play().catch(e => console.error('音效播放失敗:', e));
            if (audioPrompt) {
                audioPrompt.style.display = 'none';
            }
        }
    });

    // 初始化音效
    initAudio();
});