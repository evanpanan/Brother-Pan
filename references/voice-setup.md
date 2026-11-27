# 第一次让潘哥和小辣开口

示例用 Python 3.12、uv、FFmpeg。从仓库根目录运行。潘哥用本机的 Kokoro v1.0 普通话 Yunxi，小辣沿用 Edge 在线 Xiaoxiao 的 +7% 语速和 +2Hz 音高。模型可跨期共用，单期的配音和时间码存在当期工程。

## 准备模型

从发行页取得 `kokoro-v1.0.int8.onnx` 和 `voices-v1.0.bin`，放进自己选择的目录。用 v1.0 的声音包，其中包含 `zm_yunxi`。[Kokoro 文件与下载入口](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0)

第一次用本机音频给男声字幕对齐时，下载多语言 Whisper small。以下命令仅下载对齐模型和软件依赖。后续男声合成和对齐都可以离线执行。[对齐模型](https://huggingface.co/Systran/faster-whisper-small)

```bash
uv run --python 3.12 --with-requirements requirements-voice.txt python -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8')"
```

## 生成与复核

```bash
python3 scripts/new_episode.py --out ./my-episode
export KOKORO_MODEL="/path/to/models/kokoro-v1.0.int8.onnx"
export KOKORO_VOICES="/path/to/models/voices-v1.0.bin"
uv run --python 3.12 --with-requirements requirements-voice.txt python scripts/prepare_voice.py --project ./my-episode
python3 scripts/audit_episode.py ./my-episode
```

已有工程从设置两个模型路径开始。也可用参数 `--kokoro-model`、`--kokoro-voices`、`--align-model` 明确选文件和对齐模型目录。第一次生成小辣的某句台词会把该句送到 Edge 语音服务，遇到网络故障会显示原因。同一文本、声线和参数的已有合成可以直接复用。

产物是工程里的 `public/narration.wav`、`outputs/captions.srt` 和 `src/episode.json`。男声按完整轮次合成，再把写好的文字对齐实际录音。特别长的轮次仅在字幕分析时分窗。女声使用服务返回的词时间码。每个镜头的 `voicedMs` 从实际波形计算，单位是从本镜开头起的毫秒，供人物在听对方和等待接话时闭嘴。

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
