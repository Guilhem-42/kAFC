export default function CocoDisplay({ cocorico }) {
  if (!cocorico) return null

  return (
    <div style={{
      marginTop: '1.5rem',
      textAlign: 'center',
      animation: 'fadeIn 0.5s ease',
    }}>
      <div style={{
        fontSize: '2.5rem',
        fontWeight: 'bold',
        color: '#f39c12',
        letterSpacing: '0.05em',
      }}>
        {cocorico.text}
      </div>
      <div style={{
        fontSize: '0.9rem',
        color: '#aaa',
        marginTop: '0.3rem',
      }}>
        {cocorico.lang} — /{cocorico.phonetic}/
      </div>

      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(8px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  )
}
