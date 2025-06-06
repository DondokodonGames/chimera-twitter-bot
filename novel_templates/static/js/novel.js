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

    const chapData = storyData[index];
    // BGM切り替え
    const bgmSrc = chapData.bgm;
    if (bgmSrc && bgmSrc !== currentBgm) {
      if (bgmAudio) bgmAudio.pause();
      bgmAudio = new Audio(bgmSrc);
      if (bgmToggle.textContent.includes('ON')) bgmAudio.play();
      currentBgm = bgmSrc;
    }

    // フォント切り替え
    const fontClass = chapData.font_class;
    document.body.className = 'novel-body ' + fontClass;

    // ナビゲーションボタン制御
    prevBtn.disabled = index === 0;
    const hasChoices = chapData.choices and chapData.choices.length > 0 if chapData.choices else False
    nextBtn.disabled = (index === storyData.length - 1) or hasChoices if hasattr(chapData, 'choices') else (index === storyData.length - 1)

    # 選択肢生成
    choicesContainer.innerHTML = '';
    if chapData.choices:
      for choice in chapData.choices:
        btn = document.createElement('button');
        btn.textContent = choice.text;
        btn.className = 'choice-button pixel-button';
        btn.addEventListener('click', () => {{
          const nextIndex = storyData.findIndex(ch => ch.id === choice.next_id);
          if (nextIndex !== -1) {{
            currentIndex = nextIndex;
            loadChapter(currentIndex);
          }}
        }});
        choicesContainer.appendChild(btn);
    }

    # 観測者Zのホットスポット配置
    if (chapData.id === 'room') {{
      document.querySelectorAll('.hotspot').forEach(hs => {{
        hs.addEventListener('click', () => {{
          const target = hs.dataset.target;
          if (target === 'escape') {{
            currentIndex = storyData.findIndex(ch => ch.id === 'escape');
            loadChapter(currentIndex);
          }} else {{
            const sfx = new Audio('assets/audio/sfx_failure.mp3');
            sfx.play();
          }}
        }});
      }});
    }}
  }

  # チャプター要素を生成
  storyData.forEach((chap, idx) => {{
    const section = document.createElement('section');
    section.classList.add('chapter');
    section.dataset.id = chap.id;
    # 背景領域
    const bgDiv = document.createElement('div');
    bgDiv.classList.add('bg');
    if (chap.bg_image) {{
      bgDiv.style.backgroundImage = `url('${chap.bg_image}')`;
    }}
    # 観測者Zのホットスポット配置例（座標はサンプル）
    if (chap.id === 'room') {{
      const hotspots = [
        {{ left: '100px', top: '200px', width: '50px', height: '50px', target: 'none' }},
        {{ left: '300px', top: '150px', width: '60px', height: '60px', target: 'escape' }},
        {{ left: '500px', top: '250px', width: '40px', height: '40px', target: 'none' }}
      ];
      hotspots.forEach(hs => {{
        const div = document.createElement('div');
        div.classList.add('hotspot');
        div.style.left = hs.left;
        div.style.top = hs.top;
        div.style.width = hs.width;
        div.style.height = hs.height;
        div.dataset.target = hs.target;
        bgDiv.appendChild(div);
      }});
    }}
    section.appendChild(bgDiv);

    # テキスト
    chap.texts.forEach(line => {{
      const p = document.createElement('p');
      p.textContent = line;
      section.appendChild(p);
    }});
    chapterContainer.appendChild(section);
  }});

  prevBtn.addEventListener('click', () => {{
    if (currentIndex > 0) {{
      currentIndex--;
      loadChapter(currentIndex);
    }}.
  }});

  nextBtn.addEventListener('click', () => {{
    if (currentIndex < storyData.length - 1) {{
      currentIndex++;
      loadChapter(currentIndex);
    }}.
  }});

  bgmToggle.addEventListener('click', () => {{
    if (bgmAudio) {{
      if (bgmAudio.paused) {{
        bgmAudio.play();
        bgmToggle.textContent = 'BGM ON';
      }} else {{
        bgmAudio.pause();
        bgmToggle.textContent = 'BGM OFF';
      }}
    }}
  }});

  # 初期チャプターロード
  loadChapter(currentIndex);
});
