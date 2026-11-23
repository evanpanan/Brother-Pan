# 历史节点与建筑对象

`library/scenes/RecoveryObjects.tsx` 导出 RecoveryPath 与 BusinessBuilding。来自已渲染检查过的历史回顾动画，入库时移除了具体事件、年份和数值。

RecoveryPath 参数：t为动作时间、d为完整绘制秒数；start/end/label为调用者提供的文字；drop为经过核实的峰谷回撤百分比；troughX为低点的示意横坐标；marker可选money/bank/web/health/rates/trade/clock。标记主题由调用者明确传入，不能根据跌幅自动推断事件。参数含有限值与范围检查。

这是节点示意图，不是逐日行情；横轴不按日期比例，几何高度也不按跌幅比例，必须配合明确的示意说明。历史收复不能拿来保证未来。d须与口播中收复前高的时点对齐，不能等到场景末尾才到位。字体theme与MotionObjects是同库依赖。完整构图不能在每期机械换字复用。

BusinessBuilding 参数x/y/t/label/c/dead，用于企业、成员更替或倒闭的概念表达，不冒充任何具体企业。预览见recovery-objects-preview.png。入库版本已单独做类型与实际渲染检查；抽帧不等于全片正常速度审听。

# 完整毛笔字库

assets/fonts/MaShanZheng-Regular.ttf 未修改的上游原版，来源 https://github.com/google/fonts/tree/main/ofl/mashanzheng ，SIL OFL见同目录OFL-MaShanZheng.txt。用于每期新标题，不再复用只含旧标题几个字的子集。每个新标题仍需查缺字并实际渲染。库中不含历史照片、配音或成片。
