# 华尔街潘哥 · Brother Pan

面向 Codex 等支持 `SKILL.md` 的智能体，复用潘哥、小辣的角色、动画组件和制作经验，制作中文财经、美股、科技与商业解说视频。

这个仓库同时包含 **skill、可运行工程、动画库和检查工具**。不用每期重新画人物、重写车辆或芯片，也不把每期视频做成同一套画面换字。

## 已确定的风格

![角色和配色参考](assets/references/channel-style.png)

- 账号 **华尔街潘哥**；男主持 **潘哥**，女主持 **小辣**，白色高领毛衣带红辣椒。
- 默认竖版 1080×1920、30fps；不强制时长。
- 人物情境动画＋机制拆解＋按需要出现的真实照片/实拍。
- 对观众讲话看镜头，两人聊天看对方，介绍物件看主体；说话者才动嘴。
- 第一帧人物/事件主体＋大标题，迅速转入动作；米白、深绿、荧光绿统一。
- **字幕不显示逗号、句号、顿号等句读标点，问号保留**；小数点、百分号、负号等数值含义保留。口播稿继续用标点控制自然停顿。

全部有效规则见 [config/rules.json](config/rules.json)。它是最新规则清单，不是历史聊天记录。

## 安装与调用

常见安装器：

```bash
npx skills add evanpanan/Brother-Pan
```

也可以把仓库克隆到智能体的 skills 目录，目录名使用 `brother-pan-video`：

```bash
git clone git@github.com:evanpanan/Brother-Pan.git ~/.codex/skills/brother-pan-video
```

在智能体中说：

> 使用 $brother-pan-video 做一期……。先核实资料，沿用潘哥和小辣，给我成片、封面和发布文案。

不使用 skill 安装器也能直接阅读根目录 [SKILL.md](SKILL.md)。安装器、配音供应商和浏览器能力随环境变化，不是仓库自动提供的云服务。

## 先跑通一个演示

需要 Python 3.10+、Node.js 22.13+ 或 24+、npm、ffmpeg/ffprobe。视频引擎依赖锁定在随工程提供的 `package-lock.json`；Remotion 的使用条款独立适用。

```bash
python3 scripts/new_episode.py --out ./my-episode
cd my-episode
npm ci
npm run check
npm run still
npm run render
```

首次 Remotion 渲染可能下载其浏览器，需要网络。默认生成可运行的无声演示；为新片写文稿后再生成配音，不要把演示稿当模板逐镜换词。

```bash
# 在仓库目录运行；先安装 edge-tts，或用 uv 临时依赖
uv run --with edge-tts==7.3.1 python scripts/prepare_voice.py --project ./my-episode
python3 scripts/audit_episode.py ./my-episode
```

在线配音沿用 `zh-CN-YunjianNeural` 和 `zh-CN-XiaoxiaoNeural`，也支持准备好录音和时序后导入。未复制任何凭证，不保证供应商永久免费、永不变更或授予商用权。

[查看基础工程实际渲染的首帧](docs/starter-preview.png) · [验证记录](docs/validation.md)

## 已有动画库

| 分类 | 可复用内容 |
| --- | --- |
| 人物 | 正面/侧向各八姿势图；两位主持各四种；口型坐标、当前说话人控制、身体/手部网格形变 |
| 车辆 | 金色无人车、手机、方向盘、道路、住宅/办公楼、服务图标 |
| 芯片 | 板卡、功能层展开、任务图标、计算阵列 |
| 航天 | 已有星舰片提取的火箭/助推器，位置、角度、火焰动作 |
| 机制 | 月费/首年账单、地理围栏、营运授权闸门、收入与成本流向 |
| 基础 | 统一配色、文字/面板、居中字幕、安全区、按语义切换朝向的主持人包装 |
| 画面资产 | 原创车内和实验室背景，认可的封面/品牌参考 |

```bash
python3 scripts/find_asset.py 芯片
python3 scripts/find_asset.py 正面
python3 scripts/find_asset.py 地图
```

索引见 [assets/registry.json](assets/registry.json)。先搜索并读命中组件的参数，不需要把所有源码塞进上下文。

## 每期增加一点库

1. 先搜索现有资产，选择真正适合本期的部件。
2. 新画面、新表演或新物件在本期检查通过后，把不含时效事实的部分提取到 `library/`。
3. 原创图片加入 `assets/`，登记标签、来源、用途、参数与 SHA-256；已有同哈希资源不重复存放。
4. 第三方照片/视频只在每期记录来源和使用范围；不因为网上能下载就作为自有素材重新授权。
5. 维护者按 [维护流程](references/maintenance.md) 验证、提交、同步。新鲜事实仍要重新查，不从旧片直接继承。

这是“减少重复生成、少读重复代码”的原理：脚本可以直接运行，组件通过索引按需读取，角色不必每次再生成。它能节省时间和部分 token，但研究、文案、分镜和审片依然需要投入；不承诺固定节省比例。

## 更新规则

规则更新同时修改 `config/rules.json`、必要配置/实现和对应说明，运行测试，记录改动，再提交。**原维护者已在自己的工作环境授权规则更新后同步此仓库**；其他使用者需要自己的仓库写权限与授权，不自动向此仓库推送。

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
# 在获得维护权限和本次/持续授权的检出中使用
python3 scripts/sync_repo.py --message "Update caption rules" --push
```

同步脚本不强推、不自动解决冲突、不上传成片、缓存、环境文件或个人照片。推送失败时如实报告“本地已更新，远端未同步”，不能声称完成。

## 怎样让别人也能接近同样的质量

提供同一角色、字体、组件、依赖版本、字幕规则、示例与审查流程，是保持一致的基础。最终表现还取决于资料准确性、文案、镜头安排、配音表现和真实观看检查，**不能保证任何题目、任何模型一键产出完全相同的质量，更不承诺爆款**。

最低交付检查包括：文字不压主体、动作峰值不遮挡、倾听者闭嘴、视线正确、照片不重复、字幕同步/无句读标点、音量不过载、全片可解码、片头可抓封面、片尾有具体关注理由。审片记录必须区分抽帧、代表性播放和全片播放。

## 文件地图

```text
SKILL.md                 给智能体的短入口
config/                  最新规则和品牌参数
references/              文案/画面/制作/审查/维护，按需阅读
library/                 可复用 React/SVG/人物动画组件
assets/                  原创人物、背景、字体、索引、基础工程
scripts/                 建工程、配音、字幕、索引、检查、同步
examples/                演示及历史分镜/机制参考
tests/                   字幕数值语义、时序、资产去重和工程检查
ASSETS.md                资产来源与授权边界
CHANGELOG.md             对规则和库有影响的更新
```
