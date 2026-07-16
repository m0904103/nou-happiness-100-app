import re
import uuid

with open('concepts.html', 'rb') as f:
    text = f.read().decode('utf-8', errors='ignore')

# 1. Add progress bar UI
progress_html = """
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
        <div style="flex-grow: 1; background: rgba(255,255,255,0.1); border-radius: 12px; height: 16px; margin-right: 15px; overflow: hidden; position: relative;">
          <div id="progress-bar-fill" style="width: 0%; height: 100%; background: linear-gradient(90deg, var(--accent), var(--green)); transition: width 0.5s ease;"></div>
          <div id="progress-text" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; text-align: center; line-height: 16px; font-size: 0.65rem; color: #fff; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">0 / 32 已掌握</div>
        </div>
        <label style="font-size: 0.8rem; color: var(--text-light); display: flex; align-items: center; cursor: pointer; user-select: none;">
          <input type="checkbox" id="hide-mastered-toggle" style="margin-right: 6px;" onchange="toggleHideMastered()"> 隱藏已掌握
        </label>
      </div>
"""
text = re.sub(r'(<h3[^>]*>.*?核心字卡</h3>)', r'\1\n' + progress_html, text)

# 2. Extract and process each flip-card
# A typical card ends with:
#             <div class="flip-card-back">
#               <p>Text</p>
#             </div>
#           </div>
#         </div>
# We want to insert buttons inside flip-card-back, after the <p> tag.

def card_replacer(match):
    div_start = match.group(1)
    content = match.group(2)
    end_tags = match.group(3)
    
    card_id = "UNKNOWN"
    id_match = re.search(r'id="([^"]+)"', div_start)
    if id_match:
        card_id = id_match.group(1)
    else:
        card_id = f"card-auto-{uuid.uuid4().hex[:8]}"
        div_start = div_start.replace('class="flip-card"', f'id="{card_id}" class="flip-card"')

    btn_html = f"""
              <div class="card-controls" style="margin-top: 15px; display: flex; gap: 8px; justify-content: center;">
                <button class="btn-master" onclick="markCard(event, '{card_id}', true)" style="background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; color: #10b981; padding: 4px 10px; border-radius: 6px; cursor: pointer; font-size: 0.8rem; transition: all 0.2s;">✅ 記熟了</button>
                <button class="btn-review" onclick="markCard(event, '{card_id}', false)" style="background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #ef4444; padding: 4px 10px; border-radius: 6px; cursor: pointer; font-size: 0.8rem; transition: all 0.2s;">🔄 需複習</button>
              </div>
"""
    return div_start + content + btn_html + end_tags

pattern_card = r'(<div[^>]*class="flip-card"[^>]*>)(.*?</p>\s*)(</div>\s*</div>\s*</div>)'
text = re.sub(pattern_card, card_replacer, text, flags=re.DOTALL)

# 3. Inject Javascript logic
js_logic = """
    // --- Version 2.0: Mastery Tracking Logic ---
    let hideMastered = false;
    
    function loadMastery() {
      const cards = document.querySelectorAll('.flip-card');
      let masteredCount = 0;
      
      cards.forEach(card => {
        const status = localStorage.getItem('mastery_' + card.id);
        const btnMaster = card.querySelector('.btn-master');
        const btnReview = card.querySelector('.btn-review');
        
        if (status === 'true') {
          masteredCount++;
          card.style.opacity = '0.6';
          card.style.border = '1px solid var(--green)';
          if (btnMaster) {
            btnMaster.style.background = 'var(--green)';
            btnMaster.style.color = '#fff';
            if (btnReview) {
              btnReview.style.background = 'rgba(239, 68, 68, 0.2)';
              btnReview.style.color = '#ef4444';
            }
          }
          if (hideMastered) {
            card.style.display = 'none';
          } else {
            card.style.display = 'block';
          }
        } else {
          card.style.opacity = '1';
          card.style.border = 'none';
          card.style.display = 'block';
          if (btnMaster) {
            btnMaster.style.background = 'rgba(16, 185, 129, 0.2)';
            btnMaster.style.color = '#10b981';
            if (btnReview) {
               btnReview.style.background = 'var(--red)';
               btnReview.style.color = '#fff';
            }
          }
        }
      });
      
      const total = cards.length;
      const progressFill = document.getElementById('progress-bar-fill');
      const progressText = document.getElementById('progress-text');
      if (progressFill && progressText) {
        const percentage = total === 0 ? 0 : Math.round((masteredCount / total) * 100);
        progressFill.style.width = percentage + '%';
        progressText.innerText = masteredCount + ' / ' + total + ' 已掌握 (' + percentage + '%)';
      }
    }
    
    function markCard(event, cardId, isMastered) {
      event.stopPropagation(); // prevent flipping the card when clicking the button
      localStorage.setItem('mastery_' + cardId, isMastered ? 'true' : 'false');
      loadMastery();
    }
    
    function toggleHideMastered() {
      const toggle = document.getElementById('hide-mastered-toggle');
      hideMastered = toggle.checked;
      loadMastery();
    }
    
    // Call loadMastery on startup
    window.addEventListener('DOMContentLoaded', () => {
      loadMastery();
    });
"""

text = re.sub(r'(</script>\s*</body>)', js_logic + r'\1', text)

with open('concepts.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Modification complete.")
