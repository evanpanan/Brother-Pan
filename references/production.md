# 工程、声音、字幕

## 项目隔离

`scripts/new_episode.py` 把基础工程、库和选定资产复制到独立项目。不要直接在安装的 skill 中制作成片；不要依赖维护者机器的绝对路径、缓存、node_modules 或凭证。工程锁文件随包提供。

项目使用 `script.json`（口播/内容源）和 `src/episode.json`（逐镜时序/字幕/镜头参数）。语音脚本更新后重新对齐，而不是把旧字幕拉伸到不匹配的声音。每镜配 `sceneId`、`kind`、`speaker`、镜头逻辑，必要素材出场清单和来源另列。

```bash
python3 scripts/new_episode.py --out /path/to/new-episode
uv run --with edge-tts==7.3.1 python scripts/prepare_voice.py --project /path/to/new-episode
python3 scripts/audit_episode.py /path/to/new-episode
```

默认声音在 `config/brand.json`。缓存键包含文本、声线、语速和音高，不能只按文稿缓存，避免改声音仍用旧音频。语音在线服务失败时报告，不悄悄改用别的付费/克隆服务；也可导入已授权录音和对齐时序。

## 字幕显示清理

先用文稿标点分短语，再清理显示；文稿本身保留标点给配音自然停顿。`scripts/caption_rules.py` 和 `library/captions.ts` 处理相同约定：去句读，保留问号、数值小数点、负号、比例/时间和数学/货币符号。千位逗号删除不改数值。

清理SRT：

```bash
python3 scripts/caption_rules.py --input captions.srt --output captions-clean.srt
```

不要通过重新分句改变原时间码。长字幕按语义和实际字体字宽分行，不能只按字数保证不出界。空字幕跳过，不能把旧一句挂到新说话人。

## 声音与渲染

片头、正文和片尾可以不同音乐，密集解说压低；动作相关提示音少量使用。外部音乐先试听，带原旁白的MP4不当纯配乐。保留配乐来源/授权信息，不硬编码某人的桌面目录。

工程自带无声演示，不假装它已经有正式配音。正式交付需要人声清楚、尾字完整、无削波；参考 -16 LUFS、真峰不超过 -1.5 dB，按素材实际调整。

渲染由 Remotion 帧时间驱动，不使用依赖真实墙钟的CSS动画/随机数；随机动作固定种子。播放器、编码器和字体版本可能造成细微差异，所以保留锁文件和检查图。

```bash
cd /path/to/new-episode
npm ci
npm run check
npm run still
npm run render
python3 /path/to/skill/scripts/verify_export.py outputs/video.mp4
```

输出目录和缓存不进动画库。收集新的通用组件时删除本期事实、机器路径和外部照片依赖。

## 新选题不是只改JSON

基础工程支持的kind见src/scene-kinds.json：hook/intro/duo/outro、chip、array、geofence、cost、gates、income、rocket。遇到新机制（如收入增长但预期落空、估值下调），需要在Film.tsx增加有真实动作逻辑的场景分支，并把kind加入清单。不能拿无关图表或默认双人画面替代。未知kind会拒绝渲染；审计也会报错。新增组件需要本期验证后才入库。

素材已内置不等于全流程首次离线可跑：npm包和Remotion浏览器需要预装或首次联网下载。在线配音也需要网络；可使用事先准备的授权录音。

## 多音字与显示稿
行情读 háng qíng。brand.json 的 pronunciation.same_length_substitutions 用等长同音字生成语音（行情→航情），对齐时恢复原字，缓存按实际生成文本区分。该替换不是听音验收；人名、多音字与读数仍需实际检查。显式 ttsText 若改变字符数，应另行对齐原文，不能把同音替换字交付成字幕。
