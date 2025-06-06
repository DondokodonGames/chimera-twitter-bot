/* novel.js: ノベルゲーム用スクリプト */

// ストーリー JSON を読み込む
const storyData = JSON.parse(document.getElementById('story-data').textContent);
let currentChapterIndex = 0;

// DOM 要素取得
const chapterContainer = document.getElementById('chapter-container');
const prevButton = document.getElementById('prev-button');
const nextButton = document.getElementById('next-button');
const choicesContainer = document.getElementById('choices-container');
const bgmToggle = document.getElementById('bgm-toggle');
let bgmAudio = null;

// 初期化
function init() {
  loadChapter(currentChapterIndex);
  prevButton.addEventListener('click', () => navigateChapter(-1));
  nextButton.addEventListener('click', () => navigateChapter(1));
  bgmToggle.addEventListener('click', toggleBGM);
}

// チャプター読み込み
function loadChapter(index) {
  const chapter = storyData[index];
  chapterContainer.innerHTML = '';

  // BGM切り替え
  if (chapter.bgm) {
    if (bgmAudio) bgmAudio.pause();
    bgmAudio = new Audio(chapter.bgm);
    bgmAudio.loop = true;
    bgmAudio.play();
  }

  // 背景画像表示
  if (chapter.bg_image) {
    chapterContainer.style.backgroundImage = `url(${chapter.bg_image})`;
    chapterContainer.style.backgroundSize = 'cover';
  } else {
    chapterContainer.style.backgroundImage = '';
  }

  // テキスト表示
  chapter.texts.forEach(line => {
    const p = document.createElement('p');
    p.textContent = line;
    chapterContainer.appendChild(p);
  });

  // 選択肢 or 次へボタン制御
  choicesContainer.innerHTML = '';
  if (chapter.choices && chapter.choices.length > 0) {
    nextButton.disabled = true;
    chapter.choices.forEach(choice => {
      const btn = document.createElement('button');
      btn.textContent = choice.text;
      btn.addEventListener('click', () => {
        const nextIndex = storyData.findIndex(ch => ch.id === choice.next_id);
        if (nextIndex !== -1) {
          currentChapterIndex = nextIndex;
          loadChapter(currentChapterIndex);
        }
      });
      choicesContainer.appendChild(btn);
    });
  } else {
    choicesContainer.innerHTML = '';
    nextButton.disabled = (index >= storyData.length - 1);
  }

  prevButton.disabled = (index <= 0);
}

// ナビゲーション
function navigateChapter(direction) {
  const newIndex = currentChapterIndex + direction;
  if (newIndex >= 0 && newIndex < storyData.length) {
    currentChapterIndex = newIndex;
    loadChapter(currentChapterIndex);
  }
}

// BGM ON/OFF
function toggleBGM() {
  if (bgmAudio) {
    if (bgmAudio.paused) {
      bgmAudio.play();
      bgmToggle.textContent = 'BGM OFF';
    } else {
      bgmAudio.pause();
      bgmToggle.textContent = 'BGM ON';
    }
  }
}

// ページ読み込み後に初期化
window.addEventListener('DOMContentLoaded', init);
