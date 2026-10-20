import { useRef, useEffect } from 'react'

/**
 * Mapping état → fichier vidéo.
 * Les séquences en loop sont jouées en boucle jusqu'au prochain état.
 */
const SEQUENCES = {
  idle:      { src: null,                     loop: false },
  intro:     { src: '/videos/intro.mp4',      loop: false },
  waiting:   { src: '/videos/waiting_a.mp4',  loop: true,  alt: '/videos/waiting_b.mp4' },
  receiving: { src: '/videos/receiving.mp4',  loop: false },
  talking:   { src: '/videos/talking.mp4',    loop: true  },
  dance:     { src: '/videos/dance.mp4',      loop: false },
  spin:      { src: '/videos/spin.mp4',       loop: true  },
  exit:      { src: '/videos/exit.mp4',       loop: false },
}

// Alterne entre waiting_a et waiting_b pour éviter la répétition
let waitingToggle = false

export default function PuppetPlayer({ state }) {
  const videoRef = useRef(null)
  const currentStateRef = useRef(null)

  useEffect(() => {
    const video = videoRef.current
    if (!video || state === currentStateRef.current) return

    currentStateRef.current = state
    const seq = SEQUENCES[state]
    if (!seq || !seq.src) return

    // Alterner les variantes waiting
    let src = seq.src
    if (state === 'waiting' && seq.alt) {
      waitingToggle = !waitingToggle
      src = waitingToggle ? seq.alt : seq.src
    }

    video.src = src
    video.loop = seq.loop
    video.play().catch(e => console.warn('Video play error', e))
  }, [state])

  return (
    <video
      ref={videoRef}
      style={{
        width: '100%',
        maxWidth: '640px',
        borderRadius: '12px',
        background: '#111',
      }}
      playsInline
      muted={false}
    />
  )
}
