---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

<div class="hero">
  <h1 class="hero-title">An Online Human Evaluation Platform for Debate Performance</h1>
  <p class="hero-subtitle">Help shape the future of AI debate through your valuable feedback</p>
</div>

<div class="container is-max-desktop">
  <div class="section overview">
    <h2>Overview</h2>
    <div class="card">
      <p>Welcome to our debate evaluation platform! Here, you'll have the opportunity to evaluate 20-minute debates where two sides discuss important topics. Your opinion is valuable - you'll vote both before and after listening to the debate. We use your feedback to continuously improve debate quality.</p>
    </div>
  </div>

  <div class="section how-it-works">
    <h2>How It Works</h2>
    <div class="timeline">
      <div class="timeline-item">
        <div class="timeline-number">1</div>
        <div class="timeline-content">
          <h3>Opening</h3>
          <p>Initial arguments and positions</p>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-number">2</div>
        <div class="timeline-content">
          <h3>Rebuttal</h3>
          <p>Response to opposing arguments</p>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-number">3</div>
        <div class="timeline-content">
          <h3>Closing</h3>
          <p>Final statements and conclusions</p>
        </div>
      </div>
    </div>
  </div>

  <div class="section evaluation">
    <h2>Evaluation Process</h2>
    <div class="process-steps">
      <!-- <div class="step">
        <i class="fas fa-clipboard-list"></i>
        <h3>Complete Questionnaire</h3>
        <p>Share your initial thoughts and expectations</p>
      </div> -->
      <div class="step">
        <i class="fas fa-vote-yea"></i>
        <h3>Vote</h3>
        <p>Cast your vote before and after the debate</p>
      </div>
      <div class="step">
        <i class="fas fa-balance-scale"></i>
        <h3>Compare Performance</h3>
        <p>Evaluate each side's performance in each stage</p>
      </div>
      <div class="step">
        <i class="fas fa-comment-alt"></i>
        <h3>Provide Feedback</h3>
        <p>Share your thoughts for improvement</p>
      </div>
    </div>
  </div>

  <div class="section examples">
    <h2>Example Debates</h2>
    
    <div class="example-section">
      <h3>End-to-End Comparison Examples</h3>
      <div class="example-grid">
        {% for file in site.static_files %}
          {% if file.path contains "forms/example/e2e" and file.extname == ".html" %}
            {% assign filename = file.name | split: '.html' | first %}
            <a href="{{ site.baseurl }}/{{ file.path }}" class="example-card">
              <span class="example-number">Case {{ filename }}</span>
            </a>
          {% endif %}
        {% endfor %}
      </div>
    </div>

    <div class="example-section">
      <h3>Stage-Level Head-to-Head Comparison Examples</h3>
      <div class="example-grid">
        {% for file in site.static_files %}
          {% if file.path contains "forms/example/h2h" and file.extname == ".html" %}
            {% assign filename = file.name | split: '.html' | first %}
            {% assign case_parts = filename | split: '(' %}
            {% assign case_number = case_parts[0] %}
            {% assign side_info = case_parts[1] | split: ')' | first %}
            {% assign side_number = side_info | split: '_' | last | replace: 'n0', 'S1' | replace: 'n1', 'S2' | replace: 'n2', 'S3' | replace: 'n3', 'S4' | replace: 'n4', 'S5' | replace: 'n5', 'S6' %}
            <a href="{{ site.baseurl }}/{{ file.path }}" class="example-card">
              <span class="example-number">Case {{ case_number }} {{ side_number }}</span>
            </a>
          {% endif %}
        {% endfor %}
      </div>
    </div>

    See more examples in the <a href="{{ site.baseurl }}/active">active</a> page.
  </div>
</div>

<style>
.hero {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  margin-bottom: 2rem;
}

.hero-title {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #34495e;
}

.container.is-max-desktop {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 1rem;
}

.section {
  margin-bottom: 3rem;
}

.card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.timeline {
  display: flex;
  justify-content: space-between;
  margin: 2rem 0;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background: #e0e0e0;
  z-index: 1;
}

.timeline-item {
  text-align: center;
  position: relative;
  z-index: 2;
  flex: 1;
  padding: 0 1rem;
}

.timeline-number {
  width: 40px;
  height: 40px;
  background: #3498db;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-weight: bold;
}

.process-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.step {
  text-align: center;
  padding: 1rem;
  transition: transform 0.3s ease;
}

.step:hover {
  transform: translateY(-5px);
}

.step i {
  font-size: 2rem;
  color: #3498db;
  margin-bottom: 1rem;
}

.step h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.step p {
  color: #666;
  font-size: 0.95rem;
}

.example-section {
  margin-bottom: 3rem;
}

.example-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 0.75rem;
  margin-top: 1rem;
}

.example-card {
  display: block;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
  text-decoration: none;
  color: #2c3e50;
  transition: all 0.3s ease;
}

.example-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  position: relative;
  padding-bottom: 0.5rem;
}

h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 50px;
  height: 3px;
  background: #3498db;
}

@media (max-width: 768px) {
  .timeline {
    flex-direction: column;
  }
  
  .timeline::before {
    display: none;
  }
  
  .timeline-item {
    margin-bottom: 2rem;
  }
  
  .process-steps {
    grid-template-columns: 1fr;
  }

  .example-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
