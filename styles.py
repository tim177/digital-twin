"""Presentation layer for the Digital Twin app.

Exports three things consumed by ``app.py``:

    CSS      -> custom stylesheet, pass to ``demo.launch(css=CSS)``
    JS       -> on-load script,    pass to ``demo.launch(js=JS)``
    EXAMPLES -> starter prompts,   pass to ``gr.ChatInterface(examples=EXAMPLES)``

Note: on Gradio 6, ``css``, ``js`` and ``theme`` are arguments of ``launch()``,
not of the ``ChatInterface`` constructor.

The stylesheet works in two layers:

    1. It overrides Gradio's own CSS custom properties, so every built-in
       component (buttons, inputs, blocks) picks up the palette for free.
    2. It adds a small number of structural rules for the pieces Gradio
       does not expose as variables (bubbles, header, composer, examples).

Layout is a full-height app shell: the header sits at the top, the transcript
flexes to fill whatever height is left, and the composer stays at the bottom.
That relies on ``fill_height=True`` on the ChatInterface.

Both light and dark are supported. Gradio puts a ``.dark`` class on an
ancestor element, and custom properties inherit, so redefining the tokens
under ``.dark`` is enough to flip the whole theme.
"""

__all__ = ["CSS", "JS", "EXAMPLES"]


