/**
 * ============================================================================
 * STATISTICAL VISUAL TEXTBOOK — INTERACTIVE SIMULATION SUITE
 * Visual Intuition Engines for ANOVA, k-Means, Logistic, Moderation, and CMB
 * ============================================================================
 */

window.StatSims = window.StatSims || {};

document.addEventListener('DOMContentLoaded', () => {
  initAnovaSim();
  initKmeansSim();
  initLogisticSim();
  initModerationSim();
  initSiemsenSim();
});

/* ============================================================================
   SIMULATOR 1: ANOVA SIGNAL VS. NOISE BALANCE
   ============================================================================ */
function initAnovaSim() {
  const canvas = document.getElementById('canvas-anova');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const sliderDiff = document.getElementById('anova-diff');
  const sliderNoise = document.getElementById('anova-noise');
  const valDiff = document.getElementById('anova-diff-val');
  const valNoise = document.getElementById('anova-noise-val');

  const statF = document.getElementById('anova-f');
  const statP = document.getElementById('anova-p');
  const statEta = document.getElementById('anova-eta');

  function render() {
    const diff = parseFloat(sliderDiff.value); // Group separation
    const noise = parseFloat(sliderNoise.value); // Within-group SD
    valDiff.textContent = diff.toFixed(1);
    valNoise.textContent = noise.toFixed(1);

    const W = canvas.width;
    const H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    // Three groups: Executives, Managers, Staff
    const means = [
      4.2 - diff * 0.8,
      4.2,
      4.2 + diff * 0.8
    ];
    const colors = ['#005BAC', '#00838F', '#C86258'];
    const labels = ['一般社員 (Staff)', '中間管理職 (Manager)', '経営層 (Exec)'];

    // Draw normal curves for each group
    const xMin = 1.0;
    const xMax = 7.0;
    const scaleX = (x) => 60 + ((x - xMin) / (xMax - xMin)) * (W - 120);

    // Draw grid lines
    ctx.strokeStyle = '#E2E8F0';
    ctx.lineWidth = 1;
    for (let x = 1; x <= 7; x++) {
      const px = scaleX(x);
      ctx.beginPath();
      ctx.moveTo(px, H - 40);
      ctx.lineTo(px, 30);
      ctx.stroke();

      ctx.fillStyle = '#64748B';
      ctx.font = '12px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(x.toFixed(0), px, H - 20);
    }

    // Baseline
    ctx.strokeStyle = '#94A3B8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(40, H - 40);
    ctx.lineTo(W - 40, H - 40);
    ctx.stroke();

    // Plot curves
    means.forEach((m, idx) => {
      ctx.beginPath();
      ctx.strokeStyle = colors[idx];
      ctx.fillStyle = colors[idx] + '22'; // 13% opacity
      ctx.lineWidth = 3;

      let first = true;
      for (let x = xMin; x <= xMax; x += 0.05) {
        const px = scaleX(x);
        // Gaussian PDF
        const z = (x - m) / noise;
        const yVal = (1 / (noise * Math.sqrt(2 * Math.PI))) * Math.exp(-0.5 * z * z);
        const py = (H - 40) - (yVal * 120);

        if (first) {
          ctx.moveTo(px, py);
          first = false;
        } else {
          ctx.lineTo(px, py);
        }
      }
      ctx.stroke();
      ctx.lineTo(scaleX(xMax), H - 40);
      ctx.lineTo(scaleX(xMin), H - 40);
      ctx.closePath();
      ctx.fill();

      // Draw Mean marker
      const pmx = scaleX(m);
      ctx.strokeStyle = colors[idx];
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(pmx, H - 40);
      ctx.lineTo(pmx, 50);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = colors[idx];
      ctx.beginPath();
      ctx.arc(pmx, 50, 5, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = colors[idx];
      ctx.font = 'bold 12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(labels[idx], pmx, 38);
    });

    // Statistical calculations (simulated F and eta^2)
    const nPerGroup = 678; // 2035 / 3
    const signal = Math.pow(diff, 2) * nPerGroup;
    const noiseVar = Math.pow(noise, 2);
    const simulatedF = Math.max(0.1, (signal / (noiseVar * 80)));
    
    // Approximate p-value
    let pValStr = '< 0.001';
    if (simulatedF < 3.0) pValStr = '0.052 (有意差なし)';
    else if (simulatedF < 4.6) pValStr = '0.010';
    else if (simulatedF < 6.9) pValStr = '0.001';

    // eta^2
    const eta2 = (simulatedF * 2) / (simulatedF * 2 + (2035 - 3));

    statF.textContent = simulatedF.toFixed(2);
    statP.textContent = pValStr;
    statEta.textContent = eta2.toFixed(3);

    if (simulatedF >= 3.0) {
      statF.className = 'stat-chip-value success';
      statP.className = 'stat-chip-value success';
    } else {
      statF.className = 'stat-chip-value highlight';
      statP.className = 'stat-chip-value highlight';
    }
  }

  sliderDiff.addEventListener('input', render);
  sliderNoise.addEventListener('input', render);
  render();
}

/* ============================================================================
   SIMULATOR 2: K-MEANS CENTROID MAGNET ANIMATION & ELBOW
   ============================================================================ */
function initKmeansSim() {
  const canvas = document.getElementById('canvas-kmeans');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const btnReset = document.getElementById('kmeans-reset');
  const btnStep = document.getElementById('kmeans-step');
  const btnAuto = document.getElementById('kmeans-auto');
  const statStep = document.getElementById('kmeans-step-val');
  const statWcss = document.getElementById('kmeans-wcss-val');

  const W = canvas.width;
  const H = canvas.height;
  const K = 3;
  const N_POINTS = 180;
  const colors = ['#005BAC', '#00838F', '#C86258'];

  let points = [];
  let centroids = [];
  let stepCount = 0;
  let autoTimer = null;

  function initData() {
    points = [];
    const trueCenters = [
      { x: W * 0.45, y: H * 0.50, weight: 0.52 }, // 52% Passive
      { x: W * 0.75, y: H * 0.25, weight: 0.35 }, // 35% Champion
      { x: W * 0.25, y: H * 0.75, weight: 0.13 }  // 13% Antagonist
    ];

    trueCenters.forEach((tc) => {
      const count = Math.round(N_POINTS * tc.weight);
      for (let i = 0; i < count; i++) {
        const u1 = Math.random();
        const u2 = Math.random();
        const z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
        const z1 = Math.sqrt(-2.0 * Math.log(u1)) * Math.sin(2.0 * Math.PI * u2);
        points.push({
          x: tc.x + z0 * 36,
          y: tc.y + z1 * 36,
          cluster: -1
        });
      }
    });

    centroids = [];
    for (let k = 0; k < K; k++) {
      centroids.push({
        x: W * 0.2 + Math.random() * (W * 0.6),
        y: H * 0.2 + Math.random() * (H * 0.6),
        color: colors[k]
      });
    }

    stepCount = 0;
    assignPoints();
    draw();
  }

  function assignPoints() {
    points.forEach(p => {
      let minDist = Infinity;
      let bestC = -1;
      centroids.forEach((c, cIdx) => {
        const d = Math.hypot(p.x - c.x, p.y - c.y);
        if (d < minDist) {
          minDist = d;
          bestC = cIdx;
        }
      });
      p.cluster = bestC;
    });
  }

  function updateCentroids() {
    stepCount++;
    centroids.forEach((c, cIdx) => {
      const assigned = points.filter(p => p.cluster === cIdx);
      if (assigned.length > 0) {
        const avgX = assigned.reduce((acc, p) => acc + p.x, 0) / assigned.length;
        const avgY = assigned.reduce((acc, p) => acc + p.y, 0) / assigned.length;
        c.x = avgX;
        c.y = avgY;
      }
    });
    assignPoints();
  }

  function calcWCSS() {
    let wcss = 0;
    points.forEach(p => {
      if (p.cluster >= 0) {
        const c = centroids[p.cluster];
        wcss += Math.pow(p.x - c.x, 2) + Math.pow(p.y - c.y, 2);
      }
    });
    return Math.round(wcss / 100);
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);

    // Axis labels
    ctx.fillStyle = '#64748B';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText('DX推進意向 → (高い)', W - 20, H - 15);
    ctx.save();
    ctx.translate(20, 20);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('組織的不安・反発度 → (高い)', 0, 0);
    ctx.restore();

    // Connection lines to centroids
    points.forEach(p => {
      if (p.cluster >= 0) {
        const c = centroids[p.cluster];
        ctx.strokeStyle = colors[p.cluster] + '20';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(c.x, c.y);
        ctx.stroke();
      }
    });

    // Draw points
    points.forEach(p => {
      ctx.fillStyle = p.cluster >= 0 ? colors[p.cluster] : '#94A3B8';
      ctx.beginPath();
      ctx.arc(p.x, p.y, 4.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#FFFFFF';
      ctx.lineWidth = 1;
      ctx.stroke();
    });

    // Draw Centroids
    centroids.forEach((c, idx) => {
      ctx.fillStyle = c.color + '33';
      ctx.beginPath();
      ctx.arc(c.x, c.y, 16, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = c.color;
      ctx.beginPath();
      ctx.arc(c.x, c.y, 8, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#FFFFFF';
      ctx.lineWidth = 2.5;
      ctx.stroke();

      ctx.fillStyle = '#0F172A';
      ctx.font = 'bold 11px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`C${idx + 1}`, c.x, c.y - 18);
    });

    statStep.textContent = stepCount;
    statWcss.textContent = calcWCSS().toLocaleString();
  }

  btnReset.addEventListener('click', () => {
    if (autoTimer) clearInterval(autoTimer);
    initData();
  });

  btnStep.addEventListener('click', () => {
    updateCentroids();
    draw();
  });

  btnAuto.addEventListener('click', () => {
    if (autoTimer) {
      clearInterval(autoTimer);
      autoTimer = null;
      btnAuto.textContent = '自動収束実行';
    } else {
      btnAuto.textContent = '停止';
      autoTimer = setInterval(() => {
        if (stepCount >= 15) {
          clearInterval(autoTimer);
          autoTimer = null;
          btnAuto.textContent = '自動収束実行';
        } else {
          updateCentroids();
          draw();
        }
      }, 350);
    }
  });

  initData();
}

/* ============================================================================
   SIMULATOR 3: LINEAR BREAKDOWN VS. LOGISTIC SIGMOID
   ============================================================================ */
function initLogisticSim() {
  const canvas = document.getElementById('canvas-logistic');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const btnLinear = document.getElementById('btn-mode-linear');
  const btnLogistic = document.getElementById('btn-mode-logistic');
  const sliderBeta = document.getElementById('logistic-beta');
  const valBeta = document.getElementById('logistic-beta-val');
  const statOR = document.getElementById('logistic-or');
  const statProb = document.getElementById('logistic-prob');

  let mode = 'logistic';

  function render() {
    const beta1 = parseFloat(sliderBeta.value);
    valBeta.textContent = beta1.toFixed(2);
    const orVal = Math.exp(beta1);
    statOR.textContent = orVal.toFixed(2) + ' 倍';

    const W = canvas.width;
    const H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    const padLeft = 60;
    const padRight = 40;
    const padTop = 40;
    const padBottom = 50;
    const graphW = W - padLeft - padRight;
    const graphH = H - padTop - padBottom;

    const scaleY = (y) => (H - padBottom) - (y * graphH);
    const scaleX = (x) => padLeft + (x * graphW);

    // Hazard Zones
    ctx.fillStyle = 'rgba(200, 98, 88, 0.12)';
    ctx.fillRect(padLeft, 0, graphW, padTop);
    ctx.fillRect(padLeft, H - padBottom, graphW, padBottom);

    // Y = 1 & Y = 0
    ctx.strokeStyle = '#005BAC';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(padLeft, scaleY(1));
    ctx.lineTo(W - padRight, scaleY(1));
    ctx.moveTo(padLeft, scaleY(0));
    ctx.lineTo(W - padRight, scaleY(0));
    ctx.stroke();
    ctx.setLineDash([]);

    // Y Axis labels
    ctx.fillStyle = '#64748B';
    ctx.font = '12px monospace';
    ctx.textAlign = 'right';
    ctx.fillText('P = 1.0 (反発層所属)', padLeft - 10, scaleY(1) + 4);
    ctx.fillText('P = 0.5', padLeft - 10, scaleY(0.5) + 4);
    ctx.fillText('P = 0.0 (非反発)', padLeft - 10, scaleY(0) + 4);

    ctx.fillStyle = '#C86258';
    ctx.font = 'bold 11px sans-serif';
    ctx.fillText('破綻領域: 確率 > 100%', W - padRight - 10, padTop - 12);
    ctx.fillText('破綻領域: 確率 < 0%', W - padRight - 10, H - 15);

    // X axis
    ctx.strokeStyle = '#94A3B8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padLeft, H - padBottom);
    ctx.lineTo(W - padRight, H - padBottom);
    ctx.stroke();

    ctx.fillStyle = '#64748B';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('職位階層（左: 経営幹部 ───────────→ 右: 一般社員・非役職者）', padLeft + graphW / 2, H - 15);

    // Data points
    ctx.fillStyle = '#334155';
    const samplePoints = [
      { x: 0.05, y: 0 }, { x: 0.12, y: 0 }, { x: 0.18, y: 0 }, { x: 0.22, y: 0 }, { x: 0.28, y: 0 },
      { x: 0.35, y: 0 }, { x: 0.42, y: 0 }, { x: 0.55, y: 0 }, { x: 0.65, y: 0 }, { x: 0.72, y: 1 },
      { x: 0.60, y: 1 }, { x: 0.78, y: 1 }, { x: 0.82, y: 1 }, { x: 0.88, y: 1 }, { x: 0.92, y: 1 }, { x: 0.96, y: 1 }
    ];
    samplePoints.forEach(pt => {
      ctx.beginPath();
      ctx.arc(scaleX(pt.x), scaleY(pt.y), 4, 0, Math.PI * 2);
      ctx.fill();
    });

    if (mode === 'linear') {
      const intercept = -0.3;
      const slope = beta1 * 0.45;

      ctx.strokeStyle = '#C86258';
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      for (let x = 0; x <= 1.0; x += 0.02) {
        const predY = intercept + slope * x;
        const px = scaleX(x);
        const py = scaleY(predY);
        if (x === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();

      statProb.textContent = '破綻（負の確率・100%超過）';
      statProb.className = 'stat-chip-value highlight';
    } else {
      const beta0 = -1.5;
      ctx.strokeStyle = '#005BAC';
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      for (let x = 0; x <= 1.0; x += 0.01) {
        const logit = beta0 + beta1 * (x - 0.2) * 2.5;
        const pVal = 1 / (1 + Math.exp(-logit));
        const px = scaleX(x);
        const py = scaleY(pVal);
        if (x === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();

      const staffLogit = beta0 + beta1 * (0.85 - 0.2) * 2.5;
      const staffP = 1 / (1 + Math.exp(-staffLogit));
      statProb.textContent = (staffP * 100).toFixed(1) + ' %';
      statProb.className = 'stat-chip-value success';
    }
  }

  btnLinear.addEventListener('click', () => {
    mode = 'linear';
    btnLinear.className = 'btn-pill active';
    btnLogistic.className = 'btn-pill';
    render();
  });

  btnLogistic.addEventListener('click', () => {
    mode = 'logistic';
    btnLogistic.className = 'btn-pill active';
    btnLinear.className = 'btn-pill';
    render();
  });

  sliderBeta.addEventListener('input', render);
  render();
}

/* ============================================================================
   SIMULATOR 4: MODERATION EFFECT & SIMPLE SLOPE
   ============================================================================ */
function initModerationSim() {
  const canvas = document.getElementById('canvas-moderation');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const sliderDialogue = document.getElementById('mod-dialogue');
  const valDialogue = document.getElementById('mod-dialogue-val');
  const statSlope = document.getElementById('mod-slope');
  const statImpact = document.getElementById('mod-impact');

  function render() {
    const dialogue = parseFloat(sliderDialogue.value);
    valDialogue.textContent = (dialogue > 0 ? '+' : '') + dialogue.toFixed(1) + ' SD';

    const W = canvas.width;
    const H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    const padLeft = 60;
    const padRight = 40;
    const padTop = 40;
    const padBottom = 50;
    const graphW = W - padLeft - padRight;
    const graphH = H - padTop - padBottom;

    const scaleX = (x) => padLeft + ((x + 2.5) / 5.0) * graphW;
    const scaleY = (y) => (H - padBottom) - ((y - 1.0) / 4.0) * graphH;

    // Grid & Axis
    ctx.strokeStyle = '#E2E8F0';
    ctx.lineWidth = 1;
    for (let y = 1; y <= 5; y++) {
      const py = scaleY(y);
      ctx.beginPath();
      ctx.moveTo(padLeft, py);
      ctx.lineTo(W - padRight, py);
      ctx.stroke();

      ctx.fillStyle = '#64748B';
      ctx.font = '12px monospace';
      ctx.textAlign = 'right';
      ctx.fillText(y.toFixed(1), padLeft - 10, py + 4);
    }

    ctx.fillStyle = '#64748B';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('組織的不公平感（手続的正義の欠落度: -2SD 〜 +2SD）', padLeft + graphW / 2, H - 15);

    ctx.save();
    ctx.translate(20, padTop + graphH / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('DX抵抗感・反発スコア (1〜5)', 0, 0);
    ctx.restore();

    const currentSlope = 0.45 - 0.14 * dialogue;

    const benchmarks = [
      { d: -1.5, color: '#C86258' },
      { d: 0.0, color: '#94A3B8' },
      { d: 1.5, color: '#228543' }
    ];

    benchmarks.forEach(bm => {
      const bSlope = 0.45 - 0.14 * bm.d;
      ctx.strokeStyle = bm.color + '44';
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      for (let x = -2.0; x <= 2.0; x += 0.5) {
        const y = 2.5 + bSlope * x - 0.20 * bm.d;
        const px = scaleX(x);
        const py = scaleY(y);
        if (x === -2.0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();
      ctx.setLineDash([]);
    });

    const curColor = dialogue >= 0.5 ? '#228543' : (dialogue <= -0.5 ? '#C86258' : '#005BAC');
    ctx.strokeStyle = curColor;
    ctx.lineWidth = 4;
    ctx.beginPath();
    for (let x = -2.0; x <= 2.0; x += 0.1) {
      const y = 2.5 + currentSlope * x - 0.20 * dialogue;
      const px = scaleX(x);
      const py = scaleY(y);
      if (x === -2.0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();

    statSlope.textContent = (currentSlope > 0 ? '+' : '') + currentSlope.toFixed(3);
    if (currentSlope < 0.25) {
      statImpact.textContent = '反発が劇的に緩和（緩やか）';
      statImpact.className = 'stat-chip-value success';
    } else if (currentSlope > 0.50) {
      statImpact.textContent = '不公平感で怒りが急増（危険）';
      statImpact.className = 'stat-chip-value highlight';
    } else {
      statImpact.textContent = '標準的な反発勾配';
      statImpact.className = 'stat-chip-value';
    }
  }

  sliderDialogue.addEventListener('input', render);
  render();
}

/* ============================================================================
   SIMULATOR 5: SIEMSEN ET AL. (2010) CMB ATTENUATION THEOREM
   ============================================================================ */
function initSiemsenSim() {
  const canvas = document.getElementById('canvas-siemsen');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const sliderNoise = document.getElementById('siemsen-noise');
  const valNoise = document.getElementById('siemsen-noise-val');
  const statMain = document.getElementById('siemsen-main-stat');
  const statInt = document.getElementById('siemsen-int-stat');

  function render() {
    const cmb = parseFloat(sliderNoise.value);
    valNoise.textContent = Math.round(cmb * 100) + ' %';

    const W = canvas.width;
    const H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    const trueMain = 0.25;
    const trueInt = -0.32;

    const obsMain = trueMain + cmb * 0.48;
    const obsInt = trueInt / (1.0 + cmb * 2.8);

    const barW = 120;
    const centerY = H / 2;

    const x1 = W * 0.28;
    const h1 = obsMain * 220;
    ctx.fillStyle = '#C86258';
    ctx.fillRect(x1 - barW / 2, centerY - h1, barW, h1);

    ctx.strokeStyle = '#0F172A';
    ctx.lineWidth = 2;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(x1 - barW / 2 - 15, centerY - trueMain * 220);
    ctx.lineTo(x1 + barW / 2 + 15, centerY - trueMain * 220);
    ctx.stroke();

    const x2 = W * 0.72;
    const h2 = Math.abs(obsInt) * 220;
    ctx.fillStyle = '#005BAC';
    ctx.fillRect(x2 - barW / 2, centerY, barW, h2);

    ctx.beginPath();
    ctx.moveTo(x2 - barW / 2 - 15, centerY + Math.abs(trueInt) * 220);
    ctx.lineTo(x2 + barW / 2 + 15, centerY + Math.abs(trueInt) * 220);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.strokeStyle = '#94A3B8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(40, centerY);
    ctx.lineTo(W - 40, centerY);
    ctx.stroke();

    ctx.fillStyle = '#0F172A';
    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('主効果 (見かけの相関が水増し肥大化)', x1, centerY - h1 - 12);
    ctx.fillText('交互作用項 (CMBによってゼロへ押し潰される)', x2, centerY + h2 + 24);

    ctx.fillStyle = '#64748B';
    ctx.font = '11px monospace';
    ctx.fillText(`真の値: +${trueMain.toFixed(2)} (破線)`, x1, centerY - trueMain * 220 - 6);
    ctx.fillText(`真の値: ${trueInt.toFixed(2)} (破線)`, x2, centerY + Math.abs(trueInt) * 220 + 16);

    statMain.textContent = '+' + obsMain.toFixed(3) + ' (水増し)';
    statInt.textContent = obsInt.toFixed(3) + ' (縮小中)';
  }

  sliderNoise.addEventListener('input', render);
  render();
}
