// static/js/index.js
document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('loader');
    const forestAnimation = document.getElementById('forest-animation');
    const mainSection = document.getElementById('main-section');
    const forestVideo = document.getElementById('forest-video');
    const skipBtn = document.querySelector('.skip-animation');
    
    // 初始化頁面
    setTimeout(() => loader.style.display = 'none', 1000); // 隱藏載入動畫

    // 影片事件處理
    forestVideo.addEventListener('loadeddata', () => {
        forestVideo.play().catch(() => handleAnimationEnd());
    });

    forestVideo.addEventListener('ended', handleAnimationEnd);
    forestVideo.addEventListener('error', handleAnimationEnd);
    
    // 跳過按鈕
    skipBtn.addEventListener('click', handleAnimationEnd);

    function handleAnimationEnd() {
        forestAnimation.style.opacity = '0';
        setTimeout(() => {
            forestAnimation.style.display = 'none';
            mainSection.style.display = 'flex';
            void mainSection.offsetHeight; // 強制重繪
            mainSection.classList.add('active');
            startDialogue();
        }, 800);
    }



   

        // ==================================================
        // 以下是新增的程式碼（從跳過按鈕之後開始）
        // ==================================================
    
        // 重新測驗按鈕
        const startBtn = document.querySelector('.start-btn');
        if (startBtn) {
            startBtn.addEventListener('click', () => {
                // 重置頁面狀態
                resetPage();
                window.location.href = '/test';
            });
        }
    
        // 重置頁面狀態
        function resetPage() {
            const dialogueText = document.querySelector('.dialogue-text');
            if (dialogueText) {
                dialogueText.textContent = ''; // 清空對話框內容
            }
            if (mainSection) {
                mainSection.style.display = 'none'; // 隱藏主內容區
                mainSection.style.opacity = '0'; // 重置透明度
                mainSection.classList.remove('active'); // 移除 active 類
            }
            if (forestAnimation) {
                forestAnimation.style.display = 'flex'; // 顯示動畫區
                forestAnimation.style.opacity = '1'; // 重置透明度
            }
        }
    
       
    // 打字機效果（分段顯示）
    function startDialogue() {
        const text = [
            "歡迎來到潛意識財富森林！\n",
            "我是潛意識無限學院的院長\n",
            "～大K老師～\n",
            "準備好探索你的金錢動物了嗎？"
        ];
        const dialogueText = document.querySelector('.dialogue-text');
        if (dialogueText) {
            dialogueText.textContent = ''; // 清空原有內容
            let lineIndex = 0;
            let charIndex = 0;

            const typeWriter = () => {
                if (lineIndex < text.length) {
                    if (charIndex < text[lineIndex].length) {
                        // 逐字顯示
                        dialogueText.textContent += text[lineIndex].charAt(charIndex);
                        charIndex++;
                        const typeSound = document.getElementById('type-sound');
                        if (typeSound) {
                            typeSound.currentTime = 0; // 重置音效
                            typeSound.play(); // 播放打字音效
                        }
                        setTimeout(typeWriter, 100); // 控制打字速度
                    } else {
                        // 換行並顯示下一段文字
                        dialogueText.innerHTML += '<br>'; // 使用 <br> 換行
                        lineIndex++;
                        charIndex = 0;
                        setTimeout(typeWriter, 500); // 換行後稍作停頓
                    }
                } else {
                    // 顯示測驗按鈕
                    const quizSection = document.getElementById('quiz-section');
                    if (quizSection) {
                        quizSection.style.display = 'flex';
                    }
                }
            };
            typeWriter();
        }
    }
    
        // 音效處理
        const bgMusic = document.getElementById('bg-music');
        if (bgMusic) {
            bgMusic.volume = 0.6;
            bgMusic.play().catch(() => {
                const audioPrompt = document.getElementById('audio-prompt');
                if (audioPrompt) {
                    audioPrompt.style.display = 'block';
                }
            });
        }
    
        document.body.addEventListener('click', () => {
            if (bgMusic) {
                bgMusic.play().catch(console.error);
            }
        });
    });
