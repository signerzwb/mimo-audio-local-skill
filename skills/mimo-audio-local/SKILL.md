---
name: mimo-audio-local
description: 在本地隔离部署、运行和验证小米 MiMo-Audio-7B 的语音理解、语音对话和合成；适用于该模型的安装与实测，不自动发布内容。
---

# MiMo-Audio 本地安装与实测

以用户已有硬件、操作系统和许可要求为准。先查 GPU 空闲显存、主机内存、磁盘空间和现有服务；未经授权不要停止其他任务或重写已有环境。项目包含 Base、Instruct 和独立 MiMo-Audio-Tokenizer：基础部署只在用户需求明确时下载所需版本，不能将 Base 的演示误记为 Instruct 已测试。

1. 查阅 [官方项目](https://github.com/XiaomiMiMo/MiMo-Audio) 的当前 README 和模型卡。官方提供 Linux、Python 3.12、CUDA 12+ 路线；Windows 可在已就绪的 WSL 2 中尝试，先检查 Linux 内 `nvidia-smi`。模型代码 Apache-2.0，权重与各组件以模型卡为准。
2. 建立独立目录与 Python 环境。记录代码提交、模型仓库修订、文件大小及 SHA-256。先比较官方下载源和镜像速度、核对内容哈希；不可将未校验的下载碎片交给加载器。Instruct 与音频编码器权重文件合计约 20 GB 十进制，但文件大小不等于运行峰值显存。显存不足时如需量化或卸载，应标明与官方原始路径不同并重新验证。
3. 按对应官方 README 安装 PyTorch、Transformers 和 Flash Attention。预编译 wheel 必须对应 Python、PyTorch、CUDA 与 C++ ABI；若 `flash_attn` 安装时使用 `--no-deps`，自行确认 `einops` 等依赖。不要把某一次测试的机器路径写成其他机器的默认配置。
4. 下载 Instruct 和 Tokenizer，并用官方示例或本技能的 `scripts/smoke_test.py` 进行真实测试。脚本提供参数而非固定路径，输出各项状态、耗时、音频文件和 PyTorch 显存峰值；结果只说明当前输入与当前机器。区分加载显存、生成峰值、首轮冷启动和后续运行，保留具体失败日志，不凭模型卡宣称本机效果。测试真人声音克隆须有授权。
5. 需要网页界面时参照官方 `run_mimo_audio.py` 检查模型路径、端口与监听地址；默认仅本机访问，不自动公开。语音对话不自动等同低延迟、可打断实时通话；必须另行实测延迟与并发。

需要公开分发样音、文章或视频时先核对对应权重、素材与平台条件，只有用户授权才发布。不要将官方演示、图片示意或生成成功提示伪装为本机实测。
