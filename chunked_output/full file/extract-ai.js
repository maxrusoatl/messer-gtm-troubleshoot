const fs = require('fs');
const json = JSON.parse(fs.readFileSync('tag_assistant_messerattach_com_2025_12_24.json', 'utf8'));

const outDir = './ai-optimized';
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

// ============ FILE 1: Summary & Config ============
const summary = {
  name: json.name,
  timestamp: new Date(json.timestamp).toISOString(),
  containers: json.data.containers.map(c => ({
    publicId: c.publicId,
    product: c.product,
    version: c.version,
    errorCount: c.errorCount,
    logCount: c.logCount,
    numPages: c.numPages,
    tagName: c.tagName,
    environmentName: c.environmentName,
    aliases: c.aliases,
    destinations: c.destinations
  }))
};
fs.writeFileSync(outDir + '/1_summary.json', JSON.stringify(summary, null, 2));
console.log('1_summary.json:', (fs.statSync(outDir + '/1_summary.json').size / 1024).toFixed(1) + ' KB');

// ============ FILE 2: All Unique Tags with firing details ============
const allTags = new Map();
json.data.containers.forEach((c, ci) => {
  Object.entries(c.tagsFired || {}).forEach(([name, firings]) => {
    const key = name + '|' + ci;
    if (!allTags.has(key)) {
      allTags.set(key, { name, container: c.publicId, firings: [] });
    }
    Object.values(firings).forEach(f => {
      if (f && f.tagName) {
        allTags.get(key).type = f.tagType;
        allTags.get(key).firings.push({
          status: f.status,
          event: f.eventName,
          trigger: f.triggerInfo?.name || null
        });
      }
    });
  });
});
const tags = { totalUniqueTags: allTags.size, tags: Array.from(allTags.values()) };
fs.writeFileSync(outDir + '/2_tags.json', JSON.stringify(tags, null, 2));
console.log('2_tags.json:', (fs.statSync(outDir + '/2_tags.json').size / 1024).toFixed(1) + ' KB');

// ============ FILE 3: All Unique Variables (deduplicated, sample values only) ============
const allVars = new Map();
json.data.containers.forEach((c, ci) => {
  c.messages.forEach(m => {
    (m.macroInfo || []).forEach(v => {
      const key = v.name + '|' + ci;
      if (!allVars.has(key)) {
        allVars.set(key, {
          name: v.name,
          type: v.variableType,
          container: c.publicId,
          sampleValues: []
        });
      }
      // Keep max 3 unique sample values, truncated
      if (v.resolvedValue !== undefined && allVars.get(key).sampleValues.length < 3) {
        let val = v.resolvedValue;
        if (typeof val === 'string' && val.length > 100) val = val.slice(0, 100) + '...';
        const valStr = JSON.stringify(val);
        if (!allVars.get(key).sampleValues.includes(valStr)) {
          allVars.get(key).sampleValues.push(val);
        }
      }
    });
  });
});
const vars = { totalUniqueVars: allVars.size, variables: Array.from(allVars.values()) };
fs.writeFileSync(outDir + '/3_variables.json', JSON.stringify(vars, null, 2));
console.log('3_variables.json:', (fs.statSync(outDir + '/3_variables.json').size / 1024).toFixed(1) + ' KB');

// ============ FILE 4: Event Flow (lightweight timeline) ============
const eventFlow = json.data.containers.map((c, ci) => ({
  container: c.publicId,
  totalEvents: c.messages.length,
  events: c.messages.map(m => ({
    idx: m.index,
    event: m.eventName,
    page: m.title,
    tagCount: (m.tagInfo || []).filter(t => t && !t.isHidden).length,
    consent: m.consentData ? {
      ad: m.consentData.ad_storage,
      analytics: m.consentData.analytics_storage
    } : null
  }))
}));
fs.writeFileSync(outDir + '/4_event_flow.json', JSON.stringify(eventFlow, null, 2));
console.log('4_event_flow.json:', (fs.statSync(outDir + '/4_event_flow.json').size / 1024).toFixed(1) + ' KB');

