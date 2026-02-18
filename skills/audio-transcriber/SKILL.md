---
name: audio-transcriber
description: Transcribe and understand audio/voice messages from WhatsApp and other channels. Use when the user sends an audio message, voice note, or any audio file and expects a response based on its content. Handles speech-to-text conversion and processes the transcribed instructions or questions.
---

# Audio Transcriber

## Overview

This skill enables understanding of audio messages by transcribing speech to text and processing the content. When a user sends a voice message or audio file, use this skill to convert it to text and respond appropriately.

## When to Use

Activate this skill when:
- User sends a WhatsApp voice message
- User shares an audio file with instructions or questions
- User expects a response to spoken content
- Any request involving understanding audio content

## How It Works

1. **Audio location**: Audio files are typically at `/root/.openclaw/media/inbound/` with extensions like `.ogg`, `.mp3`, `.m4a`, `.wav`
2. **Transcription method**: Use `sessions_spawn` with a model that has audio capabilities to transcribe and understand
3. **Response**: Process the transcribed text and respond to the user

## Quick Start

### Basic Audio Transcription

When user sends an audio message:

```python
# Transcribe and understand the audio
sessions_spawn(
    task="Transcribe this audio file and summarize what the user is asking or saying: /path/to/audio.ogg",
    model="kimi-coding/k2p5"  # Audio-capable model
)
```

### Transcribe and Act

```python
# Transcribe and execute the instruction
sessions_spawn(
    task="Listen to this audio and do what the user requests: /path/to/audio.mp3",
    model="kimi-coding/k2p5"
)
```

## Workflow

1. **Receive audio** → Note the file path from the inbound context
2. **Transcribe** → Use `sessions_spawn` with an audio-capable model
3. **Process** → Understand the request from the transcription
4. **Respond** → Execute the request and reply to the user

## Notes

- Audio files from WhatsApp are typically `.ogg` format (Opus codec)
- Always use a model with audio capabilities
- If transcription fails, ask the user to re-send or type their message
- The audio agent hears the audio directly; describe the task clearly