CSS = """
/* ==========================================================================
   1. Design tokens
   ========================================================================== */

:root {
  --dt-font: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
             "Helvetica Neue", Arial, sans-serif;
  --dt-font-mono: "JetBrains Mono", "SF Mono", ui-monospace, Menlo, Consolas,
                  monospace;

  /* Overall width of the app. This is the knob to turn for a wider or
     narrower layout -- everything else is relative to it. */
  --dt-max-width: 1180px;

  --dt-radius-xl: 24px;
  --dt-radius-lg: 18px;
  --dt-radius-md: 14px;
  --dt-radius-sm: 10px;

  --dt-accent: #5b5bd6;
  --dt-accent-hover: #4b4bc8;
  --dt-accent-grad: linear-gradient(135deg, #5b5bd6 0%, #9333ea 100%);
  --dt-accent-glow: rgba(91, 91, 214, 0.22);

  --dt-page: #f4f4f8;
  --dt-panel: rgba(255, 255, 255, 0.86);
  --dt-surface: #ffffff;
  --dt-surface-alt: #f1f1f6;
  --dt-border: #e2e2ec;
  --dt-border-soft: rgba(20, 20, 30, 0.06);
  --dt-text: #14141c;
  --dt-text-muted: #66667a;

  --dt-user-bg: linear-gradient(135deg, #5b5bd6 0%, #8b46e6 100%);
  --dt-user-text: #ffffff;
  --dt-bot-bg: #ffffff;
  --dt-bot-text: #1a1a24;

  --dt-shadow-sm: 0 1px 2px rgba(16, 16, 29, 0.05);
  --dt-shadow-md: 0 2px 8px rgba(16, 16, 29, 0.05),
                  0 14px 40px rgba(16, 16, 29, 0.07);
}

.dark {
  --dt-accent: #7f7ff5;
  --dt-accent-hover: #9292ff;
  --dt-accent-grad: linear-gradient(135deg, #6d6df0 0%, #a855f7 100%);
  --dt-accent-glow: rgba(124, 108, 245, 0.30);

  --dt-page: #08080c;
  --dt-panel: rgba(19, 19, 25, 0.82);
  --dt-surface: #13131a;
  --dt-surface-alt: #1c1c26;
  --dt-border: #272733;
  --dt-border-soft: rgba(255, 255, 255, 0.06);
  --dt-text: #f0f0f6;
  --dt-text-muted: #8f8fa6;

  --dt-user-bg: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
  --dt-user-text: #ffffff;
  --dt-bot-bg: #1a1a24;
  --dt-bot-text: #e9e9f2;

  --dt-shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.35);
  --dt-shadow-md: 0 2px 8px rgba(0, 0, 0, 0.4),
                  0 18px 50px rgba(0, 0, 0, 0.5);
}

/* ==========================================================================
   2. Map the tokens onto Gradio's own variables
   Everything Gradio renders internally inherits from these.
   ========================================================================== */

.gradio-container,
.gradio-container.dark {
  --body-background-fill: transparent;
  --background-fill-primary: var(--dt-surface);
  --background-fill-secondary: var(--dt-surface-alt);
  --block-background-fill: transparent;
  --block-border-color: transparent;
  --block-label-background-fill: var(--dt-surface-alt);
  --block-title-text-color: var(--dt-text-muted);
  --block-shadow: none;

  --border-color-primary: var(--dt-border);
  --border-color-accent: var(--dt-accent);

  --body-text-color: var(--dt-text);
  --body-text-color-subdued: var(--dt-text-muted);
  --link-text-color: var(--dt-accent);
  --link-text-color-hover: var(--dt-accent-hover);

  --color-accent: var(--dt-accent);
  --color-accent-soft: var(--dt-surface-alt);

  --input-background-fill: var(--dt-surface);
  --input-border-color: var(--dt-border);
  --input-border-color-focus: var(--dt-accent);
  --input-placeholder-color: var(--dt-text-muted);
  --input-shadow: none;

  --button-primary-background-fill: var(--dt-accent);
  --button-primary-background-fill-hover: var(--dt-accent-hover);
  --button-primary-border-color: transparent;
  --button-primary-text-color: #ffffff;
  --button-secondary-background-fill: var(--dt-surface-alt);
  --button-secondary-background-fill-hover: var(--dt-border);
  --button-secondary-border-color: var(--dt-border);
  --button-secondary-text-color: var(--dt-text);

  --radius-sm: var(--dt-radius-sm);
  --radius-lg: var(--dt-radius-md);
  --radius-xl: var(--dt-radius-lg);
  --block-radius: var(--dt-radius-lg);
  --input-radius: var(--dt-radius-md);

  --font: var(--dt-font);
  --font-mono: var(--dt-font-mono);
}

/* ==========================================================================
   3. Page shell
   ========================================================================== */

html, body, gradio-app {
  height: 100%;
  background: var(--dt-page) !important;
}

/* Two soft colour washes behind the app, fixed so they don't scroll away. */
gradio-app::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background:
    radial-gradient(48rem 26rem at 15% -8%, var(--dt-accent-glow), transparent 65%),
    radial-gradient(42rem 24rem at 88% 4%, rgba(168, 85, 247, 0.14), transparent 62%);
}

.gradio-container {
  position: relative;
  z-index: 1;
  max-width: var(--dt-max-width) !important;
  width: 100% !important;
  margin: 0 auto !important;
  padding: 1.5rem 1.5rem 1rem !important;
  font-family: var(--dt-font);
  color: var(--dt-text);
}

/* fill_height=True puts the app in a flex column; let the chat area absorb
   the leftover space instead of the whole thing scrolling. */
.gradio-container > .main,
.gradio-container .contain,
.gradio-container > .wrap {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

footer,
.gradio-container footer {
  display: none !important;
}

/* ==========================================================================
   4. Header
   ========================================================================== */

.gradio-container h1 {
  margin: 0 0 0.3rem !important;
  font-size: 2.1rem !important;
  font-weight: 700 !important;
  letter-spacing: -0.03em;
  text-align: center;
  background: var(--dt-accent-grad);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ChatInterface renders `description` as a paragraph under the title. */
.gradio-container h1 + div p,
.gradio-container h1 ~ .prose p:first-child {
  margin: 0 auto 1.35rem !important;
  text-align: center;
  font-size: 0.98rem;
  color: var(--dt-text-muted);
}

/* ==========================================================================
   5. Chat panel
   ========================================================================== */

#dt-chatbot,
.gradio-container .chatbot {
  flex: 1 1 auto;
  min-height: 420px;
  border: 1px solid var(--dt-border) !important;
  border-radius: var(--dt-radius-xl) !important;
  background: var(--dt-panel) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: var(--dt-shadow-md);
  overflow: hidden;
}

.message-wrap,
.bubble-wrap {
  padding: 1.6rem 1.5rem !important;
  gap: 1rem !important;
  background: transparent !important;
}

/* Bubbles. Gradio has shuffled these class names between majors, so match
   the older (`.message.user`) and current (`.message-row.user-row`) shapes. */
.message,
.message-row .message {
  max-width: 74% !important;
  padding: 0.85rem 1.15rem !important;
  border: none !important;
  border-radius: var(--dt-radius-lg) !important;
  font-size: 0.97rem !important;
  line-height: 1.68 !important;
  box-shadow: var(--dt-shadow-sm);
  animation: dt-rise 0.3s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.message.user,
.user > .message,
.message-row.user-row .message {
  background: var(--dt-user-bg) !important;
  color: var(--dt-user-text) !important;
  border-bottom-right-radius: var(--dt-radius-sm) !important;
}

.message.bot,
.bot > .message,
.message-row.bot-row .message {
  background: var(--dt-bot-bg) !important;
  color: var(--dt-bot-text) !important;
  border: 1px solid var(--dt-border-soft) !important;
  border-bottom-left-radius: var(--dt-radius-sm) !important;
}

.avatar-container {
  border: 1px solid var(--dt-border) !important;
  box-shadow: var(--dt-shadow-sm);
}

/* Keep links legible on the coloured user bubble. */
.message.user a,
.message-row.user-row .message a {
  color: #ffffff;
  text-decoration: underline;
  text-underline-offset: 2px;
}

/* ==========================================================================
   6. Markdown inside a reply
   ========================================================================== */

.message p:first-child { margin-top: 0 !important; }
.message p:last-child  { margin-bottom: 0 !important; }

.message h1, .message h2, .message h3 {
  margin: 1rem 0 0.5rem !important;
  font-size: 1.05em !important;
  font-weight: 650 !important;
  letter-spacing: -0.01em;
}

.message ul, .message ol {
  margin: 0.5rem 0 !important;
  padding-left: 1.3rem !important;
}

.message li { margin: 0.28rem 0 !important; }

.message code {
  padding: 0.14em 0.42em;
  border-radius: 6px;
  font-family: var(--dt-font-mono);
  font-size: 0.87em;
  background: var(--dt-surface-alt);
  color: var(--dt-text);
}

.message pre {
  margin: 0.7rem 0;
  padding: 0.95rem 1.1rem;
  border: 1px solid var(--dt-border);
  border-radius: var(--dt-radius-md);
  background: var(--dt-surface-alt) !important;
  overflow-x: auto;
}

.message pre code {
  padding: 0;
  background: transparent;
  font-size: 0.86em;
  line-height: 1.6;
}

.message blockquote {
  margin: 0.6rem 0;
  padding: 0.15rem 0 0.15rem 0.9rem;
  border-left: 3px solid var(--dt-accent);
  color: var(--dt-text-muted);
}

.message table {
  width: 100%;
  margin: 0.6rem 0;
  border-collapse: collapse;
  font-size: 0.9em;
}

.message th,
.message td {
  padding: 0.45rem 0.7rem;
  border: 1px solid var(--dt-border);
  text-align: left;
}

.message th {
  background: var(--dt-surface-alt);
  font-weight: 600;
}

/* ==========================================================================
   7. Composer
   ========================================================================== */

.gradio-container .form,
.gradio-container .input-container {
  border: none !important;
  background: transparent !important;
}

.gradio-container textarea,
.gradio-container input[type="text"] {
  padding: 0.85rem 1.1rem !important;
  border: 1px solid var(--dt-border) !important;
  border-radius: var(--dt-radius-lg) !important;
  background: var(--dt-surface) !important;
  box-shadow: var(--dt-shadow-sm) !important;
  font-family: var(--dt-font) !important;
  font-size: 0.97rem !important;
  line-height: 1.55 !important;
  resize: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.gradio-container textarea:focus,
.gradio-container input[type="text"]:focus {
  outline: none !important;
  border-color: var(--dt-accent) !important;
  box-shadow: 0 0 0 4px var(--dt-accent-glow) !important;
}

.gradio-container button {
  border-radius: var(--dt-radius-md) !important;
  font-weight: 550 !important;
  transition: transform 0.12s ease, filter 0.12s ease, background 0.15s ease;
}

.gradio-container button.primary,
.gradio-container button[variant="primary"] {
  background: var(--dt-accent-grad) !important;
  border: none !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px var(--dt-accent-glow);
}

.gradio-container button:hover  { filter: brightness(1.06); }
.gradio-container button:active { transform: translateY(1px); }

.gradio-container button:focus-visible {
  outline: 2px solid var(--dt-accent);
  outline-offset: 2px;
}

/* ==========================================================================
   8. Example prompts
   ========================================================================== */

.examples .gallery-item,
.gradio-dataset .gallery-item,
button.example {
  padding: 0.5rem 1rem !important;
  border: 1px solid var(--dt-border) !important;
  border-radius: 999px !important;
  background: var(--dt-surface) !important;
  color: var(--dt-text-muted) !important;
  font-size: 0.875rem !important;
  white-space: normal !important;
  box-shadow: var(--dt-shadow-sm);
  transition: border-color 0.15s ease, color 0.15s ease, transform 0.12s ease;
}

.examples .gallery-item:hover,
.gradio-dataset .gallery-item:hover,
button.example:hover {
  border-color: var(--dt-accent) !important;
  color: var(--dt-text) !important;
  background: var(--dt-surface) !important;
  transform: translateY(-1px);
}

/* ==========================================================================
   9. Scrollbar
   ========================================================================== */

.gradio-container *::-webkit-scrollbar { width: 10px; height: 10px; }
.gradio-container *::-webkit-scrollbar-track { background: transparent; }

.gradio-container *::-webkit-scrollbar-thumb {
  border: 3px solid transparent;
  border-radius: 999px;
  background-clip: padding-box;
  background-color: var(--dt-border);
}

.gradio-container *::-webkit-scrollbar-thumb:hover {
  background-color: var(--dt-text-muted);
}

/* ==========================================================================
   10. Motion + small screens
   ========================================================================== */

@keyframes dt-rise {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: none; }
}

.dt-ready .gradio-container {
  animation: dt-rise 0.4s ease both;
}

@media (prefers-reduced-motion: reduce) {
  .gradio-container *,
  .gradio-container *::before,
  .gradio-container *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

@media (max-width: 900px) {
  .message, .message-row .message { max-width: 86% !important; }
}

@media (max-width: 640px) {
  .gradio-container { padding: 1rem 0.75rem 0.75rem !important; }
  .gradio-container h1 { font-size: 1.65rem !important; }
  .message-wrap, .bubble-wrap { padding: 1.1rem 0.9rem !important; }
  .message, .message-row .message { max-width: 92% !important; }
  #dt-chatbot, .gradio-container .chatbot { border-radius: var(--dt-radius-lg) !important; }
}
"""


# Gradio expects `js` to be a single JS function, run once the app has loaded.
# Deliberately minimal: Gradio 6's ChatInterface already handles autofocus and
# autoscroll, so anything we add here would only fight it.
JS = """
() => {
  try {
    document.title = 'Digital Twin';
    // CSS hook for the entrance fade, so it runs once and only after mount.
    document.documentElement.classList.add('dt-ready');
  } catch (err) {
    console.warn('[digital-twin] style hooks failed:', err);
  }
}
"""


EXAMPLES = [
    "Give me the 30-second version of your background.",
    "What kind of roles are you looking for right now?",
    "Which project are you most proud of, and why?",
    "How much have you actually worked with LLMs and agents?",
    "What are you weakest at, honestly?",
    "I'd like to get in touch — how do I reach you?",
]
