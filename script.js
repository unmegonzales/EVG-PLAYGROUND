<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Visitor File Submissions</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <main class="site-shell">
      <section class="hero" aria-labelledby="page-title">
        <div class="hero__image" aria-hidden="true"></div>
        <div class="hero__content">
          <div class="utility-row">
            <span>GROUP SALES · VISITOR INTAKE</span>
            <span>FISCAL YEAR 2026</span>
          </div>
          <p class="eyebrow">Secure submission portal</p>
          <h1 id="page-title">Visitor <span>file submissions</span></h1>
          <p class="hero__copy">
            Send venue documents, event files, and review materials to the sales team in one organized packet.
          </p>
          <div class="hero__stats" aria-label="Submission checklist">
            <div>
              <strong>01</strong>
              <span>Visitor details</span>
            </div>
            <div>
              <strong>02</strong>
              <span>Files attached</span>
            </div>
            <div>
              <strong>03</strong>
              <span>Receipt issued</span>
            </div>
          </div>
        </div>
      </section>

      <section class="submission-grid" aria-label="Submission workspace">
        <form class="submission-form" id="submissionForm" novalidate>
          <div class="section-heading">
            <span>01</span>
            <div>
              <p>Visitor profile</p>
              <h2>Tell us who is submitting</h2>
            </div>
          </div>

          <div class="field-grid">
            <label>
              <span>Full name</span>
              <input name="name" autocomplete="name" required placeholder="Jordan Lee">
            </label>
            <label>
              <span>Organization</span>
              <input name="organization" autocomplete="organization" required placeholder="Campus Events Co.">
            </label>
            <label>
              <span>Email</span>
              <input name="email" type="email" autocomplete="email" required placeholder="jordan@example.com">
            </label>
            <label>
              <span>Destination team</span>
              <select name="team" required>
                <option value="">Select a team</option>
                <option>Group Sales</option>
                <option>Event Operations</option>
                <option>Finance</option>
                <option>Culinary</option>
                <option>Venue Leadership</option>
              </select>
            </label>
            <label>
              <span>Submission type</span>
              <select name="category" required>
                <option value="">Select a type</option>
                <option>Annual business review</option>
                <option>Venue analysis</option>
                <option>Event photos</option>
                <option>Contract or invoice</option>
                <option>Menu or sales kit</option>
              </select>
            </label>
            <label>
              <span>Due date</span>
              <input name="dueDate" type="date">
            </label>
          </div>

          <label class="full-field">
            <span>Notes for the team</span>
            <textarea name="notes" rows="4" placeholder="Add context, event names, requested review notes, or anything the receiving team should know."></textarea>
          </label>

          <div class="section-heading section-heading--files">
            <span>02</span>
            <div>
              <p>File packet</p>
              <h2>Attach visitor files</h2>
            </div>
          </div>

          <div class="drop-zone" id="dropZone">
            <input id="fileInput" type="file" multiple>
            <div class="drop-zone__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" role="img">
                <path d="M12 3v12m0-12 4.5 4.5M12 3 7.5 7.5M5 14v4a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4"/>
              </svg>
            </div>
            <div>
              <strong>Drop files here or browse</strong>
              <p>PDF, PPTX, DOCX, XLSX, PNG, JPG, and ZIP files are accepted up to 25 MB each.</p>
            </div>
            <button class="secondary-button" type="button" id="browseButton">Choose files</button>
          </div>

          <div class="file-list" id="fileList" aria-live="polite"></div>

          <label class="consent">
            <input name="consent" type="checkbox" required>
            <span>I confirm these files are approved for review by the selected team.</span>
          </label>

          <div class="form-actions">
            <button class="primary-button" type="submit">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M5 12h14m-6-6 6 6-6 6"/>
              </svg>
              Submit packet
            </button>
            <button class="ghost-button" type="reset">Clear form</button>
          </div>
        </form>

        <aside class="review-panel" aria-label="Submission status">
          <div class="panel-topline">Submission status</div>
          <div class="receipt" id="receipt">
            <span class="receipt__number">03</span>
            <h2>Ready for files</h2>
            <p>Complete the visitor profile and attach at least one file to generate a submission receipt.</p>
          </div>

          <div class="meter" aria-label="Packet completion">
            <div class="meter__label">
              <span>Packet completion</span>
              <strong id="completionValue">0%</strong>
            </div>
            <div class="meter__track">
              <div id="completionBar"></div>
            </div>
          </div>

          <div class="history">
            <div class="history__header">
              <h2>Recent receipts</h2>
              <button type="button" id="clearHistory">Clear</button>
            </div>
            <div id="historyList" class="history__list"></div>
          </div>
        </aside>
      </section>
    </main>

    <template id="fileTemplate">
      <div class="file-item">
        <div class="file-item__mark" aria-hidden="true"></div>
        <div>
          <strong></strong>
          <span></span>
        </div>
        <button type="button" aria-label="Remove file">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M6 6l12 12M18 6 6 18"/>
          </svg>
        </button>
      </div>
    </template>

    <script src="script.js"></script>
  </body>
</html>