// ============ FILE 5: Triggers Summary ============
const triggers = new Map();
json.data.containers.forEach((c, ci) => {
  c.messages.forEach(m => {
    (m.ruleInfo || []).forEach(r => {
      const key = r.name + '|' + ci;
      if (!triggers.has(key)) {
        triggers.set(key, {
          name: r.name,
          type: r.type,
          container: c.publicId,
          fired: 0,
          blocked: 0
        });
      }
      if (r.status === 'fired') triggers.get(key).fired++;
      if (r.status === 'blocked') triggers.get(key).blocked++;
    });
  });
});
const triggerData = { totalTriggers: triggers.size, triggers: Array.from(triggers.values()) };
fs.writeFileSync(outDir + '/5_triggers.json', JSON.stringify(triggerData, null, 2));
console.log('5_triggers.json:', (fs.statSync(outDir + '/5_triggers.json').size / 1024).toFixed(1) + ' KB');

// ============ FILE 6: Console Logs from Tags (debugging gold) ============
const logs = [];
json.data.containers.forEach((c, ci) => {
  (c.summaryLogInfos || []).forEach(log => {
    logs.push({
      container: c.publicId,
      source: log.source,
      level: log.level,
      message: log.message,
      eventId: log.eventId
    });
  });
});
fs.writeFileSync(outDir + '/6_console_logs.json', JSON.stringify({ totalLogs: logs.length, logs }, null, 2));
console.log('6_console_logs.json:', (fs.statSync(outDir + '/6_console_logs.json').size / 1024).toFixed(1) + ' KB');

// ============ FILE 7: Trigger Evaluations (why tags did/didn't fire) ============
const triggerEvals = [];
json.data.containers.forEach((c, ci) => {
  c.messages.forEach(m => {
    (m.ruleInfo || []).forEach(r => {
      triggerEvals.push({
        container: c.publicId,
        event: m.eventName,
        trigger: r.name,
        passed: r.pass,
        wouldFireTags: r.firingTags?.length || 0,
        wouldBlockTags: r.blockingTags?.length || 0
      });
    });
  });
});
// Dedupe - keep only unique trigger/event/result combos with counts
const triggerCounts = new Map();
triggerEvals.forEach(t => {
  const key = t.container + '|' + t.trigger + '|' + t.event + '|' + t.passed;
  if (!triggerCounts.has(key)) {
    triggerCounts.set(key, { ...t, count: 0 });
  }
  triggerCounts.get(key).count++;
});
fs.writeFileSync(outDir + '/7_trigger_evals.json', JSON.stringify({ evaluations: Array.from(triggerCounts.values()) }, null, 2));
console.log('7_trigger_evals.json:', (fs.statSync(outDir + '/7_trigger_evals.json').size / 1024).toFixed(1) + ' KB');

// ============ FILE 8: DataLayer/Ecommerce with FULL items ============
const dataLayerEvents = [];
json.data.containers.forEach((c, ci) => {
  c.messages.forEach(m => {
    if (m.abstractModel && m.abstractModel.ecommerce) {
      dataLayerEvents.push({
        container: c.publicId,
        idx: m.index,
        event: m.eventName,
        page: m.title,
        ecommerce: m.abstractModel.ecommerce // Full ecommerce object
      });
    }
  });
});
fs.writeFileSync(outDir + '/8_ecommerce_full.json', JSON.stringify({ events: dataLayerEvents }, null, 2));
console.log('8_ecommerce_full.json:', (fs.statSync(outDir + '/8_ecommerce_full.json').size / 1024).toFixed(1) + ' KB');

