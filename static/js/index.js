document.addEventListener('DOMContentLoaded', () => {
    const forestAnimation = document.getElementById('forest-animation');
    const mainSection = document.getElementById('main-section');
    const quizSection = document.getElementById('quiz-section');
    const forestVideo = document.getElementById('forest-video');
    const dialogueText = document.querySelector('.dialogue-text');
    const typeSound = document.getElementById('type-sound');
    const bgMusic = document.getElementById('bg-music');
    const audioPrompt = document.getElementById('audio-prompt');

    // 統一音量控制 (30%)
    bgMusic.volume = 0.3;
    typeSound.volume = 0.3;

    // 檢查背景音樂是否被阻止
    bgMusic.play().catch(() => {
        // 如果被阻止，顯示提示訊息
        audioPrompt.style.display = 'block';
    });

    // 用戶互動後啟用音效
    const enableAudio = () => {
        bgMusic.muted = false; // 取消靜音
        audioPrompt.style.display = 'none'; // 隱藏提示訊息
    };

    // 點擊或觸摸頁面後啟用音效
    document.body.addEventListener('click', enableAudio);
    document.body.addEventListener('touchstart', enableAudio);

    // 動畫播放結束處理
    forestVideo.addEventListener('ended', () => {
        forestAnimation.style.opacity = '0';
        setTimeout(() => {
            forestAnimation.style.display = 'none';
            mainSection.style.display = 'flex';
            setTimeout(() => {
                mainSection.style.opacity = '1';
                startDialogue();
            }, 100);
        }, 1000);
    });

    // 打字機效果
    function startDialogue() {
        const text = "歡迎來到潛意識財富大森林！\n我是潛意識無限學院的院長\n~大K老師～\n準備好探索你的財富性格了嗎？";
        let index = 0;

        const typeWriter = () => {
            if (index < text.length) {
                dialogueText.textContent += text.charAt(index);
                index++;
                typeSound.currentTime = 0; // 重置音效
                typeSound.play(); // 播放打字音效
                setTimeout(typeWriter, 100);
            } else {
                setTimeout(() => {
                    quizSection.style.display = 'flex';
                }, 1000);
            }
        };
        typeWriter();
    }

    // 確保按鈕功能
    document.querySelector('.start-btn').addEventListener('click', () => {
        window.location.href = '/test';
    });
});