"""Presentation layer for the Digital Twin app.

Exports three things consumed by ``app.py``:

    CSS      -> custom stylesheet, pass to ``gr.ChatInterface(css=CSS)``
    JS       -> on-load script,    pass to ``gr.ChatInterface(js=JS)``
    EXAMPLES -> starter prompts,   pass to ``gr.ChatInterface(examples=EXAMPLES)``

Note: ``css``, ``js`` and ``theme`` are constructor arguments of the
interface, NOT of ``.launch()``.

The stylesheet works in two layers:

    1. It overrides Gradio's own CSS custom properties, so every built-in
       component (buttons, inputs, blocks) picks up the palette for free.
    2. It adds a small number of structural rules for the pieces Gradio
       does not expose as variables (bubbles, header, examples, scrollbar).

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

  --dt-radius-lg: 20px;
  --dt-radius-md: 14px;
  --dt-radius-sm: 10px;

  --dt-accent: #5b5bd6;
  --dt-accent-hover: #4f4fc4;
  --dt-accent-glow: rgba(91, 91, 214, 0.28);

  --dt-page: #f6f6fa;
  --dt-surface: #ffffff;
  --dt-surface-alt: #f0f0f6;
  --dt-border: #e3e3ec;
  --dt-text: #14141c;
  --dt-text-muted: #6a6a7c;

  --dt-user-bg: linear-gradient(135deg, #5b5bd6 0%, #7d5cf0 100%);
  --dt-user-text: #ffffff;
  --dt-bot-bg: #ffffff;
  --dt-bot-text: #14141c;

  --dt-shadow-sm: 0 1px 2px rgba(16, 16, 29, 0.05);
  --dt-shadow-md: 0 2px 6px rgba(16, 16, 29, 0.06),
                  0 12px 32px rgba(16, 16, 29, 0.07);
}

.dark {
  --dt-accent: #7b7bf0;
  --dt-accent-hover: #8d8dfa;
  --dt-accent-glow: rgba(123, 123, 240, 0.32);

  --dt-page: #0c0c12;
  --dt-surface: #16161f;
  --dt-surface-alt: #1e1e2a;
  --dt-border: #2a2a38;
  --dt-text: #ececf2;
  --dt-text-muted: #9a9aae;

  --dt-user-bg: linear-gradient(135deg, #5b5bd6 0%, #8b5cf6 100%);
  --dt-user-text: #ffffff;
  --dt-bot-bg: #1b1b26;
  --dt-bot-text: #ececf2;

  --dt-shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --dt-shadow-md: 0 2px 6px rgba(0, 0, 0, 0.35),
                  0 12px 32px rgba(0, 0, 0, 0.45);
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
  --block-background-fill: var(--dt-surface);
  --block-border-color: var(--dt-border);
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
  --block-radius: var(--dt-radius-md);
  --input-radius: var(--dt-radius-md);

  --font: var(--dt-font);
  --font-mono: var(--dt-font-mono);
}

/* ==========================================================================
   3. Page shell
   ========================================================================== */

body,
gradio-app {
  background: var(--dt-page) !important;
}

/* Soft accent glow behind the conversation. */
gradio-app::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background:
    radial-gradient(60rem 32rem at 50% -12rem, var(--dt-accent-glow), transparent 70%);
  opacity: 0.75;
}

.gradio-container {
  position: relative;
  z-index: 1;
  max-width: 880px !important;
  margin: 0 auto !important;
  padding: 1.5rem 1rem 2rem !important;
  font-family: var(--dt-font);
  color: var(--dt-text);
}

/* Gradio's "Use via API / Built with Gradio" strip. */
footer,
.gradio-container footer {
  display: none !important;
}

/* ==========================================================================
   4. Header (title + description rendered by ChatInterface)
   ========================================================================== */

.gradio-container h1 {
  margin: 0 0 0.35rem !important;
  font-size: 2rem !important;
  font-weight: 700 !important;
  letter-spacing: -0.025em;
  text-align: center;
  background: var(--dt-user-bg);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ChatInterface renders `description` as a paragraph right under the title. */
.gradio-container h1 + div p,
.gradio-container h1 ~ .prose p:first-child {
  margin: 0 0 1.25rem !important;
  text-align: center;
  font-size: 0.95rem;
  color: var(--dt-text-muted);
}

/* ==========================================================================
   5. Chat surface
   ========================================================================== */

.gradio-container .block,
.gradio-container .form {
  border-radius: var(--dt-radius-lg) !important;
  border-color: var(--dt-border) !important;
}

#dt-chatbot,
.chatbot,
.gradio-container .chatbot {
  border: 1px solid var(--dt-border) !important;
  border-radius: var(--dt-radius-lg) !important;
  background: var(--dt-surface) !important;
  box-shadow: var(--dt-shadow-md);
  overflow: hidden;
}

.message-wrap,
.bubble-wrap {
  padding: 1.25rem 1rem !important;
  gap: 0.75rem !important;
  background: transparent !important;
}

/* Bubbles. Gradio has shuffled these class names between majors, so match
   the v4 (`.message.user`) and v5 (`.message-row.user-row`) shapes both. */
.message,
.message-row .message {
  max-width: 78% !important;
  padding: 0.7rem 1rem !important;
  border: none !important;
  border-radius: var(--dt-radius-md) !important;
  font-size: 0.95rem !important;
  line-height: 1.6 !important;
  box-shadow: var(--dt-shadow-sm);
  animation: dt-rise 0.28s ease both;
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
  border: 1px solid var(--dt-border) !important;
  border-bottom-left-radius: var(--dt-radius-sm) !important;
}

/* Keep links readable on the coloured user bubble. */
.message.user a,
.message-row.user-row .message a {
  color: #ffffff;
  text-decoration: underline;
}

/* Markdown inside a reply. */
.message p:first-child { margin-top: 0 !important; }
.message p:last-child  { margin-bottom: 0 !important; }

.message code {
  padding: 0.12em 0.4em;
  border-radius: 6px;
  font-family: var(--dt-font-mono);
  font-size: 0.875em;
  background: var(--dt-surface-alt);
  color: var(--dt-text);
}

.message pre {
  padding: 0.85rem 1rem;
  border: 1px solid var(--dt-border);
  border-radius: var(--dt-radius-sm);
  background: var(--dt-surface-alt) !important;
  overflow-x: auto;
}

.message pre code {
  padding: 0;
  background: transparent;
}

.message table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
}

.message th,
.message td {
  padding: 0.4rem 0.6rem;
  border: 1px solid var(--dt-border);
  text-align: left;
}

/* ==========================================================================
   6. Composer
   ========================================================================== */

.gradio-container textarea,
.gradio-container input[type="text"] {
  border-radius: var(--dt-radius-md) !important;
  font-family: var(--dt-font) !important;
  font-size: 0.95rem !important;
  resize: none;
}

.gradio-container textarea:focus,
.gradio-container input[type="text"]:focus {
  outline: none !important;
  border-color: var(--dt-accent) !important;
  box-shadow: 0 0 0 3px var(--dt-accent-glow) !important;
}

.gradio-container button {
  border-radius: var(--dt-radius-md) !important;
  font-weight: 550 !important;
  transition: transform 0.12s ease, filter 0.12s ease, background-color 0.12s ease;
}

.gradio-container button:hover  { filter: brightness(1.05); }
.gradio-container button:active { transform: translateY(1px); }

.gradio-container button:focus-visible {
  outline: 2px solid var(--dt-accent);
  outline-offset: 2px;
}

/* ==========================================================================
   7. Example prompts
   ========================================================================== */

.examples .gallery-item,
.gradio-dataset .gallery-item,
button.example {
  border: 1px solid var(--dt-border) !important;
  border-radius: 999px !important;
  padding: 0.45rem 0.95rem !important;
  background: var(--dt-surface) !important;
  color: var(--dt-text-muted) !important;
  font-size: 0.875rem !important;
  box-shadow: var(--dt-shadow-sm);
}

.examples .gallery-item:hover,
.gradio-dataset .gallery-item:hover,
button.example:hover {
  border-color: var(--dt-accent) !important;
  color: var(--dt-text) !important;
  background: var(--dt-surface-alt) !important;
}

/* ==========================================================================
   8. Scrollbar
   ========================================================================== */

.gradio-container *::-webkit-scrollbar { width: 9px; height: 9px; }
.gradio-container *::-webkit-scrollbar-track { background: transparent; }

.gradio-container *::-webkit-scrollbar-thumb {
  border: 2px solid transparent;
  border-radius: 999px;
  background-clip: padding-box;
  background-color: var(--dt-border);
}

.gradio-container *::-webkit-scrollbar-thumb:hover {
  background-color: var(--dt-text-muted);
}

/* ==========================================================================
   9. Motion + small screens
   ========================================================================== */

@keyframes dt-rise {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: none; }
}

.dt-ready .gradio-container {
  animation: dt-rise 0.35s ease both;
}

@media (prefers-reduced-motion: reduce) {
  .gradio-container *,
  .gradio-container *::before,
  .gradio-container *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

@media (max-width: 640px) {
  .gradio-container { padding: 1rem 0.65rem 1.5rem !important; }
  .gradio-container h1 { font-size: 1.6rem !important; }
  .message, .message-row .message { max-width: 90% !important; }
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
