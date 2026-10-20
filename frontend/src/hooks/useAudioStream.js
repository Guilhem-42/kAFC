import { useRef, useCallback } from 'react'

const BACKEND_WS = 'ws://localhost:8000/ws/session'
const SAMPLE_RATE = 16000
const CHUNK_MS = 100  // envoi toutes les 100ms

/**
 * useAudioStream
 * Gère la connexion WebSocket avec le backend et le streaming audio micro.
 *
 * @param {function} onMessage - callback appelé à chaque message reçu du backend
 */
export function useAudioStream({ onMessage }) {
  const wsRef = useRef(null)
  const audioCtxRef = useRef(null)
  const processorRef = useRef(null)
  const streamRef = useRef(null)

  const start = useCallback(async () => {
    // 1. Ouvrir le WebSocket
    const ws = new WebSocket(BACKEND_WS)
    wsRef.current = ws

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data)
        onMessage(msg)
      } catch (e) {
        console.error('WS parse error', e)
      }
    }

    ws.onerror = (e) => console.error('WS error', e)

    // Attendre que le WS soit ouvert
    await new Promise((resolve, reject) => {
      ws.onopen = resolve
      ws.onerror = reject
    })

    // 2. Demander accès micro
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        sampleRate: SAMPLE_RATE,
        channelCount: 1,
        echoCancellation: true,
        noiseSuppression: true,
      }
    })
    streamRef.current = stream

    // 3. Créer le contexte audio et le processor
    const audioCtx = new AudioContext({ sampleRate: SAMPLE_RATE })
    audioCtxRef.current = audioCtx

    const source = audioCtx.createMediaStreamSource(stream)

    // ScriptProcessor (compatible large browsers, AudioWorklet en v2)
    const processor = audioCtx.createScriptProcessor(4096, 1, 1)
    processorRef.current = processor

    processor.onaudioprocess = (e) => {
      if (ws.readyState !== WebSocket.OPEN) return
      const float32 = e.inputBuffer.getChannelData(0)
      // Envoyer les bytes PCM float32 little-endian
      ws.send(float32.buffer)
    }

    source.connect(processor)
    processor.connect(audioCtx.destination)

  }, [onMessage])

  const stop = useCallback(() => {
    processorRef.current?.disconnect()
    audioCtxRef.current?.close()
    streamRef.current?.getTracks().forEach(t => t.stop())
    wsRef.current?.close()
  }, [])

  return { start, stop }
}
