const fs = require('fs');
const json = JSON.parse(fs.readFileSync('tag_assistant_messerattach_com_2025_12_24.json', 'utf8'));

const outDir = './ai-analysis';
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

// ============ ANALYSIS 1: Data Flow Summary ============
// Shows: Event → Triggers Evaluated → Tags Fired → What's Missing
const dataFlow = [];

json.data.containers.forEach((c, ci) => {
  c.messages.forEach(m => {
    const triggersEvaluated = (m.ruleInfo || []).map(r => ({
      name: r.name,
      passed: r.pass,
      wouldFireTagCount: r.firingTags?.length || 0
    }));

    const triggersPassed = triggersEvaluated.filter(t => t.passed);
    const triggersFailed = triggersEvaluated.filter(t => !t.passed);

    const tagsFired = (m.tagInfo || []).filter(t => !t.isHidden).map(t => t.name);

    // Only include events with activity
    if (triggersEvaluated.length > 0 || tagsFired.length > 0) {
      dataFlow.push({
        container: c.publicId,
        containerType: c.product, // "gtm" or "gtm-server"
        eventIndex: m.index,
        event: m.eventName,
        page: m.title,
        consent: m.consentData ? {
          ad_storage: m.consentData.fullConsentList?.ad_storage?.isConsentGranted,
          analytics_storage: m.consentData.fullConsentList?.analytics_storage?.isConsentGranted
        } : null,
        triggersPassed: triggersPassed.length,
        triggersFailed: triggersFailed.length,
        tagsTriggered: tagsFired.length,
        tags: tagsFired,
        // Flag potential issues
        issues: []
      });

      const entry = dataFlow[dataFlow.length - 1];

      // Flag: Triggers passed but no tags fired
      if (triggersPassed.length > 0 && tagsFired.length === 0) {
        entry.issues.push('TRIGGERS_PASSED_NO_TAGS');
      }

      // Flag: Consent denied
      if (m.consentData?.fullConsentList?.ad_storage?.isConsentGranted === false) {
        entry.issues.push('AD_STORAGE_DENIED');
      }
      if (m.consentData?.fullConsentList?.analytics_storage?.isConsentGranted === false) {
        entry.issues.push('ANALYTICS_DENIED');
      }
    }
  });
});

fs.writeFileSync(outDir + '/1_data_flow.json', JSON.stringify({
  description: 'Event-by-event data flow showing triggers evaluated and tags fired',
  totalEvents: dataFlow.length,
  eventsWithIssues: dataFlow.filter(e => e.issues.length > 0).length,
  flow: dataFlow
}, null, 2));
console.log('1_data_flow.json:', (fs.statSync(outDir + '/1_data_flow.json').size / 1024).toFixed(1) + ' KB');

// ============ ANALYSIS 2: Tag Coverage Matrix ============
// Shows which tags fire on which events - gaps are visible
const tagMatrix = {};
const allEvents = new Set();
const allTags = new Set();

json.data.containers.forEach((c, ci) => {
  c.messages.forEach(m => {
    const eventKey = m.eventName;
    allEvents.add(eventKey);

    (m.tagInfo || []).forEach(t => {
      if (!t.isHidden) {
        allTags.add(t.name);
        if (!tagMatrix[t.name]) tagMatrix[t.name] = {};
        if (!tagMatrix[t.name][eventKey]) tagMatrix[t.name][eventKey] = 0;
        tagMatrix[t.name][eventKey]++;
      }
    });
  });
});

// Convert to array format showing gaps
const tagCoverage = Array.from(allTags).map(tag => {
  const events = tagMatrix[tag] || {};
  const firesOn = Object.keys(events);
  const doesNotFireOn = Array.from(allEvents).filter(e => !events[e]);

  return {
    tag,
    firesOnEvents: firesOn,
    firesCount: Object.values(events).reduce((a, b) => a + b, 0),
    doesNotFireOn: doesNotFireOn.slice(0, 10), // Limit for readability
    coverage: ((firesOn.length / allEvents.size) * 100).toFixed(1) + '%'
  };
});

