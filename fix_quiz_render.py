
import re
import os

# List of all 12 quiz files
QUIZ_FILES = [
    "thaikid.html", "mathkid.html", "artkid.html", "music_kid.html", "pe_kid.html",
    "social_kid.html", "science_kid.html", "tech_kid.html", "reading_kid.html",
    "creative_kid.html", "health_kid.html", "life_kid.html"
]

# The common JavaScript block to ensure renderQuiz is called
RENDER_QUIZ_CALL = """
      // Initial render and event listener setup
      renderQuiz();
      quizForm.addEventListener('submit', checkAnswers);
    });
  </script>
"""

# The new JavaScript block to replace the old one
NEW_SCRIPT_BLOCK_TEMPLATE = """
  <script>
    const QUIZ_DATA = [
        // QUIZ_DATA will be here
    ];

    document.addEventListener('DOMContentLoaded', () => {
      const quizForm = document.getElementById('quizForm');
      const submitBtn = quizForm.querySelector('.submit-btn');
      const questionsContainer = document.createElement('div');
      quizForm.insertBefore(questionsContainer, submitBtn);

      // Function to render the quiz questions
      function renderQuiz() {
        let html = '';
        QUIZ_DATA.forEach((qData, index) => {
          const qNum = index + 1;
          html += `
            <div class="question-card">
              <h4>ข้อ ${qNum}: ${qData.q}</h4>
              <div class="options">
          `;
          qData.options.forEach((option, optIndex) => {
            const optionId = `q${qNum}_${optIndex}`;
            html += `
                <label for="${optionId}"><input type="radio" name="q${qNum}" id="${optionId}" value="${option}"> ${option}</label>
            `;
          });
          html += `
              </div>
            </div>
          `;
        });
        
        questionsContainer.innerHTML = html;
      }

      // Function to check answers (redirect logic)
      function checkAnswers(e) {
        e.preventDefault();
        
        let score = 0;
        let totalQuestions = QUIZ_DATA.length;
        let subject = document.querySelector('.header h1').textContent.replace('แบบฝึกหัด', '').trim();

        QUIZ_DATA.forEach((qData, index) => {
          const qNum = index + 1;
          const selectedOption = quizForm.querySelector(`input[name="q${qNum}"]:checked`);
          
          if (selectedOption && selectedOption.value === qData.answer) {
            score++;
          }
        });

        // Redirect to result.html with score, total, and subject as URL parameters
        window.location.href = `result.html?score=${score}&total=${totalQuestions}&subject=${subject}`;
      }

      // Initial render and event listener setup
      renderQuiz();
      quizForm.addEventListener('submit', checkAnswers);
    });
  </script>
"""

for filename in QUIZ_FILES:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Extract the QUIZ_DATA array content
        quiz_data_match = re.search(r'const QUIZ_DATA = \[(.*?)\];', content, re.DOTALL)
        
        if not quiz_data_match:
            print(f"Error: Could not find QUIZ_DATA in {filename}. Skipping.")
            continue
            
        quiz_data_content = quiz_data_match.group(1).strip()

        # 2. Extract the subject name from the header for the template
        subject_match = re.search(r'<h1>แบบฝึกหัด(.*?)<\/h1>', content)
        subject_name = subject_match.group(1).strip() if subject_match else "วิชา"

        # 3. Create the final script block with the extracted data
        final_script_block = NEW_SCRIPT_BLOCK_TEMPLATE.replace("// QUIZ_DATA will be here", quiz_data_content)
        
        # 4. Replace the entire old script block with the new one
        # Find the entire <script>...</script> block
        script_block_full_match = re.search(r'<script>.*?<\/script>', content, re.DOTALL)
        
        if script_block_full_match:
            # Replace the old script block with the new one
            new_content = content.replace(script_block_full_match.group(0), final_script_block)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Successfully fixed rendering for {filename}")
        else:
            print(f"Error: Could not find script block in {filename}. Skipping.")

    except FileNotFoundError:
        print(f"Error: File not found: {filename}. Skipping.")
    except Exception as e:
        print(f"An unexpected error occurred while processing {filename}: {e}")
