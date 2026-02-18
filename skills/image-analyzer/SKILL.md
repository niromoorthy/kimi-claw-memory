---
name: image-analyzer
description: Analyze and describe images using vision-capable AI models. Use when the user shares an image and asks for description, analysis, OCR (text extraction), object identification, or any visual understanding task. Works with local image files and URLs. Supports photos, screenshots, diagrams, documents, and any image format.
---

# Image Analyzer

## Overview

This skill enables image understanding by routing image analysis to a vision-capable AI model. When a user shares an image and asks for description, analysis, or any visual task, use this skill to process it.

## When to Use

Activate this skill when:
- User shares an image and asks "describe this" or "what is this"
- User wants text extracted from an image (OCR)
- User asks about objects, people, or content in an image
- User shares a screenshot and wants explanation
- User shares a document photo and wants analysis
- Any request involving understanding visual content

## How It Works

1. **Image location**: Images are typically at `/root/.openclaw/media/inbound/` or provided as URLs
2. **Analysis method**: Use `sessions_spawn` with a vision-capable model (e.g., `kimi-coding/k2p5`) to analyze the image
3. **Response**: Return the description/analysis to the user

## Quick Start

### Basic Image Description

```python
# When user shares an image at /path/to/image.jpg and asks "describe this"
# Spawn a vision-capable session to analyze it

sessions_spawn(
    task="Describe this image in detail: /path/to/image.jpg",
    model="kimi-coding/k2p5"  # Vision-capable model
)
```

### OCR / Text Extraction

```python
# Extract text from an image
sessions_spawn(
    task="Extract all text from this image. Preserve formatting: /path/to/image.jpg",
    model="kimi-coding/k2p5"
)
```

### Analysis with Specific Focus

```python
# Analyze specific aspects
sessions_spawn(
    task="Analyze this diagram and explain the architecture shown: /path/to/image.jpg",
    model="kimi-coding/k2p5"
)
```

## Workflow

1. **Receive image** → Note the file path from the inbound context
2. **Understand request** → What does the user want to know?
3. **Spawn vision agent** → Use `sessions_spawn` with a vision model
4. **Return result** → Pass the analysis back to the user

## Notes

- Always use a vision-capable model (check model capabilities)
- If the image path is not provided, ask the user to share it again
- For sensitive images, remind the user of privacy considerations
- The vision agent sees the image directly; describe the task clearly
