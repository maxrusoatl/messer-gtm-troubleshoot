const fs = require('fs');
const path = require('path');

const INPUT = './GTM-MNRP4PF_workspace247.json';
const OUTPUT_DIR = './gtm-parts';

// Create output directory
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR);
}

// Read and parse
const data = JSON.parse(fs.readFileSync(INPUT, 'utf8'));
const cv = data.containerVersion;

console.log('GTM Container:', cv.container.publicId);
console.log('Tags:', cv.tag?.length || 0);
console.log('Triggers:', cv.trigger?.length || 0);
console.log('Variables:', cv.variable?.length || 0);
console.log('Built-in Variables:', cv.builtInVariable?.length || 0);
console.log('Custom Templates:', cv.customTemplate?.length || 0);

// Split tags into 10 parts
const tags = cv.tag || [];
const PARTS = 10;
const chunkSize = Math.ceil(tags.length / PARTS);

for (let i = 0; i < PARTS; i++) {
  const start = i * chunkSize;
  const end = Math.min(start + chunkSize, tags.length);
  const chunk = tags.slice(start, end);

  if (chunk.length === 0) continue;

  const part = {
    part: i + 1,
    totalParts: PARTS,
    containerId: cv.container.publicId,
    containerName: cv.container.name,
    tagRange: `${start + 1}-${end} of ${tags.length}`,
    tags: chunk.map(t => ({
      tagId: t.tagId,
      name: t.name,
      type: t.type,
      firingTriggerId: t.firingTriggerId,
      blockingTriggerId: t.blockingTriggerId,
      consentSettings: t.consentSettings,
      parameter: t.parameter
    }))
  };

  const outPath = path.join(OUTPUT_DIR, `gtm-tags-part-${String(i + 1).padStart(2, '0')}.json`);
  fs.writeFileSync(outPath, JSON.stringify(part, null, 2));
  console.log(`\nPart ${i + 1}: ${chunk.length} tags (${start + 1}-${end})`);
  chunk.forEach(t => console.log(`  - ${t.name} (${t.type})`));
}

// Also create separate files for triggers and variables
const triggers = cv.trigger || [];
fs.writeFileSync(
  path.join(OUTPUT_DIR, 'gtm-triggers.json'),
  JSON.stringify({
    containerId: cv.container.publicId,
    totalTriggers: triggers.length,
    triggers: triggers.map(t => ({
      triggerId: t.triggerId,
      name: t.name,
      type: t.type,
      filter: t.filter,
      customEventFilter: t.customEventFilter
    }))
  }, null, 2)
);
console.log(`\nTriggers file: ${triggers.length} triggers`);

const variables = cv.variable || [];
fs.writeFileSync(
  path.join(OUTPUT_DIR, 'gtm-variables.json'),
  JSON.stringify({
    containerId: cv.container.publicId,
    totalVariables: variables.length,
    variables: variables.map(v => ({
      variableId: v.variableId,
      name: v.name,
      type: v.type,
      parameter: v.parameter
    }))
  }, null, 2)
);
console.log(`Variables file: ${variables.length} variables`);

console.log(`\nDone! Files saved to ${OUTPUT_DIR}/`);
