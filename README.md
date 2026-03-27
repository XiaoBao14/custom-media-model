# 🎨 Custom Media Model - OpenClaw 自定义媒体生成技能

OpenClaw技能生态的通用媒体生成插件，支持任意自定义图片/视频生成API，无需修改代码，仅通过环境变量即可快速接入所有主流大模型生成接口。

## ✨ 特性
- 🔧 **零代码配置**：仅需设置环境变量即可接入任意自定义API
- 🤝 **全兼容**：支持OpenAI/豆包/SeedDance/Pika/Stable Diffusion WebUI等所有主流生成式API格式
- 🖼️ **图片生成**：支持文生图、自定义尺寸/分辨率、批量生成
- 🎬 **视频生成**：支持文生视频、图生视频、自定义时长/帧率
- 🚀 **开箱即用**：配置完成后直接通过自然语言调用，无需记忆命令参数
- 🔒 **安全可控**：所有配置保存在本地，不会泄露API密钥

## 📦 安装方法
### 方式1：通过ClawHub安装（推荐）
```bash
clawhub install XiaoBao14/custom-media-model --force
```

### 方式2：手动安装
```bash
git clone https://github.com/XiaoBao14/custom-media-model.git ~/.openclaw/workspace/skills/custom-media-model
python -m pip install httpx -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## ⚙️ 配置方法
### 图片生成配置（仅需配置一次）
```powershell
# 图片生成API完整地址（必填）
$env:MEDIA_GEN_IMAGE_BASE_URL = "你的图片API地址，如https://open-gateway.anspire.cn/v6/images/generations"
# 图片API密钥（必填）
$env:MEDIA_GEN_IMAGE_API_KEY = "你的API密钥"
# 图片生成默认模型（可选）
$env:MEDIA_GEN_IMAGE_DEFAULT_MODEL = "Doubao-Seedream-5.0-lite"
# 图片默认尺寸（可选）
$env:MEDIA_GEN_IMAGE_DEFAULT_SIZE = "1024x1024"
```

### 视频生成配置（仅需配置一次）
```powershell
# 视频生成API完整地址（必填）
$env:MEDIA_GEN_VIDEO_BASE_URL = "你的视频API地址"
# 视频API密钥（必填）
$env:MEDIA_GEN_VIDEO_API_KEY = "你的API密钥"
# 视频生成默认模型（可选）
$env:MEDIA_GEN_VIDEO_DEFAULT_MODEL = "seeddance-1.5-turbo"
# 视频默认时长/分辨率（可选）
$env:MEDIA_GEN_VIDEO_DEFAULT_DURATION = "5"
$env:MEDIA_GEN_VIDEO_DEFAULT_RESOLUTION = "1080p"
```

## 🚀 使用方法
### 自然语言调用（推荐）
直接向OpenClaw描述需求即可：
> 示例1："生成一张像素风格的红色龙虾助手卡通头像，1024x1024"
> 示例2："生成赛博朋克风格城市夜景，1792x1024横屏"
> 示例3："生成一只小猫在草地上打滚的视频，5秒，1080P"
> 示例4："把这张图片做成镜头缓慢拉近的3秒动效视频"

### 命令行调用
```powershell
# 生成图片
python ~/.openclaw/workspace/skills/custom-media-model/scripts/generate_image.py "提示词" --model 模型名 --size 尺寸 --output 保存路径.png

# 生成视频
python ~/.openclaw/workspace/skills/custom-media-model/scripts/generate_video.py "提示词" --image 输入图片路径 --duration 时长 --resolution 分辨率 --output 保存路径.mp4
```

## 📝 支持的API格式
- ✅ OpenAI/DALL-E 3 接口格式
- ✅ 字节跳动SeedDance视频生成接口
- ✅ 豆包/文心一言/通义万相等国内大模型生成接口
- ✅ Stable Diffusion WebUI / Forge API
- ✅ Pika/Runway 等第三方视频生成接口
- ✅ 任何自定义HTTP API，可简单调整参数适配

## 📄 协议
本项目采用 [CC BY-ND 4.0 协议](LICENSE)，允许自由下载使用，禁止修改代码后二次分发。
