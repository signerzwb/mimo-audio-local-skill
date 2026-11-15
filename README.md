# MiMo-Audio 本地部署 Skill

面向 Codex 等支持 Skill 的智能体：根据当前机器安装和测试 [小米 MiMo-Audio](https://github.com/XiaomiMiMo/MiMo-Audio)，而不是把另一台电脑的硬编码路径当成通用配置。

## 使用

将 `skills/mimo-audio-local` 安装到支持的技能目录，在智能体里说明系统、显卡与目标，例如：“用 mimo-audio-local 检查环境，在隔离目录部署 Instruct 并生成一段中文样音。” 智能体应先检查可用资源，再下载官方版本并核验哈希。模型与 CUDA 依赖体积较大，需要足够时间和磁盘空间。

程序和权重来源：

- [上游源码及说明](https://github.com/XiaomiMiMo/MiMo-Audio)
- [指令模型](https://huggingface.co/XiaomiMiMo/MiMo-Audio-7B-Instruct)
- [音频编码器](https://huggingface.co/XiaomiMiMo/MiMo-Audio-Tokenizer)
- [基础模型](https://huggingface.co/XiaomiMiMo/MiMo-Audio-7B-Base)

不要将模型文件体积当作最低显存保证；Base 的示例能力也不能直接视为 Instruct 的实测。原项目代码采用 Apache-2.0；模型卡与素材权利须分别核对。Skill 不内置模型、不自动下载，也不自动对外发布。

## 一次本机试验（2026-11-15）

Windows + WSL 2 Ubuntu，RTX 3080 **20 GiB**，系统内存约 48 GB；Python 3.12，PyTorch 2.6.0+cu124，Flash Attention 2.7.4.post1。官方 Instruct 与 Tokenizer，BF16、未量化。加载用时 327.17 秒，PyTorch 加载后分配 17.37 GiB。该机器的 3080 为 20 GiB，不能代表所有 3080。

| 单次任务 | 输出 | 生成耗时 | PyTorch 峰值分配 |
| --- | --- | --- | --- |
| 中文 TTS | [6.08 秒音频](samples/tts-zh-question.wav) | 41.07 秒 | 17.414 GiB |
| 英文 TTS | [5.76 秒音频](samples/tts-en.wav) | 23.77 秒 | 17.414 GiB |
| 语音对话 | [24 秒音频](samples/spoken-dialogue.wav) | 101.80 秒 | 17.456 GiB |

中文音频理解输入是上面的合成问题，要求“复述音频”时，模型回答了问题而不是复述原话，不能算准确转写。语音回答中出现“本地部署一定避免泄露、延迟很低”等过度绝对的说法，实际安全和延迟取决于环境。以上为单输入单次测试，没有测试真人录音、实时打断、并发或稳定性，也不以此给不同模型排名；请结合原始样音自行判断。

代码提交 `3b3562e9a97f5c222b76c004f435faab51d1daaf`；Instruct 权重修订 `2b8c0171dd106cdb709baa04c96597f53ab7ac90`；Tokenizer 权重修订 `8a41b556798a8cd9d83c79dcd5f48ac8e319ff0b`；随机种子 `20261115`。主模型四片和编码器权重均与模型仓库的 LFS SHA-256 核对一致。

由神都猫 AI 研究所整理。此项目是独立部署辅助资料，非小米官方项目。