fs.writeFileSync(outDir + '/2_tag_coverage.json', JSON.stringify({
  description: 'Which tags fire on which events - look for unexpected gaps',
  totalTags: allTags.size,
  totalEventTypes: allEvents.size,
  eventTypes: Array.from(allEvents),
  tags: tagCoverage
}, null, 2));
console.log('2_tag_coverage.json:', (fs.statSync(outDir + '/2_tag_coverage.json').size / 1024).toFixed(1) + ' KB');

// ============ ANALYSIS 3: Variable Problems ============
// Shows variables with undefined/null values or type mismatches
const varProblems = [];
const varValues = new Map();

json.data.containers.forEach((c, ci) => {
  c.messages.forEach(m => {
    (m.macroInfo || []).forEach(v => {
      const key = v.name + '|' + c.publicId;
      if (!varValues.has(key)) {
        varValues.set(key, {
          name: v.name,
          container: c.publicId,
          type: v.variableType,
          values: [],
          undefinedCount: 0,
          totalCount: 0
        });
      }

      const entry = varValues.get(key);
      entry.totalCount++;

      if (v.resolvedValue === undefined || v.resolvedValue === null || v.resolvedValue === '') {
        entry.undefinedCount++;
      } else {
        // Keep unique sample values (max 3)
        const valStr = JSON.stringify(v.resolvedValue).slice(0, 100);
        if (entry.values.length < 3 && !entry.values.includes(valStr)) {
          entry.values.push(valStr);
        }
      }
    });
  });
});

// Filter to only problematic variables
const problematicVars = Array.from(varValues.values()).filter(v => {
  const undefinedRate = v.undefinedCount / v.totalCount;
  return undefinedRate > 0.5 || v.values.length === 0;
}).map(v => ({
  ...v,
  undefinedRate: ((v.undefinedCount / v.totalCount) * 100).toFixed(0) + '%',
  problem: v.values.length === 0 ? 'ALWAYS_UNDEFINED' : 'OFTEN_UNDEFINED'
}));

fs.writeFileSync(outDir + '/3_variable_problems.json', JSON.stringify({
  description: 'Variables that are often undefined - likely data layer issues',
  totalVariables: varValues.size,
  problematicCount: problematicVars.length,
  problems: problematicVars
}, null, 2));
console.log('3_variable_problems.json:', (fs.statSync(outDir + '/3_variable_problems.json').size / 1024).toFixed(1) + ' KB');

// ============ ANALYSIS 4: Trigger Failures Explained ============
// Groups failures by trigger and shows the actual conditions that failed
const triggerFailures = new Map();

json.data.containers.forEach((c, ci) => {
  c.messages.forEach(m => {
    (m.ruleInfo || []).forEach(r => {
      if (!r.pass && r.predicates) {
        const key = r.name + '|' + c.publicId;
        if (!triggerFailures.has(key)) {
          triggerFailures.set(key, {
            trigger: r.name,
            container: c.publicId,
            failCount: 0,
            passCount: 0,
            failedOnEvents: new Set(),
            failureReasons: new Map()
          });
        }

        const entry = triggerFailures.get(key);
        entry.failCount++;
        entry.failedOnEvents.add(m.eventName);

        // Collect failure reasons
        r.predicates.filter(p => !p.pass && !p.isIgnored).forEach(p => {
          const reason = `${p.function}(${p.arg0?.[0]?.value || '?'}, ${p.arg1?.[0]?.value || '?'})`;
          if (!entry.failureReasons.has(reason)) {
            entry.failureReasons.set(reason, 0);
          }
          entry.failureReasons.set(reason, entry.failureReasons.get(reason) + 1);
        });
      } else if (r.pass) {
        const key = r.name + '|' + c.publicId;
        if (!triggerFailures.has(key)) {
          triggerFailures.set(key, {
            trigger: r.name,
            container: c.publicId,
            failCount: 0,
            passCount: 0,
            failedOnEvents: new Set(),
            failureReasons: new Map()
          });
        }
        triggerFailures.get(key).passCount++;
      }
    });
  });
});

