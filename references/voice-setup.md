# 第一次让潘哥和小辣开口

示例用 Python 3.12、uv、FFmpeg。从仓库根目录运行。默认两位主持都用 Edge 在线合成，潘哥用云健（+5%、-2Hz），小辣用晓晓（+7%、+2Hz）。在线服务会接收需要生成的台词。同一文本、声线和参数的已有合成可复用。

## 生成与复核

```bash
python3 scripts/new_episode.py --out ./my-episode
uv run --python 3.12 --with edge-tts python scripts/prepare_voice.py --project ./my-episode
python3 scripts/audit_episode.py ./my-episode
```

产物是工程里的 `public/narration.wav`、`outputs/captions.srt` 和 `src/episode.json`。Edge 词时间码用来对齐字幕，人物开口区间 `voicedMs` 从波形计算，单位是本镜开头起的毫秒。

### 旧工程的 Kokoro 音轨

用 Kokoro 的旧工程仍可按其音色设置重建。获取 `kokoro-v1.0.int8.onnx` 和 `voices-v1.0.bin` 及多语言 Whisper small。安装 `requirements-voice.txt` 的依赖后，向合成命令传入 `--kokoro-model`、`--kokoro-voices` 和所需的 `--align-model`。字幕以实际合成音轨为准。[Kokoro 模型](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0) · [对齐模型](https://huggingface.co/Systran/faster-whisper-small)

## 把停顿交给表演

`script.json` 的每行是一个轮次。原句中的逗号、问号给合成器决定语气。剪辑时先连听提问、反应和回答，再改具体接点。`gapAfterMs` 表示希望上一轮可闻尾音之后至少留多少毫秒。原音自带的尾部静音计入间隔，下一轮本身的起音也影响实际听感。

若小辣正在消化一个意外的数字，可以在潘哥说完的那一轮加 `"gapAfterMs": 900`。如果两人在抢答，同一处可适当收紧。数值是表演选择，试听时以这段对话为准。

男声可用 `ttsText` 调整专名读法，显示仍用 `text`。例如在发音稿写“克劳德”，屏幕可保留“Claude”。自动时间码是初剪依据，专名、急问和长停顿应连同声音复查。需要精准指定屏显时，使用本轮相对时间的 `captionCues`。以下时间仅用于说明字段，实际取值以本期录音为准。

```json
{
  "sceneId": "chili-reaction",
  "kind": "duo",
  "speaker": "F",
  "text": "股数翻倍。那我的钱呢？",
  "audioFile": "recordings/reaction.wav",
  "gapAfterMs": 760,
  "captionCues": [
    {"text": "股数翻倍", "startMs": 80, "endMs": 900},
    {"text": "那我的钱呢？", "startMs": 1160, "endMs": 2300}
  ]
}
```

当轮有已授权录音时，把原始文件放进工程的 `recordings/`，合成结果另写到 `public/narration.wav`。设置 `audioFile` 和核对过的 `captionCues`，该轮直接用录音。只设置 `captionCues` 也行，仍会照常合成。若所有轮次都有已授权录音和时间码，则只需 Python 及 FFmpeg。