// ============ FILE 9: Tag Firing Details (which tags fired on which events) ============
const tagFirings = [];
json.data.containers.forEach((c, ci) => {
  Object.entries(c.tagsFired || {}).forEach(([tagName, events]) => {
    Object.entries(events).forEach(([eventIdx, data]) => {
      if (data && data.tagInfo) {
        data.tagInfo.forEach(t => {
          if (!t.isHidden) {
            tagFirings.push({
              container: c.publicId,
              eventIdx: parseInt(eventIdx),
              event: data.eventName,
              tag: t.name,
              type: t.type
            });
          }
        });
      }
    });
  });
});
// Dedupe
const uniqueFirings = [];
const seen = new Set();
tagFirings.forEach(f => {
  const key = f.container + '|' + f.eventIdx + '|' + f.tag;
  if (!seen.has(key)) {
    seen.add(key);
    uniqueFirings.push(f);
  }
});
fs.writeFileSync(outDir + '/9_tag_firings.json', JSON.stringify({ firings: uniqueFirings }, null, 2));
console.log('9_tag_firings.json:', (fs.statSync(outDir + '/9_tag_firings.json').size / 1024).toFixed(1) + ' KB');

// ============ FILE 10: Failed Trigger Conditions (WHY triggers didn't fire) ============
const failedConditions = [];
json.data.containers.forEach((c, ci) => {
  c.messages.forEach(m => {
    (m.ruleInfo || []).forEach(r => {
      if (!r.pass && r.predicates) {
        const failedPreds = r.predicates.filter(p => !p.pass && !p.isIgnored);
        if (failedPreds.length > 0) {
          failedConditions.push({
            container: c.publicId,
            event: m.eventName,
            trigger: r.name,
            failedConditions: failedPreds.map(p => ({
              function: p.function,
              arg0: p.arg0?.[0]?.value || p.arg0,
              arg1: p.arg1?.[0]?.value || p.arg1
            }))
          });
        }
      }
    });
  });
});
// Dedupe by trigger+event
const uniqueFailures = new Map();
failedConditions.forEach(f => {
  const key = f.container + '|' + f.trigger + '|' + f.event;
  if (!uniqueFailures.has(key)) {
    uniqueFailures.set(key, f);
  }
});
fs.writeFileSync(outDir + '/10_failed_triggers.json', JSON.stringify({ failures: Array.from(uniqueFailures.values()) }, null, 2));
console.log('10_failed_triggers.json:', (fs.statSync(outDir + '/10_failed_triggers.json').size / 1024).toFixed(1) + ' KB');

// ============ FILE 11: Full DataLayer State per Event (what SHOULD have been sent) ============
const dataLayerStates = [];
json.data.containers.forEach((c, ci) => {
  c.messages.forEach(m => {
    if (m.abstractModel) {
      dataLayerStates.push({
        container: c.publicId,
        idx: m.index,
        event: m.eventName,
        page: m.title,
        // Full dataLayer state - this is what tags had available to send
        dataLayer: {
          event: m.abstractModel.event,
          user_id: m.abstractModel.user_id,
          user_data: m.abstractModel.user_data,
          ecommerce: m.abstractModel.ecommerce,
          gtm: m.abstractModel.gtm ? {
            uniqueEventId: m.abstractModel.gtm.uniqueEventId,
            elementId: m.abstractModel.gtm.elementId,
            elementClasses: m.abstractModel.gtm.elementClasses,
            elementUrl: m.abstractModel.gtm.elementUrl,
            elementText: m.abstractModel.gtm.elementText
          } : null,
          consent: {
            ads_data_redaction: m.abstractModel.ads_data_redaction,
            url_passthrough: m.abstractModel.url_passthrough
          }
        }
      });
    }
  });
});
fs.writeFileSync(outDir + '/11_datalayer_states.json', JSON.stringify({
  description: 'Full dataLayer state at each event - this is what tags had available to send',
  note: 'Tag Assistant does NOT capture actual HTTP requests. Use Chrome HAR export or sGTM logs for that.',
  states: dataLayerStates
}, null, 2));
console.log('11_datalayer_states.json:', (fs.statSync(outDir + '/11_datalayer_states.json').size / 1024).toFixed(1) + ' KB');

// ============ TOTAL ============
const files = fs.readdirSync(outDir);
let total = 0;
files.forEach(f => { total += fs.statSync(outDir + '/' + f).size; });
console.log('\nTotal:', (total / 1024).toFixed(1) + ' KB');
console.log('Original: 59.9 MB');
console.log('Reduction:', ((1 - total / 62835591) * 100).toFixed(1) + '%');