const triggerAnalysis = Array.from(triggerFailures.values()).map(t => ({
  trigger: t.trigger,
  container: t.container,
  passCount: t.passCount,
  failCount: t.failCount,
  failRate: ((t.failCount / (t.passCount + t.failCount)) * 100).toFixed(0) + '%',
  failedOnEvents: Array.from(t.failedOnEvents),
  topFailureReasons: Array.from(t.failureReasons.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([reason, count]) => ({ reason, count }))
})).filter(t => t.failCount > 0);

fs.writeFileSync(outDir + '/4_trigger_failures.json', JSON.stringify({
  description: 'Why triggers failed - shows exact conditions that did not match',
  totalTriggers: triggerFailures.size,
  triggersWithFailures: triggerAnalysis.length,
  failures: triggerAnalysis
}, null, 2));
console.log('4_trigger_failures.json:', (fs.statSync(outDir + '/4_trigger_failures.json').size / 1024).toFixed(1) + ' KB');

// ============ ANALYSIS 5: Ecommerce Data Quality ============
// Checks for missing required fields in ecommerce events
const ecomIssues = [];
const requiredFields = {
  'purchase': ['transaction_id', 'value', 'currency', 'items'],
  'add_to_cart': ['items', 'value', 'currency'],
  'view_item': ['items'],
  'begin_checkout': ['items', 'value', 'currency'],
  'view_item_list': ['items']
};

json.data.containers.forEach((c, ci) => {
  c.messages.forEach(m => {
    const ecom = m.abstractModel?.ecommerce;
    const eventName = m.eventName;

    if (requiredFields[eventName] && ecom) {
      const missing = requiredFields[eventName].filter(field => {
        if (field === 'items') return !ecom.items || ecom.items.length === 0;
        return ecom[field] === undefined || ecom[field] === null || ecom[field] === '';
      });

      if (missing.length > 0) {
        ecomIssues.push({
          container: c.publicId,
          event: eventName,
          page: m.title,
          missingFields: missing,
          presentData: {
            hasItems: !!ecom.items,
            itemCount: ecom.items?.length || 0,
            value: ecom.value,
            currency: ecom.currency,
            transaction_id: ecom.transaction_id
          }
        });
      }
    }
  });
});

fs.writeFileSync(outDir + '/5_ecommerce_issues.json', JSON.stringify({
  description: 'Ecommerce events with missing required fields',
  totalIssues: ecomIssues.length,
  issues: ecomIssues
}, null, 2));
console.log('5_ecommerce_issues.json:', (fs.statSync(outDir + '/5_ecommerce_issues.json').size / 1024).toFixed(1) + ' KB');

// ============ ANALYSIS 6: Container Comparison ============
// Compares all containers and their data flow
const comparison = {
  description: 'Comparison between containers and Data Tag analysis for sGTM',
  containers: json.data.containers.map(c => ({
    publicId: c.publicId,
    product: c.product,
    tagName: c.tagName,
    aliases: c.aliases,
    eventCount: c.messages.length,
    uniqueEvents: [...new Set(c.messages.map(m => m.eventName))],
    tagsFired: Object.keys(c.tagsFired || {}),
    errorCount: c.errorCount,
    logCount: c.logCount
  })),
  gaps: []
};

