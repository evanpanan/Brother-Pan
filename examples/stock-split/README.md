# 一拆二，钱也翻倍？动作排练

这是一段正文排练。小辣发现账户里的股数翻了倍，潘哥把一张写着一百元的纸票递到镜头前，沿齿线撕开。两张票留下问号。等小辣自己算出答案，两张票才各自露出五十元。忽略市场波动，只演示一拆二的股数与理论价格调整。

## 从新目录跑起来

在仓库根目录运行。准备 Python 3.10+、Node 22.13+ 和 FFmpeg。首次安装依赖或渲染浏览器需要联网；预备好依赖与浏览器后，画面和审片工具可离线运行。

```bash
python3 examples/stock-split/create.py --out ./outputs/split-rehearsal
cd outputs/split-rehearsal
npm ci
npm run check
npm run render
```

产物是 `outputs/video.mp4`。内置19.3秒静音节奏仅供看动作。要听正式配音，在此工程按仓库 [双人配音安装与运行说明](../../references/voice-setup.md) 运行配音入口，再重新渲染即可。镜头和字幕从该次生成的时间线读取，发声者由音轨标记的有声区间驱动。撕开时有一声轻纸响，创建工程时本地生成。静音版两人闭嘴。

可以将字幕暂时挡住，试着复述角色的误会、纸票撕开后还有什么悬念、最后两个数加起来是多少。在原速带声版本上再核对纸张是否在“撕”字附近分开、小辣说“五十”时是否才出现答案，以及她开口前潘哥的嘴是否已经收住。画面动作随这几个关键词调度，若改写台词，应一并更新动作锚点。

需要单独回看双方交接时，回到仓库根目录，抽取中间一句及前后各两秒。输入应为对应工程的实际成片。默认要求音轨；明确只想看无声排练时可加 `--allow-silent`。

```bash
python3 scripts/review_turn.py --project outputs/split-rehearsal --turn cut-the-ticket --out outputs/split-handoff.mp4
```

抽段命令可用于其他单集的任意 `sceneId`。不同选题应另选道具和动作。角色和伸手动作来自仓库原创组件，[撕票组件](../../library/scenes/SplitCertificate.tsx) 是原创示意，可用不同面值和揭晓时机重用。
