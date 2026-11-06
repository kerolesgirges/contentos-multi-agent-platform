const state = { workflow: null, selectedTask: null };

const seed = {
  id: 'wf_7f31a8c2', title: 'Feedback loops for early-career engineers', audience: 'Early-career engineers', state: 'needs_review',
  tasks: [
    { id:'tsk_plan', name:'Shape requirements', kind:'planning', state:'approved', owner:'Planner', duration_ms:1840, artifact_id:'art_2a4d90c1', summary:'Clarified outcomes for early-career engineers.', confidence:96 },
    { id:'tsk_slides', name:'Draft slide outline', kind:'slides', state:'needs_review', owner:'Slide worker', duration_ms:4210, artifact_id:'art_8d2c71fe', summary:'12-slide outline with pacing notes and learning objectives.', confidence:88 },
    { id:'tsk_docs', name:'Write reading material', kind:'reading_material', state:'running', owner:'Docs worker', duration_ms:null, artifact_id:'art_414c9b18', summary:'Structured draft with examples and a glossary.', confidence:null },
    { id:'tsk_quiz', name:'Build knowledge check', kind:'quiz', state:'queued', owner:'Assessment worker', duration_ms:null, artifact_id:'art_0fd2a62b', summary:'Scenario-based questions aligned to the stated outcomes.', confidence:null },
    { id:'tsk_validate', name:'Validate artifact set', kind:'validation', state:'queued', owner:'QA worker', duration_ms:null, artifact_id:null, summary:'Cross-check objectives, terminology, and deliverable consistency.', confidence:null }
  ],
  events: [
    {timestamp:new Date().toISOString(), label:'Review checkpoint opened', detail:'Slide outline is waiting for a human decision.'},
    {timestamp:new Date(Date.now()-60000).toISOString(), label:'Planner completed', detail:'Requirements artifact approved automatically.'},
    {timestamp:new Date(Date.now()-120000).toISOString(), label:'Workflow created', detail:'Brief accepted and dependency graph assembled.'}
  ]
};

function stateLabel(value){ return value.replace('_',' '); }
function badge(value){ return `<span class="status-badge ${value}">${stateLabel(value)}</span>`; }
function runtime(value){ return value ? `${(value/1000).toFixed(2)}s` : '—'; }
function render(){
  const wf = state.workflow;
  document.querySelector('#active-workflow').textContent = `ACTIVE WORKFLOW / ${wf.id.toUpperCase()}`;
  document.querySelector('#page-title').textContent = wf.title;
  document.querySelector('#page-lede').textContent = `A synthetic content run for ${wf.audience}, showing how planning, generation, validation, and review fit together.`;
  document.querySelector('#page-state').className = `status-badge ${wf.state}`;
  document.querySelector('#page-state').textContent = stateLabel(wf.state);
  document.querySelector('#task-rows').innerHTML = wf.tasks.map(task => `<tr data-id="${task.id}" class="${task.id===state.selectedTask?.id?'selected':''}"><td><span class="task-name">${task.name}</span><span class="task-kind">${task.kind}</span></td><td class="owner">${task.owner}</td><td>${badge(task.state)}</td><td class="confidence ${task.confidence && task.confidence<90?'low':''}">${task.confidence ? `${task.confidence}%` : '—'}</td><td class="mono">${runtime(task.duration_ms)}</td></tr>`).join('');
  document.querySelector('#events').innerHTML = wf.events.map(event => `<div class="event"><span class="event-marker"></span><time>${new Date(event.timestamp).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}</time><strong>${event.label}</strong><span>${event.detail}</span></div>`).join('');
  document.querySelectorAll('#task-rows tr').forEach(row => row.addEventListener('click', () => { state.selectedTask = wf.tasks.find(task => task.id===row.dataset.id); renderDetail(); render(); }));
  renderDetail();
}
function renderDetail(){
  const task = state.selectedTask || state.workflow.tasks.find(item => item.state==='needs_review') || state.workflow.tasks[0]; state.selectedTask = task;
  document.querySelector('#detail-title').textContent = task.name; document.querySelector('#detail-state').outerHTML = badge(task.state).replace('status-badge','status-badge').replace('>',' id="detail-state">');
  document.querySelector('#detail-summary').textContent = task.summary; document.querySelector('#detail-owner').textContent = task.owner; document.querySelector('#detail-artifact').textContent = task.artifact_id || 'not created'; document.querySelector('#detail-confidence').textContent = task.confidence ? `${task.confidence}%` : 'pending';
  document.querySelector('#review-box').style.display = task.state==='needs_review' ? 'block' : 'none';
}
async function review(decision){
  const task = state.selectedTask; if(!task || task.state!=='needs_review') return;
  const note = document.querySelector('#review-note').value.trim() || (decision==='approve' ? 'Approved after human review.' : 'Please revise the artifact and return it to review.');
  try { const res = await fetch(`/api/workflows/${state.workflow.id}/tasks/${task.id}/review`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({decision,note})}); if(!res.ok) throw new Error('API unavailable'); state.workflow = await res.json(); state.selectedTask = state.workflow.tasks.find(item => item.id===task.id); render(); } catch { task.state = decision==='approve'?'approved':'running'; task.review_note=note; state.workflow.events.unshift({timestamp:new Date().toISOString(),label:`Review: ${decision}`,detail:note}); render(); }
}
document.querySelector('#approve').addEventListener('click', () => review('approve')); document.querySelector('#revise').addEventListener('click', () => review('revise'));
document.querySelector('#new-workflow').addEventListener('click', () => document.querySelector('#workflow-dialog').showModal());
document.querySelector('#workflow-form').addEventListener('submit', async event => { event.preventDefault(); const data = new FormData(event.target); const payload = {title:data.get('title'), audience:data.get('audience'), deliverables:data.get('deliverables').split(',')}; try { const res = await fetch('/api/workflows',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}); state.workflow = res.ok ? await res.json() : {...seed,id:`wf_${Math.random().toString(16).slice(2,10)}`,title:payload.title,audience:payload.audience}; } catch { state.workflow={...seed,id:`wf_${Math.random().toString(16).slice(2,10)}`,title:payload.title,audience:payload.audience}; } state.selectedTask=null; document.querySelector('#workflow-dialog').close(); render(); });
state.workflow = seed; render();