// Find GTM container and analyze Data Tag (sends to sGTM)
const gtmContainer = json.data.containers.find(c => c.product === 'GTM');
if (gtmContainer) {
  // Data Tag analysis - this is what sends data to sGTM
  const dataTagFirings = [];
  gtmContainer.messages.forEach(m => {
    const dataTag = (m.tagInfo || []).find(t => t.name === 'Data Tag');
    if (dataTag) {
      dataTagFirings.push({
        event: m.eventName,
        page: m.title
      });
    }
  });

  // Dedupe
  const uniqueDataTagEvents = [...new Set(dataTagFirings.map(f => f.event))];

  comparison.dataTagAnalysis = {
    description: 'Data Tag sends events from wGTM to sGTM. Events NOT in this list are NOT sent to server.',
    totalFirings: dataTagFirings.length,
    eventsWithDataTag: uniqueDataTagEvents,
    eventsWITHOUT_DataTag: comparison.containers[0].uniqueEvents.filter(e => !uniqueDataTagEvents.includes(e))
  };

  // Flag events missing Data Tag as potential sGTM gaps
  comparison.dataTagAnalysis.eventsWITHOUT_DataTag.forEach(e => {
    comparison.gaps.push({
      event: e,
      issue: 'NO_DATA_TAG',
      impact: 'This event is NOT sent to sGTM'
    });
  });
}

fs.writeFileSync(outDir + '/6_container_comparison.json', JSON.stringify(comparison, null, 2));
console.log('6_container_comparison.json:', (fs.statSync(outDir + '/6_container_comparison.json').size / 1024).toFixed(1) + ' KB');

// ============ ANALYSIS 7: Complete Issues Summary ============
// AI-friendly summary of all detected issues
const allIssues = {
  description: 'SUMMARY OF ALL DETECTED ISSUES - Start troubleshooting here',
  summary: {
    dataFlowIssues: dataFlow.filter(e => e.issues.length > 0).length,
    variableProblems: problematicVars.length,
    triggerFailures: triggerAnalysis.length,
    ecommerceIssues: ecomIssues.length,
    eventsNotSentToSGTM: comparison.gaps.length
  },
  criticalIssues: [],
  warnings: []
};

// Add critical issues
if (problematicVars.filter(v => v.problem === 'ALWAYS_UNDEFINED').length > 0) {
  allIssues.criticalIssues.push({
    type: 'VARIABLES_ALWAYS_UNDEFINED',
    count: problematicVars.filter(v => v.problem === 'ALWAYS_UNDEFINED').length,
    variables: problematicVars.filter(v => v.problem === 'ALWAYS_UNDEFINED').map(v => v.name)
  });
}

if (ecomIssues.filter(i => i.event === 'purchase').length > 0) {
  allIssues.criticalIssues.push({
    type: 'PURCHASE_MISSING_DATA',
    count: ecomIssues.filter(i => i.event === 'purchase').length,
    details: 'Purchase events missing required fields'
  });
}

if (comparison.gaps.length > 0) {
  allIssues.criticalIssues.push({
    type: 'EVENTS_NOT_SENT_TO_SGTM',
    description: 'These events do NOT have Data Tag firing - they are NOT sent to sGTM',
    events: comparison.gaps.map(g => g.event)
  });
}

// Tags with low coverage
const lowCoverageTags = tagCoverage.filter(t => parseFloat(t.coverage) < 20);
if (lowCoverageTags.length > 0) {
  allIssues.warnings.push({
    type: 'LOW_COVERAGE_TAGS',
    tags: lowCoverageTags.map(t => ({ name: t.tag, coverage: t.coverage }))
  });
}

fs.writeFileSync(outDir + '/0_issues_summary.json', JSON.stringify(allIssues, null, 2));
console.log('0_issues_summary.json:', (fs.statSync(outDir + '/0_issues_summary.json').size / 1024).toFixed(1) + ' KB');

// ============ TOTAL ============
const files = fs.readdirSync(outDir);
let total = 0;
files.forEach(f => { total += fs.statSync(outDir + '/' + f).size; });
console.log('\nTotal:', (total / 1024).toFixed(1) + ' KB');
console.log('Original: 59.9 MB');
console.log('Reduction:', ((1 - total / 62835591) * 100).toFixed(1) + '%');
