const LABELS = {
  idle:      '🎙️ Parlez au poussin',
  listening: '🔴 En écoute…',
  processing:'⏳ Le poussin réfléchit…',
  talking:   '🐣 Le poussin répond…',
  dance:     '🕺 Danse !',
  exit:      '👋 Au revoir…',
}

export default function MicButton({ sessionState, onClick, disabled }) {
  const label = LABELS[sessionState] ?? LABELS.idle
  const isActive = sessionState === 'listening'

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        marginTop: '2rem',
        padding: '1rem 2.5rem',
        fontSize: '1.1rem',
        fontFamily: 'Georgia, serif',
        background: isActive ? '#c0392b' : '#f39c12',
        color: '#fff',
        border: 'none',
        borderRadius: '999px',
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.5 : 1,
        transition: 'background 0.3s',
        boxShadow: isActive ? '0 0 20px rgba(192,57,43,0.6)' : 'none',
      }}
    >
      {label}
    </button>
  )
}
