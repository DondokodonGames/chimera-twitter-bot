// novel.js
document.addEventListener('DOMContentLoaded', () => {
  const storyData = JSON.parse(document.getElementById('story-data').textContent);
  let currentIndex = 0;

  const chapterContainer = document.getElementById('chapter-container');
  const prevBtn = document.getElementById('prev-button');
  const nextBtn = document.getElementById('next-button');
  const choicesContainer = document.getElementById('choices-container');
  const bgmToggle = document.getElementById('bgm-toggle');

  let bgmAudio = null;
  let currentBgm = null;

  function loadChapter(index) {
    const chapterElements = chapterContainer.querySelectorAll('.chapter');
    chapterElements.forEach(el => el.classList.remove('active'));
    const currentChapter = chapterElements[index];
    currentChapter.classList.add('active');

    // BGM切り替え
    const bgmSrc = storyData[index].bgm;
    if (bgmSrc && bgmSrc !== currentBgm) {
      if (bgmAudio) bgmAudio.pause();
      bgmAudio = new Audio(bgmSrc);
      if (bgmToggle.textContent.includes('ON')) bgmAudio.play();
      currentBgm = bgmSrc;
    }

    // フォント切り替え
    const fontClass = storyData[index].font_class;
    document.body.className = 'novel-body ' + fontClass;

    // ナビゲーションボタン制御
    prevBtn.disabled = index === 0;
    nextBtn.disabled = index === storyData.length - 1 || storyData[index].choices.length > 0;

    // 選択肢生成
    choicesContainer.innerHTML = '';
    if (storyData[index].choices.length > 0) {
      storyData[index].choices.forEach(choice => {
        const btn = document.createElement('button');
        btn.textContent = choice.text;
        btn.className = 'choice-button';
        btn.addEventListener('click', () => {
          const nextIndex = storyData.findIndex(ch => ch.id === choice.next_id);
          if (nextIndex !== -1) {
            currentIndex = nextIndex;
            loadChapter(currentIndex);
          }
        });
        choicesContainer.appendChild(btn);
      });
    }
  }

  // チャプター要素を生成
  storyData.forEach((chap, idx) => {
    const section = document.createElement('section');
    section.classList.add('chapter');
    section.dataset.id = chap.id;
    chap.texts.forEach(line => {
      const p = document.createElement('p');
      p.textContent = line;
      section.appendChild(p);
    });
    section.style.backgroundImage = chap.bg_image ? `url('${chap.bg_image}')` : '';
    chapterContainer.appendChild(section);
  });

  prevBtn.addEventListener('click', () => {
    if (currentIndex > 0) {
      currentIndex--;
      loadChapter(currentIndex);
    }
  });

  nextBtn.addEventListener('click', () => {
    if (currentIndex < storyData.length - 1) {
      currentIndex++;
      loadChapter(currentIndex);
    }
  });

  bgmToggle.addEventListener('click', () => {
    if (bgmAudio) {
      if (bgmAudio.paused) {
        bgmAudio.play();
        bgmToggle.textContent = 'BGM ON';
      } else {
        bgmAudio.pause();
        bgmToggle.textContent = 'BGM OFF';
      }
    }
  });

  // 初期チャプターロード
  loadChapter(currentIndex);
});
