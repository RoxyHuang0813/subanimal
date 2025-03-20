document.addEventListener('DOMContentLoaded', () => {
    const forestAnimation = document.getElementById('forest-animation');
    const mainSection = document.getElementById('main-section');
    const quizSection = document.getElementById('quiz-section');
    const forestVideo = document.getElementById('forest-video');
    const dialogueText = document.querySelector('.dialogue-text');
    const typeSound = document.getElementById('type-sound');
    const bgMusic = document.getElementById('bg-music');
    const audioPrompt = document.getElementById('audio-prompt');

    // 統一音量控制 (60%)
    bgMusic.volume = 0.6;
    typeSound.volume = 0.6;

    // 嘗試自動播放背景音樂
    const playBackgroundMusic = () => {
        bgMusic.play()
            .then(() => {
                console.log("背景音樂自動播放成功");
                audioPrompt.style.display = 'none'; // 隱藏提示訊息
            })
            .catch((error) => {
                console.log("背景音樂自動播放被阻止：", error);
                audioPrompt.style.display = 'block'; // 顯示提示訊息
            });
    };

    // 進入頁面時嘗試播放音樂
    playBackgroundMusic();

    // 用戶互動後重新嘗試播放音樂
    const enableAudio = () => {
        bgMusic.play()
            .then(() => {
                console.log("背景音樂播放成功");
                audioPrompt.style.display = 'none'; // 隱藏提示訊息
            })
            .catch((error) => {
                console.log("背景音樂播放失敗：", error);
            });
    };

    // 點擊或觸摸頁面後重新嘗試播放音樂
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