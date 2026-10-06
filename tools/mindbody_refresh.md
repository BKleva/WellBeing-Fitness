# Refreshing the schedule and events snapshot

The native `/schedule/` and `/events/` pages are built from `data/mindbody.json`, a snapshot of the studio's Mindbody
schedule (3 weeks of classes) and special events. Mindbody does not offer a public feed for this studio and blocks
server-side scraping, so the snapshot is captured from a real browser. Reservations always finish on Mindbody, so the
snapshot only has to be reasonably current. Beyond the last synced day, the schedule page shows the regular weekly
lineup (the most recent complete week) and says so.

Refresh when classes change, ideally weekly:

1. Open each Mindbody week in a browser and run the **schedule snippet** in the console. Use
   `https://clients.mindbodyonline.com/classic/ws?studioid=729963&stype=-7&sView=week&sLoc=0&date=M/D/YYYY`
   for the Monday of each week. Copy the printed JSON into `sched_w1.json`, `sched_w2.json`, `sched_w3.json`.
2. Open `https://clients.mindbodyonline.com/asp/main_enroll.asp?studioid=729963&tabID=103`, run the **events snippet**,
   and save the result as `ev_103.json`.
3. Put those files in one folder, then:

```
python tools/import_mindbody.py <that folder>
python tools/build.py
git add -A && git commit -m "Refresh schedule" && git push
```

## Schedule snippet

```js
const t=document.getElementById('classSchedule-mainTable');let cur=null;const rows=[];
for(const el of t.children){if(el.classList.contains('header'))cur=el.innerText.trim();else if(/Row/.test(el.className)){
const g=s=>{const n=el.querySelector(s);return n?n.textContent.replace(/\s+/g,' ').trim():''};
const btn=el.querySelector('.SignupButton');const oc=btn?btn.getAttribute('onclick'):'';
const m=oc.match(/classId=(\d+)&classDate=([^&']+)&clsLoc=(\d+)/);const tg=(oc.match(/tg=(\d+)/)||[])[1]||'';
const sp=el.innerText.match(/\((\d+) Reserved, (\d+) Open\)/)||[];
const c2=el.querySelector('.col-2');const dm=(c2?c2.textContent:'').replace(/\s+/g,' ').match(/(\d+\s*(?:hours?|minutes?)(?:\s*\d+\s*minutes?)?)/i);
rows.push({day:cur,time:g('.col-first'),name:g('.modalClassDesc'),teacher:g('.modalBio'),loc:g('.modalLocationInfo'),dur:dm?dm[1]:'',classId:m?m[1]:'',clsLoc:m?m[3]:'',tg,reserved:sp[1]||'',open:sp[2]||''})}}
copy(JSON.stringify(rows))
```

## Events snippet

```js
const ev=[...document.querySelectorAll('.mainText.enrollment.group')].map(b=>{const t=n=>{const e=b.querySelector(n);return e?e.textContent.replace(/\s+/g,' ').trim():''};
const head=b.querySelector('.mainTextBig > span');const full=head?head.textContent.replace(/\s+/g,' ').trim():'';const title=t('strong');
const teacher=full.replace(title,'').replace(/^\s*with\s*/i,'').trim();const btn=b.querySelector('.sign-up-now');const oc=btn?btn.getAttribute('onclick'):'';
const m=oc.match(/classId=(\d+)(?:&courseID=(\d*))?&classDate=([^&']+)&clsLoc=(\d+)/);const tg=(oc.match(/tg=(\d+)/)||[])[1]||'';
return{title,teacher,loc:t('.modalLocationInfo'),clsLoc:m?m[4]:'',weekday:t('.weekDayName'),date:t('.dateSpan').replace('Date:','').trim(),time:t('.times').replace('From:','').trim(),desc:t('#enrollmentDesc'),notes:t('#enrollmentNotes'),classId:m?m[1]:'',tg,img:''}});
copy(JSON.stringify(ev))
```

## Making it fully live

Ask the studio's Mindbody admin to enable the Public API (or Branded Web Tools widgets). With an API key the
snapshot step can become a scheduled job and the schedule would update itself.
