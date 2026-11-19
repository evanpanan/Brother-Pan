# 规则与动画库维护

## 更新规则

1. 把用户最新决定写进 `config/rules.json`，替换同事项旧规则，不继续累积互相矛盾的历史段落。
2. 涉及默认参数改 `config/brand.json`；涉及实际行为同时改组件/脚本和有意义的测试；对应说明只维护一处。
3. `CHANGELOG.md` 记录日期、变更和是否追溯旧片。默认不重做历史成片，除非用户要求。
4. 跑测试、仓库检查、必要渲染。维护者在已获授权的检出中提交并推送，核实远端提交SHA；失败时报告剩余项。

本仓库原维护者要求规则更新后持续同步。**这一偏好不赋予其他用户原仓库写权限，也不授权发送消息、发布视频或上传私人资料**。其他使用者维护自己的fork，或交付本地变更供维护者合并。

## 新增组件/资产

先查询索引。只有通用且经过本期检查的东西进入库：稳定参数、中文标签、用途、推荐安全区、依赖文件、来源、限制。历史事实留在注明日期的例子中，不塞进通用组件。

原创位图/矢量去重后登记：

```bash
python3 scripts/register_asset.py assets/backgrounds/new-scene.png --id new-scene --kind background --tags 场景,背景 --origin original-generated
python3 scripts/check_repository.py
```

首次登记生成哈希；内容相同的文件拒绝重复。向外部项目复制时可按索引选资产，避免整个库打包到每一片。

不纳入：node_modules、缓存、成片、TTS长音频、原始私人照片、账户数据截图、密钥、cookie、环境文件，以及没有转授权依据的第三方照片/新闻视频。可登记外部素材来源和取得方式，不能偷偷附进去。

## 同步

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
python3 scripts/sync_repo.py --message "Describe the actual change" --push
```

脚本只处理明确允许的仓库文件，不强推、不自动pull/重置、不处理冲突。远端有新提交先停止并检查。凭证由 Git/SSH 正常管理，不进入仓库；不要在日志打印凭证。

安装副本不是天然的维护检出。先定位有`.git`且远端正确的维护仓库再更新，不能把其他项目的变更一起提交。
