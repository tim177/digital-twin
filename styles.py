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
    2. It adds targeted rules for the pieces Gradio does not expose as
       variables, scoped under ``#dt-chatbot`` so they reliably beat Gradio's
       own Svelte-scoped rules.

Two things this deliberately does NOT do, both learned the hard way:

    * It never sets a width or max-width on ``.message``. Gradio sizes that
      element with ``width: 100%`` and constrains the row around it instead;
      adding a percentage max-width there collapses the bubble to one
      character wide.
    * It never forces ``display: flex`` onto Gradio's generic layout wrappers
      (``.main``, ``.contain``, ``.wrap``). Those class names appear at many
      nesting levels, and reflowing them pushes the composer off-screen.

Chat height comes from the ``height``/``min_height`` arguments on ``gr.Chatbot``
in app.py, not from CSS, so the composer always stays in the viewport.
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
  --dt-border-soft: rgba(20, 20, 30, 0.07);
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
  --dt-accent: #8b8bf8;
  --dt-accent-hover: #9d9dff;
  --dt-accent-grad: linear-gradient(135deg, #6d6df0 0%, #a855f7 100%);
  --dt-accent-glow: rgba(124, 108, 245, 0.30);

  --dt-page: #08080c;
  --dt-panel: rgba(19, 19, 25, 0.82);
  --dt-surface: #13131a;
  --dt-surface-alt: #1c1c26;
  --dt-border: #272733;
  --dt-border-soft: rgba(255, 255, 255, 0.07);
  --dt-text: #f0f0f6;
  --dt-text-muted: #9494ab;

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
  --block-background-fill: var(--dt-surface);
  --block-border-color: var(--dt-border);
  --block-label-background-fill: var(--dt-surface-alt);
  --block-title-text-color: var(--dt-text-muted);
  --block-shadow: none;

  --border-color-primary: var(--dt-border);
  --border-color-accent: var(--dt-accent);
  --border-color-accent-subdued: var(--dt-border);

  --body-text-color: var(--dt-text);
  --body-text-color-subdued: var(--dt-text-muted);
  --link-text-color: var(--dt-accent);
  --link-text-color-hover: var(--dt-accent-hover);
  --color-text-link: var(--dt-accent);

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

body, gradio-app {
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
  padding: 1.25rem 1.5rem 1rem !important;
  font-family: var(--dt-font);
  color: var(--dt-text);
}

footer,
.gradio-container footer {
  display: none !important;
}

/* ==========================================================================
   4. Header
   ChatInterface renders the title as an <h1> with inline centering, and the
   description as its own Markdown block. app.py wraps the description in
   .dt-subtitle so it can be targeted directly.
   ========================================================================== */

.gradio-container h1 {
  margin: 0 0 0.25rem !important;
  color: var(--dt-accent) !important;
  font-size: 2.05rem !important;
  font-weight: 700 !important;
  letter-spacing: -0.03em;
}

.dt-subtitle {
  margin: 0 0 1.1rem !important;
  text-align: center;
  font-size: 0.97rem;
  color: var(--dt-text-muted);
}

/* ==========================================================================
   5. Chat panel
   ========================================================================== */

#dt-chatbot {
  border: 1px solid var(--dt-border) !important;
  border-radius: var(--dt-radius-xl) !important;
  background: var(--dt-panel) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: var(--dt-shadow-md);
  overflow: hidden;
}

#dt-chatbot .bubble-wrap,
#dt-chatbot .message-wrap {
  background: transparent !important;
}

/* Bubbles. `.user` / `.bot` sit on the same element as `.message`; the id
   prefix is what makes these win against Gradio's scoped rules. Appearance
   only -- Gradio owns the sizing. */
#dt-chatbot .message.user,
#dt-chatbot .message.bot {
  padding: 0.8rem 1.1rem !important;
  border-radius: var(--dt-radius-lg) !important;
  font-size: 0.97rem !important;
  line-height: 1.68 !important;
  box-shadow: var(--dt-shadow-sm) !important;
  animation: dt-rise 0.3s cubic-bezier(0.22, 1, 0.36, 1) both;
}

#dt-chatbot .message.user {
  background: var(--dt-user-bg) !important;
  border: none !important;
  color: var(--dt-user-text) !important;
  border-bottom-right-radius: var(--dt-radius-sm) !important;
}

