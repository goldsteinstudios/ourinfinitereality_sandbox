import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import GlyphComposer from './components/GlyphComposer'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <GlyphComposer />
  </StrictMode>,
)
