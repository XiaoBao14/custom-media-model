---
name: custom-media-model
description: 完全自定义的图片/视频生成技能，支持配置任意自定义baseurl、API密钥、模型，兼容OpenAI/豆包/SeedDance/Pika/Stable Diffusion等所有主流生成式API格式，开箱即用。
metadata: {"openclaw":{"emoji":"🎨","requires":{"env":["MEDIA_GEN_IMAGE_BASE_URL","MEDIA_GEN_IMAGE_API_KEY","MEDIA_GEN_VIDEO_BASE_URL","MEDIA_GEN_VIDEO_API_KEY"],"bins":["python"]}}}
---

# 🎨 自定义媒体生成技能
支持自定义配置任意图片/视频生成API，无需修改代码，仅需设置环境变量即可使用。

## ✨ 特性
- 🔧 完全自定义：支持任意baseurl、API密钥、模型配置
- 🤝 全兼容：支持OpenAI格式、豆包、SeedDance、Pika、Stable Diffusion WebUI等所有主流API
- 🖼️ 图片生成：支持文生图、自定义尺寸、批量生成
- 🎬 视频生成：支持文生视频、图生视频、自定义时长分辨率
- 🚀 开箱即用：配置环境变量后直接通过自然语言调用

## ⚙️ 配置方法
### 图片生成配置（仅需配置一次）
```powershell
# 图片生成API地址（必填）
$env:MEDIA_GEN_IMAGE_BASE_URL = "你的图片API baseurl，如https://open-gateway.anspire.cn/v6/images/generations"
# 图片API密钥（必填）
$env:MEDIA_GEN_IMAGE_API_KEY = "你的API密钥"
# 图片生成默认模型（可选，默认自动适配）
$env:MEDIA_GEN_IMAGE_DEFAULT_MODEL = "Doubao-Seedream-5.0-lite"
# 图片默认尺寸（可选，默认1024x1024）
$env:MEDIA_GEN_IMAGE_DEFAULT_SIZE = "1024x1024"
# 鉴权头格式（可选，默认Bearer，支持自定义如x-api-key）
$env:MEDIA_GEN_IMAGE_AUTH_HEADER = "Bearer"
```

### 视频生成配置（仅需配置一次）
```powershell
# 视频生成API地址（必填）
$env:MEDIA_GEN_VIDEO_BASE_URL = "你的视频API baseurl"
# 视频API密钥（必填）
$env:MEDIA_GEN_VIDEO_API_KEY = "你的API密钥"
# 视频生成默认模型（可选）
$env:MEDIA_GEN_VIDEO_DEFAULT_MODEL = "seeddance-1.5-turbo"
# 视频默认参数（可选）
$env:MEDIA_GEN_VIDEO_DEFAULT_DURATION = "5"
$env:MEDIA_GEN_VIDEO_DEFAULT_RESOLUTION = "1080p"
```

## 🚀 使用方法
### 生成图片
直接告诉我你想要的图片描述即可：
> "生成一张可爱的橘猫卡通头像，1024x1024"
> "生成赛博朋克风格城市夜景，1792x1024横屏"

高级参数调用：
```powershell
python skills/custom-media-gen/scripts/generate_image.py "提示词" --model 模型名 --size 尺寸 --output 保存路径.png
```

### 生成视频
直接告诉我你想要的视频内容即可：
> "生成一只小猫在草地上打滚的视频，5秒，1080P"
> "把这张图片做成镜头拉近的动效视频，3秒"

高级参数调用：
```powershell
python skills/custom-media-gen/scripts/generate_video.py "提示词" --model 模型名 --duration 时长 --resolution 分辨率 --output 保存路径.mp4
```

## 📝 支持的接口格式
- ✅ OpenAI/DALL-E 格式
- ✅ 字节跳动SeedDance格式
- ✅ 豆包/文心/通义等国内大模型生成API
- ✅ Stable Diffusion WebUI API
- ✅ Pika/Runway等视频生成API
- ✅ 任何自定义HTTP API（只需简单调整请求格式）
