import { useState, useCallback, useRef } from 'react'
import PuppetPlayer from './components/PuppetPlayer'
import MicButton from './components/MicButton'
import CocoDisplay from './components/CocoDisplay'
import { useAudioStream } from './hooks/useAudioStream'

/**
 * États de session possibles :
 * idle → intro → waiting → receiving → talking → dance → exit → idle
 */

export default function App() {
  const [puppetState, setPuppetState] = useState('idle')
  const [sessionState, setSessionState] = useState('idle')
  const [cocorico, setCocorico] = useState(null)
  const [transcript, setTranscript] = useState('')
  const audioRef = useRef(null)

  // Gère les messages entrants du backend
  const handleMessage = useCallback((msg) => {
    switch (msg.type) {

      case 'state':
        setPuppetState(msg.value)
        setSessionState(msg.value)
        break

      case 'transcript':
        setTranscript(msg.text)
        break

      case 'cocorico':
        setCocorico({ lang: msg.lang, text: msg.text, phonetic: msg.phonetic })
        break

      case 'audio':
        // Décoder le base64 et jouer l'audio
        const binary = atob(msg.data)
        const bytes = new Uint8Array(binary.length)
        for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i)
        const blob = new Blob([bytes], { type: 'audio/mp3' })
        const url = URL.createObjectURL(blob)
        if (audioRef.current) {
          audioRef.current.src = url
          audioRef.current.play()
        }
        break

      case 'error':
        console.error('Backend error:', msg.message)
        setSessionState('idle')
        setPuppetState('idle')
        break

      default:
        break
    }
  }, [])

  const { start, stop } = useAudioStream({ onMessage: handleMessage })

  const handleStartSession = async () => {
    if (sessionState !== 'idle') return
    setCocorico(null)
    setTranscript('')
    setSessionState('listening')
    await start()
  }

  const isDisabled = sessionState !== 'idle'

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '2rem',
      minHeight: '100vh',
    }}>

      {/* Header */}
      <header style={{ marginBottom: '2rem', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2rem', color: '#f39c12', letterSpacing: '0.1em' }}>
          kAFC
        </h1>
        <p style={{ fontSize: '0.85rem', color: '#888', marginTop: '0.3rem' }}>
          Kute Artificial Friend Chicken
        </p>
      </header>

      {/* Marionnette */}
      <PuppetPlayer state={puppetState} />

      {/* Bouton micro */}
      <MicButton
        sessionState={sessionState}
        onClick={handleStartSession}
        disabled={isDisabled}
      />

      {/* Transcription (debug / démo) */}
      {transcript && (
        <p style={{
          marginTop: '1rem',
          fontSize: '0.85rem',
          color: '#666',
          fontStyle: 'italic',
          maxWidth: '480px',
          textAlign: 'center',
        }}>
          « {transcript} »
        </p>
      )}

      {/* Cocorico */}
      <CocoDisplay cocorico={cocorico} />

      {/* Player audio caché */}
      <audio ref={audioRef} style={{ display: 'none' }} />

    </div>
  )
}
