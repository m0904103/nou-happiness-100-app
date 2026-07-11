import re

# 1. Patch karaoke.css
with open("karaoke.css", "r", encoding="utf-8") as f:
    css = f.read()

# Replace .lyrics-wrapper
css = re.sub(
    r'\.lyrics-wrapper\s*\{[^}]+\}',
    """.lyrics-wrapper {
    flex-grow: 1;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    position: relative;
    mask-image: linear-gradient(to bottom, transparent 0%, black 15%, black 85%, transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 15%, black 85%, transparent 100%);
}
.lyrics-wrapper::-webkit-scrollbar {
    display: none; /* Hide scrollbar for a cleaner look */
}""",
    css
)

# Replace .lyrics-container
css = re.sub(
    r'\.lyrics-container\s*\{[^}]+\}',
    """.lyrics-container {
    width: 100%;
    padding: 40vh 0; /* Allow first and last lines to be centered */
}""",
    css
)

with open("karaoke.css", "w", encoding="utf-8") as f:
    f.write(css)

# 2. Patch karaoke.js
with open("karaoke.js", "r", encoding="utf-8") as f:
    js = f.read()

# Replace the transform logic with scrollIntoView
old_logic = """                // Scroll container to center the active line
                const wrapperHeight = document.getElementById('lyrics-wrapper').offsetHeight;
                const offset = newEl.offsetTop - (wrapperHeight / 2) + (newEl.offsetHeight / 2);
                lyricsContainer.style.transform = `translateY(-${offset}px)`;"""

new_logic = """                // Scroll container to center the active line smoothly
                newEl.scrollIntoView({ behavior: 'smooth', block: 'center' });"""

js = js.replace(old_logic, new_logic)

with open("karaoke.js", "w", encoding="utf-8") as f:
    f.write(js)

print("CSS and JS patched for iOS scrolling and click support.")