#dt-chatbot .message.bot {
  background: var(--dt-bot-bg) !important;
  border: 1px solid var(--dt-border-soft) !important;
  color: var(--dt-bot-text) !important;
  border-bottom-left-radius: var(--dt-radius-sm) !important;
}

/* Gradio dims assistant prose to 80% by default; full strength reads better
   against these bubbles. */
#dt-chatbot .message-wrap .prose.chatbot.md {
  opacity: 1 !important;
}

#dt-chatbot .message.user a {
  color: #ffffff !important;
  text-decoration: underline;
  text-underline-offset: 2px;
}

#dt-chatbot .avatar-container {
  border-color: var(--dt-border) !important;
  box-shadow: var(--dt-shadow-sm);
}

/* Typing indicator between turns. */
#dt-chatbot .bubble.pending {
  border-radius: var(--dt-radius-lg) !important;
  border-color: var(--dt-border-soft) !important;
  background: var(--dt-bot-bg) !important;
}

/* ==========================================================================
   6. Markdown inside a reply
   ========================================================================== */

#dt-chatbot .message p:first-child { margin-top: 0 !important; }
#dt-chatbot .message p:last-child  { margin-bottom: 0 !important; }

#dt-chatbot .message ul,
#dt-chatbot .message ol {
  margin: 0.45rem 0 !important;
  padding-left: 1.25rem !important;
}

#dt-chatbot .message li { margin: 0.25rem 0 !important; }

#dt-chatbot .message code {
  padding: 0.14em 0.42em;
  border-radius: 6px;
  font-family: var(--dt-font-mono);
  font-size: 0.87em;
  background: var(--dt-surface-alt);
}

#dt-chatbot .message pre {
  margin: 0.65rem 0;
  padding: 0.9rem 1.05rem;
  border: 1px solid var(--dt-border);
  border-radius: var(--dt-radius-md);
  background: var(--dt-surface-alt) !important;
  overflow-x: auto;
}

#dt-chatbot .message pre code {
  padding: 0;
  background: transparent;
  font-size: 0.86em;
  line-height: 1.6;
}

#dt-chatbot .message blockquote {
  margin: 0.55rem 0;
  padding: 0.1rem 0 0.1rem 0.85rem;
  border-left: 3px solid var(--dt-accent);
  color: var(--dt-text-muted);
}

#dt-chatbot .message table {
  width: 100%;
  margin: 0.55rem 0;
  border-collapse: collapse;
  font-size: 0.9em;
}

#dt-chatbot .message th,
#dt-chatbot .message td {
  padding: 0.42rem 0.65rem;
  text-align: left;
}

#dt-chatbot .message th {
  background: var(--dt-surface-alt);
  font-weight: 600;
}

/* ==========================================================================
   7. Example prompts
   These render as a card grid inside the empty chatbot, not as chips.
   ========================================================================== */

#dt-chatbot .example {
  padding: 0.9rem 1.05rem !important;
  border: 1px solid var(--dt-border) !important;
  border-radius: var(--dt-radius-md) !important;
  background: var(--dt-surface) !important;
  color: var(--dt-text-muted) !important;
  box-shadow: var(--dt-shadow-sm);
  transition: border-color 0.15s ease, color 0.15s ease, transform 0.15s ease;
}

#dt-chatbot .example:hover {
  border-color: var(--dt-accent) !important;
  background: var(--dt-surface) !important;
  color: var(--dt-text) !important;
  transform: translateY(-2px);
}

#dt-chatbot .example-text {
  font-size: 0.9rem !important;
  line-height: 1.5;
}

/* ==========================================================================
   8. Composer
   ========================================================================== */

.gradio-container textarea,
.gradio-container input[type="text"] {
  padding: 0.8rem 1.05rem !important;
  border: 1px solid var(--dt-border) !important;
  border-radius: var(--dt-radius-lg) !important;
  background: var(--dt-surface) !important;
  box-shadow: var(--dt-shadow-sm) !important;
  font-family: var(--dt-font) !important;
  font-size: 0.97rem !important;
  line-height: 1.55 !important;
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
  transition: transform 0.12s ease, filter 0.12s ease;
}

.gradio-container button.primary {
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

@media (max-width: 640px) {
  .gradio-container { padding: 0.9rem 0.7rem 0.7rem !important; }
  .gradio-container h1 { font-size: 1.6rem !important; }
  #dt-chatbot { border-radius: var(--dt-radius-lg) !important; }
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
