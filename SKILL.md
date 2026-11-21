---
name: brother-pan-video
description: 制作或修改华尔街潘哥与小辣的中文财经科技动画视频，混合双人表演、机制拆解和真实素材；适用于同风格选题、文案、分镜、配音、字幕、成片及动画库维护。
metadata:
  short-description: 潘哥小辣双人动画视频与可复用素材库
---

# 华尔街潘哥视频制作

使用已经选定的角色和画面语言，按本期内容重新设计故事。不要先套整片模板再填词。

## 开始时只读这些

1. [config/brand.json](config/brand.json)：人物、声音、配色、画幅和字幕参数。
2. [config/rules.json](config/rules.json)：整理后的有效规则。用户当次明确要求优先；不要从历史案例恢复已否定的偏好。
3. 用 `python3 scripts/find_asset.py 关键词` 找素材或组件，只打开命中的文件。

## 按工作阶段加载

- **选题和文案**：读 [references/editorial.md](references/editorial.md)。先核实会变化的事实，写具体钩子，再让小辣的追问推动解释。时长由内容决定。
- **人物、布局、动画**：读 [references/visuals.md](references/visuals.md)。人物朝向按交流对象切换；双人自我介绍同框。现有位图姿势＋网格形变不是完整三维骨骼，不声称能做任意动作。
- **工程、配音、字幕**：读 [references/production.md](references/production.md)。用 `scripts/new_episode.py` 建工程。文稿保留标点；屏显字幕/SRT去句读标点，保留问号和数值语义。
- **审查、交付**：读 [references/quality.md](references/quality.md)。做运动前中末和平台UI检查，正常速度检查有代表性的片段，如实记录范围，不把通过编译或抽帧当成“全片看过”。
- **更新规则或动画库**：读 [references/maintenance.md](references/maintenance.md)。维护者有授权时同步原仓库；普通使用者不因此获得原仓库推送权限。

## 默认成片约定

前三秒有可核实的吸引点，尽快交付第一份可用答案；双人自我介绍简短融入，再用故事与机制展开，结尾给完整回查工具和关注理由。小辣应有真实处境与合理反对意见，不能只负责问下一道题。前置价值测试与数据判断边界见 references/editorial.md；不把测试秒数或结构变成永久机械台词。

默认1080×1920、30fps；米白、深绿、荧光绿。封面最上方居中潘哥头像，头像下方只写账号名称，顶部不加其他署名或话题小字；主体人物/事件和醒目大标题保留，并迅速衔接动作。不是横版小条，也不是长静态海报。

对观众说话看镜头，聊天看对方，介绍物件看物件；只有当前发声者张嘴，倾听者闭嘴。动作、身体、眉眼和手势参与解释，不能只动嘴。

每张照片在本片仅一个连续出场区间，同一完整构图不换字回放。跨片复用原创角色、矢量组件和动作代码是允许且推荐的，复用不等于重放旧分镜。

交付视频、实际首帧封面、文稿、SRT、来源、发布标题和描述。正文取消固定顶部账号人物署名与常驻底部核对小字；封面品牌和片尾关注保留。动态事实核对日期记在发布说明和来源文件；授权≠执行、邀请≠交付、个人购买≠营运许可、营收≠利润。

## 可运行入口

```bash
python3 scripts/new_episode.py --out /path/to/episode
cd /path/to/episode
npm ci
npm run check
npm run still
npm run render
```

演示分镜和人物素材已内置，可先无声渲染；首次安装依赖与渲染浏览器仍可能需要联网。新一期的口播、事实、动作和素材仍须自己设计。环境和配音可用性见 README，不承诺安装 skill 就能自动达到同等叙事质量。
